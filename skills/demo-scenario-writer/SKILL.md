---
name: demo-scenario-writer
description: Rewrite a solution consultant's free-form Creatio demo scenario into three files — a narrative scenario they present from, an object model of what to add or change on the demo stand, and the processes, stage models and rules that make it move. Reads the existing instance first, so the build is told what is already there rather than rebuilding it. Closes the step-logic gaps by asking before writing, never by guessing. Use when someone provides a demo scenario, demo notes, a client call summary, use cases in free form or a scenario docx for a Creatio demo and wants it reformatted, checked, or turned into a build-ready scenario.
---

# Demo scenario writer

## What this is for

A solution consultant writes their demo in free form: use cases one after
another, business language, in whatever order the client call went. It is
readable by them and by nobody else. The engineer cannot build from it and
neither can a coding agent.

You turn it into three files — a scenario the consultant presents from, an
object model of what to add or change on the stand, and the processes, stage
models and rules that make the demo move — without losing a detail of what they
wrote, without redesigning their use cases, and without quietly inventing the
answers to the questions their text left open.

The three split the way the work does. The consultant reads one document and
never the other two. The build reads the object model to know what to create,
and the processes file to know what makes it run — and those fail differently
enough that mixing them buries the stage model under column tables.

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

And one thing that is not negotiable: **the gate closes before you write.**
Everything that breaks the logic, the consistency or the order of the steps is
asked in one message before the document exists, with options to pick from.
Everything else you decide yourself and report at hand-over. What never happens
is a plausible guess going into a step with nobody told about it.

## Read these before writing

1. `reference/format.md` — the document contract. Non-negotiable.
2. `reference/question-gate.md` — what to ask, in which order, and how.
3. `reference/objects-file.md` — the object model, written for Claude Code, and
   how to read the instance before writing it.
4. `reference/processes-file.md` — the stage models, processes and rules.
5. `reference/golden-use-case.md` — one worked example, with the consultant's
   original text beside it. Match its density.
6. `reference/best-practices.md` — what you may specify, what you may not, and
   what to decide instead of asking.
7. `reference/anti-examples.md` — real failures and their fixes.

---

## Two modes

**Rewrite mode** — the consultant drops a finished or half-finished scenario in
and asks for it to be reformatted or checked. This is the flow below, and it is
the mode this skill currently implements.

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

Walk `question-gate.md` Tier A over the mapped source. Ten things fire; only six
of them earn a question, and the line is sharp: **you ask only about the logic,
the consistency and the order of the steps.** Orphan preconditions, dead
results, actor jumps, impossible order, contradictions, unreachable pages.

The other four — silent mechanisms, phase boundaries, two readings, unexplained
terms — you resolve, write into the step, and report at hand-over.

**Silent mechanism is the one to watch.** A result with no stated cause is the
defect that survives every review and then fails in the room, and it fires more
often than everything else combined. Name the mechanism from
`best-practices.md` section 1, write the provenance marker, carry it into the
objects file — do not ask. The consultant left it out because they do not know
what produced it either.

### Step 3 — Ask Tier A, once, with options

One message, numbered, before a line of the document exists. Every question
names what it blocks, quotes their own words back, and offers **two to four
concrete options** — one of them marked as recommended, each with half a line on
what it costs elsewhere in the scenario. Include the option that keeps their
text as written whenever it is viable.

If you cannot name two concrete resolutions, it is not a question yet: you have
not understood the ambiguity well enough to ask about it.

Say that anything unanswered goes with the recommendation. Wait once. Then
proceed — do not stall and do not chase.

### Step 4 — Read the instance

A demo is almost never built on an empty stand, and the expensive mistake is
rebuilding what is already there. Before writing the object model, look at the
instance the scenario names.

With clio registered for that stand:

```
list-environments                       is it registered at all?
find-entity-schema   search-pattern     what the client prefix already carries
get-entity-schema-properties            the MERGED view — columns from all packages
get-entity-schema-column-properties     one column's real type and lookup target
list-packages / list-apps               where a build would put things
list-app-sections / list-pages          what is already on screen
```

Read `get-entity-schema-properties` **without** a package name. That returns the
merged view across every package; an empty column list from a single-package
read does not prove a column is absent.

For every object the scenario touches, establish three things: which columns
already exist, which lookups already hold the values the scenario needs, and
what is already built that the scenario could use instead of something new.

This is what produces the middle state in the object model — `existing
(instance)`, meaning *already built here, do not rebuild*. The snapshot cannot
tell you that: it is out-of-the-box only.

**If the stand is not reachable** — not registered, no credentials, offline —
say so in the object model header, mark every non-OOTB row `existing (instance,
unverified)`, and report it at hand-over. Never promote a consultant's claim to
a verified fact; distinguishing the two is the whole point of the state column.

### Step 5 — Verify every name against the snapshot

Collect every object, field, lookup and lookup value the files will assert as
out-of-the-box, one per line, and check the list in a single call:

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

### Step 6 — Write the three files

The scenario holds no questions and no record of what you changed. It is the
resolved demo, written to the answers from Step 3.

In one pass, in the exact structure of `format.md`, `objects-file.md` and
`processes-file.md`. The scenario carries the narrative; the object model
carries what to add or change and the seed data; the processes file carries the
stage models, processes, rules, AI skills and integrations. **A fact appears in
exactly one of the three.**

Two cross-checks before delivering, both of which run in both directions:

- **Columns against steps.** Every column in the object model names the steps
  that put it on screen, and every field a step shows has a row. A column with
  no step is a column nobody asked for; a step with no row is a build item
  nobody will build.
- **Provenance markers against the processes file.** Collect every marker in the
  scenario that is not *(seeded)*. Each one has a line in the processes file
  naming its step. A marker with no line is unbuilt automation; a line serving
  no step is work nobody asked for.

### Step 7 — Hand over

In the conversation, not in the documents:

- the three file paths;
- use cases and step counts;
- **what the instance read found** — what was already there, and anything the
  scenario assumed exists that does not. If the stand was unreachable, say so
  plainly and name what is therefore unverified;
- the coverage residue — how many source sentences mapped, and every dropped one
  quoted with its reason;
- the `check` result;
- **what you decided** — the mechanisms you named where the source stated none,
  and the wording you resolved, one line each. This is the deviation record, and
  it belongs here rather than in the document, where the consultant can push
  back on it while it is still cheap;
- **Tier B** — one message of content questions, each with its default already in
  the draft;
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
7. **A fact appears once**, in exactly one of the three files.
8. **No unverified assertion.** Object, field, lookup, value, mechanism —
   checked against the snapshot, or decided by the rules, or asked.
9. **Decide far more than you ask.** Check every candidate question against
   `best-practices.md` section 2 first. Missing lookup values, missing simple
   fields, licensing and standard admin operations are decided, not asked.
10. **Every question is asked in the chat before the document exists**, with two
    to four concrete options and one of them recommended. No question and no
    deviation record ever appears in the document itself.
11. **No GUIDs, no record Ids, no credentials** in any of the three files.
12. **Banned words** — `format.md` section 7. Check your own draft against the
    list before delivering.
13. **Never quantify scope.** No money, no man-days, no effort estimates,
    anywhere.
14. **Never mark something existing on the instance without having looked**, or
    having said that you could not.
15. **Nothing outside the sections** the three contracts define.

## What good looks like

A five-use-case scenario runs about 700–1 100 words of body text, with two to
four bubbles per use case and no bubble narrating what the next step already
shows. The objects file is as long as it needs to be; nobody skims it.

The object model and the processes file are as long as they need to be; nobody
skims them.

The test of the set is a colleague who was not on the client call: they read the
scenario once and could present it, and a coding agent reads the other two and
builds without asking a question.
