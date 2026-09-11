# Output format — the contract

Two files come out of this skill, and the split is the whole idea:

| File | Reader | Holds |
|---|---|---|
| `<client>-demo-scenario-v<n>.md` | the consultant, presenting | the narrative: use cases, phases, bubbles, steps |
| `<client>-objects-v<n>.md` | Claude Code, building | the data model and the seed data — see `objects-file.md` |

Nothing appears in both. The scenario names an object or a value only where a
step actually shows it on screen; what to configure lives in the objects file.
This is why the scenario stays short enough to be read in a meeting and the
objects file stays complete enough to be handed to a coding agent without a
covering explanation.

This file is a contract, not a suggestion. Every rule exists because a real
scenario failed without it.

---

## 1. Document skeleton

```
# <Client> — Demo scenario
v<n> · <date> · <N> use cases

## Before you present

## UC1 — <name>
## UC2 — <name>
...

## Basis vs. nice-to-have
```

No purpose section, no goals, no brief summary, no attachments, no closing
notes, no object tables, no acceptance table, **no questions and no record of
what you changed**. The document is the resolved demo. Everything you decided
and everything you asked is reported in the conversation instead — see section 7,
and `question-gate.md`.

---

## 2. Header

Telegraph lines under the title — values, never prose. One line each, only the
lines that have content:

```
Client · Contoso Motors, automotive retail, 400 staff
Use cases · 4 — call intake · warranty claim · OEM review · service dashboard
Demo user · Supervisor, and one dealer role for UC3
Instance · https://contoso-demo.creatio.com
Integrations · CTI emulator; OEM warranty feed emulated with seed data
```

An integration that is emulated says so here. A consultant who discovers in the
room that the OEM feed was seed data has been ambushed by their own document.

---

## 3. Before you present

Exactly one line:

> Run the **Run before demo** process — it resets every record this demo touches
> to its opening state.

Not a checklist. The reset itself is a build artifact and is specified in the
objects file, alongside the seed data it restores.

---

## 4. Use case

```
## UC<n> — <name>

*<flow line>*

### Phase 1 — <name>

> <bubble>

1.  <step>
2.  <step>

### Phase 2 — <name>

> <bubble>

3.  <step>
```

**The use case count and order are the consultant's.** In rewrite mode you never
merge two, never split one, never renumber, and never invent a fifth. A use case
that runs long gets phases, not a new number. This is their scenario; you are
making it legible, not redesigning it.

### The flow line

One italic line under the title, plain language, arrows, **no element names and
no field names** — the skeleton the steps then demonstrate.

**This line is the only place in the document where arrows carry the story.** A
chain of arrows is fast to scan across one summary line and unreadable the
moment it runs down a phase, which is exactly why the summary gets them and the
steps do not:

> *Service visit closed → warranty checked automatically → claim created → OEM
> reviews → reimbursement paid*

A reader who only reads flow lines still knows what the demo does. Write it
that way.

### Phases

A phase is a named stretch of one use case. It exists to break a long use case
without touching the step numbers, and it is only allowed where the story
actually turns:

- **the actor changes** — the dealer hands off to the OEM reviewer,
- **the system changes** — the demo moves to the mobile app, the portal, a chat,
- **time passes** — overnight, next visit, after the approval.

Nothing else is a phase boundary. A use case with one actor, one screen and no
wait is one phase, and then the phase heading is omitted entirely — do not wrap
a three-step use case in `Phase 1` to look thorough.

**Step numbers run continuously through the whole use case**, across phases. UC3
step 7 is step 7 whichever phase it sits in.

### The bubble — narration above a group of steps

Everything the presenter *says* but does not *do* lives in a bubble, placed
above the steps it covers, as a Markdown blockquote.

- **Two to four per use case**, each covering a stretch of three to eight steps.
  A bubble per step is the exact mistake this format exists to prevent.
- **Placed where the story turns** — opening the use case, entering a phase, and
  the payoff.
- **Built from the consultant's own words.** This is a rewrite, not a rewrite of
  their voice: their pain points, their value language, the client's vocabulary
  and the numbers the story hangs on move into the bubbles nearly intact. If you
  find yourself improving their phrasing into house style, stop — you are
  deleting the thing they wrote the scenario for.
- **Problem → what you are about to see → what it means.** Three sentences is the
  ceiling.
- **This is where every explaining sentence goes.** Whatever you strip out of a
  step — why it matters, what it replaces, what the agent no longer does — lands
  here or is dropped. The bubbles are not decoration around the steps; they are
  the other half of the same content, and the split between them is what makes
  both halves readable.
- Never a claim the steps do not demonstrate. No *seamlessly*, no "the system
  automatically" without naming the mechanism, no emoji.

### The step — what you do, and what appears

Written in prose, first person, present tense — the way a consultant already
narrates a demo, and the way the presenter will actually speak it:

> 7.  I set **Decision** to **Accepted** on claim **WC-0042**. The stage moves to
>     **Reimbursement** and the dealer's **Recovered this month** tile reads
>     **42 750 SAR** *(rolled up by the process)*.

1. **Three things only: the action, what appears, what the system did.** One or
   two sentences. Nothing else is allowed in a step — not why it matters, not
   how it compares to today, not what the presenter avoided having to do.

   > **Water:** *"The customer card is loaded for me — I never search for it,
   > and there is nothing to open in parallel."*
   >
   > **Step:** *"I open the case. The **SAP data** block shows account tier,
   > credit limit and credit status *(returned by the SAP mock)*."*

   The test is deletion: if a sentence can go without changing what is on
   screen or what has to be built, it does not belong in a step. It is either a
   bubble sentence or it is nothing. Almost every draft fails here first,
   because the source is written in exactly that voice — moving those
   sentences into the bubbles **is** the rewrite.
2. **Say where you are looking, every time.** Not "where the page changes" —
   every step. A step names the place on screen and then what is in it: the
   **Timeline**, the **Feed**, the **Subtasks** list, the stage bar, the
   **Agent Inbox** queue, the CTI panel. A presenter reading the step must know
   which part of the screen to point at.

3. **Plain words, short sentences, active voice.** "I open X. I see Y." Nothing
   that has to be parsed twice.

   > **Too clever:** *"An acknowledgement e-mail quoting CC-20251 goes to the
   > customer in the contact's language."*
   >
   > **Step:** *"I open the **Timeline** on the case. The acknowledgement e-mail
   > is already there. It quotes the case number **CC-20251** and is written in
   > the language from the contact record *(sent by the process, from the
   > out-of-the-box template)*."*

   The first sentence is shorter and says less. It is passive, it never says
   where to look, and a presenter cannot perform it — they would have to work
   out for themselves that the proof is on the Timeline.

4. **Automation is shown, not asserted.** The system does plenty the presenter
   never watches happen — a case is created, an owner is set, a rating comes
   back. The step is not the event; the step is **the presenter opening the
   place where the result is visible**. If there is nowhere to open, it is not a
   step: it is a line in the objects file.
5. **Every step ends on something the audience can see.** A step that produces
   nothing to look at is not a step; fold it into the one before it.
6. **Name the mechanics inline** — the column caption, the lookup value in
   quotes, the component — in **bold**. Bold is for element and value names
   only, never for emphasis.
7. **Provenance in italics** for every value the presenter did not type:
   *(created by the process)*, *(from the OEM feed)*, *(calculated by the rule)*,
   *(seeded)*. See section 5 — this rule does more work than any other.
8. **A step says what happens; it never sells and never explains.** "I do not
   have to remember what comes next" is a bubble. "The **Next steps** panel
   carries the task **Review case information**" is a step. The difference is
   not tone, it is who the sentence is addressed to: a step addresses the person
   driving the screen, a bubble addresses the room.
9. **One step, one coherent move.** A step may hold several actions when they are
   one gesture — open the tab, pick the record, the form opens — but not two
   unrelated ideas.
10. **One path.** *If*, *or*, *optionally*, *alternatively*, *in case of* are
   banned. An alternative flow is dropped or becomes its own step, never a
   branch inside one.
11. **Numbering never shifts.** Steps are numbered per use case and keep their
   numbers across every revision, so "UC2 step 7" means the same thing in the
   meeting, in the objects file and in the build. A removed step leaves a gap
   rather than renumbering the rest.

### An exchange with Creatio.ai

Where the step is a conversation with the AI, write the conversation. Indent it
under the step as a quoted block, with the prompt exactly as the presenter will
type it and the answer trimmed to what will be on screen:

> 12. I ask Creatio.ai for a briefing rather than reading the whole thread.
>
>     > **Me:** Summarise this case for me.
>     >
>     > **Creatio.ai:** CC-20251 — Quote request, registered today 08:42 by
>     > Alexander Wilson (Alpha Business, Gold tier). The customer asks for
>     > 5 000 pcs of product XYZ and a price offer. First response due 12:02.
>     > The account has five previous cases, two of them quote requests that
>     > both became orders.
>
>     *(read from the case, the account and the SAP mock by the AI skill)*

The answer is content, not decoration: an engineer builds the AI skill's output
shape from it, so it is written the way it must come back, not paraphrased.

---

## 5. Provenance — the rule that makes the demo credible

Every value on screen came from somewhere. Either the presenter typed it, or
the system produced it. If the presenter did not type it, the step says what
did, in italics, in parentheses:

| Marker | Means |
|---|---|
| *(seeded)* | it was in the data set before the demo started |
| *(created by the process)* | a business process wrote it during the demo |
| *(calculated by the rule)* | a business rule or calculated field derived it |
| *(from the CTI emulator)* | an integration or emulator supplied it |
| *(set by the stage model)* | the DCM case moved it |
| *(returned by the AI skill)* | Creatio.ai produced it |

Two things fall out of this, which is why it earns a section of its own:

**For the consultant** it is the whole sales argument made visible — the
audience sees the system doing the work rather than the presenter typing an
answer they were always going to type.

**For the engineer** it is the build list hiding inside the narrative. A step
that says *(created by the process)* is a process to build; *(calculated by the
rule)* is a rule; *(seeded)* is a row in the objects file. A result with no
marker and no typing is a hole, and finding those holes is most of what the
question gate does — see `question-gate.md`, check 5.

---

## 6. Basis vs. nice-to-have

The last section of the document, and the only one whose content is not yours to
decide. A demo scenario is also a scope proposal: some of what it shows is what
the customer is buying, and some of it is you being generous. Left implicit, the
generous half gets built, presented, and then quoted as if it were included.

One table, one row per demonstrable capability, each row naming the use cases
that need it:

```
## Basis vs. nice-to-have

A starting point for prioritisation, from the scenario. The €/time impact of
each item still needs to be quantified by the commercial team.

| Item | Classification | Note |
|---|---|---|
| Calculation-to-document generation (UC1) | Basis | Directly addresses the two biggest pain points in Prepare/Write |
| Approval matrix enforcement by order value (UC3) | Basis | Matrix already exists; enforcement is the gap |
| Hard stop on an unapproved issue (UC4) | Open — J-Tec to decide | Procedure already exists; enforcement is optional pending a decision |
| Customer portal | Nice-to-have | Explicitly parked for a later phase |
```

### The three classifications

| Classification | Means |
|---|---|
| **Basis** | remove it and a step in the scenario stops working |
| **Nice-to-have** | remove it and every step still runs; only a bubble's claim gets smaller |
| **Open — `<who>` to decide** | it needs a decision on the customer's side, and the name of who decides is part of the value |

That first test is mechanical, and it is why this table can be drafted rather
than invented: walk the steps, remove the capability, and see whether a step
still ends on something visible. An item that only weakens the narration is not
basis, however much the consultant likes it.

### Who fills it in

**You draft it; the consultant decides it.** Propose a classification for every
row with the one-line reason in *Note*, then interview them on it — see
`question-gate.md`, Tier C. What comes back is theirs, including the rows they
flip against your reasoning. Never quantify the money or the effort: the intro
line says the commercial team owns that, and it means it.

An item the consultant will not classify becomes `Open — <who> to decide`, not
a guess and not a blank. A blank cell here is the same defect as a highlight in
the prose: nobody owns it.

### Granularity

One row per capability a step actually demonstrates, not one per field and not
one per use case. If two use cases need the same capability, it is one row
naming both. The table is usually eight to fourteen rows for a five-use-case
scenario; past twenty you are listing configuration rather than capabilities.

---

## 7. What this format deliberately does not have

**No object or field tables.** They are in the objects file, whose reader is a
coding agent. A consultant reading past a column-type table is a consultant not
reading the next use case.

**No acceptance table.** Rule 5 of the step already forces every step to end on
something visible, which *is* the expected result. A separate acceptance table
would restate every step in a second column — the duplication that turns a
600-word scenario into 7 000. The engineer verifies by walking the steps.

**No Foundation section.** Shared setup and the state every record starts in
live in the objects file's seed data, which is what makes a use case runnable
without another use case having been run first.

**No open questions, and no list of what you changed.** Both used to sit at the
end of the document, and both were the wrong place for them. A question printed
in a document is a question nobody answers — it is asked in the chat before the
document exists, with options to pick from, and the document is written to the
answer. What you changed relative to the consultant's text is reported in the
same conversation, where they can push back on it while it is still cheap.

---

## 8. Banned words

Reject your own draft if it contains any of these, and rewrite:

`should be able to` · `etc.` · `if possible` · `as needed` ·
`various` · `some` · `several` · `a few` · `and/or` · `optionally` · `TBD` ·
`N/A` · `we could` · `it would be nice` · `similar to` · `and so on` ·
`seamlessly` · `powerful` · `robust`

`e.g.` is allowed in the header. Nowhere else.

---

## 9. Delivery

Two Markdown files, UTF-8, in the working directory:

```
<client>-demo-scenario-v<n>.md
<client>-objects-v<n>.md
```

Lower case, hyphens for spaces — `contoso-motors-demo-scenario-v1.md`. Both
files carry the same version, and a revision after the consultant's comments
increments both together even if only one changed, so a pair on disk is always a
matching pair. Never overwrite the previous version; the consultant compares
them.

Markdown only, and only this much of it: `#` for the title, `##` for the
sections and use cases, `###` for phases, `>` for bubbles, numbered lists for
steps, `-` for every other list, `**bold**` for element and value names,
`*italic*` for the flow line and provenance, backticks for a name that could be
read as prose. Exactly one pipe table in this file — *Basis vs. nice-to-have*;
every other table belongs in the objects file.

No raw HTML, no images, no footnotes, no colour, no highlighting. A doubt that a
highlight would have carried is an open question with a default — the only form
a question takes in this document.

---

## 10. Length

A five-use-case scenario runs about 700–1 100 words of body text. Past that you
are duplicating, and the usual culprit is a bubble narrating what the next step
already shows. Check that before anything else.
