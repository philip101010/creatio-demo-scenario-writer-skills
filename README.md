# Creatio Demo Scenario Writer Skills

A Claude Code plugin with one skill: it turns a solution consultant's case — free-form
notes, a scenario, or discovery material — into the two files a Creatio demo is
presented and built from: a scenario, and an object model with its pages.

## What it does

The consultant writes a case: notes after a client call, a scenario, or just
discovery documents — free-form, out of order, business language, technically
naive in places. The skill writes the whole thing in one pass: a scenario with
modular use cases, one happy path each, and an object model whose every object,
field, lookup and lookup value has been checked against a bundled Creatio
object-model snapshot, with the pages and seed data to build. Automation —
processes, stage models, rules, AI skills — is not a separate file: each step
says what happens and what produces it, and the build agent derives the rest.

It does not interrogate the consultant. Every gap in the step logic is closed
with the best-fitting step, and handed over as a numbered proposal with a
one-line undo. The consultant reads the draft, replies with what to change, and
the skill issues the next version of both files. Anything that only a person can
settle is flagged **needs your input** or **engineer to confirm** without
stopping the draft.

## Install

```
/plugin marketplace add philip101010/creatio-demo-scenario-writer-skills
/plugin install creatio-demo-scenario-writer-skills
```

Then just hand Claude the case — the skill triggers on demo notes, a client
call summary, discovery documents, a draft demo script or a use-case description
for a Creatio demo. It delivers two Markdown files,
`<client>-demo-scenario-v<n>.md` and `<client>-objects-v<n>.md`, plus a list of
proposals in the chat. Reply with changes and it issues `v<n+1>` of both.

## What's inside

```
skills/demo-scenario-writer/
  SKILL.md                    the flow: map, close gaps, read, verify, write, revise
  reference/format.md         the scenario contract (steps, bubbles, provenance, banned words)
  reference/objects-file.md   the object model contract (objects, lookups, pages, seed data)
  reference/gap-closing.md    the ten gap checks, how to close them, how proposals are written
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
