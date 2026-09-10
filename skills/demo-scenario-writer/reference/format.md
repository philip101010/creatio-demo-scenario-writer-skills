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

## What I changed
## Open questions
## Basis vs. nice-to-have
```

No purpose section, no goals, no brief summary, no attachments, no closing
notes, no object tables, no acceptance table. The reasons for the last two are
in section 8.

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

1.  <chain>
2.  <chain>

### Phase 2 — <name>

> <bubble>

3.  <chain>
```

**The use case count and order are the consultant's.** In rewrite mode you never
merge two, never split one, never renumber, and never invent a fifth. A use case
that runs long gets phases, not a new number. This is their scenario; you are
making it legible, not redesigning it.

### The flow line

One italic line under the title, plain language, arrows, **no element names and
no field names** — the skeleton the steps then demonstrate:

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
- Never a claim the steps do not demonstrate. No *seamlessly*, no "the system
  automatically" without naming the mechanism, no emoji.

### The step — a chain ending on something visible

> `7.  Claim WC-0042 → Decision **Accepted** → stage moves to **Reimbursement**
>     → dashboard tile **Recovered this month** reads **42 750 SAR**
>     *(rolled up by the process)*`

1. **The words "click" and "say" never appear.** The arrow carries the action;
   the bubble carries the voice.
2. **Location first, when the page changes.** The first link names where you are
   — list page, form page plus tab, mini page, Home page, chat panel. Omit it
   only while you stay on the same page.
3. **Every chain ends on something the audience can see.** A step that produces
   nothing to look at is not a step; it belongs inside the previous chain.
4. **Name the mechanics inline** — the column caption, the lookup value in
   quotes, the component — in **bold**. Bold is for element and value names
   only, never for emphasis.
5. **Provenance in italics** for every value the presenter did not type:
   *(created by the process)*, *(from the OEM feed)*, *(calculated by the rule)*,
   *(seeded)*. See section 5 — this rule does more work than any other.
6. **One step, one coherent move.** A chain may hold several actions when they
   are one gesture ("open the tab → pick the record → the form opens"); it must
   not hold two unrelated ideas.
7. **One path.** *If*, *or*, *optionally*, *alternatively*, *in case of* are
   banned. An alternative flow is dropped or becomes its own step, never a
   branch inside one.
8. **Numbering never shifts.** Steps are numbered per use case and keep their
   numbers across every revision, so "UC2 step 7" means the same thing in the
   meeting, in the objects file and in the build. A removed step leaves a gap
   rather than renumbering the rest.

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

## 6. What I changed, and Open questions

**What I changed** — the deviation record, in the document rather than hidden,
because the consultant handed you their text and must be able to find where it
was altered. One line each, newest concern first:

> - UC2 steps 4–6 were one paragraph; split into three steps because the
>   approval happens on the manager's screen, not the rep's.
> - "Information request" added to **Case category** — the snapshot holds only
>   Incident and Service request, and UC4 routes on this value.
> - Dropped the SMS reminder: it needs development, and nothing in the demo
>   depends on it.

**Open questions** — only what survived the gate: what the consultant declined
to answer, or deferred. Each one states three things, and the third is not
optional:

> - **Q1** · blocks UC2 step 4 · Is the case routed by the account's region or
>   the contact's region? · **Applied: the account's region**, because the
>   routing rule reads the account.

The step affected still appears, written to the default. A document with open
questions is still presentable and still buildable — that is the point of
stating the default rather than leaving a hole.

---

## 7. Basis vs. nice-to-have

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
than invented: walk the steps, remove the capability, and see whether a chain
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

## 8. What this format deliberately does not have

**No object or field tables.** They are in the objects file, whose reader is a
coding agent. A consultant reading past a column-type table is a consultant not
reading the next use case.

**No acceptance table.** Rule 3 of the step already forces every chain to end on
something visible, which *is* the expected result. A separate acceptance table
would restate every step in a second column — the duplication that turns a
600-word scenario into 7 000. The engineer verifies by walking the steps.

**No Foundation section.** Shared setup and the state every record starts in
live in the objects file's seed data, which is what makes a use case runnable
without another use case having been run first.

---

## 9. Banned words

Reject your own draft if it contains any of these, and rewrite:

`click` · `say` · `should be able to` · `etc.` · `if possible` · `as needed` ·
`various` · `some` · `several` · `a few` · `and/or` · `optionally` · `TBD` ·
`N/A` · `we could` · `it would be nice` · `similar to` · `and so on` ·
`seamlessly` · `powerful` · `robust`

`e.g.` is allowed in the header. Nowhere else.

---

## 10. Delivery

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

## 11. Length

A five-use-case scenario runs about 700–1 100 words of body text. Past that you
are duplicating, and the usual culprit is a bubble narrating what the next step
already shows. Check that before anything else.
