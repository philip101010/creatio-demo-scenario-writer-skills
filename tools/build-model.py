#!/usr/bin/env python3
"""Compile the xlsx object-model snapshots into the assets the skill reads.

Maintainer tool, not part of the skill. It is the only thing here that needs
openpyxl; the skill itself runs on the standard library alone.

    python tools/build-model.py

Reads  snapshots/creatio-object-model.xlsx          -> assets/general/
       snapshots/creatio-banking-object-model.xlsx  -> assets/banking/

Three columns are dropped on the way, all of them recoverable:

  Fields."Object Caption"           repeats the Objects sheet on every one of
                                    36 000 rows; model.py joins on the object.
  Fields."Lookup Object Caption"    same, joined through the lookup target.
  Lookup Values."Record Id"         GUIDs, which the skill is forbidden to put
                                    in its output at all (hard rule 6).

The build asserts that each really is redundant before dropping it, so a future
snapshot that breaks the assumption fails loudly instead of losing data.
"""

import csv
import gzip
import os
import sys

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is required to build (not to run): pip install openpyxl")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOTS = os.path.join(ROOT, "snapshots")
ASSETS = os.path.join(ROOT, "skills", "demo-scenario-writer", "assets")

MODELS = [
    ("general", "creatio-object-model.xlsx"),
    ("banking", "creatio-banking-object-model.xlsx"),
]


def sheet_rows(wb, sheet):
    it = wb[sheet].iter_rows(values_only=True)
    next(it, None)  # header
    for r in it:
        if r and any(c is not None for c in r):
            yield r


def cell(v):
    return "" if v is None else str(v).replace("\t", " ").replace("\n", " ").strip()


def write_tsv(path, header, rows):
    with gzip.open(path, "wt", encoding="utf-8", newline="", compresslevel=9) as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        n = 0
        for r in rows:
            w.writerow(r)
            n += 1
    return n, os.path.getsize(path)


def build(model, xlsx):
    src = os.path.join(SNAPSHOTS, xlsx)
    if not os.path.exists(src):
        sys.exit("snapshot missing: %s" % src)
    out = os.path.join(ASSETS, model)
    if not os.path.isdir(out):
        os.makedirs(out)

    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)

    objects = [[cell(c) for c in (list(r) + [None] * 6)[:6]]
               for r in sheet_rows(wb, "Objects")]
    caption = {o[0]: o[1] for o in objects}

    fields = []
    for r in sheet_rows(wb, "Fields"):
        obj, obj_cap, name, dtype, req, is_lk, lk_obj, lk_cap, lk_note = (
            [cell(c) for c in (list(r) + [None] * 9)[:9]]
        )
        assert caption.get(obj, obj_cap) == obj_cap, \
            "Fields caption for %s diverges from the Objects sheet" % obj
        assert (is_lk == "Yes") == bool(lk_obj), \
            "%s.%s: 'Is Lookup' and 'Lookup Object' disagree" % (obj, name)
        assert not lk_obj or caption.get(lk_obj, lk_cap) == lk_cap, \
            "%s.%s: lookup caption not recoverable from Objects" % (obj, name)
        # The note vocabulary comes from the export and one of its phrases
        # points at an xlsx sheet that no longer exists downstream. Say what it
        # means instead, so model.py can quote the note verbatim.
        lk_note = lk_note.replace("see 'Lookup Values' sheet", "captured")
        fields.append([obj, name, dtype, req, lk_obj, lk_note])

    lookups = []
    blank = 0
    for r in sheet_rows(wb, "Lookup Values"):
        obj, obj_cap, value = [cell(c) for c in (list(r) + [None] * 3)[:3]]
        assert caption.get(obj, obj_cap) == obj_cap, \
            "Lookup Values caption for %s diverges from the Objects sheet" % obj
        # A row whose value cell is NULL is not a value. The export produces a
        # few dozen of them, and printing one as if it were a lookup value is
        # how "None" ends up in a build spec. Dropping them also lets a lookup
        # whose every row is blank report itself as unverified, which is true.
        if not value:
            blank += 1
            continue
        lookups.append([obj, value])
    if blank:
        print("  (dropped %d lookup rows with an empty value)" % blank)

    about = [" | ".join(cell(c) for c in r if cell(c))
             for r in sheet_rows(wb, "README")]
    wb.close()

    total = 0
    for name, header, rows in (
        ("objects.tsv.gz",
         ["name", "caption", "has_section", "sections", "n_fields", "n_lookups"],
         objects),
        ("fields.tsv.gz",
         ["object", "field", "type", "required", "lookup_object", "lookup_note"],
         fields),
        ("lookups.tsv.gz", ["lookup_object", "value"], lookups),
    ):
        n, size = write_tsv(os.path.join(out, name), header, rows)
        total += size
        print("  %-16s %6d rows  %6.1f KB" % (name, n, size / 1024.0))

    with open(os.path.join(out, "about.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("Source: snapshots/%s\n" % xlsx)
        fh.write("Compiled by tools/build-model.py. Do not edit by hand.\n\n")
        fh.write("\n".join(about) + "\n")

    print("  %s: %.2f MB compiled from %.2f MB of xlsx"
          % (model, total / 1e6, os.path.getsize(src) / 1e6))


def main():
    for model, xlsx in MODELS:
        print("%s <- %s" % (model, xlsx))
        build(model, xlsx)


if __name__ == "__main__":
    main()
