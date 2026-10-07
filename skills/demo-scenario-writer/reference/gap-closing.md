# Gap closing

The consultant handed you a case. It has holes — every free-form scenario does.
You do not send them back to the consultant as questions. You close each one
with the step you judge fits best, write it into the draft, and hand it over as
a numbered proposal they can accept or change.

The reasoning is about attention. A consultant who is asked five questions
before they have anything to read answers "as you recommend" five times and
learns nothing from it; a consultant who is given a finished draft and a short
list of what was filled in reacts to something real, and spots the one
proposal that is wrong. Proposals cost them one line each, and only where they
disagree.

The work has three parts: **find** the gaps (ten checks), **close** them (the
ranking below), and **report** them (the proposal format). Then **revise** from
feedback, and **coverage**, which is the promise that nothing is lost.

---

## Find — ten checks

Ten things go wrong in a free-form scenario. All ten are closed by you. They
differ only in how much the closing step shows up in the hand-over: the first
six change the shape of the steps and are listed as *steps I added or changed*;
the last four are resolved in passing and are one line each.

### The six that change the steps

**1 · Orphan precondition.** A step acts on a record, role, page or value that no
earlier step created and no seed data provides.

> *"The manager approves the discount"* — no step created a discount request,
> and no earlier step put the manager anywhere near this record.

Close it with seed data when the record's identity does not change the story:
the request exists in its opening state, in the objects file. Close it with a
step when the precondition has to be *produced* on screen — the presenter
creates the request first.

**2 · Dead result.** A step produces something no later step, bubble or use case
ever uses. Either a step is missing after it, or the result is decoration.

> *"…and an approval task is created for the regional director."* Nobody opens
> it.

Close it with the shortest step that shows the result being used — the director
opens the task — when the consultant's wording says it matters. Fold it into a
bubble as a spoken claim when it is plainly colour. Never leave it as an
unexplained consequence.

**3 · Actor jump.** The acting role changes and the text does not say who is now
at the keyboard. A demo has somebody's screen on the projector at every moment,
and switching users costs minutes of a slot that is already short.

Close it by keeping one user on screen: give the demo user the rights the later
step needs and say so in the objects file. Write a user switch only when the
story is the hand-off itself, and then as its own step.

**4 · Impossible order.** A step reads a value that a later step writes, or shows
a state the flow has not reached yet.

Close it by moving the later write ahead of the read — the smallest reorder that
makes every step true. Step numbers in the first draft are free; they are fixed
from the first delivery on.

**5 · Contradiction.** Two places assert different things about the same record,
field, state or clock. Usually a scenario that grew over several client calls,
and usually invisible until someone does the arithmetic.

Close it by keeping the version the text states more specifically or later, and
adjusting the other to match. Report both.

**6 · Unreachable page.** The step happens somewhere the previous step could not
have navigated to.

Close it by writing the navigation into the step: I open the section, I click
the record. One clause, not a step.

### The four resolved in passing

**7 · Silent mechanism.** A result appears and nothing says what produced it. Name
the most likely mechanism from `best-practices.md` section 1, write the
provenance marker, and carry it into the objects file as the thing to build.
This fires more than any other check — the consultant does not know what
produced it either, which is why they left it out.

**8 · Phase boundary.** Where the phases fall is yours. Cut at a change of actor,
system or time; if the text offers no such turn, it is one phase.

**9 · Two readings.** A sentence that can be read two ways: pick the reading that
keeps the rest of the flow consistent and say which you picked. When the two
readings would build very differently, that is check 5 and gets a proposal of
its own.

**10 · Unexplained term.** Explain it on first use in a bubble, or cut it. A term
whose meaning is the client's own — where a wrong guess misdescribes their
business — becomes a proposal flagged **needs your input**, with the placeholder
meaning you used.

---

## Close — how to pick the step

For any gap there are usually several steps that would close it. Pick by this
ranking, top first, and stop at the first that fits:

1. **Their text as written**, whenever it can be made to hold with seed data or a
   named mechanism. They wrote it for a reason, and keeping it tells them you
   understood it rather than corrected it.
2. **The smallest change to the steps.** The option that moves the fewest other
   steps, objects and markers wins.
3. **Seed before produce.** A record that exists in its opening state beats a
   step that creates it, because it keeps the demo short and re-runnable.
4. **A mechanism from the white list.** Anything on `best-practices.md` section 1,
   named exactly. A mechanism not on it is written as the closest listed one and
   flagged **engineer to confirm**.
5. **The existing object before a new one.** Check `best-practices.md` section 5
   and what the instance read found.

Two guards apply to every closure:

- **Do not invent the story.** You close the logic between their steps; you do
  not add a feature, a use case or a claim they did not make. A closing step
  uses only what the consultant's text already established.
- **Do not hide it.** Whatever you wrote that was not in the source is a
  proposal in the hand-over. A closure with no proposal is a silent guess, which
  is the one failure this process exists to prevent.

When nothing in the source can settle a gap — the metric has no source on any
object, the term is the client's own — close it with the cheapest honest
version (leave the metric off, use a labelled placeholder), mark the proposal
**needs your input**, and carry on. The draft never waits.

### What you never write as a proposal

These have one correct answer. Decide them, put them in the objects file, and
give them one line under *mechanisms I named* — they are notes, not choices:

- a missing lookup value, or a missing simple field;
- a mechanism with exactly one implementation;
- licensing, entitlement, provider and feature availability;
- standard administrative operations (rights, ownership, deactivation);
- telephony: the CTI emulator, stated in the header.

`best-practices.md` section 2 has the full list.

---

## Report — the proposal format

Proposals live in the hand-over message, never in the documents. Number them
`P1`, `P2`… in the order they appear in the scenario, and group them:

- **Steps I added or changed** — checks 1–6.
- **Mechanisms I named** — check 7, and the decided categories above.
- **Defaults I applied** — the content a consultant would otherwise be asked
  for: client name, records and figures, base currency, languages, who is in the
  room, slot, instance, real versus emulated integrations, branding, what must
  not be shown. Every one ships as a placeholder that reads as a placeholder, or
  as a stated default. None blocks anything.

Each proposal is at most three lines:

```
P3 · UC2 step 7 — the discount request had no source
Missing: the manager approves a request that no step creates.
Wrote: the request CR-1041 is seeded in "Awaiting approval"; step 7 opens it.
Undo: say "P3: presenter creates it" and I add the creating step before step 6.
```

Three rules keep them honest:

1. **Quote their words, name the step.** The consultant must be able to find the
   place in the draft in five seconds.
2. **One-line undo.** The alternative that keeps the story intact, phrased as
   what they would say. A bare "no" then has a defined meaning: apply the undo.
3. **Flag what only a person can settle.** **Needs your input** for what only the
   consultant can answer; **engineer to confirm** for a capability the white list
   does not cover. Say what each blocks. Nothing else in the hand-over is a
   question.

Do not append a questionnaire. Do not ask "is this what you meant" about
something you could close. The one closing line is: reply with what to change.

**Nothing about any of this reaches the document.** The scenario is the resolved
demo, with the proposals already written in. A proposal printed in a deliverable
is a doubt nobody owns.

---

## Revise — from feedback to the next version

The consultant's reply is feedback, in any form: a proposal number, a use case
and step, a pasted paragraph, a general remark. Sort every comment into one of
these:

| Comment | What you do |
|---|---|
| Not mentioned | The proposal stands. Silence is acceptance. |
| Accepted or "fine" | It stops being a proposal and becomes their text. |
| "No" with an alternative | Apply their alternative. |
| "No" without one | Apply the proposal's stated undo. |
| New or changed content | Treat it as source: re-run the ten checks on it. |

Then rebuild both files together, re-verify, and issue `v<n+1>`. A change
to a step can move a column, a marker or a seed record, so neither file is
edited in isolation. The revision hand-over is a short change list — comment →
what changed — plus any knock-on you had to close yourself, as new proposals
continuing the numbering.

---

## Coverage — the promise that nothing is lost

The consultant's text is the input, and losing a detail of it is the one failure
this process cannot recover from. So before closing anything, map it.

Go through the source in order and tag every sentence with where it lands:

| Tag | Lands in |
|---|---|
| `step` | a numbered step, with its use case and step number |
| `bubble` | narration, with its use case and phase |
| `object` | the objects file — an object, a column, a lookup value, a seed record |
| `flow` | the flow line of a use case |
| `header` | the telegraph header |
| `proposal` | a numbered proposal in the hand-over |
| `dropped` | deliberately left out — **with the reason** |

Then report the residue in the conversation, not in the document: how many
sentences mapped, and every `dropped` one quoted with its reason. `dropped` is
legitimate — a needs-dev feature, a repetition, a note to themselves — but it is
never silent. A consultant who finds their own sentence missing and no
explanation for it stops trusting the whole document, correctly.

The map itself is working material. Keep it out of both deliverables.
