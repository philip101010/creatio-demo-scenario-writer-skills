# Output format — the contract

This file defines the document you produce. It is a contract, not a suggestion.
Every rule here exists because a real scenario failed without it.

---

## 1. Document skeleton

```
# <Client> — Demo scenario
Version <n> — <date>

## 1. Demo card
## 2. Use case index
## 3. Running order
## 4. Foundation
## 5. Use cases
```

Five sections. Nothing else. No "Brief demo summary", no "Purpose", no
"Goals / Problems", no "Attachments", no closing notes, and **no collected list
of open questions at the end** — every question lives inside the use case it
belongs to.

---

## 2. Demo card

One table, these thirteen rows and no others. Fill from the intake checklist.
Unknown after asking → `?OPEN`, never a guess, never "TBD".

| Row | Content |
|---|---|
| Client | Name, industry, size |
| Client website | URL — source of product names and terminology |
| Demo date / slot | Date, length in minutes |
| Audience | Role — and what that person must be convinced of. One line per person in the room |
| Who clicks | Consultant or solution engineer |
| Instance | Existing URL, or "new OOTB", or the specific stand |
| Base currency | Currency code |
| Languages | Codes; state whether real translation of custom captions or OOTB language pack only |
| Mobile | In scope / out of scope |
| Telephony | CTI emulator / real telephony / not in scope |
| Branding | Logo and colours applied / not applied |
| Out of scope | What must not be shown |
| Object model | `general` or `banking` — which snapshot was used for verification |

---

## 3. Use case index

The first thing the reader sees after the card, and the only thing they need in
order to say "wrong, change this". One row per use case.

| ID | Use case | Wow | Covers input | Requires | Open |
|---|---|---|---|---|---|

- **ID** — `UC1`, `UC2`, … Stable. Never renumbered once issued.
- **Wow** — one line: what the client says out loud when they see it.
- **Covers input** — which part of the consultant's text this came from, so they
  can check nothing was lost and nothing was invented.
- **Requires** — Foundation items only (`F1`, `F3`). **Never another use case.**
- **Open** — how many open questions this use case carries, and for whom:
  `1 consultant`, `2 engineer`, or `—`.

The Open column is how the reader finds the holes without a separate section.

---

## 4. Running order

One line: `F → UC2 → UC1 → UC4 → UC3`.

The demo narrative order. It is deliberately separate from the use case
numbering so that story sequencing never creates a technical dependency.

---

## 5. Foundation

Everything shared by two or more use cases lives here, once. If a fact appears
in a use case, it must not appear in Foundation, and the reverse.

- **F1 Instances** — URLs and what each stand is for. Never credentials.
- **F2 Roles and access rights** — one table: role, business unit, what they see,
  what they may not see. This is the single place access rights are described.
- **F3 Data set** — every record any use case needs, named, with the field values
  that matter. Counts and amounts exact.
- **F4 Global settings** — base currency, languages, mailbox, CTI, workplaces,
  default pages.

**F3 is what makes use cases independently testable.** If UC4 needs a case
already in status "In progress", that case exists in F3 in that status. A use
case never requires that another use case was executed first.

---

## 6. Use case

Fixed shape. Every use case has all six parts, in this order.

```
### UC<n> <Name>

**Wow:** one line.
**Roles:** the roles used, in order of appearance. Maximum two role switches.
**Requires:** F<n>, F<n>.

**Happy path**
1. …

**Build spec**
Objects and fields
- …
Logic
- …
Processes
- …
Access
- …
UI
- …
Dashboards
- …

**Data**
- …

**Acceptance**
| # | Action | Expected result |

**Open**
- ?OPEN-<n> …
```

### Use case contract

1. **One wow-moment per use case.** Two wows means two use cases.
2. **Maximum 8 happy-path steps.** Over 8 → split.
3. **Testable by one person in under 10 minutes**, with no other use case run first.
4. **One use case = one engineer task = one test run.**
5. **Acceptance is self-contained** — readable without opening another use case.
6. **Dependencies point down to Foundation only, never sideways to a use case.**

### Happy path

Grammar, every step, no exceptions:

> `<Role>` `<does>` → `<what is now visible>`

- One sentence. Present tense. Third person or first person, chosen once per
  document and never mixed.
- Only one path. The words *if*, *or*, *optionally*, *alternatively*,
  *in case of* are banned. An alternative flow is a separate use case or is
  dropped.
- Name UI elements exactly as they appear. An element whose real caption you do
  not know is an `?OPEN`, not a plausible guess.
- No adjectives about value ("powerful", "seamless", "modern"). The wow line
  carries the selling; the steps carry the facts.

### Build spec

What to configure. Never what the user sees — that is the happy path's job.
If a line could belong to both, it belongs here only.

- Bullets under the group headings shown in the template above, in that order.
  Omit a group that has nothing in it; never reorder them.
- Every object, field and lookup value verified against the snapshot with
  `scripts/model.py`. Mark each as:
  - `(existing field)` — present in the snapshot, used as is.
  - `(existing lookup)` — with the rename convention:
    `Status (existing lookup): rename value "New" to "Prospect", keep all other values as is.`
  - `(new value in existing lookup)` — the default answer when a value the
    scenario needs is absent. State it; do not ask about it.
  - `(new field)` — with type, and lookup target if a lookup.
  - `(new object)` — with every field, and where it appears as a detail.
- Prefer renaming an existing field or lookup value over creating a new one, and
  say so explicitly. Renaming is cheaper to build than creating.
- Never output a GUID, a record Id or any identifier from the snapshot. Names only.

### Data

The records this use case needs, by name, with exact values. Never "a few leads",
never "several orders". If the acceptance checks a count, the count is stated here.

Records shared with another use case live in F3 and are referenced, not repeated.

### Acceptance

One row per happy-path step, same numbering, one-to-one. This is how the engineer
verifies the build without reading prose.

| # | Action | Expected result |
|---|---|---|
| 3 | Click the caller's name | KYC tab opens, Incoming calls = 3, Champion = true |

Expected result must be observable on screen and checkable in under a minute.
"Works correctly" is not an expected result.

### Open

Numbered `?OPEN-<n>`, unique across the document, listed inside the use case that
needs them and nowhere else. Each one states:

- what is unresolved,
- which step or acceptance row it blocks,
- who answers: `consultant` or `engineer`.

Format:

```
**Open**
- **?OPEN-3** — consultant. Blocks step 4. Is the case assigned by the account's
  region or the contact's region? The input says "by region" without saying whose.
```

A step referencing an `?OPEN` still appears in the happy path, with the marker
inline, so the reader sees where the hole is.

**Before writing any `?OPEN`, check it against the "Decide, don't ask" list in
`best-practices.md` section 2.** Most first-draft questions belong there — they
have one correct answer and asking them wastes the consultant's attention and
makes the document look unfinished.

A use case with no open questions writes `**Open** — none.` and moves on.

---

## 7. Banned words

Reject your own draft if it contains any of these, and rewrite:

`should be able to` · `etc.` · `if possible` · `as needed` · `various` ·
`some` · `several` · `a few` · `e.g.` in a build-spec line · `and/or` ·
`optionally` · `TBD` · `N/A` · `we could` · `it would be nice` ·
`similar to` · `and so on`

`e.g.` is allowed in the Demo card and in a wow line. Nowhere else.

---

## 8. Length

A five-use-case scenario is roughly 600–900 words of body text plus tables.
If you are past that, you are duplicating. The single most common cause is a
build-spec line restating a happy-path step. Check that first.
