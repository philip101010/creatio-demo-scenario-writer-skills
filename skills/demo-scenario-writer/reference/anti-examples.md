# Anti-examples

Every pair below is taken from a real Creatio demo scenario, or from a real
first draft this skill produced. The left column is what was written. The right
column is what the engineer needed.

Read the pairs, not just the rules — the rules are abstract, these are the
actual failure modes.

---

## Part 1 — Asking what should have been decided

These are the most expensive defect class, because each one looks like diligence.
A question with one correct answer wastes the consultant's attention, delays the
build, and makes the document read as unfinished.

### 1. Asking whether to add a missing lookup value

> **Bad** — "?OPEN-2 — consultant. Case category "Information request" does not exist. CaseCategory holds two values in the general snapshot: Incident and Service request. Add a third value, rename one, or route on Service instead?"

> **Good** — "Case.CategoryId (existing lookup CaseCategory): add value **"Information request"** *(new value in existing lookup)*. The snapshot holds only "Incident" and "Service request"; neither means the same thing."

Adding a lookup value is a task, not a decision. Three options with one obvious
answer is not a question — it is the work left undone. The only case worth
mentioning is when an existing value already means the same thing: then use it
and say why.

### 2. Asking which mechanism to use for a standard operation

> **Bad** — "?OPEN — engineer. "Access rights are also reassigned, the departing AM's rights are revoked". Record-level rights transfer is not a standard action. Which mechanism: a process that rewrites the rights records, a change of business unit, or user deactivation only?"

> **Good** — Build spec, Access: "BP 'Transfer ownership': reassigns the departing AM's accounts and their open leads, opportunities, orders and invoices to the Successor; grants the Successor read and edit rights on those records; removes the departing AM's rights on them; sets the departing AM to inactive." Open: "?OPEN — consultant. Does the departing AM keep read access to their old accounts for handover, or lose it immediately?"

Ownership transfer is a standard operation. Never ask *how*. What may genuinely
be unclear is the **end state** — which role gains what, which loses what, on
which records — and that is a business question, phrased as an outcome.

### 3. Asking permission to use the only implementation

> **Bad** — "?OPEN-13 — engineer. The Owner lookup on the Account page and the Successor lookup on the mini page are both specified as showing only the current user's own people. A lookup cannot be filtered for one page only; an entity business rule applies everywhere that lookup is used. Accept the rule everywhere, or drop the filtering?"

> **Good** — Build spec, Logic: "Entity business rule on the Owner lookup restricting it to the current user's own people — applies everywhere this lookup is used."

Where the platform offers one way, state that way and its consequence in the
same line. The consequence is a note. It becomes a question only if the same demo
needs that lookup filtered *differently* on two pages, which the rule cannot do.

### 4. Asking about licensing or provider configuration

> **Bad** — "?OPEN-18 — engineer. Which AI provider is configured on POC-01, and is the AI skill licensed on that stand?"

> **Good** — nothing. Specify the AI skill and move on.

The demo stands carry every licence the team needs. Licensing, entitlement,
provider configuration and feature enablement are never questions.

### 5. Asking a telephony question that should have been an intake question

> **Bad** — "?OPEN — engineer. Which CTI provider is connected on POC-02, and does it write a missed call as a Call record?"

> **Good** — Demo card row: "Telephony: CTI emulator". Asked once, at intake, because the input mentioned calls.

If the input mentions calls, ask one question at intake: emulator or real
telephony. Nothing about providers, nothing about what writes what.

---

## Part 2 — Inventing what should have been verified

### 6. Capability asserted from memory

> **Bad** — "Nb RMAs (Orders of type Return)"

> **Good** — "?OPEN — consultant. What counts as an RMA for this client? The Order object carries no return or type column, so the metric has no source."

`sh scripts/model.sh object Order` lists 32 fields. None is a type. The line
was written because it sounded right. Note the addressee: this is not a mechanism
question for the engineer, it is a question about what the client means.

### 7. Stage list that does not match the lookup

> **Bad** — "Case stages (New / In progress / Waiting feedback customer / Resolved / Archived / Closed)"

> **Good** — "Case.StatusId (existing lookup CaseStatus): use existing values New, In progress, **Waiting for response**, Resolved, Closed — the input's "Waiting feedback customer" is the same state under the product's own caption. Add value **"Archived"** *(new value in existing lookup)*, used by UC4 when the case hands off to a lead."

Two defects in one line: a caption invented where the product already has one,
and a value that does not exist. The first is fixed by using the product's
caption; the second by adding the value, not by asking about it.

### 8. Lookup finding carried between snapshots

> **Bad** — "CaseCategory holds two values." (stated unconditionally, on a bank)

> **Good** — "CaseCategory (general snapshot): two values." The banking snapshot returns three, including "Consultation".

`Order` and `Invoice` do not exist in the banking snapshot at all. Always name
which snapshot you verified against, and never carry a finding across.

---

## Part 3 — Structure

### 9. Branching inside a step

> **Bad** — "…from preparing the day, through visiting an existing customer and (optionally) engaging a prospect, to the automatic handoffs…"

> **Good** — UC3 "Visit an existing customer". UC4 "Engage a prospect". Two use cases, each with its own data and its own acceptance.

The word *optionally* means the use case cannot be tested: a tester who skips the
optional half and a tester who does it are running different tests.

### 10. A use case depending on another having been run

> **Bad** — UC4 "a new lead is registered automatically from the case" assumes the case from UC1 was created first.

> **Good** — F3 contains case CS-1041, category "Information request", status New, unassigned. UC4 starts from that record.

If UC4 can only be tested after UC1, it is not a use case. This rule breaks most
often, and it is the whole reason the format exists.

### 11. The same fact written twice

> **Bad** — "Step description" says *"When I modify Priority to Critical, the AM is notified; I can see the email in the Timeline"*, and "Set up needed (for SE)" says *"When I modify Priority for Critical manually or create a Case with Critical priority, AM is notified (email with CTA button sent and seen in the Timeline, Feed message in the Timeline, mobile pop up notification)"*.

> **Good** — happy path: *"The CS agent sets Priority to Critical → the assigned AM receives an email, a feed message and a mobile notification."* Build spec: *"BP 'Notify AM on critical case' — trigger: Case.PriorityId changed to Critical or case created with Critical; actions: email from template 'Critical case', feed message on the case, mobile push to the account's AM."*

The two originals disagree — one covers creation, the other does not. Duplication
does not just make the document long; it makes it contradict itself.

### 12. A table repeated verbatim

> **Bad** — the nine-row country / category / contact assignment table appears twice in the same block, identically.

> **Good** — the table appears once, in F3. The use case says "assignment follows the table in F3".

### 13. Selling language in a step

> **Bad** — "The opportunity lands in Qualification and I do not have to remember what to do next: the stage panel shows four tasks, all assigned to me as owner, all created automatically when the stage opened."

> **Good** — wow line: "the salesperson never has to remember the next step." Step: "The opportunity enters Qualification → four tasks appear on the stage panel, all assigned to the owner."

The persuasion belongs in one line at the top of the use case. Repeating it in
every step is what turns 600 words into 7 000.

### 14. Vague data

> **Bad** — "we will create 10 sample Employees per each region"

> **Good** — F3 lists the ten employees by name with their region and status, because an acceptance row checks that the Successor lookup offers exactly the nine active ones.

### 15. Unresolved decision left as a highlight

> **Bad** — "Create order — BP that creates order (One or several orders?)" left highlighted in the middle of page 12.

> **Good** — the step is written for the decided case, with `?OPEN-7` inline, and the question appears in that use case's Open part with an addressee and what it blocks.

A highlight in a Word document is not a question. Nobody owns it and nobody
answers it.

### 16. Currency and localisation discovered mid-document

> **Bad** — a bold paragraph inside a use case: "CURRENCY: All monetary values in this scenario are in Romanian Lei. Before the demo we must switch the demo instance to RON wherever currency is displayed…"

> **Good** — Demo card rows "Base currency: RON" and "Languages: ro-RO, en-US — OOTB language pack only". F4 carries the setting change.

These are intake questions. If they surface inside a use case, the checklist was
skipped.

### 17. Credentials in the document

> **Bad** — "Username: Supervisor / Password: LxNeA12CwhbTrQm"

> **Good** — F1 lists the instance URL and what the stand is for. Credentials are shared out of band.
