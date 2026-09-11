#!/usr/bin/env python3
"""
Query the Creatio object-model snapshot that ships with this skill.

The snapshot is the ONLY source of truth for whether an object, a field or a
lookup value exists. Never answer these questions from memory.

Invoke it through `scripts/model.sh`, which picks the right interpreter name for
the platform. Calling this file directly works too, wherever `python3` is a real
Python 3 (it is not on most Windows machines). Nothing outside the standard
library is needed; the assets are pre-compiled by tools/build-model.py.

Usage
-----
  sh scripts/model.sh check  <item> [<item> ...] | --file <list> [--banking]
  sh scripts/model.sh object <ObjectName|Caption> [--all] [--banking]
  sh scripts/model.sh field  <substring> [--object <ObjectName|Caption>] [--banking]
  sh scripts/model.sh lookup <LookupObject|Caption> [--banking]
  sh scripts/model.sh sections [--banking]
  sh scripts/model.sh search <substring> [--banking]

`check` is the one to reach for while verifying a scenario: it answers a whole
list in one call, one line per item, instead of a field dump per name.

  sh scripts/model.sh check Case Case.PriorityId "CaseStatus=New" Order.labKind
  sh scripts/model.sh check --file spec.txt --banking     ('-' reads stdin)

  Item grammar:  Account            an object
                 Case.PriorityId    a field on an object
                 CaseStatus=New     a value of a lookup

Examples
--------
  sh scripts/model.sh object Case
  sh scripts/model.sh field priority --object Case
  sh scripts/model.sh lookup CaseStatus
  sh scripts/model.sh search opportunit
  sh scripts/model.sh sections
  sh scripts/model.sh object Loan --banking

Exit codes
----------
  0  verified: it exists in this snapshot
  1  NOT verified: it is absent, or present but empty in this snapshot.
     Either way you may not write it down as existing. Mark it as new in the
     objects file, or ask.
     For `check`, 1 means at least one item of the list was not verified.
  2  usage error (bad or missing argument)
"""

import argparse
import csv
import difflib
import gzip
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")

# Present on every object and never part of a demo spec. Hidden from the object
# dump unless --all; a substring search still finds them.
SYSTEM_FIELDS = frozenset(
    ["id", "createdon", "createdbyid", "modifiedon", "modifiedbyid",
     "processlisteners"]
)


def norm(s):
    return (s or "").strip().lower()


class Model(object):
    """The three compiled tables, each read the first time it is asked for."""

    def __init__(self, model):
        self.name = model
        self.dir = os.path.join(ASSETS, model)
        self._cache = {}

    def _table(self, table):
        if table not in self._cache:
            path = os.path.join(self.dir, "%s.tsv.gz" % table)
            if not os.path.exists(path):
                sys.exit(
                    "Compiled snapshot missing: %s\n"
                    "Rebuild it with: python tools/build-model.py" % path
                )
            with gzip.open(path, "rt", encoding="utf-8", newline="") as fh:
                reader = csv.reader(fh, delimiter="\t")
                next(reader, None)  # header
                self._cache[table] = [tuple(row) for row in reader]
        return self._cache[table]

    @property
    def objects(self):
        return self._table("objects")

    @property
    def fields(self):
        return self._table("fields")

    def fields_of(self, obj):
        by_object = self._cache.get("_fields_by_object")
        if by_object is None:
            by_object = {}
            for row in self.fields:
                by_object.setdefault(norm(row[0]), []).append(row)
            self._cache["_fields_by_object"] = by_object
        return by_object.get(norm(obj), [])

    def values_of(self, obj):
        by_object = self._cache.get("_values_by_object")
        if by_object is None:
            by_object = {}
            for row in self._table("lookups"):
                by_object.setdefault(norm(row[0]), []).append(row[1])
            self._cache["_values_by_object"] = by_object
        return by_object.get(norm(obj), [])

    def caption(self, obj_name):
        captions = self._cache.get("_captions")
        if captions is None:
            captions = {norm(o[0]): o[1] for o in self.objects}
            self._cache["_captions"] = captions
        return captions.get(norm(obj_name), "")


def load(banking):
    return Model("banking" if banking else "general")


def resolve_object(m, name):
    """Resolve a user-supplied string to one Objects row.

    An exact match on the object name always wins over a caption match.
    Returns (row, ambiguous_names) where ambiguous_names lists the other
    candidates when the string matched several rows by caption.
    """
    t = norm(name)
    by_name = [r for r in m.objects if norm(r[0]) == t]
    if by_name:
        return by_name[0], [r[0] for r in by_name[1:]]
    by_caption = [r for r in m.objects if norm(r[1]) == t]
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


def cmd_object(m, name, show_all):
    meta, others = resolve_object(m, name)
    if meta is None:
        print("NOT VERIFIED: object %r is not in this snapshot." % name)
        print("Try: sh scripts/model.sh search %s" % name)
        return 1
    note_ambiguity("object", name, others)

    obj_name, caption, has_section, sections, n_fields, n_lookups = meta
    print("Object:   %s (%s)" % (obj_name, caption))
    print("Section:  %s%s" % (has_section, (" -> " + sections) if sections else ""))
    print("Fields:   %s (%s lookup)" % (n_fields, n_lookups))
    print()

    found = m.fields_of(obj_name)
    shown = found if show_all else [
        r for r in found if norm(r[1]) not in SYSTEM_FIELDS
    ]

    print("%-34s %-28s %-4s %s" % ("FIELD", "TYPE", "REQ", "LOOKUP TARGET"))
    print("-" * 100)
    for row in shown:
        fname, dtype, req, lk_obj = row[1], row[2], row[3], row[4]
        target = ("%s (%s)" % (lk_obj, m.caption(lk_obj))) if lk_obj else ""
        print("%-34s %-28s %-4s %s" % (fname, dtype, req, target))
    print()
    hidden = len(found) - len(shown)
    if hidden:
        print("%d fields listed, %d system fields hidden (--all shows them)."
              % (len(shown), hidden))
    else:
        print("%d fields listed." % len(shown))
    print("Lookup values: sh scripts/model.sh lookup <LookupObject>")
    return 0


def cmd_field(m, substring, obj):
    obj_name = None
    if obj:
        meta, others = resolve_object(m, obj)
        if meta is None:
            print("NOT VERIFIED: object %r is not in this snapshot." % obj)
            print("The field question cannot be answered until the object exists.")
            print("Try: sh scripts/model.sh search %s" % obj)
            return 1
        note_ambiguity("object", obj, others)
        obj_name = meta[0]

    sub = norm(substring)
    pool = m.fields_of(obj_name) if obj_name else m.fields
    hits = [r for r in pool if sub in norm(r[1])]

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
    for row in hits[:400]:
        print("%-26s %-32s %-26s %-4s %s"
              % (row[0], row[1], row[2], row[3], row[4]))
    if len(hits) > 400:
        print("... %d more, narrow with --object" % (len(hits) - 400))
    return 0


def lookup_note(m, obj_name):
    """Why a lookup object in the snapshot carries no values.

    The Fields table records this per referencing field. The snapshot skipped
    lookups over 500 rows, so 'too large' means values certainly exist and were
    not captured - a different finding from a lookup that is genuinely empty.
    """
    notes = set()
    for row in m.fields:
        if norm(row[4]) == norm(obj_name) and row[5]:
            notes.add(row[5])
    # 'too large' is the one note that means values definitely exist, so it wins
    # over any other note left on a sibling field.
    for note in sorted(notes):
        if note.startswith("too large"):
            return note
    return sorted(notes)[0] if notes else ""


def cmd_lookup(m, name):
    meta, others = resolve_object(m, name)
    obj_name = meta[0] if meta is not None else name
    values = m.values_of(obj_name)

    if values:
        note_ambiguity("lookup object", name, others)
        print("Lookup: %s (%s) - %d values"
              % (obj_name, m.caption(obj_name), len(values)))
        print("-" * 60)
        for value in values:
            print(value)
        return 0

    # No values. Distinguish "object absent" from "present but not captured".
    if meta is None:
        print("NOT VERIFIED: lookup object %r is not in this snapshot." % name)
        print("Try: sh scripts/model.sh search %s" % name)
        print("Do not invent values.")
        return 1

    note = lookup_note(m, obj_name)
    print("NOT VERIFIED: lookup object %s (%s) exists, but this snapshot holds "
          "no values for it." % (obj_name, meta[1]))
    if note.startswith("too large"):
        print("Reason: %s. The snapshot captured lookups of up to 500 rows only, "
              "so this one HAS values - they were not exported." % note)
        print("Do not invent values. Ask the engineer to read them off the "
              "instance, or specify only the ones the demo needs.")
        return 1
    if note == "captured":
        print("The export did read this lookup and every row it returned was "
              "blank, so there is no display value to quote.")
    elif note:
        print("Reason: %s." % note)
    else:
        print("It may be empty on that instance, or filled per project.")
    print("Do not invent values.")
    return 1


def cmd_sections(m):
    print("%-26s %-30s %s" % ("OBJECT", "CAPTION", "SECTION(S)"))
    print("-" * 100)
    n = 0
    for row in m.objects:
        if row[2] == "Yes":
            n += 1
            print("%-26s %-30s %s" % (row[0], row[1], row[3]))
    print()
    print("%d objects with sections." % n)
    return 0


def cmd_search(m, substring):
    sub = norm(substring)
    hits = [r for r in m.objects if sub in norm(r[0]) or sub in norm(r[1])]
    if not hits:
        print("NOT VERIFIED: no object matching %r in this snapshot." % substring)
        return 1
    print("%-30s %-34s %-8s %s" % ("OBJECT", "CAPTION", "SECTION", "# FIELDS"))
    print("-" * 100)
    for row in hits[:200]:
        print("%-30s %-34s %-8s %s" % (row[0], row[1], row[2], row[4]))
    if len(hits) > 200:
        print("... %d more" % (len(hits) - 200))
    return 0


def parse_item(text):
    """One check item -> (kind, object, detail).

    `Account`            an object
    `Case.PriorityId`    a field on an object
    `CaseStatus=New`     a value of a lookup

    `=` is read first, so a lookup value may contain dots; object and field
    names contain neither character.
    """
    text = text.strip()
    if not text:
        return None
    if "=" in text:
        obj, value = text.split("=", 1)
        return ("value", obj.strip(), value.strip())
    if "." in text:
        obj, field = text.split(".", 1)
        return ("field", obj.strip(), field.strip())
    return ("object", text, None)


def check_one(m, kind, obj, detail):
    """Verify one item. Returns (ok, note) - note is compact, one line."""
    meta, _ = resolve_object(m, obj)
    if meta is None:
        return False, "no such object in this snapshot"
    obj_name = meta[0]

    if kind == "object":
        section = (" -> " + meta[3]) if meta[2] == "Yes" else ", no section"
        return True, "%s fields%s" % (meta[4], section)

    if kind == "field":
        names = [r[1] for r in m.fields_of(obj_name)]
        for row in m.fields_of(obj_name):
            if norm(row[1]) == norm(detail):
                # "Lookup (CasePriority)" already names the target; only a
                # non-lookup type needs it spelled out.
                target = ("" if row[4] and row[4] in row[2]
                          else (" -> %s" % row[4] if row[4] else ""))
                return True, "%s%s%s" % (row[2],
                                         ", required" if row[3] == "Yes" else "",
                                         target)
        # A name in the notes is usually close to the real one - a suffix, a
        # plural or a typo - so say which field was probably meant.
        near = [n for n in names if norm(detail) in norm(n)][:3]
        if not near:
            near = difflib.get_close_matches(detail, names, n=3, cutoff=0.7)
        if near:
            return False, "no such field; closest: %s" % ", ".join(near)
        return False, "no such field on %s" % obj_name

    values = m.values_of(obj_name)
    for value in values:
        if norm(value) == norm(detail):
            return True, "existing value"
    if not values:
        return False, "lookup holds no values in this snapshot"
    shown = ", ".join(values[:10])
    if len(values) > 10:
        shown += ", ... (%d total)" % len(values)
    return False, "not among: %s" % shown


def cmd_check(m, items):
    """Verify a whole list in one call.

    The scenario is verified name by name, dozens of names per document. Asking
    one at a time costs a round-trip and a full field dump for each; this asks
    once and answers in one line per name.
    """
    parsed = [parse_item(i) for i in items]
    parsed = [x for x in parsed if x]
    if not parsed:
        print("Nothing to check.")
        return 2

    width = min(46, max(len(i.strip()) for i in items if i.strip()))
    missing = 0
    for kind, obj, detail in parsed:
        ok, note = check_one(m, kind, obj, detail)
        if detail is None:
            label = obj
        elif kind == "field":
            label = "%s.%s" % (obj, detail)
        else:
            label = "%s=%s" % (obj, detail)
        if not ok:
            missing += 1
        print("%-8s %-*s %s" % ("OK" if ok else "MISSING", width, label, note))

    print()
    print("%d checked, %d verified, %d NOT verified."
          % (len(parsed), len(parsed) - missing, missing))
    if missing:
        print("A missing lookup value or a missing simple column is normally "
              "something to mark as new in the objects file, not a question - "
              "see best-practices.md section 2.")
    return 1 if missing else 0


# ---------------------------------------------------------------- main


def run():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("command",
                   choices=["object", "field", "lookup", "sections", "search",
                            "check"])
    p.add_argument("value", nargs="*", default=[])
    p.add_argument("--object", dest="obj", default=None,
                   help="restrict a field search to one object (field command only)")
    p.add_argument("--all", action="store_true",
                   help="include system fields in the object dump (object only)")
    p.add_argument("--file", dest="file", default=None,
                   help="read check items from a file, one per line ('-' for stdin)")
    p.add_argument("--banking", action="store_true",
                   help="use the banking / finserv snapshot")
    a = p.parse_args()

    items = list(a.value)
    if a.command == "check":
        if a.file:
            try:
                text = sys.stdin.read() if a.file == "-" else \
                    open(a.file, encoding="utf-8").read()
            except OSError as exc:
                p.error("cannot read %r: %s" % (a.file, exc.strerror or exc))
            # blank lines and # comments let the list carry its own structure
            items += [l for l in (x.strip() for x in text.splitlines())
                      if l and not l.startswith("#")]
        if not items:
            p.error("'check' needs items, or --file with a list of them")
    elif a.file:
        p.error("--file applies only to the 'check' command")
    elif a.command == "sections":
        if items:
            p.error("'sections' takes no value (got %r)" % items[0])
    elif len(items) != 1:
        p.error("command %r needs exactly one value (got %d)"
                % (a.command, len(items)))

    if a.obj and a.command != "field":
        p.error("--object applies only to the 'field' command")
    if a.all and a.command != "object":
        p.error("--all applies only to the 'object' command")

    m = load(a.banking)
    if a.command == "check":
        return cmd_check(m, items)
    if a.command == "sections":
        return cmd_sections(m)
    value = items[0]
    if a.command == "object":
        return cmd_object(m, value, a.all)
    if a.command == "field":
        return cmd_field(m, value, a.obj)
    if a.command == "lookup":
        return cmd_lookup(m, value)
    return cmd_search(m, value)


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
