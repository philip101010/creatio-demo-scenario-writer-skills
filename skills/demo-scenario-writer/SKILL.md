---
name: demo-scenario-writer
description: Rewrite a solution consultant's free-form Creatio demo scenario into the format an engineer can build from and a consultant can present from — use cases kept as they wrote them, split into phases, with narration in bubbles and every on-screen value carrying its provenance — plus a separate object-model file for the coding agent. Closes the logic and connectedness gaps by asking before writing, never by guessing. Use when someone provides a demo scenario, demo notes, a client call summary, use cases in free form or a scenario docx for a Creatio demo and wants it reformatted, checked, or turned into a build-ready scenario.
---

# Demo scenario writer

## What this is for

A solution consultant writes their demo in free form: use cases one after
another, business language, in whatever order the client call went. It is
readable by them and by nobody else. The engineer cannot build from it and
neither can a coding agent.

You turn it into two files — a scenario the consultant presents from, and an
object model the build reads — without losing a detail of what they wrote,
without redesigning their use cases, and without quietly inventing the answers
to the questions their text left open.

## The three things that decide everything

**Nothing is lost.** Every sentence of the source lands somewhere and you can
say where. A sentence you deliberately left out is reported with its reason.
This is a rewrite, not a summary — see `reference/question-gate.md`, *Coverage*.

**Their structure survives.** The use cases are theirs: same count, same order,
same numbers. A long one gets phases. You are making their scenario legible, not
proposing a better one.

**Their voice survives.** The pain points, the value language, the client's own
vocabulary and the numbers the story hangs on move into the narration bubbles
nearly intact. A rewrite that improves the consultant's phrasing into house
style has deleted the thing they wrote the scenario for.

And one thing that is not negotiable: **ask before you write.** Everything that
does not hold together gets asked, in one message, before the document exists —
never resolved by a plausible guess. That is the gate this skill is built
around.

## Read these before writing

1. `reference/format.md` — the document contract. Non-negotiable.
2. `reference/question-gate.md` — what to ask, in which order, and how.
3. `reference/objects-file.md` — the second deliverable, written for Claude Code.
4. `reference/golden-use-case.md` — one worked example across both files, with
   the consultant's original text beside it. Match its density.
5. `reference/best-practices.md` — what you may specify, what you may not, and
   what to decide instead of asking.
6. `reference/anti-examples.md` — real failures and their fixes.

---

## Two modes

**Rewrite mode** — the consultant drops a finished or half-finished scenario in
and asks for it to be reformatted or checked. This is the flow below, and it is
the mode this skill currently implements.

**Rewrite mode has one thing it cannot decide.** The scenario ends with a
*Basis vs. nice-to-have* table, and what counts as basis is a commercial
position, not a technical read. You draft it and the consultant rules on it —
Tier C of the gate.

**Co-writing mode** — the consultant drops in client context (files, a call
transcript, a deck) and starts inventing use cases out loud, one at a time,
phase by phase, while you build the scenario alongside them and keep it current
after every addition. Not yet specified. If a consultant asks for it, say the
skill does the rewrite properly today and offer to work through their use cases
one by one into the same format by hand.

Decide the mode from what arrived, not by asking: a scenario in the message is
rewrite mode; client material with no use cases yet is co-writing.

---

## Rewrite mode — the flow

### Step 1 — Map the source

Read the whole scenario before touching anything. Then tag every sentence with
where it will land — step, bubble, object, flow line, header, question, or
dropped-with-a-reason. `question-gate.md`, *Coverage*, has the tag list.

This is working material, not a deliverable. Its purpose is that by the end of
the job you can answer "where did my third paragraph go" without re-reading
their file.

Two things surface here for free: the use case boundaries the consultant already
drew, and the sentences that are narration rather than action. Keep both.

### Step 2 — Run the ten logic checks

Walk `question-gate.md` Tier A over the mapped source: orphan preconditions,
dead results, actor jumps, impossible order, silent mechanisms, phase boundaries
that do not hold, two-reading steps, contradictions, unexplained terms,
unreachable pages.

Anything a check fires on is either resolvable from `best-practices.md`
section 2 — and then you resolve it and record what you did — or it is a Tier A
question.

**Check 5, silent mechanism, is where the value of this skill sits.** A result
with no cause is the defect that survives every review and then fails in the
room. Every on-screen value must be either typed by the presenter or carry a
provenance marker; where you cannot name what produced it, ask.

### Step 3 — Ask Tier A, once

One message, numbered, every question three lines: what it blocks, the question
with their own words quoted back, and the default you will apply if they do not
answer. Say that unanswered items ship as open questions with the default
already written into the step.

Wait once. Then proceed regardless — do not stall and do not chase.

### Step 4 — Verify every name

Collect every object, field, lookup and lookup value the two files will assert,
one per line, and check the list in a single call:

```bash
sh scripts/model.sh check --file verification.txt
```

Items read as `Account`, `Case.PriorityId`, `CaseStatus=New`. `OK` returns the
field's type and lookup target; `MISSING` returns the closest real name, or the
values a lookup actually holds. Add `--banking` for banking, insurance and
financial services clients — and the snapshot you used goes in the objects file
header, because a finding from one snapshot never carries over to the other.

`MISSING` is not automatically a problem: a new column and a new lookup value
are supposed to be missing, and are marked **new** in the objects file. What the
list catches is a name marked `existing` that does not exist.

The single-name commands are for exploring, before you know what to put in the
list:

```bash
sh scripts/model.sh search opportunit          # which object is this?
sh scripts/model.sh object Case                # what fields does it have?
sh scripts/model.sh lookup CaseStatus          # what values exist?
sh scripts/model.sh field priority --object Case
sh scripts/model.sh sections                   # what has a UI section?
```

Run these from this skill's own directory — `scripts/` and `assets/` are
relative to it. `model.sh` works the same on macOS, Linux and Windows: it finds
a real Python 3 whatever it is called on that machine, needs nothing installed
beyond it, and locates the snapshots relative to itself. If it reports no
interpreter, say so and stop; a name you could not verify is not a name you may
write down.

Never open the tables in `assets/` yourself, and never open the xlsx in
`snapshots/` — that is the maintainer's source, 36 000 rows of it.

Then check every mechanism against `best-practices.md` section 1. A mechanism
not on that list is a question for the engineer, not an assumption.

### Step 5 — Write both files

In one pass, in the exact structure of `format.md` and `objects-file.md`. The
scenario file carries the narrative; the objects file carries the model and the
seed data. A fact appears in exactly one of them.

Cross-check the pair in both directions before delivering: every column in the
objects file names the steps that put it on screen, and every field a step shows
has a row in the objects file. A column with no step is a column nobody asked
for; a step with no row is a build item nobody will build.

### Step 6 — Hand over, and interview on scope

In the conversation, not in the documents:

- the two file paths;
- use cases and step counts;
- the coverage residue — how many source sentences mapped, and every dropped one
  quoted with its reason;
- the `check` result;
- **Tier B** — one message of content questions, each with its default already in
  the draft;
- **Tier C** — the *Basis vs. nice-to-have* table read back row by row, for the
  consultant to flip. Draft each row with the removal test: take the capability
  out and if a step stops working it is basis, if only a bubble's claim shrinks
  it is nice-to-have, and if it turns on a customer-side decision it is
  `Open — <who> to decide`. Never attach a euro figure or an effort estimate to
  a row; the commercial team owns that, and the section says so.

Then one question, and nothing else: what to change.

---

## Hard rules

1. **The use case count and order are the consultant's.** Never merge, never
   split into new numbers, never renumber, never invent one. Long use cases get
   phases.
2. **Step numbers never shift**, across phases or revisions. A removed step
   leaves a gap.
3. **Every step ends on something visible on screen.** A step with nothing to
   look at belongs inside the one before it.
4. **Every value the presenter did not type carries its provenance**, in
   italics. No exceptions — this is the rule the whole format hangs on.
5. **One path.** *If*, *or*, *optionally*, *alternatively*, *in case of* are
   banned from steps. An alternative flow is dropped or becomes its own step.
6. **A step holds three things only** — the action, what appears on screen, and
   what the system did to produce it — in short, plain, active sentences. Every
   step says **where on screen** it is visible, and automation the presenter
   cannot watch happen is written as them opening the place where its result
   shows. Every explaining sentence belongs to a bubble; arrows belong to the
   flow line and nowhere else.
7. **A fact appears once**, in one of the two files.
8. **No unverified assertion.** Object, field, lookup, value, mechanism —
   checked against the snapshot, or decided by the rules, or asked.
9. **Decide far more than you ask.** Check every candidate question against
   `best-practices.md` section 2 first. Missing lookup values, missing simple
   fields, licensing and standard admin operations are decided, not asked.
10. **Every question ships with the default already applied**, in the document
    and in the message that asks it.
11. **No GUIDs, no record Ids, no credentials** in either file.
12. **Banned words** — `format.md` section 9. Check your own draft against the
    list before delivering.
13. **Basis vs. nice-to-have is the consultant's call, not yours.** Draft it
    with the removal test, ask row by row, take their answer verbatim even
    where it contradicts your reasoning, and leave no cell blank — an item
    they will not classify is `Open — <who> to decide`.
14. **Never quantify scope.** No money, no man-days, no effort estimates,
    anywhere in either file.
15. **Nothing outside the sections** either contract defines.

## What good looks like

A five-use-case scenario runs about 700–1 100 words of body text, with two to
four bubbles per use case and no bubble narrating what the next step already
shows. The objects file is as long as it needs to be; nobody skims it.

The test of the pair is a colleague who was not on the client call: they read
the scenario once and could present it, and a coding agent reads the objects
file and builds without asking a question.
