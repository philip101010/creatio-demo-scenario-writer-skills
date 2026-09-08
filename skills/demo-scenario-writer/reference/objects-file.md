# The objects file — written for a coding agent

`<client>-objects-v<n>.md` is the second deliverable. Its reader is not a person
skimming in a meeting: it is Claude Code, opening the file as the build brief for
the demo, with the scenario file open beside it for context.

That reader changes every decision. It does not get bored, so the file is
exhaustive. It cannot see the instance, so every fact is marked existing or new.
It will build exactly what the file says, so an ambiguity here becomes a wrong
object rather than a question. And it benefits from tables, which the scenario
file bans.

---

## Skeleton

```
# <Client> — Object model and demo data
v<n> · <date> · companion to <client>-demo-scenario-v<n>.md
Snapshot verified against: general | banking

## 1. Existing objects touched
## 2. New objects
## 3. New columns on existing objects
## 4. Lookups
## 5. Logic to build
## 6. Seed data
## 7. Run before demo
## 8. Verification list
```

Omit a section with nothing in it. Never reorder them.

---

## 1–3 · Objects and columns

One table per object, and the object's own line says whether it exists:

```
### Case — existing (OOTB), section "Cases"

| Column | Caption | Type | Status | Used by |
|---|---|---|---|---|
| Subject | Subject | Text | existing | UC1 s5 |
| OriginId | Origin | Lookup → CaseOrigin | existing | UC1 s5 |
| CategoryId | Category | Lookup → CaseCategory | existing | UC1 s5, UC4 s2 |
| labWarrantyClaimId | Warranty claim | Lookup → labWarrantyClaim | **new** | UC3 s2 |
```

- **Status** is `existing` or **`new`**, for every row, with no exceptions. This
  column is the reason the file exists — a coding agent that cannot tell which
  columns to create will create all of them.
- **Used by** lists the step numbers that put this column on screen, from the
  scenario file. A column with an empty *Used by* is a column nobody asked for:
  delete it or find the step. This is the cheapest defect check in the whole
  skill, and it runs in both directions — a step that shows a field with no row
  here is the other half of the same bug.
- A new object gets its section or detail placement stated, because in Creatio a
  business object without one is invisible to the user.
- Flag anything custom that duplicates something out of the box. That is the
  most expensive mistake available here, and this file is where it gets caught
  before it is built.

---

## 4 · Lookups

```
### CaseCategory — existing lookup

| Value | Status |
|---|---|
| Incident | existing |
| Service request | existing |
| Information request | **new** |
```

Every value the demo needs, listed in full, each marked. A renamed value says
so and says what it was: `Prospect | **renamed** from "New"` — and renaming
changes it everywhere in the instance, which the line must note.

Never a GUID, never a record Id. The engineer and the coding agent both resolve
lookups by name, and the snapshot carries no Ids to leak.

---

## 5 · Logic to build

Every step in the scenario that carries a provenance marker other than
*(seeded)* has a line here, and the line names the step it serves:

```
- **Process** `Run warranty check` — on Case where **Status** = "Completed":
  creates labWarrantyClaim, sets **Coverage** from the account's OEM contract,
  sets **Reimbursable**. Serves UC3 s2 *(created by the process)*.
- **Business rule** on labWarrantyClaim: **Reimbursable** = labour + parts.
  Serves UC3 s3 *(calculated by the rule)*.
```

Use the mechanism names from `best-practices.md` section 1 exactly — page
business rule, entity business rule, business process, DCM case, approval,
printable. The coding agent builds by those names.

---

## 6 · Seed data

The records the demo needs, by name, with the field values that matter, **in the
state the first step expects**:

```
### Contact

| Name | Account | Mobile phone | Notes |
|---|---|---|---|
| Tiffany Jane Martin | Deloitte Germany | +49 151 2233445 | 3 incoming calls seeded |
```

Exact counts and amounts. Never "a few leads", never "10 sample records" without
naming them. If a step shows a total, the rows that add up to it are here.

This section is what replaces the Foundation section of an older contract: every
record any use case needs exists here in that use case's opening state, which is
what lets a use case be run on its own without another one having been run
first.

---

## 7 · Run before demo

The reset the scenario's one-line *Before you present* points at: which records
the process restores, and to which values. A demo that cannot be run twice is a
demo that cannot be rehearsed.

---

## 8 · Verification list

A fenced block of every name asserted anywhere in either file, in the grammar
`scripts/model.sh check` reads:

````
```text
Case
Case.Subject
Case.CategoryId
CaseCategory=Incident
CaseCategory=Information request
Contact.MobilePhone
```
````

Derive it from sections 1–6 rather than typing it separately, so the two cannot
drift, and paste the run's result into the conversation — not into the file.
`MISSING` here is not automatically a problem: a new column and a new lookup
value are *supposed* to be missing, and the list is how you prove the rest are
not. What it catches is the opposite mistake — a column marked `existing` that
does not exist.

```bash
sh scripts/model.sh check --file verification.txt
```
