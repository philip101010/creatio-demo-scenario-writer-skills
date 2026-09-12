# The processes file — DCM, processes and rules

`<client>-processes-v<n>.md` is the third deliverable, and it exists for one
reason: **the object model tells a build what to create, and this file tells it
what makes the demo move.** Those are different jobs with different failure
modes, and mixing them produces a document where the stage model is buried under
column tables.

Its reader is the same coding agent, plus the engineer who has to draw in the
Case Designer the parts no API can reach.

---

## Where its content comes from

Every provenance marker in the scenario that is not *(seeded)* has a line in
this file, and the line names the step it serves:

| Marker in the scenario | Lands here as |
|---|---|
| *(created by the process)*, *(sent by the process)* | a business process |
| *(calculated by the rule)*, *(set by the rule)* | a business rule |
| *(set by the stage model)*, *(moved by the stage model)* | a DCM stage or step |
| *(returned by the AI skill)*, *(drafted by the AI skill)* | an AI skill, with its trigger |
| *(from the … mock)*, *(from the … feed)* | an integration, and whether it is emulated |

That mapping is the cross-check. Walk the scenario, collect the markers, and
every one of them must appear below. A marker with no line here is a build item
nobody will build; a line here serving no step is work nobody asked for.

---

## Skeleton

```
# <Client> — Processes, stage models and rules
v<n> · <date> · companion to <client>-demo-scenario-v<n>.md

## 1. Stage models (DCM)
## 2. Business processes
## 3. Business rules
## 4. AI skills
## 5. Integrations
## 6. Run before demo
```

Omit a section with nothing in it. Never reorder them.

---

## 1 · Stage models (DCM)

Per case-managed section: the stage column, the stages in order, and per stage
its steps with the element kind.

```
### DCM 1 — Standard customer inquiry

Applies to: Category ∈ {Quote request, Order Status, Technical / Datasheet Question, …}
Stage column: Case.**Status** (CaseStatus)

| Stage | Steps | Element kind | Completes the stage |
|---|---|---|---|
| New | "Review case information and start processing" | Task | yes |
| In progress | "Prepare and send the answer to the customer" | Task | yes |
| Waiting for customer | — | — | any inbound e-mail or logged call returns it to In progress |
| Resolved | "Confirm resolution with the customer" | Task | yes |
| Closed | closure code required; CSAT triggered | Action | — |

Serves s10, s16, s19, s23, s34.
```

Three constraints decide whether a DCM design is buildable at all, and each of
them has to be stated on the page rather than discovered during the build:

- **One stage column per section.** Two stage models on the same section share
  that column. Say which column separates them — usually a Category-style
  lookup in the start condition — and give the union of stage values, because
  that is what the column has to hold.
- **DCM has no gateways.** Any branching is "change stage after this element is
  completed". A design that needs a real decision point is not a DCM; it is a
  process the stage calls.
- **Which step is stage-completing**, per stage. One per stage.

⛔ **DCM is built by hand in the Case Designer.** It is not reachable from the
API, so it is never automated work, and this page has to say so or somebody will
plan it as a script.

---

## 2 · Business processes

Per process: what starts it, what it does in order, what it writes, the steps it
serves, and whether a coding agent can build it.

```
### Route case

Trigger: Case created (signal on Case, record added)
Reads: agent availability, open-case workload, account case history,
       contact language, responsible service team on the Service record
Writes: Case.**Owner**
Serves: s7 *(assigned by the routing rule)*
Build: code-buildable — linear, no gateways
```

- **Trigger** is a signal on an object and which change, or a button, or a stage
  entry. "When the case is ready" is not a trigger.
- **Build** is `code-buildable` or `designer-only`. Designer-only means gateways,
  conditional flows, timers, sub-processes, script tasks or pre-configured
  pages — anything the process-designer API cannot express. That split *is* the
  build plan, and getting it wrong is how a build stalls halfway.
- **Serves** carries the step numbers and the exact provenance marker from the
  scenario, so the two documents can be diffed against each other.

Use the mechanism names from `best-practices.md` section 1 exactly. The coding
agent builds by those names.

---

## 3 · Business rules

Per rule: where it lives, the trigger, the condition, the effect, and the steps
that depend on it.

```
### Incoming calls on Contact

Lives on: Contact (entity-level)
Effect: **Incoming calls** = count of Call where Contact = this contact
        and Direction = "Incoming"
Serves: s3 *(calculated by the rule)*
```

State **entity-level or page-level** on every rule, because they are built with
different tools and land in different places. An entity rule applies everywhere
the object is used — including pages this demo never opens — and a scenario that
needs a lookup filtered on one page but not another cannot be built as one rule
at all.

---

## 4 · AI skills

Per skill: the trigger phrase or the place it is invoked from, what it reads,
what it returns, and whether it writes anything.

An AI skill that **writes** to a record does it through an action process, never
directly — say which process, and list it in section 2 as well. A skill that
only reads is cheaper to build and cannot damage a demo.

The answer shape matters as much as the trigger: the scenario already quotes
what the skill must come back with, and that quote is the specification. Point
at the step rather than paraphrasing it.

---

## 5 · Integrations

Per integration: what it is, whether it is **real or emulated**, what it
returns, and which steps depend on it.

An emulated integration says so in three places — here, in the scenario header,
and in the bubble that first mentions it. A consultant who discovers in the room
that the OEM feed was seed data has been ambushed by their own document.

---

## 6 · Run before demo

The reset the scenario's one-line *Before you present* points at: which records
it restores and to what values, which it deletes, and which it re-creates.

⛔ **Every delete it performs is filtered** — `Created on = today`, or an explicit
list of record numbers. A reset process with an unfiltered delete can wipe the
instance, and it will be run by somebody in a hurry five minutes before a
customer call.

A demo that cannot be run twice is a demo that cannot be rehearsed, so this
section is not optional.
