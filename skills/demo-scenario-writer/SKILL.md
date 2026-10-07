---
name: demo-scenario-writer
description: Turn a solution consultant's Creatio demo case — their own scenario, free-form notes, a client call summary, or discovery material with no use cases yet — into two build-ready files: a narrative scenario they present from, and an object model of what to add or change on the demo stand, pages included. Writes the whole thing itself in one pass, closes every gap in the step logic with the best-fitting step or decision, and hands the result over as proposals the consultant accepts or changes — it does not ask questions first. Reads the existing instance so the build is told what is already there. Then revises both files from the consultant's feedback. Use when someone provides a demo scenario, demo notes, a client call summary, use cases in free form, discovery documents or a scenario docx for a Creatio demo and wants it written, reformatted, checked, turned into a build-ready scenario, or revised after review.
---

# Demo scenario writer

## What this is for

A solution consultant writes their demo in free form: use cases one after
another, business language, in whatever order the client call went. It is
readable by them and by nobody else. The engineer cannot build from it and
neither can a coding agent. Sometimes there is not even that — only the
discovery documents, and the use cases still have to be found in them.

You turn it into two files — a scenario the consultant presents from, and an
object model of what to add or change on the stand, with the pages it needs —
without losing a detail of what they wrote and without making them answer
anything before they have something to read. Processes, stage models, rules and
AI skills are not written down: the step descriptions carry them, and the build
agent derives them from the provenance markers.

The consultant's job is to **review**, not to specify. You write the whole
thing, you close every gap with the step you judge fits best, you say plainly
which parts are yours, and they change what they disagree with. Then you issue
the next version.

The two files split the way the work does. The consultant reads the scenario and
never the object model. The build agent reads the scenario for what happens and
what produces it, and the object model for what to create.

## The three things that decide everything

**Nothing is lost.** Every sentence of the source lands somewhere and you can
say where. A sentence you deliberately left out is reported with its reason.
This is a rewrite, not a summary — see `reference/gap-closing.md`, *Coverage*.

**Their structure survives.** When the consultant wrote use cases, those are
theirs: same count, same order, same numbers. A long one gets phases. You are
making their scenario legible, not proposing a better one.

**Their voice survives.** The pain points, the value language, the client's own
vocabulary and the numbers the story hangs on move into the narration bubbles
nearly intact. A rewrite that improves the consultant's phrasing into house
style has deleted the thing they wrote the scenario for.

And one thing that is not negotiable: **a gap is closed by you, visibly.** Every
hole in the logic, the consistency or the order of the steps gets the
best-fitting step or decision written in, and a numbered proposal in the
hand-over saying what was missing, what you wrote, and how to undo it. What
never happens is a plausible guess going into a step with nobody told — and
what also never happens is the consultant being asked to choose before there is
a draft to react to.

## Read these before writing

1. `reference/format.md` — the document contract. Non-negotiable.
2. `reference/gap-closing.md` — the gap checks, how to pick the closing step,
   and how proposals are written.
3. `reference/objects-file.md` — the object model with its pages, written for
   Claude Code, and how to read the instance before writing it.
4. `reference/golden-use-case.md` — one worked example, with the consultant's
   original text beside it. Match its density.
5. `reference/best-practices.md` — what you may specify, what you may not, and
   what to decide.
6. `reference/anti-examples.md` — real failures and their fixes.

---

## Two inputs, one flow

Decide the input from what arrived, never by asking:

**The consultant wrote use cases** — a finished or half-finished scenario, notes
in demo order, a docx. Their use cases are the skeleton. Go to Step 1.

**There are no use cases yet** — a call transcript, a requirements summary, a
deck, client material. Step 1 starts by drafting them (Step 1b). The set you
propose is itself the first proposal in the hand-over, and the consultant may
reshape it freely in the revision.

The rest of the flow is the same. Either way the consultant sees a complete
draft before they are asked for anything.

---

## The flow

### Step 1 — Map the source

Read the whole source before touching anything. Then tag every sentence with
where it will land — step, bubble, object, flow line, header, proposal, or
dropped-with-a-reason. `gap-closing.md`, *Coverage*, has the tag list.

This is working material, not a deliverable. Its purpose is that by the end of
the job you can answer "where did my third paragraph go" without re-reading
their file.

Two things surface here for free: the use case boundaries the consultant already
drew, and the sentences that are narration rather than action. Keep both.

### Step 1b — Draft the use cases (only when there are none)

From discovery material, find the demo the client actually asked for.

- Take the client's own words for what hurts and what they want to see. Those
  become the bubbles later.
- Three to five use cases; a slot is short. Order them so the story builds and
  the strongest moment lands before attention drops, not last.
- Each one is anchored to a stated pain or request in the material, and has one
  visible payoff. A use case you cannot anchor to the material does not go in.
- Say in the hand-over what you took as the decision the audience must make, and
  which use case carries the moment that lands it. That sentence replaces the
  goal interview: you state your reading and the consultant corrects it.

Treat the resulting use cases as the consultant's text from here on, and apply
the same checks to them.

### Step 2 — Close the gaps

Walk `gap-closing.md` over the mapped source. Ten things go wrong in a free-form
scenario; **all ten are closed by you**. Six affect whether the steps hold
together (orphan precondition, dead result, actor jump, impossible order,
contradiction, unreachable page) and four are resolved in passing (silent
mechanism, phase boundary, two readings, unexplained term).

For every hit, pick the closing step by the ranking in `gap-closing.md`: keep
their text when it is viable, otherwise the smallest change that makes the
logic hold, built from mechanisms on the `best-practices.md` white list. Write
it straight into the scenario and keep a record: where, what was missing, what
you wrote, and the one-line undo. That record becomes the proposals list in the
hand-over.

**Silent mechanism is the one to watch.** A result with no stated cause is the
defect that survives every review and then fails in the room, and it fires more
often than everything else combined. Name the mechanism from
`best-practices.md` section 1, write the provenance marker, carry it into the
objects file. The consultant left it out because they do not know what produced
it either.

If a gap has no answer anywhere in the source — the metric has no source, the
term means something only the client knows — do not stop. Close it with the
cheapest honest version (leave the metric off, use a labelled placeholder),
mark the proposal **needs your input**, and carry on. A draft that is missing
one thing is still a draft.

### Step 3 — Read the instance

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
An unreachable stand does not stop the draft.

### Step 4 — Verify every name against the snapshot

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
not on that list is written as the closest listed one and carried as a proposal
flagged **engineer to confirm** — never silently assumed.

### Step 5 — Write the two files

The scenario holds no questions, no proposal markers and no record of what you
changed. It is the resolved demo, with your proposals already written in.

In one pass, in the exact structure of `format.md` and `objects-file.md`. The
scenario carries the narrative, and with it everything the build agent needs to
know about automation: each step says what happens and, in its provenance
marker, what produces it. The object model carries what to add or change —
objects, columns, lookups, pages and details — and the seed data. **A fact
appears in exactly one of the two.**

Two cross-checks before delivering, both of which run in both directions:

- **Columns against steps.** Every column in the object model names the steps
  that put it on screen, and every field a step shows has a row. A column with
  no step is a column nobody asked for; a step with no row is a build item
  nobody will build.
- **Provenance markers against the white list.** Collect every marker in the
  scenario that is not *(seeded)*. Each names a mechanism from
  `best-practices.md` section 1, and the step it sits in states the trigger and
  the visible result well enough to build from. A marker with no mechanism is
  automation nobody can build; a column that only a marker writes has to show
  in the object model with that step in its *Used by*.

### Step 6 — Hand over

In the conversation, not in the documents. In this order, short:

- the two file paths, and use cases with step counts;
- **Proposals** — every gap you closed, numbered `P1`, `P2`…, grouped as *steps
  I added or changed*, *mechanisms I named*, and *defaults I applied* (client
  names, numbers, currency, emulated integrations, branding, slot). Each is
  three lines at most: where, what was missing and what you wrote, and what to
  say to undo it. Anything the draft cannot settle by itself is marked **needs
  your input** or **engineer to confirm**, and says what it blocks;
- **what the instance read found** — what was already there, and anything the
  scenario assumed exists that does not. If the stand was unreachable, say so
  plainly and name what is therefore unverified;
- the coverage residue — how many source sentences mapped, and every dropped one
  quoted with its reason;
- the `check` result.

Close with one line and nothing else: reply with what to change — by proposal
number, by use case and step, or in your own words — and the next version
follows. Do not add a questionnaire. The proposals are the questions, already
answered with the best available answer.

### Step 7 — Revise from feedback

The consultant answers in whatever form they like: "P3 no, do it the other way",
"UC2 step 5 is wrong, the manager sees it first", "make UC4 shorter", or a
pasted new paragraph. Read all of it, then:

1. Sort each comment into *accepted as proposed*, *changed*, *new content*, or
   *cut*. A proposal the consultant did not mention stands; silence is
   acceptance. A bare "no" on a proposal means apply its stated undo.
2. Apply to **both files** and re-run Step 4 and the two Step 5
   cross-checks — a change to a step moves columns and markers too.
3. Issue `v<n+1>` of both, never overwriting the previous set. Step numbers
   do not shift: a removed step leaves a gap, an added step takes the next free
   number in its use case.
4. Hand over the revision as a short change list mapping each comment to what
   changed, and list any knock-on effects (a step that now needs a new column, a
   marker with a new mechanism). A knock-on you had to close yourself is a new
   numbered proposal, continuing the sequence.

Then the same one line: reply with what to change. Repeat until they stop
replying with changes.

---

## Hard rules

1. **The use cases the consultant wrote keep their count, order and numbers.**
   Never merge, never split into new numbers, never renumber, never invent one.
   Long use cases get phases. Use cases you drafted from discovery material are
   proposal P1 and may be reshaped freely in the revision.
2. **Step numbers never shift** across phases or revisions. A removed step
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
7. **A fact appears once**, in exactly one of the two files.
8. **No unverified assertion.** Object, field, lookup, value, mechanism —
   checked against the snapshot, or decided by the rules, or carried as a
   flagged proposal.
9. **Never ask; propose.** Do not put a question to the consultant before the
   draft exists, and do not hand over a questionnaire with it. Every gap is
   closed with the best-fitting step, recorded as a numbered proposal with its
   one-line undo. A proposal may say **needs your input**, but the draft stands
   without it.
10. **No proposal, question or deviation record ever appears in either
    file.** They are reported in the conversation, where they can be answered
    while changing them is still free.
11. **No GUIDs, no record Ids, no credentials** in either file.
12. **Banned words** — `format.md` section 7. Check your own draft against the
    list before delivering.
13. **Never quantify scope.** No money, no man-days, no effort estimates,
    anywhere.
14. **Never mark something existing on the instance without having looked**, or
    having said that you could not.
15. **Nothing outside the sections** the two contracts define.
16. **Revisions are a new version of both files**, and the previous version
    stays on disk.

## What good looks like

A five-use-case scenario runs about 700–1 100 words of body text, with two to
four bubbles per use case and no bubble narrating what the next step already
shows. The object model is as long as it needs to be; nobody skims it.

The test of the set is a colleague who was not on the client call: they read the
scenario once and could present it, and a coding agent reads both and builds
without asking a question.

The test of the hand-over is the consultant's first reply. If it is "fine,
except P4 and P7", the draft was right. If it is a list of answers to things you
should have decided, the proposals were too timid.
