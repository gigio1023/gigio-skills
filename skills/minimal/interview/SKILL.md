---
name: interview
description: >
  Interview or grill the user until an idea, plan, system change, research direction, or decision is clear enough to act on, ending in a brief the user approves. Use when the user asks to be questioned: "interview me", "grill me on this plan", "ask me questions until this is clear", "인터뷰해줘", "질문하면서 정리해줘".
---

# Interview

Turn incomplete intent into a clear, user-approved brief. Interview first; do not implement the result in the same invocation unless the user separately asks for that.

## Before asking

- Ground on the conversation, files, repository, and prior artifacts; never make the user repeat what can be inspected.
- Gauge where the user is (a hunch, a draft, a near-final plan) and what they know. State the inference in a line so they can correct it.
- Pick the root from the work type. For systems, research, security, or evaluation work it is usually the goal, binding constraints, failure or threat model, and which result would change direction; for a product feature, who uses it and what outcome it should change; for a rollout, what must not break and who decides. Do not default to user screens.
- Look for what the user has not considered, including what is achievable that they may not know exists. Open the first round with the findings that would change the result, each with your view. With rich prior material, open instead with a numbered synthesis of what is confirmed, inferred, ambiguous, and left for the user, which they can correct.

## Rounds in dependency order

Map the open decisions as a tree in which each hangs off the decisions it depends on. Ask every consequential decision whose prerequisites are settled as one numbered round, ordered by impact, and wait. A question that depends on another open question waits for a later round, so the user never answers a hypothetical. After each round, recap briefly, put contradictions into the next round, look again at territory the answers opened, and ask what they unblocked. Go one question per turn only when the user asks for it.

Each question is answerable in a word: why the answer matters, two to four concrete options with their consequences, and a recommended default the user can accept by agreeing. Silence or a skipped question is never consent; "I don't know" becomes an open item.

## Show, do not ask to describe

Some criteria the user recognizes on sight but cannot describe: an output format, a level of detail, a tone, an interface shape. Asking "what format do you want?" yields a vague or invented answer that later reads as a decision. Show two to four short samples that differ on the criterion, or a reference (existing code first), ask which is closest and what is wrong with the rest, and record only what the reaction establishes. Build a runnable prototype only with the user's consent.

## Facts, measurements, decisions

- A discoverable fact (current behavior, file contents, configuration, a documented limit) is the agent's job: look it up, never ask the user.
- A question only a measurement or experiment can answer is an investigation item, not a question for the user. The user can still decide what to do with each plausible outcome. A cheap, authorized check can simply be run.
- Goals, priorities, scope, acceptable risk, ownership, and tradeoffs are the user's to decide.

## Closing

Close when the next action is determined, not when every branch is visited. Restate the outcome in one sentence for the user to confirm, then give the brief in chat: confirmed decisions, evidence and inferences, investigation and open items, and the next step. Shape it to the work. The user controls the stop; if asked, summarize where things stand without arguing for more rounds. Write a file, create tickets, or message anyone only when asked.
