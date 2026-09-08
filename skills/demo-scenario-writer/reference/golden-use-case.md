# Golden use case

One worked example, both files. Read it before writing, match its density, then
forget its content — copy the shape, the chain length, the ratio of bubble to
step, never the domain.

It comes from a real scenario, verified against the general snapshot. Two
verifications failed: one became a row in the objects file, the other became the
one open question. Which is which is the whole lesson.

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

1.  Sign-in as CS agent → **Service desktop** opens *(default page for the role)*
2.  CTI panel → inbound call → caller shown as **Tiffany Jane Martin** *(resolved
    from **Mobile phone** by the CTI emulator)*
3.  Caller's name → Contact page, **KYC** tab → **Incoming calls** = **3**
    *(calculated by the rule)*, **NPS** = **8** *(seeded)*, **Champion** = **yes**
    *(seeded)*

> Three calls this month, and she is the person who championed you internally
> when they bought. That is why the next thirty seconds are not a lottery — the
> agent knows to treat this one carefully before deciding anything.

4.  **Register a case** → mini page, four fields
5.  **Subject**, **Category** = **"Information request"**, **Service**,
    **Priority** = **"Critical"** → Save → case appears on the Contact timeline
    with **Account** = **Deloitte Germany** and **Origin** = **"Call"** *(both
    set by the mini page)*

---

## In the objects file

### Contact — existing (OOTB), section "Contacts"

| Column | Caption | Type | Status | Used by |
|---|---|---|---|---|
| MobilePhone | Mobile phone | Text | existing | UC1 s2 |
| AccountId | Account | Lookup → Account | existing | UC1 s5 |
| labNps | NPS | Integer 0–10 | **new** | UC1 s3 |
| labHappinessRank | Happiness rank | Integer 1–10, slider | **new** | UC1 s3 |
| labChampion | Champion | Boolean | **new** | UC1 s3 |
| labIncomingCalls | Incoming calls | Integer, calculated | **new** | UC1 s3 |

### CaseCategory — existing lookup

| Value | Status |
|---|---|
| Incident | existing |
| Service request | existing |
| Information request | **new** |

### Logic to build

- **Business rule** on Contact: **Incoming calls** = count of Call where
  **Contact** = this contact and **Direction** = "Incoming". `Call.DirectionId`
  is an existing lookup with "Incoming" present, so no new lookup. Serves UC1 s3
  *(calculated by the rule)*.

### Seed data

| Contact | Account | Mobile phone | NPS | Champion | Calls seeded |
|---|---|---|---|---|---|
| Tiffany Jane Martin | Deloitte Germany | +49 151 2233445 | 8 | yes | 3 incoming |

### Open question in the scenario file

> - **Q1** · blocks the **RMA count** field on the KYC tab, nothing else · What
>   counts as an RMA for this client — returned orders, credit notes, or
>   something tracked outside Creatio? Nothing on Order marks a return and no
>   existing column derives into one, so the metric has no source. · **Applied:
>   the field is left off the tab**, and the tab holds five metrics instead of
>   six.

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

**Their voice went into the bubbles almost intact.** "No more what's your
account number, they've already typed it in the IVR twice" and "the you already
know me moment" are theirs — the first became the opening bubble, the second
became the payoff bubble reworded as what it means. This is the part a rewrite
most often destroys by improving it.

**Every value on screen got a provenance marker, and that is where the work
was.** The consultant wrote "agent sees who it is straight away". Who resolved
the caller? *(resolved from Mobile phone by the CTI emulator)* — a Tier A
check 5 question that took one answer and turned three build items visible:
Mobile phone must be populated, the emulator must be configured, and the seed
contact's number must match. "How many times they've called us" is
*(calculated by the rule)*, so it is a rule to build; NPS and Champion are
*(seeded)*, so they are rows in the seed table. Nothing on screen is unexplained.

**One phase, so no phase heading.** One actor, one screen, no wait. Wrapping
five steps in `Phase 1` would have added a line and no information.

**The missing lookup value was decided, not asked.** "Information request" is
not in CaseCategory — the snapshot holds only Incident and Service request, and
neither means the same thing. It became a **new** row in the lookup table and a
line in *What I changed*. An earlier draft asked the consultant whether to add
it, rename one, or route on Service instead: three options with one obvious
answer, which is a question that should never have been asked.

**The missing metric source was asked, because it has no answer.** Nothing on
Order marks a return. This is not a mechanism question for the engineer, it is a
business question about what the client means by RMA, and only the consultant can
answer it. Note the phrasing — what should it count, not which field should we
create — and note that it still ships with a default applied, so the document is
complete either way.

**The columns are in the objects file and the steps do not repeat them.** Step 4
says a mini page with four fields; it does not list their types. Step 3 names
the three metrics it shows on screen and no others. The KYC tab's full field
list lives in the objects file, once.
