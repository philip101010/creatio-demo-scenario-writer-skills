# Creatio Demo Scenario Writer

A Claude Code plugin with one skill: it turns a solution consultant's free-form
demo notes into the single document a solution engineer builds a Creatio demo
from — without a rewrite cycle.

## What it does

The consultant writes notes after a client call: free-form, out of order,
business language, technically naive in places. The skill produces a scenario
with modular use cases, one happy path each, and a build spec whose every
object, field, lookup and lookup value has been checked against a bundled
Creatio object-model snapshot.

What it will not do is invent functionality. Anything that cannot be verified
against the snapshot and cannot be decided from the rules becomes an open
question addressed to the person who can actually answer it — the consultant
for business questions, the engineer for platform ones. Consultants are never
asked platform questions, which is the technical guesswork this whole process
exists to remove.

## Install

```
/plugin marketplace add philip101010/creatio-demo-scenario-writer
/plugin install creatio-demo-scenario-writer
```

Then just hand Claude the notes — the skill triggers on demo notes, a client
call summary, a draft demo script or a use-case description for a Creatio demo.
It answers with an intake checklist, then delivers the scenario as one Markdown
file named `<client>-demo-scenario-v<n>.md`.

## What's inside

```
skills/demo-scenario-writer/
  SKILL.md                    the flow: intake, decompose, verify, write
  reference/format.md         the document contract (five sections, banned words)
  reference/best-practices.md what to specify, what to decide instead of asking
  reference/golden-use-case.md one worked use case to match for density
  reference/anti-examples.md  real failures and their fixes
  scripts/model.sh            cross-platform launcher for the query script
  scripts/model.py            query the object-model snapshot
  assets/general/             compiled standard object model
  assets/banking/             compiled FinServ / banking object model
snapshots/*.xlsx              the raw exports the assets are compiled from
tools/build-model.py          the compiler (maintainers only)
```

`scripts/model.sh` is the verification path, and `check` is the command the
skill leans on: a scenario asserts dozens of names, and asking one at a time
cost a round-trip and a full field dump each. On a 35-name list, one batch call
answers in 395 ms and ~600 tokens where the single-name commands took 15 s and
~11 500.

```bash
sh scripts/model.sh check Case Case.PriorityId "CaseStatus=New" Order.labKind
sh scripts/model.sh check --file spec.txt --banking
```

`OK` carries the field's type and lookup target; `MISSING` carries the closest
real name, or the values a lookup actually holds. The single-name commands —
objects, lookups, fields, sections, free-text search, with `--banking` selecting
the financial-services snapshot — remain for exploring:

```bash
sh scripts/model.sh object Case
sh scripts/model.sh lookup CaseStatus --banking
sh scripts/model.sh field priority --object Case
sh scripts/model.sh search opportunit
sh scripts/model.sh sections
```

## Requirements

Python 3.9 or newer, and nothing else. The launcher works the same on macOS,
Linux and Windows: it finds a real Python 3 whatever it happens to be called on
that machine — `python3` on macOS and Linux, `python` or `py -3` on Windows,
where `python3` is usually the Microsoft Store stub that prints an advert and
exits 49 — and it resolves the snapshots relative to itself, so the command runs
from any directory. On Windows use it from Git Bash or WSL, which is where
Claude Code runs shell commands anyway.

## The compiled snapshots

The skill queries three gzipped TSV tables per model rather than the xlsx
exports, because a query is a hot path: the scenario is verified name by name,
dozens of calls per document. Parsing xlsx cost `openpyxl` plus 870 ms per call;
the compiled tables cost 25 ms and only the standard library, which is also what
lets the launcher skip probing for a dependency. Three columns are dropped along
the way — two captions that repeat the objects table on every one of 36 000 rows,
and the lookup `Record Id` column, which is GUIDs the skill is forbidden to emit.
So are the 65 lookup rows whose display value is NULL: the old reader printed
those as the literal text `None`, and for two lookups every captured row was
blank, so it reported them as verified with a list of `None`s. Both models
together come to 0.36 MB, down from 2.49 MB.

To regenerate after replacing a snapshot in `snapshots/` (needs `openpyxl`,
the only dependency left anywhere in the repo):

```bash
python tools/build-model.py
```

It asserts that every dropped column really is recoverable before dropping it,
so a future export that breaks the assumption fails the build instead of
quietly losing data.

## Related

- [creatio-demo-toolkit](https://github.com/isavenkocreatio/creatio-demo-toolkit) —
  the build half: object model, Freedom UI pages, dashboards, demo data and
  processes via clio, once a scenario is approved.
