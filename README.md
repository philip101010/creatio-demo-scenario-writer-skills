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

## What's inside

```
skills/demo-scenario-writer/
  SKILL.md                              the flow: intake, decompose, verify, write
  reference/format.md                   the document contract (five sections, banned words)
  reference/best-practices.md           what to specify, what to decide instead of asking
  reference/golden-use-case.md          one worked use case to match for density
  reference/anti-examples.md            real failures and their fixes
  scripts/model.py                      query the object-model snapshot
  assets/creatio-object-model.xlsx      standard object model
  assets/creatio-banking-object-model.xlsx   FinServ / banking object model
```

`scripts/model.py` is the verification path — objects, lookups, fields,
sections, free-text search, with `--banking` selecting the financial-services
snapshot. Exit code 1 means not verified. The xlsx files are never read
directly; they run to 17 000 rows.

```bash
python3 scripts/model.py object Case
python3 scripts/model.py lookup CaseStatus --banking
python3 scripts/model.py field priority --object Case
python3 scripts/model.py search opportunit
python3 scripts/model.py sections
```

## Related

- [creatio-demo-toolkit](https://github.com/isavenkocreatio/creatio-demo-toolkit) —
  the build half: object model, Freedom UI pages, dashboards, demo data and
  processes via clio, once a scenario is approved.
