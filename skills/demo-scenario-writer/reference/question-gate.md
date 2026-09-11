# The question gate

The consultant handed you a scenario. Before you write a single line of the
rewrite, you close the questions that would otherwise be answered by guessing.

The gate has three tiers, and **the order between them is the point of this
file**:

| | Tier A — structure | Tier B — content | Tier C — priority |
|---|---|---|---|
| About | whether the steps hold together | what the records are called | what is in scope |
| Changes | the shape of the document | values inside a fixed shape | nothing in the document |
| Asked | first, before writing | last, with the draft delivered | last, with the draft delivered |
| Blocking | yes | no — every item carries its default | no, but nothing may be left blank |
| Decided by | you, mostly | you, mostly | the consultant, always |

Tier A questions add steps, split steps, re-attribute them to another actor and
move phase boundaries. Tier B questions swap "Contoso Motors" for the real
client name and 42 750 for the real number. Ask Tier B first and you spend the
consultant's attention on decoration while the skeleton is still wrong — and
their attention runs out long before your question list does.

---

## Tier A — six checks that ask, four that you resolve

Ten things go wrong in a free-form scenario. Only six of them are worth a
consultant's attention, and the line between the two groups is sharp: **a Tier A
question is about whether the steps hold together — their logic, their
consistency, their order — and nothing else.**

Everything else you resolve, write into the step, and report at hand-over so the
consultant sees the decision without having to answer for it. A gate that asks
twelve questions gets five answers; a gate that asks five gets five.

### The six that ask

**1 · Orphan precondition.** A step acts on a record, role, page or value that no
earlier step created and no seed data provides.

> *"The manager approves the discount"* — no step created a discount request,
> and no earlier step put the manager anywhere near this record.

Resolve it instead when seed data obviously fixes it and the choice of record
does not change the story. Ask when the precondition has to be *produced* on
screen and no step produces it.

**2 · Dead result.** A step produces something no later step, bubble or use case
ever uses. Either a step is missing after it, or the result is decoration.

> *"…and an approval task is created for the regional director."* Nobody opens
> it. Does the demo show the director acting, or does the task exist only to
> prove it can?

**3 · Actor jump.** The acting role changes and the text does not say who is now
at the keyboard. Consultants write "then it's approved" constantly; a demo has
somebody's screen on the projector at every moment, and switching users costs
minutes of a slot that is already short.

**4 · Impossible order.** A step reads a value that a later step writes, or shows
a state the flow has not reached yet.

**5 · Contradiction.** Two places assert different things about the same record,
field, state or clock. Usually a scenario that grew over several client calls,
and usually invisible until someone does the arithmetic.

**6 · Unreachable page.** The step happens somewhere the previous step could not
have navigated to — easy to miss when the use cases were written weeks apart.

### The four you resolve

These fire often and answer themselves. Decide, write the decision into the
step, and put one line in the hand-over report.

**7 · Silent mechanism.** A result appears and nothing says what produced it. Name
the most likely mechanism from `best-practices.md` section 1, write the
provenance marker, and carry it into the objects file as the thing to build.
This fires more than any other check, and turning each hit into a question is
exactly how a gate becomes unanswerable — the consultant does not know what
produced it either, which is why they left it out.

**8 · Phase boundary.** Where the phases fall is yours. Cut at a change of actor,
system or time; if the text offers no such turn, it is one phase.

**9 · Two readings.** A sentence that can be read two ways: pick the reading that
keeps the rest of the flow consistent and say which you picked. It becomes a
question only when the two readings build *differently enough to matter* — and
then it is really check 5.

**10 · Unexplained term.** Explain it on first use in a bubble, or cut it. Only a
term whose meaning is the client's own — where a wrong guess misdescribes their
business — is worth asking about.

---

## How to ask Tier A

**One message, numbered, all of it, before a line of the document exists.**
Never one question at a time; never a second round unless an answer opened
something genuinely new, and then at most one.

**Every question comes with options.** Not "what should happen here?" but two to
four concrete answers, each one complete enough to be written straight into the
step, with the one you recommend marked and half a line of reason. A consultant
picks a letter in fifteen seconds; an open question sits in their inbox for
three days.

```
A1 · Phase 4 step 17, and the SLA widget in Phase 9 — the clock does not add up
The briefing says the case was registered 08:42 with first response due 10:02,
and the reply goes out at 10:35. The demo narrates a breached SLA and then shows
a compliance dashboard.

  a) First-response target is three hours, so it is due 12:02.   ← recommended
     Nothing else in the scenario moves.
  b) The reply goes out at 09:45, inside the 10:02 target.
     The AI briefing and the offer step both need new times.
  c) Keep 10:02 and show the breach on purpose.
     Then Phase 9 needs a line about what happens to a missed SLA.
```

Three rules keep the options honest:

1. **Include the reading that keeps their text as written**, whenever it is
   viable. They wrote it for a reason, and seeing it offered back tells them you
   understood it rather than corrected it.
2. **Say what each option costs**, in half a line — which other steps move. That
   is the part they cannot see from their side and the part that decides the
   answer.
3. **If you cannot propose options, it is not a Tier A question.** Not being able
   to name two concrete resolutions means you have not understood the ambiguity
   well enough to ask about it. Understand it, or decide it.

Say plainly that anything unanswered goes with the recommended option. Then wait
once. If the answers do not come, proceed on the recommendations — do not stall
and do not chase.

**Nothing about any of this reaches the document.** The scenario is written to
the answers, and what you decided is reported back in the same conversation at
hand-over. A question printed in a deliverable is a question nobody answers.

---

## Tier B — content, at the end

These go in **one message after the draft is delivered**, so the consultant
reads them with the document in front of them:

- Client name, industry, size, and the real product names from their site.
- The records and the numbers: which accounts, which amounts, which dates. Exact
  values, because `several` and `a few` are banned from the document.
- Base currency; languages, and whether custom captions are really translated or
  the demo runs on the out-of-the-box language pack.
- Who is in the room and what each of them must be convinced of.
- Demo date and slot length; who clicks.
- Instance, and whether integrations are real or emulated.
- Branding: are the client's logo and colours applied.
- What must not be shown.
- Mobile in scope; telephony real or emulated.

Every one of them carries a default in the draft — placeholder names that read
as placeholders, a stated currency, emulated integrations. Nothing here blocks
delivery. A Tier B question that turns out to change the structure was a Tier A
question you misfiled; move it and re-ask.

---

## Tier C — the prioritisation interview

The scenario's last section is *Basis vs. nice-to-have* (`format.md` section 6),
and it is the one part of the document you may not decide. What is basis is a
commercial position: it says what the customer is buying. Guess it and the
generous half gets built, presented, and then quoted as if it had always been
included.

So you draft the table and interview the consultant on it. In the same message
as Tier B, after the draft is delivered.

**Draft it with the removal test.** For each capability, take it out of the
scenario and look at what breaks:

- a step stops working → **Basis**
- every step still runs and only a bubble's claim gets smaller → **Nice-to-have**
- it turns on a decision the customer has not taken → **Open — `<who>` to decide**

That test is mechanical, which is what makes a draft legitimate rather than an
invention. Put the one-line reason in *Note*, in their terms — "matrix already
exists, enforcement is the gap" — not in yours.

**Then ask, row by row, in one message:**

```
The last section is a first pass at scope. Flip anything I have wrong — these
are your calls, not mine:

  Basis        Calculation-to-document generation (UC1)
               — the two pain points you opened the call with
  Basis        Approval matrix enforcement by order value (UC3)
               — the matrix exists, enforcement is the gap
  Open         Hard stop on an unapproved issue (UC4)
               — needs a J-Tec decision; who owns it?
  Nice-to-have Customer portal
               — you parked it for a later phase

Three things I need from you: which rows are wrong, who decides each Open one,
and whether anything the scenario shows is missing from the list.
```

**What you never do here:**

- **Never quantify.** No euros, no man-days, no effort estimates. The section's
  own intro line says the commercial team owns the €/time impact, and that is
  not modesty — a number you invent becomes a number someone quotes.
- **Never leave a cell blank.** An item the consultant will not classify is
  `Open — <who> to decide`. A blank is the same defect as a highlighted doubt in
  the prose: nobody owns it.
- **Never overrule them.** If they call something basis that your removal test
  says is decoration, it is basis. Their reason may be a commitment already made
  on a call you were not on.
- **Never promote something to basis because it is already built.** The demo
  instance having a feature says nothing about whether the customer is buying it.

Their answers replace your draft verbatim, and the objects file marks every
nice-to-have item so the build order is obvious to whoever picks it up.

---

## Coverage — the promise that nothing is lost

The consultant's scenario is the input, and losing a detail of it is the one
failure this mode cannot recover from. So before asking anything, map it.

Go through the source in order and tag every sentence with where it lands:

| Tag | Lands in |
|---|---|
| `step` | a numbered step, with its use case and step number |
| `bubble` | narration, with its use case and phase |
| `object` | the objects file — an object, a column, a lookup value, a seed record |
| `flow` | the flow line of a use case |
| `header` | the telegraph header |
| `question` | a Tier A or Tier B question |
| `dropped` | deliberately left out — **with the reason** |

Then report the residue in the conversation, not in the document: how many
sentences mapped, and every `dropped` one quoted with its reason. `dropped` is
legitimate — a needs-dev feature, a repetition, a note to themselves — but it is
never silent. A consultant who finds their own sentence missing and no
explanation for it stops trusting the whole document, correctly.

The map itself is working material. Keep it out of both deliverables.
