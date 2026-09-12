# The object model file — written for a coding agent

`<client>-objects-v<n>.md` is the second deliverable. Its reader is not a person
skimming in a meeting: it is Claude Code, opening the file as the build brief for
the demo, with the scenario file open beside it.

That reader changes every decision. It does not get bored, so the file is
exhaustive. It cannot see the instance, so every fact is marked. It will build
exactly what the file says, so an ambiguity here becomes a wrong object rather
than a question. And it benefits from tables, which the scenario file bans.

**This file says what to add and what to change — not what a Creatio looks
like.** A demo is almost never built on an empty stand. Half of what the
scenario needs is already there, and the expensive mistake is rebuilding it.
So the file is written *after* looking at the instance, and everything in it
carries one of three states.

---

## The three states

| State | Means | How it is established |
|---|---|---|
| `existing (OOTB)` | ships with Creatio | verified against the snapshot with `model.sh check` |
| `existing (instance)` | already built on this stand | **read from the instance**, or the consultant's claim, marked as which |
| **`new`** | this demo has to create it | absent from both |

The middle state is why the investigation step exists. The snapshot is
out-of-the-box only: it cannot tell you that somebody added **Channel** to Case
for the first customer meeting, and a coding agent that cannot tell will either
rebuild it or treat it as standard.

An `existing (instance)` row that came from the consultant rather than from the
instance says so — `existing (instance, unverified)` — because those are the
rows a build discovers are missing at the worst possible moment.

---

## Investigating the instance

Do this before writing a line of this file, whenever the instance is reachable.

With clio registered for the stand, the reads that matter:

```
list-environments                      is this stand registered at all?
find-entity-schema      search-pattern the client's prefix - what was added
get-entity-schema-properties           the MERGED view: columns from all packages
get-entity-schema-column-properties    one column's real type and lookup target
list-packages / list-apps              which package a demo build would go into
list-app-sections / list-pages         what is already on screen
```

`get-entity-schema-properties` without a package name returns the merged view
across every package. Use that one for column discovery: an empty list from a
single-package read does not prove a column is absent.

Then, for each object the scenario touches, answer three questions and write the
answers into the tables below:

1. **Which columns already exist** — OOTB or added on this stand.
2. **Which lookups already hold the values the scenario needs**, and which need
   a value added or renamed.
3. **What is already built that the scenario could use instead of a new object**
   — a section, a detail, a page, a process with the same job.

**If the stand is not reachable** — not registered, credentials not shared,
offline — say so in the file header, mark every non-OOTB row
`existing (instance, unverified)`, and report it at hand-over. Do not quietly
promote a consultant's claim to a verified fact; the whole value of the state
column is that it distinguishes them.

---

## Skeleton

```
# <Client> — Object model
v<n> · <date> · companion to <client>-demo-scenario-v<n>.md
Snapshot: general | banking
Instance: <url> — read on <date> | not reachable, instance rows unverified

## 1. What is already there
## 2. Objects and columns
## 3. Lookups
## 4. Pages and details
## 5. Seed data
## 6. Verification list
```

Omit a section with nothing in it. Never reorder them.

---

## 1 · What is already there

Three to six lines, before any table: what the investigation found, in plain
words. Which app or package the earlier build lives in, what it already carries
that this scenario needs, and the one or two things everybody assumes exist and
do not.

This section is what stops a build starting with a rebuild.

---

## 2 · Objects and columns

One table per object, and the object's own line says whether it exists:

```
### Case — existing (OOTB), section "Cases"

| Column | Caption | Type | State | Used by |
|---|---|---|---|---|
| Subject | Subject | Text | existing (OOTB) | s5 |
| CategoryId | Category | Lookup → CaseCategory | existing (instance) | s10, s37 |
| labRegistrationSourceId | Registration source | Lookup → labCaseRegistrationSource | **new** | s5, s13 |
```

- **State** on every row, no exceptions. This column is the reason the file
  exists.
- **Used by** lists the step numbers that put this column on screen. A column
  with an empty *Used by* is a column nobody asked for: delete it or find the
  step. The check runs in both directions — a step showing a field with no row
  here is the other half of the same bug.
- A new object states its section or detail placement, because a Creatio
  business object without one is invisible to the user.
- Flag anything custom that duplicates something out of the box, or something
  the instance already has. That is the most expensive mistake available here,
  and this file is where it gets caught.

---

## 3 · Lookups

```
### CaseCategory — existing (instance) lookup

| Value | State |
|---|---|
| Order Status | existing (instance) |
| Quote request | **new** |
| Waiting for customer | **renamed** from "Waiting for response" |
```

Every value the demo needs, in full, each marked. A rename says what it was —
and that renaming changes the caption everywhere in the instance, which the line
must note.

Where a lookup holds two records with the same display value, say so and say to
bind by record rather than by caption. The snapshot has forty-three such
lookups, and "resolve it by name" silently picks one of them.

Never a GUID, never a record Id.

---

## 4 · Pages and details

What has to appear on which page: a new tab, a new detail and the object it
lists, a mini page and its fields, a dashboard widget and its filter. Each with
its state and the steps it serves.

Placement instructions that the consultant wrote into their narrative — "the
subtasks list has to be reachable from the case at any time" — belong here, not
in a step.

---

## 5 · Seed data

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

Every record any use case needs exists here in that use case's opening state,
which is what lets a use case run on its own without another one having been run
first.

---

## 6 · Verification list

A fenced block of every name this file asserts as `existing (OOTB)`, in the
grammar `scripts/model.sh check` reads:

````
```text
Case
Case.Subject
CaseCategory=Incident
Contact.MobilePhone
```
````

Derive it from the tables rather than typing it separately, so the two cannot
drift, and paste the run's result into the conversation — not into the file.

`MISSING` here is not automatically a problem: a **new** column and a **new**
lookup value are supposed to be missing. What the list catches is the opposite
mistake — a row marked `existing (OOTB)` that does not exist.

`existing (instance)` rows are **not** in this list. The snapshot is
out-of-the-box and cannot confirm them; they were confirmed against the instance
or they are marked unverified.

```bash
sh scripts/model.sh check --file verification.txt
```
