# Golden use case

One worked example, both files. Read it before writing, match its density, then
forget its content — copy the shape, the length of a step, the ratio of bubble
to step, never the domain.

It comes from a real scenario, verified against the general snapshot. Two
verifications failed: one became a row in the objects file, the other became a
proposal in the hand-over. Which is which is the whole lesson.

The consultant's original text for this use case is at the bottom, so you can
see what the rewrite actually did to it.

---

## In the scenario file

### UC1 — Call intake

*Customer calls → the agent already knows who it is → the whole history is on
one screen → a case is registered without leaving it*

> Right now your agents answer with "may I take your account number". The
> customer has already typed it twice into the IVR. What you are about to see is
> the agent knowing who is calling before they say hello — and everything they
> need to decide how to treat this person sitting on one screen.

1.  I sign in as a CS agent. The **Service desktop** opens on its own *(the
    default page for the role)*.
2.  I trigger an inbound call from the CTI emulator. The CTI panel shows the
    caller as **Tiffany Jane Martin** *(resolved from her **Mobile phone** by
    the emulator)* — I never search for her.
3.  I open the caller's name and land on the Contact page, **KYC** tab.
    **Incoming calls** reads **3** *(calculated by the rule)*, **NPS** is **8**
    and **Champion** is **yes** *(both seeded)*.

> Three calls this month, and she is the person who championed you internally
> when they bought. That is why the next thirty seconds are not a lottery — the
> agent knows to treat this one carefully before deciding anything.

4.  I run **Register a case** from the tab. A mini page opens with four fields
    and nothing else.
5.  I fill **Subject**, set **Category** to **"Information request"**, pick the
    **Service** and set **Priority** to **"Critical"**, and save. The case
    appears on the Contact timeline with **Account** = **Deloitte Germany** and
    **Origin** = **"Call"** *(both set by the mini page)*.

---

## In the object model

### Contact — existing (OOTB), section "Contacts"

| Column | Caption | Type | Status | Used by |
|---|---|---|---|---|
| MobilePhone | Mobile phone | Text | existing (OOTB) | UC1 s2 |
| AccountId | Account | Lookup → Account | existing (OOTB) | UC1 s5 |
| labNps | NPS | Integer 0–10 | existing (instance) | UC1 s3 |
| labHappinessRank | Happiness rank | Integer 1–10, slider | **new** | UC1 s3 |
| labChampion | Champion | Boolean | **new** | UC1 s3 |
| labIncomingCalls | Incoming calls | Integer, calculated: count of Call where Contact = this contact and Direction = "Incoming" | **new** | UC1 s3 |

### CaseCategory — existing lookup

| Value | Status |
|---|---|
| Incident | existing (OOTB) |
| Service request | existing (OOTB) |
| Information request | **new** |

### Seed data

| Contact | Account | Mobile phone | NPS | Champion | Calls seeded |
|---|---|---|---|---|---|
| Tiffany Jane Martin | Deloitte Germany | +49 151 2233445 | 8 | yes | 3 incoming |

---

## The one gap with no answer in the text, as it was handed over

```
P2 · UC1 step 3 — the RMA count has no source
You listed "RMA count" among the six metrics on the tab. Nothing on Order marks
a return, and no existing column derives into one.
Wrote: the tab shows five metrics; RMA count is left off.
Undo: say "P2: count orders with a credit note" and I add the column on Order
and the rule that fills it, or "P2: it comes from outside Creatio" and it
becomes an import plus a seeded number.
Needs your input: what the client means by an RMA.
```

The draft was complete without it — five metrics on the tab, no hole — and the
consultant's first reply could be "fine" or a one-line correction.

---

## The consultant's original text

> **Use case 1 — call intake.** Customer calls in. Agent sees who it is straight
> away — no more "what's your account number", they've already typed it in the
> IVR twice. Agent gets the full picture on one screen: NPS, how happy they are,
> how many times they've called us, whether they're a champion, RMA count. Then
> registers the case right there without leaving the screen — subject, category
> (information request), service, priority. Case lands on the contact's
> timeline. This is the "you already know me" moment.

---

## What the rewrite did, and why

**Five steps out of one paragraph, and the paragraph's order kept.** The
consultant's sentences already ran in demo order; the rewrite numbered them and
gave each one a visible ending. Nothing was resequenced, because nothing needed
to be.

**The steps stayed prose, in their first person.** Compressing step 3 to
`Caller's name → KYC tab → Incoming calls = 3` saves two lines and costs the
presenter the sentence they were going to say out loud. Arrows earn their place
on the flow line, where the whole use case fits on one row; inside a phase they
turn a demo into a diagram.

**Their voice went into the bubbles almost intact.** "No more what's your
account number, they've already typed it in the IVR twice" and "the you already
know me moment" are theirs — the first became the opening bubble, the second
became the payoff bubble reworded as what it means. This is the part a rewrite
most often destroys by improving it.

**Every value on screen got a provenance marker, and that is where the work
was.** The consultant wrote "agent sees who it is straight away". Who resolved
the caller? *(resolved from Mobile phone by the CTI emulator)* — a silent
mechanism, check 7, so it was decided rather than asked, and deciding it made
three build items visible at once: Mobile phone must be populated, the emulator
must be configured, and the seed contact's number must match. The decision is
one line in the hand-over report. "How many times they've called us" is
*(calculated by the rule)*, so it is a rule to build; NPS and Champion are
*(seeded)*, so they are rows in the seed table. Nothing on screen is unexplained.

**One phase, so no phase heading.** One actor, one screen, no wait. Wrapping
five steps in `Phase 1` would have added a line and no information.

**The missing lookup value was decided, not asked.** "Information request" is
not in CaseCategory — the snapshot holds only Incident and Service request, and
neither means the same thing. It became a **new** row in the lookup table and a
line in the hand-over report. An earlier draft asked the consultant whether to add
it, rename one, or route on Service instead: three options with one obvious
answer, which is a question that should never have been asked.

**The missing metric source was proposed, not asked, because it has no answer.**
Nothing on Order marks a return. This is not a mechanism question for the
engineer, it is a business question about what the client means by RMA, and only
the consultant can answer it — so the draft takes the cheapest honest version
(leave it off), says so in the hand-over with the undo, and flags it **needs your
input**. Note the phrasing — what should it count, not which field should we
create. The document itself carries no trace of it.

**The columns are in the object model and the steps do not repeat them.** Step 4
says a mini page with four fields; it does not list their types. Step 3 names
the three metrics it shows on screen and no others. The KYC tab's full field
list lives in the object model, once.

**The rule is a marker and a formula, not a third document.** `Incoming calls`
is a calculated column in the object model, with its formula stated, and step 3
says *(calculated by the rule)*. The build agent reads the marker for what
produces the value and the object model for what to create — nothing else needs
writing down, and a demo where the columns are right and nothing moves is
caught by the marker-against-white-list check.

**NPS was already on the stand.** The instance read found `labNps` from an
earlier build, so it is `existing (instance)` rather than **new** — one row that
stops the build recreating a column and orphaning the seeded values behind it.
