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
  sh scripts/model.sh object <ObjectName|Caption> [--all] [--banking]
  sh scripts/model.sh field  <substring> [--object <ObjectName|Caption>] [--banking]
  sh scripts/model.sh lookup <LookupObject|Caption> [--banking]
  sh scripts/model.sh sections [--banking]
  sh scripts/model.sh search <substring> [--banking]

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
     Either way you may not write a build-spec line about it. Raise an ?OPEN.
  2  usage error (bad or missing argument)
"""

import argparse
import csv
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
        print("Do not invent values. Raise an ?OPEN.")
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
    print("Do not invent values. Raise an ?OPEN.")
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
    p.add_argument("--all", action="store_true",
                   help="include system fields in the object dump (object only)")
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
    if a.all and a.command != "object":
        p.error("--all applies only to the 'object' command")

    m = load(a.banking)
    if a.command == "object":
        return cmd_object(m, a.value, a.all)
    if a.command == "field":
        return cmd_field(m, a.value, a.obj)
    if a.command == "lookup":
        return cmd_lookup(m, a.value)
    if a.command == "sections":
        return cmd_sections(m)
    return cmd_search(m, a.value)


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
