# Golden use case

One example. Read it before writing, match its density, then forget its content.

This is a real use case derived from a real scenario and verified against the
object-model snapshot. Two verifications failed. One became a build-spec
decision; the other became the single `?OPEN`. Which is which is the whole
lesson.

Do not copy the domain. Copy the shape, the sentence length, the ratio of
happy path to build spec, and the discipline of the acceptance table.

---

### UC1 Case intake from an inbound call

**Wow:** the support agent knows who is calling and their whole history before saying hello.
**Roles:** CS agent (HQ).
**Requires:** F2, F3, F4.

**Happy path**

1. The CS agent signs in → the Service desktop opens as the default page.
2. The CS agent triggers an inbound call from the CTI emulator → the CTI panel shows the caller's name and number, resolved from the Contact by phone number.
3. The CS agent clicks the caller's name → the Contact page opens on the KYC tab.
4. The CS agent clicks **Register a case** → a mini page opens.
5. The CS agent fills the four fields and saves → the case is created, linked to the Contact and the Account, and appears on the Contact timeline.

**Build spec**

Objects and fields
- Contact.**NPS** (new field, Integer 0–10).
- Contact.**NPS date** (new field, Date).
- Contact.**Happiness rank** (new field, Integer 1–10, rendered as a slider).
- Contact.**Champion** (new field, Boolean).
- Contact.**Incoming calls** (new field, Integer, calculated) = count of Call where ContactId = the contact and Direction = "Incoming". `Call.DirectionId` (existing field, existing lookup CallDirection, values Incoming / Outgoing / Not determined) — no new lookup needed.
- Contact.**RMA count** — `?OPEN-1`. Nothing on Order distinguishes a return, and no existing column can be derived into one, so there is nothing to count yet.
- Case.**OriginId** (existing field, existing lookup CaseOrigin, value "Call" exists) — set by the mini page.
- Case.**CategoryId** (existing field, existing lookup CaseCategory, general snapshot): add value **"Information request"** *(new value in existing lookup)*. The snapshot holds only "Incident" and "Service request"; neither means the same thing, and UC4 routes on this value.
- Case.**ServiceItemId** (existing field, existing lookup ServiceItem, section "Services").
- Case.**PriorityId** (existing field, existing lookup CasePriority, values Critical / High / Medium / Low).

Processes
- None. Caller resolution by phone number is standard CTI behaviour; nothing is hardcoded.

UI
- Contact page: new tab **KYC** — Cases detail, Orders detail, and the six Contact fields above.
- Contact page: new mini page **Register a case** with Subject, Case category, Service, Priority. Contact and Account prefilled from the record. Origin set to "Call".
- Service desktop set as the default page for the CS role (see F4).

**Data**

Uses F3 records only: Contact "Tiffany Jane Martin", as F3 defines her.

**Acceptance**

| # | Action | Expected result |
|---|---|---|
| 1 | Sign in as CS agent | Service desktop is the landing page |
| 2 | Trigger a call from the emulator on Tiffany Jane Martin's number | CTI panel shows "Tiffany Jane Martin" and the number |
| 3 | Click the caller's name | KYC tab opens; Incoming calls = 3, Champion = true, NPS = 8 |
| 4 | Click Register a case | Mini page opens with exactly four fields |
| 5 | Fill the four fields and save | Case created, Account = Deloitte Germany, Origin = Call, Category = Information request, visible on the Contact timeline |

**Open**

- **?OPEN-1** — consultant. Blocks the RMA count field and nothing else. What counts as an RMA for this client — returned orders, credit notes, or something they track outside Creatio? The Order object carries no return or type column, so the metric has no source until this is answered.

---

## What to notice

**Five steps, five acceptance rows, same numbers.** No step without a check, no
check without a step.

**The happy path never repeats the build spec.** Step 3 says the KYC tab opens.
Step 4 says a mini page opens. Neither lists the fields, because the build spec
already does, and acceptance rows 3 and 4 are what check them. An earlier draft
listed the four mini-page fields in the step *and* the build spec — that is the
duplication that turns a scenario into seven thousand words.

**Every existing thing is marked, and the marking is verified.** "existing lookup
CaseOrigin, value 'Call' exists" was checked with
`python3 scripts/model.py lookup CaseOrigin`. Nothing is asserted from memory.

**The missing lookup value was decided, not asked.** "Information request" is not
in CaseCategory. An earlier draft asked the consultant whether to add it, rename
one, or route on Service instead. That was three options with one obvious answer:
add the value, say so, move on. The engineer now has a task instead of a meeting.

**The missing metric source was asked, because it has no answer.** Nothing on
Order marks a return. This is not a mechanism question for the engineer — it is a
business question about what the client actually means by RMA, and only the
consultant can answer it. Note how it is phrased: what should it count, not
which field should we create.

**Nothing about the customer's pain, the market, or why this matters.** That
lives in the wow line, in one sentence, and nowhere else.
