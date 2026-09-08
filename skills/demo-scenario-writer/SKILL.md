---
name: demo-scenario-writer
description: Turn a solution consultant's free-form demo notes into a build-ready Creatio demo scenario — modular use cases, single happy path, verified against the Creatio object model, with genuinely unresolved points raised as questions inside the use case instead of invented functionality. Use when someone provides demo notes, a client call summary, a draft demo script or a use-case description for a Creatio demo and wants a scenario, demo script or technical spec the solution engineer can build from.
---

# Demo scenario writer

## What this is for

A solution consultant finishes a client call and writes notes: free-form, in any
order, business language, technically naive in places. You turn that into one
document the solution engineer builds from without a rewrite cycle.

The engineer writes nothing. They read your document, join one sync call to
resolve the open questions, and start building. Everything they need is in the
document — nothing is left to interpretation and nothing is invented.

## The four things that make this work

**One reading only.** Every sentence has exactly one possible meaning. A step
either states a fact or is an open question. There is no third state.

**Use cases that test independently.** A use case depends on the Foundation,
never on another use case having been run. If UC4 needs a case in progress, that
case exists in the Foundation data set.

**Never invent functionality.** You have no access to a demo environment. You
have an object-model snapshot and a best-practices file. Anything you cannot
verify against them and cannot decide from the rules is an `?OPEN` addressed to
the person who can actually answer it.

**Decide far more than you ask.** A question that has one correct answer is not
a question — it is you failing to do the job. Missing lookup values, missing
simple fields, licensing, standard admin operations and single-implementation
mechanisms are all decided, not asked. See `reference/best-practices.md`
section 2 before you write any `?OPEN`.

## Read these before writing

1. `reference/format.md` — the document contract. Non-negotiable.
2. `reference/best-practices.md` — what you may specify, what you may not, what
   to decide instead of asking, and how to query the object model.
3. `reference/golden-use-case.md` — one worked use case. Match its density.
4. `reference/anti-examples.md` — real failures and their fixes.

---

## The flow

### Step 1 — Intake

Read the consultant's input. Then ask, in **one single message**, only the
checklist items the input does not already answer. Never ask about something they
already told you. Never ask one question at a time.

1. Client name, industry, size. **Is it banking, insurance or financial services?**
   This decides which object-model snapshot you verify against.
2. Link to the client's website — the source of their product names and terminology.
3. Demo date and slot length.
4. Who is in the room: role, and what that person must be convinced of.
5. Who clicks during the demo — the consultant or the solution engineer.
6. Which instance: an existing stand, a new OOTB stand, or a specific one.
7. Base currency.
8. Languages: which ones, and is this a real translation of custom captions or
   the out-of-the-box language pack only?
9. Is the mobile application in scope?
10. If the input mentions calls or telephony: CTI emulator, or real telephony?
11. Branding: are the client's logo and colours applied in the demo?
12. What must not be shown.
13. Is there a reference — a previous demo or standard product this builds on?

Say plainly that unanswered items will appear in the document as open questions.
If the consultant does not answer some, proceed — do not stall and do not guess.

### Step 2 — Decompose

Cut the input into use cases. One wow-moment each, maximum eight steps, testable
alone in under ten minutes. A long use case in the input almost always contains
three to five of them; find the seams at the points where the role changes or
the wow changes.

Pull everything shared by two or more use cases into the Foundation: instances,
roles and access rights, the data set, global settings. Each fact lives in
exactly one place.

Give the Foundation data set every record any use case needs, in the state that
use case needs it. This is what removes the dependencies between use cases.

### Step 3 — Verify

First write the list. Go through the decomposition and put down every name the
document is going to assert — each object, each field, each lookup, each lookup
value — one per line, in a file:

```
Case
Case.PriorityId
CaseStatus=In progress
Order.labReturnType
```

Then verify the whole list in one call:

```bash
sh scripts/model.sh check --file spec.txt
```

One line comes back per name: `OK` with the field's type and lookup target, or
`MISSING` with the closest real name and, for a lookup value, the values that
are actually there. Exit code 1 means at least one name did not verify.

**The list is the discipline.** A name that never entered it is a name you did
not verify, and the batch call is what makes verifying all of them cheap enough
that there is no excuse to skip any: 35 names cost one call instead of 35.
Extend the file and re-run it whenever the draft grows a new name.

The single-name commands are for exploring, when you do not yet know what to
put in the list:

```bash
sh scripts/model.sh search opportunit          # which object is this?
sh scripts/model.sh object Case                # what fields does it have?
sh scripts/model.sh lookup CaseStatus          # what values exist?
sh scripts/model.sh field priority --object Case
sh scripts/model.sh sections                   # what has a UI section?
```

Add `--banking` for financial services clients.

Run these from this skill's own directory — `scripts/` and `assets/` are
relative to it. `model.sh` works the same on macOS, Linux and Windows: it finds
a real Python 3 whatever it is called on that machine, needs nothing installed
beyond it, and locates the snapshots relative to itself. If it reports no
interpreter, say so and stop; do not write build-spec lines you could not
verify.

Every object, field, lookup and lookup value gets checked. `MISSING` — or exit
code 1 — means **not verified**: absent from the snapshot, or present but empty
in it. A finding from one snapshot never carries over to the other. Query
through the commands above; never open the tables in `assets/` yourself, and
never open the xlsx in `snapshots/` — that is the maintainer's source, 36 000
rows of it.

`object` hides the six system columns (`Id`, `CreatedOn/By`, `ModifiedOn/By`,
`ProcessListeners`) that every object has and no demo spec needs; pass `--all`
if you actually need them.

**Not verified is not automatically a question.** A missing lookup value or a
missing simple column is a build-spec line, not an `?OPEN` — see
`reference/best-practices.md` section 2. It becomes a question only when there
is nothing to count, derive or add cheaply.

Check every mechanism against `reference/best-practices.md` section 1. A
mechanism not on that list is an `?OPEN` for the engineer.

### Step 4 — Write

Produce the whole document in one pass, in the exact structure of
`reference/format.md`. Deliver it as one Markdown file — see section 9 of the
format contract for the file name and what Markdown is allowed in it.

Open questions go in the `Open` part of the use case that needs them. There is no
collected list at the end of the document; the Open column of the use case index
is how the reader finds them.

### Step 5 — Ask what to change

End with a short message: the use case count, the number of open questions split
by addressee, and one question — what to change. Nothing else. No summary of the
document; they have the document.

---

## The three kinds of question

Getting the addressee right is the point of this whole skill. The original
problem was consultants guessing at technical decisions.

| Kind | Asked when | Asked of | Example |
|---|---|---|---|
| **Checklist** | Step 1, in one batch | Consultant | "Which languages, and is this a real translation or the OOTB language pack?" |
| **`?OPEN` business** | In the use case | Consultant | "Is the case assigned by the account's region or the contact's region?" |
| **`?OPEN` business** | In the use case | Consultant | "What counts as an RMA for this client? Nothing on Order marks a return, so the metric has no source." |
| **`?OPEN` platform** | In the use case | Engineer | "UC7 and UC9 need the same lookup restricted differently on two pages; one entity business rule cannot do both. Which page keeps the restriction?" |

**Never ask a consultant a platform question.** They cannot answer it, and their
attempt to answer it is exactly the technical guesswork this process removes.

**Never ask the engineer to pick a mechanism.** Ask for the outcome. "Which
mechanism: a process, a business unit change, or deactivation?" is you offloading
your own job. State the standard mechanism; ask what the end state should be.

---

## Hard rules

1. **One happy path.** No branches. *If*, *or*, *optionally*, *alternatively*,
   *in case of* are banned from steps. An alternative flow is its own use case or
   is dropped.
2. **A use case never requires another use case.** Only Foundation items.
3. **A fact appears once.** The happy path says what the user sees; the build
   spec says what to configure. If a line fits both, it goes in the build spec.
4. **No unverified assertion.** Object, field, lookup, value, mechanism — checked
   against the snapshot, or decided by the rules, or `?OPEN`.
5. **Decide before you ask.** Check every candidate question against
   `reference/best-practices.md` section 2 first.
6. **No GUIDs, no record Ids, no credentials** in the output.
7. **Acceptance is one-to-one with the happy path**, same numbering, every result
   observable on screen.
8. **Exact data.** Never "a few", never "several", never "10 sample records"
   without naming them.
9. **Banned words** — see `reference/format.md` section 7. Check your own draft
   against that list before delivering.
10. **Nothing outside the five sections.** No purpose, no goals, no brief summary,
    no closing notes, no collected question list.
11. **Never renumber a use case** once the consultant has seen the index.

## What good looks like

A five-use-case scenario is roughly 600–900 words of body text plus tables. If
you are well past that, you are duplicating something — most often a build-spec
line restating a step. Check that before anything else.

One use case, read once, built, its acceptance rows run, and on to the next —
without ever opening another section.
