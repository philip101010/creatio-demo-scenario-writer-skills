# Best practices — the white list

You have no access to a demo environment. This file plus the object-model
snapshot is your only ground truth. **A build-spec line you cannot trace to this
file or to `scripts/model.py` output is not a line — it is an `?OPEN`.**

Keep this file current. When the team learns a new limitation or adds a reusable
block, it is edited here, not remembered.

---

## 1. Mechanisms you may specify

Use these names exactly. The engineer builds by them.

**Data**
- New object, with a section or as a detail only.
- New field on an existing object: Text, Integer, Decimal, Currency, Date,
  Date/Time, Boolean, Lookup.
- Calculated field, with the formula stated.
- New lookup, or a new value in an existing lookup, or a renamed value in an
  existing lookup.

**Logic**
- **Page business rule** — conditional visibility, editability, required state;
  setting or clearing a field value from another field. Not code.
- **Entity business rule (static filter)** — restricting which records a lookup
  offers. Applies everywhere that lookup is used, not on one page.
- **Business process (BP)** — triggered on record create, field change, or a
  button; creates records, sends email, sets fields, starts approvals.
- **DCM case (stage model)** — stages with steps; a step can be a task, an
  email, an approval, or an action. One step per stage may be marked as
  stage-completing.
- **Approval** — the existing OpportunityVisa / approval mechanism, assigned to a
  role rather than a named user.
- **Printable** — a document generated from a record and its details.

**UI**
- New tab on a record page.
- New detail on a record page.
- Mini page, opened from a button or a detail.
- Field card, KPI strip, expansion panel with a data grid.
- Slider, colour picker, rich-text editor, image and file input on a field.
- Kanban view on a section list page.
- Dashboard widget: metric, list, bar chart, pie chart, gauge.
- Workplace, and a default page per role.

**Access**
- Rights by organisational unit (business unit) and by functional role.
- Record-level rights: own records, own unit, all records.
- Column-level and tab-level restriction on a page.
- Workplace visibility per role.
- Ownership transfer: reassigning records and their linked records to a
  successor, granting the successor the departing user's rights, revoking the
  departing user's rights, deactivating the user. Standard operations — specify
  the end state per role, never ask which mechanism.

**Channels**
- Email from a template, visible on the record timeline.
- Feed message on the record.
- Mobile push notification.
- Notification centre entry.
- CTI emulator for inbound and outbound calls.

**AI**
- AI skill invoked from a business process (the "Sub-agent" process element),
  with a text input and a JSON-schema-constrained output.
- AI skill on a page, in the context of the open record.

When a scenario step involves AI, write the step as the exchange between the
user and the agent: what the user asks or clicks, and what the agent returns.

---

## 2. Decide, don't ask

An `?OPEN` costs the consultant's attention and makes the document look
unfinished. Raise one only when the answer **changes what gets built** and you
cannot derive it. The categories below have exactly one correct answer. Decide
them, write the decision into the build spec, and move on.

**A missing lookup value.** The scenario needs a value the lookup does not have?
Add it. Write `(new value in existing lookup)` and name the value. Only if an
existing value clearly means the same thing, use that one and say so:
`Category (existing lookup): use "Service request" — the input's "Information
request" is the same state under the product's own caption.` Never ask whether
to add a value.

**A missing simple field.** A Text, Integer, Decimal, Currency, Date, Boolean or
Lookup column the scenario needs and the object lacks? Specify it as
`(new field)` with its type. Never ask whether to create it.

**A mechanism with exactly one implementation.** Where the platform offers one
way to do something, state that way and its consequence in the same line — do
not ask for permission to use the only option. Example: restricting the records
a lookup offers is an entity business rule, so it applies everywhere that lookup
is used. Write `Owner (existing field): entity business rule restricting the
lookup to the current user's own people — applies everywhere this lookup is
used.` That is a note, not a question.

**Licensing, entitlement and provider availability.** Never ask whether a
capability is licensed, which AI provider is configured, or whether a feature is
enabled on the stand. The demo stands carry every licence the team needs.

**Standard administrative operations.** Rights reassignment, revoking a user's
access, changing a business unit, deactivating a user, transferring record
ownership — all standard. Never ask *how* to do them. What you may need to ask
is the **expected end state**: which role gains what, which loses what, on which
records. That is a business question for the consultant, phrased as an outcome,
never as a choice of mechanism.

**Telephony.** Never ask which CTI provider is connected or what it writes to the
database. Ask once, in the intake checklist, whether the demo uses the CTI
emulator or real telephony — and nothing further.

### What is still a real question

- **Business semantics.** Which region, which role, which rule, which threshold.
  The input says "assigned by region" without saying whose region.
- **Expected end state** where two outcomes are both plausible and materially
  differ, and picking wrong means a rebuild.
- **A capability absent from the snapshot with no cheap equivalent** — a field to
  count that does not exist and cannot be derived. Engineer.

### How to phrase what is left

State what is unresolved, what it blocks, and who answers. One sentence of
context, then the question. Never offer the engineer a menu of mechanisms; ask
for the outcome and let them choose the mechanism.

---

## 3. Known limitations — grounds to refuse

This list is why you can say no. Add to it whenever the team hits a new wall.

- **No funnel chart type.** A funnel must be specified as a bar chart.
- **A lookup cannot be filtered for one page only.** Restricting the records a
  lookup offers is an entity business rule and applies everywhere that lookup is
  used. Specify the rule and note that consequence in the same line — this is not
  a question. It becomes an `?OPEN` only when the same demo needs *different*
  contents for that lookup on two different pages, which the rule cannot do.
- **Mobile pages are more limited than web pages** — a separate component
  catalogue, and no handlers, validators or converters. Complex mobile logic is
  an `?OPEN`, not an assumption.
- **A user-visible caption in a multilingual demo must be a localisable string.**
  Every custom caption multiplies by the number of languages. If the Demo card
  lists more than one language, say so in the build spec; it is a real cost.
- **Freshly added columns can lag in OData**, so seeded data may not appear
  immediately after the build. Relevant to timing, not to the scenario.
- **A total that is a sum of child records must be recalculated by the platform**,
  never typed. Say "recalculated from the branch lines, never entered manually".
- **Renaming a lookup value changes it everywhere.** If the scenario needs the
  old caption somewhere else in the same demo, that is an `?OPEN`.
- **Never output a GUID or a record Id.** The engineer resolves every lookup by
  name. The snapshot contains Record Ids; they are for verification only.

---

## 4. Object model — how to verify

The snapshot in `assets/` is a live export.

| Model | Objects | Fields | Lookup values | Objects with a section |
|---|---|---|---|---|
| general | 1 494 | 17 407 | 9 254 | 67 |
| banking | 1 659 | 19 310 | 7 204 | 81 |

Use the banking model when the client is a bank, an insurer or any financial
services firm; the general model otherwise. State which one you used in the
Demo card.

Never read the xlsx yourself. Query it:

```bash
sh scripts/model.sh object Case              # all fields of an object
sh scripts/model.sh lookup CaseStatus       # all values of a lookup
sh scripts/model.sh field priority --object Case
sh scripts/model.sh search opportunit       # find an object by name
sh scripts/model.sh sections                # every object with a UI section
sh scripts/model.sh object Loan --banking
```

Exit code 1 means **not verified** — either it is absent from the snapshot, or it
is present but empty there. The message tells you which. Both outcomes mean the
same thing for your draft: `?OPEN`, never a guess. A finding from one snapshot
never carries over to the other; the two models differ, sometimes sharply —
`Order` and `Invoice` do not exist in the banking model at all, and
`CaseCategory` has two values in one and three in the other.

**Verify before you write, not after.** Every object, field, lookup and lookup
value in a build spec is checked. This is not optional and it is not slow — it is
one command per object.

---

## 5. Standard objects to reach for first

Creating a new object is the expensive answer. Check these first — they carry
sections, pages, dashboards and rights out of the box.

| Need | Object |
|---|---|
| Ticket, complaint, incident, service request | **Case** |
| Task, email, meeting, visit, call as an activity | **Activity** |
| Phone call with direction and duration | **Call** |
| Deal | **Opportunity** |
| Unqualified demand | **Lead** |
| Company, legal entity, branch | **Account** |
| Person | **Contact** |
| Sales order | **Order** — general model only, absent from the banking snapshot |
| Bill | **Invoice** — general model only, absent from the banking snapshot |
| Contract | **Contract** |
| Approval | the approval objects on Opportunity, Order, Invoice, Contract |
| Catalogue item | **Product** |
| Service catalogue item | **ServiceItem** |
| SLA | **ServicePact** |
| Article, FAQ | **KnowledgeBase** |
| Employee | **Employee** |
| Document | **Document** |
| User, role, org unit | **SysAdminUnit** |
| Workplace | **SysModuleFolder** |
| Campaign, bulk email, landing page | **Campaign**, **BulkEmail**, **LandingPage** |

`sh scripts/model.sh sections` lists every object that has a section — 67
in the general model, 81 in the banking one. If the need is on that list, do not
create a new object without saying why.

---

## 6. Conventions

- **Mark every existing thing.** `(existing field)`, `(existing lookup)`.
- **Rename rather than create**, and write the rename in full:
  `Status (existing lookup): rename value "New" to "Prospect", keep all other values as is.`
- **Prefix new custom names** with the client or app prefix, consistently across
  the document.
- **Name UI elements as they appear on screen**, in the demo language.
- **Amounts, counts and dates are exact.** A count in an acceptance row must
  match the data in F3.
- **Credentials never appear in the document.**

---

## 7. Reusable demo blocks

The blocks this team has built more than once. When a consultant's text matches
one, reuse the block name and its known shape instead of designing from zero.

*This section is the team's own inventory and is expected to grow. Add a block
after the second time you build it, with: name, what it proves, the objects it
touches, and anything that caught you out.*

| Block | Proves | Touches |
|---|---|---|
| Case intake from an inbound call | agent knows the caller before answering | Contact, Call, Case |
| Case pipeline with Kanban and rule-based assignment | ticket routes itself | Case, CaseStatus, BP |
| Escalation with three-channel notification | nothing gets lost between teams | Case, Order, Activity, BP |
| Support case to lead handoff | commercial signal survives the support queue | Case, Lead, BP |
| Service metrics on home page and account tab | manager sees SLA without a spreadsheet | Case, Account, dashboards |
| Account hierarchy with a group rollup | one customer group, local ownership, group number | Account, Opportunity, Currency |
| Cross-border deal with per-branch lines | regional teams on one record | Opportunity, new branch object, Order |
| Ownership transfer on a departing employee | successor inherits history and rights | Employee, Account, rights |
| Opportunity DCM with a required approval | the offer cannot leave without a sign-off | Opportunity, approval, BP |
| Lead from an inbound email via an AI skill | the rep never retypes an email | Activity, Lead, AI skill, BP |
