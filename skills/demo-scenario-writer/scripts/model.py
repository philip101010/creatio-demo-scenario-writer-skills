#!/usr/bin/env python3
"""
Query the Creatio object-model snapshot that ships with this skill.

The snapshot is the ONLY source of truth for whether an object, a field or a
lookup value exists. Never answer these questions from memory.

Usage
-----
  python3 scripts/model.py object <ObjectName|Caption> [--banking]
  python3 scripts/model.py field  <substring> [--object <ObjectName|Caption>] [--banking]
  python3 scripts/model.py lookup <LookupObject|Caption> [--banking]
  python3 scripts/model.py sections [--banking]
  python3 scripts/model.py search <substring> [--banking]

Examples
--------
  python3 scripts/model.py object Case
  python3 scripts/model.py field priority --object Case
  python3 scripts/model.py lookup CaseStatus
  python3 scripts/model.py search opportunit
  python3 scripts/model.py sections
  python3 scripts/model.py object Loan --banking

Exit codes
----------
  0  verified: it exists in this snapshot
  1  NOT verified: it is absent, or present but empty in this snapshot.
     Either way you may not write a build-spec line about it. Raise an ?OPEN.
  2  usage error (bad or missing argument)
"""

import argparse
import os
import sys

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is required: pip install openpyxl --break-system-packages")

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
GENERAL = os.path.join(ASSETS, "creatio-object-model.xlsx")
BANKING = os.path.join(ASSETS, "creatio-banking-object-model.xlsx")


def load(banking):
    path = BANKING if banking else GENERAL
    if not os.path.exists(path):
        sys.exit("Model snapshot not found: %s" % path)
    return openpyxl.load_workbook(path, read_only=True, data_only=True)


def rows(wb, sheet):
    ws = wb[sheet]
    it = ws.iter_rows(values_only=True)
    next(it, None)  # header
    for r in it:
        if r and any(c is not None for c in r):
            yield r


def norm(s):
    return (s or "").strip().lower()


def resolve_object(wb, name):
    """Resolve a user-supplied string to one Objects row.

    An exact match on the object name always wins over a caption match.
    Returns (row, ambiguous_names) where ambiguous_names lists the other
    candidates when the string matched several rows by caption.
    """
    t = norm(name)
    by_name = [r for r in rows(wb, "Objects") if norm(r[0]) == t]
    if by_name:
        return by_name[0], [r[0] for r in by_name[1:]]
    by_caption = [r for r in rows(wb, "Objects") if norm(r[1]) == t]
    if by_caption:
        return by_caption[0], [r[0] for r in by_caption[1:]]
    return None, []


def note_ambiguity(kind, value, others):
    if others:
        sys.stderr.write(
            "AMBIGUOUS: %r also matches %s %s. Showing the first; re-run with an "
            "exact object name.\n" % (value, kind, ", ".join(others[:8]))
        )


# ---------------------------------------------------------------- commands


def cmd_object(wb, name):
    meta, others = resolve_object(wb, name)
    if meta is None:
        print("NOT VERIFIED: object %r is not in this snapshot." % name)
        print("Try: python3 scripts/model.py search %s" % name)
        return 1
    note_ambiguity("object", name, others)

    obj_name, caption, has_section, sections, n_fields, n_lookups = (
        list(meta) + [None] * 6
    )[:6]
    print("Object:   %s (%s)" % (obj_name, caption))
    print("Section:  %s%s" % (has_section, (" -> " + sections) if sections else ""))
    print("Fields:   %s (%s lookup)" % (n_fields, n_lookups))
    print()

    found = [r for r in rows(wb, "Fields") if norm(r[0]) == norm(obj_name)]

    print("%-34s %-28s %-4s %s" % ("FIELD", "TYPE", "REQ", "LOOKUP TARGET"))
    print("-" * 100)
    for r in found:
        _, _, fname, dtype, req, is_lk, lk_obj, lk_cap, _ = (list(r) + [None] * 9)[:9]
        tgt = ("%s (%s)" % (lk_obj, lk_cap)) if is_lk == "Yes" and lk_obj else ""
        print("%-34s %-28s %-4s %s" % (fname, dtype or "", req or "", tgt))
    print()
    print(
        "%d fields listed. Lookup values: python3 scripts/model.py lookup <LookupObject>"
        % len(found)
    )
    return 0


def cmd_field(wb, substring, obj):
    obj_name = None
    if obj:
        meta, others = resolve_object(wb, obj)
        if meta is None:
            print("NOT VERIFIED: object %r is not in this snapshot." % obj)
            print("The field question cannot be answered until the object exists.")
            print("Try: python3 scripts/model.py search %s" % obj)
            return 1
        note_ambiguity("object", obj, others)
        obj_name = norm(meta[0])

    sub = norm(substring)
    hits = []
    for r in rows(wb, "Fields"):
        if obj_name and norm(r[0]) != obj_name:
            continue
        if sub in norm(r[2]):
            hits.append(r)

    if not hits:
        print(
            "NOT VERIFIED: no field matching %r%s in this snapshot."
            % (substring, (" on object %s" % obj) if obj else "")
        )
        return 1

    print(
        "%-26s %-32s %-26s %-4s %s"
        % ("OBJECT", "FIELD", "TYPE", "REQ", "LOOKUP TARGET")
    )
    print("-" * 120)
    for r in hits[:400]:
        o, _, fname, dtype, req, is_lk, lk_obj, _, _ = (list(r) + [None] * 9)[:9]
        tgt = lk_obj if is_lk == "Yes" and lk_obj else ""
        print("%-26s %-32s %-26s %-4s %s" % (o, fname, dtype or "", req or "", tgt))
    if len(hits) > 400:
        print("... %d more, narrow with --object" % (len(hits) - 400))
    return 0


def cmd_lookup(wb, name):
    t = norm(name)
    vals = [r for r in rows(wb, "Lookup Values")
            if norm(r[0]) == t or norm(r[1]) == t]
    if vals:
        print("Lookup: %s (%s) - %d values" % (vals[0][0], vals[0][1], len(vals)))
        print("-" * 60)
        for r in vals:
            print(r[2])
        return 0

    # No values. Distinguish "object absent" from "object present but empty".
    meta, _ = resolve_object(wb, name)
    if meta is None:
        print("NOT VERIFIED: lookup object %r is not in this snapshot." % name)
        print("Try: python3 scripts/model.py search %s" % name)
    else:
        print(
            "NOT VERIFIED: lookup object %s (%s) exists, but this snapshot holds "
            "no values for it." % (meta[0], meta[1])
        )
        print("It may be empty on that instance, or filled per project.")
    print("Do not invent values. Raise an ?OPEN.")
    return 1


def cmd_sections(wb):
    print("%-26s %-30s %s" % ("OBJECT", "CAPTION", "SECTION(S)"))
    print("-" * 100)
    n = 0
    for r in rows(wb, "Objects"):
        if r[2] == "Yes":
            n += 1
            print("%-26s %-30s %s" % (r[0], r[1] or "", r[3] or ""))
    print()
    print("%d objects with sections." % n)
    return 0


def cmd_search(wb, substring):
    sub = norm(substring)
    hits = [r for r in rows(wb, "Objects") if sub in norm(r[0]) or sub in norm(r[1])]
    if not hits:
        print("NOT VERIFIED: no object matching %r in this snapshot." % substring)
        return 1
    print("%-30s %-34s %-8s %s" % ("OBJECT", "CAPTION", "SECTION", "# FIELDS"))
    print("-" * 100)
    for r in hits[:200]:
        print("%-30s %-34s %-8s %s" % (r[0], r[1] or "", r[2] or "", r[4] or ""))
    if len(hits) > 200:
        print("... %d more" % (len(hits) - 200))
    return 0


# ---------------------------------------------------------------- main


def run():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("command",
                   choices=["object", "field", "lookup", "sections", "search"])
    p.add_argument("value", nargs="?", default=None)
    p.add_argument("--object", dest="obj", default=None,
                   help="restrict a field search to one object (field command only)")
    p.add_argument("--banking", action="store_true",
                   help="use the banking / finserv snapshot")
    a = p.parse_args()

    if a.command == "sections":
        if a.value:
            p.error("'sections' takes no value (got %r)" % a.value)
    elif not a.value:
        p.error("command %r needs a value" % a.command)

    if a.obj and a.command != "field":
        p.error("--object applies only to the 'field' command")

    wb = load(a.banking)
    try:
        if a.command == "object":
            return cmd_object(wb, a.value)
        if a.command == "field":
            return cmd_field(wb, a.value, a.obj)
        if a.command == "lookup":
            return cmd_lookup(wb, a.value)
        if a.command == "sections":
            return cmd_sections(wb)
        return cmd_search(wb, a.value)
    finally:
        wb.close()


def main():
    try:
        rc = run()
    except BrokenPipeError:
        # Output was piped into something that closed early (head, less).
        try:
            sys.stdout.close()
        except Exception:
            pass
        os._exit(0)
    sys.exit(rc)


if __name__ == "__main__":
    main()
