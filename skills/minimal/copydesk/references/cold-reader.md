# Cold Reader

Use before handing over a document that someone will act on without its writer: a design document, delivery brief, proposal, guide, handoff, or a substantial issue or PR body. The writer cannot unsee the drafting context, so a reader who never had it shows whether the document carries what the conversation supplied. A short message or a local wording correction needs only the ordinary final read.

## What the reader gets

Start one subagent with a fresh context. Give it the document's contents inline and the role of the intended reader, such as "an engineer on the billing team who will implement this and did not follow the design discussion". Never give a path: a path invites the reader to open the repository, neighboring files, or earlier drafts, and those hold the context the test removes. Never give the writer's intent, the conversation, the source notes, or the answers the writer expects.

Before starting the reader, write one line for yourself: what the document is meant to be, who it is for, and what it should lead the reader to do or decide. The reader never sees this line.

## What the reader returns

The reader returns two things. First, what it takes the document to be: the subject, the purpose, and the action or decision it asks for. Second, only the questions where it would have to guess and a wrong guess would matter, ranked by consequence. Wording preferences, points the document leaves to the reader, and anything a competent reader could settle alone stay out of the list. "Nothing important left" is a complete answer.

```text
You are [READER ROLE]. You have the document below and will act on it without being able to ask its writer anything.

Using only this document:
1. In two or three sentences, say what the document is, who it is for, and what it asks you to do or decide.
2. List the questions you would still need answered before acting, only where you would otherwise have to guess and a wrong guess would change what you do. Rank them by consequence. For each, say what you would guess and what would change if that guess were wrong.

Do not open other files. For a link, use only its text and the sentence around it. Skip wording preferences and anything the document leaves to your judgment. If nothing important is left, say "nothing important left".

[DOCUMENT CONTENTS]
```

The link rule tests a property the skill asks of every document: the explanation stays understandable without opening every link.

## Compare the reading with the intent

Compare the reader's account with the intent line. A mismatch is a defect of the document. A reader who takes a proposal for a decision, misses the requested action, or names a different audience shows where the text failed to say so. Find the passage that produced the reading, usually the opening, the status of a claim, or the action line, and fix it there. A guess the reader had to make is also a finding, even when the guess happened to be right.

## Sort each question

| Answer source | Where the answer goes |
| --- | --- |
| The drafting context already holds it | Into the document, where the reader needed it |
| A minor point the writer can settle without changing the outcome | Settled by the writer and marked with its status, such as a proposed default |
| Only the user can answer, and the answer changes the substance | One message to the user, most consequential question first |

The first pile is the common case: the writer knew the answer and left it out. For the second, the status mark lets the reader tell a writer's call from a decision; list these calls for the user at handover so they can check them while reading. Ask the third pile in that one message, then update the document with the answers. The pass produces one round of questions. Start a new reader only when the fixes changed the document's structure or purpose. One reader is one sample, so a high-stakes document can justify a second independent reader.

## Without a subagent

When the harness cannot start a subagent, read as that reader yourself, paragraph by paragraph. After each paragraph, ask: could someone who read only up to here, with no access to the conversation, follow this? Note each term, reference, or step that leans on something not yet on the page, and each question the next paragraph assumes is settled. This read is weaker than a fresh context because the writer already knows the answers. When reporting a document whose stakes called for the pass, say that it was a self-read.

## Sources

The three-way sort of the reader's questions adapts the builder check in the `brainstorming` skill of [obra/superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7/skills/brainstorming), read on 2026-11-04. Passing contents instead of a path, keeping the writer's intent from the reader, and treating a mismatch as a document defect adapt the `shower` skill in [LilMGenius/paperthin](https://github.com/LilMGenius/paperthin). The fresh-context reader test follows the Reader Testing step of Anthropic's `doc-coauthoring` skill ([anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring), read at commit `ca45fc4` on 2026-10-28).
