# Source Notes

Last reviewed 2026-10-03.

## Sources

- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): a progress file and the git log let each new session get its bearings before it implements anything.
- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): point to high-signal artifacts and let the agent fetch detail on demand.
- Claude Code docs, [Manage sessions](https://code.claude.com/docs/en/sessions): even a same-harness resume restores the conversation but not background Bash tasks, and a tool still running when the process ended does not finish. Transcripts stay on disk as files that can be located later.
- OpenAI Agents SDK, [Handoff prompt](https://openai.github.io/openai-agents-python/ref/extensions/handoff_prompt/): a runtime handoff passes conversation context automatically, which a file handoff must make explicit.

## Why the File Opens With an Order

Users start a successor with the handoff path alone. A path to a Markdown file with headings reads like a document to review, and successors have answered it by editing the handoff instead of doing the work. The bold opening line names the file as the reader's task and forbids editing it, and the description's NOT clause keeps a pasted path from loading this skill.

## Questions for the User

The Questions for the User table follows the pack's question rules: ask only what would change the work, never ask what inspection can settle, offer concrete options with a recommended default, and record what happens without an answer instead of treating silence as consent.
