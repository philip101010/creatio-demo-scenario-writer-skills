# The question gate

The consultant handed you a scenario. Before you write a single line of the
rewrite, you close the questions that would otherwise be answered by guessing.

The gate has two tiers, and **the order between them is the point of this
file**:

| | Tier A — structure | Tier B — content |
|---|---|---|
| About | whether the steps hold together | what the records are called |
| Changes | the shape of the document | values inside a fixed shape |
| Asked | first, before writing | last, with the draft already delivered |
| Blocking | yes | no — every item carries its default |

Tier A questions add steps, split steps, re-attribute them to another actor and
move phase boundaries. Tier B questions swap "Contoso Motors" for the real
client name and 42 750 for the real number. Ask Tier B first and you spend the
consultant's attention on decoration while the skeleton is still wrong — and
their attention runs out long before your question list does.

---

## Tier A — the ten logic checks

Walk these over the consultant's text before writing. Each one that fires is
either something you can resolve from `best-practices.md` section 2, or a Tier A
question. Nothing else earns a Tier A question.

**1 · Orphan precondition.** A step acts on a record, role, page or value that no
earlier step created and no seed data provides.

> *"The manager approves the discount"* — no step created a discount request,
> and no earlier step put the manager anywhere near this record.

**2 · Dead result.** A step produces something no later step, bubble or use case
ever uses. Either a step is missing after it, or the result is decoration and
the step should end somewhere else.

> *"…and an approval task is created for the regional director."* Nobody opens
> it. Does the demo show the director acting, or does the task exist only to
> prove it can?

**3 · Actor jump.** The acting role changes and the text does not say who is now
at the keyboard. Consultants write "then it's approved" constantly; a demo has
somebody's screen on the projector at every moment.

**4 · Impossible order.** A step reads a value that a later step writes, or shows
a state the flow has not reached yet.

**5 · Silent mechanism.** A result appears and nothing says what produced it — a
field fills itself, a record shows up, a number changes, a stage moves. This is
the provenance rule from `format.md` section 5 used as a detector: if the
presenter did not type it and you cannot name what did, that is a question, and
it is the single most productive check on this list. Most demos that collapse in
the room collapse here.

**6 · Phase boundary that does not hold.** A long block with no change of actor,
system or time cannot be split into phases. If the consultant's text has no such
turn, either the block is one phase or you have misread where it turns.

**7 · Two readings.** A step that can be read two ways, where the readings build
differently. *"Routed by region"* — whose region, the account's or the
contact's?

**8 · Contradiction.** Two places assert different things about the same record,
field or state. Usually a scenario that grew over several client calls.

**9 · Unexplained term.** A term is introduced and never resolved. A reader who
trips on an unexplained word stops thinking, so the term is either explained on
the spot or cut — and if only the client knows what it means, it is a question.

**10 · Unreachable page.** The step happens somewhere the previous step could not
have navigated to. Cheap to miss when the consultant wrote the use cases weeks
apart.

---

## How to ask Tier A

**One message, numbered, all of it.** Never one question at a time; never a
second Tier A round unless an answer opened something genuinely new, and then at
most one.

Each question is three lines and nothing more:

```
A3 · UC2 steps 4–5
"Then it's approved and the customer gets the quote." Who approves — the sales
manager, or the regional director who appears in UC4? The two see different
records and the demo shows a different screen for each.
Applied if unanswered: the sales manager, because UC2 never leaves their unit.
```

- **What it blocks** — the use case and step numbers, so the consultant can look
  at the exact place in their own text.
- **The question** — quote their words, then ask. Quoting is what makes them
  recognise the ambiguity instead of defending the sentence.
- **The default you will apply** — always. A consultant who does not answer has
  still shipped a document, and a consultant who disagrees with your default
  will say so far more readily than they will answer an open question.

Say plainly that anything unanswered becomes an open question in the document
with the default already written into the step. Then wait once. If the answers
do not come, proceed — do not stall, do not chase.

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

## Coverage — the promise that nothing is lost

The consultant's scenario is the input, and losing a detail of it is the one
failure this mode cannot recover from. So before asking anything, map it.

Go through the source in order and tag every sentence with where it lands:

| Tag | Lands in |
|---|---|
| `step` | a numbered chain, with its use case and step number |
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
