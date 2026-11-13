# Repository Sources And Installed Copies

## Source Of Truth

Honor the selected repository or private project scope. In this repository, edit the selected checkout under skills/<install-set>/<skill-name>; the install sets are minimal/ (installed by default) and additional/ (installed on request). Elsewhere follow the owning project's discoverable skill layout. Reuse existing conventions, read applicable project instructions, and preserve unrelated changes. A project-local skill does not need migration into a public or global pack to be useful.

Update catalogs when adding, removing, renaming, or changing advertised scope. Do not rewrite unrelated catalog entries to standardize wording.

Keep a shared method separate from its private project bindings: source maps, schemas, runner commands, and access constraints belong with their authorized owner and are loaded when relevant. Stable private instructions may live in a private skill; mutable task records stay outside replaceable installed packages. Do not move confidential material into a public repository merely to make a link self-contained.

## Development And Installation

Resolve installed paths and symlink targets before editing:

- A plain global directory is a deployed copy. Edit repository sources and report that the installed version remains unchanged.
- A development symlink may make repository edits live immediately; respect that scope and do not silently repoint it.
- Per-skill links and shared-directory links are both valid. Preserve topology; do not replace an entire agent skill directory to expose one change.

Installing a pack is a separate request; source editing does not itself authorize replacing global packages.

## Local-Only Migration

When migration is requested, copy the entire local package to its intended source, compare files, and preserve user data. Repoint the installed copy only within the migration's scope. Do not overwrite local-only work because names match.

## Verification

Check name/folder identity, trigger clarity, resource paths, and documented commands. Report source branch/path and whether an installed copy changed. Size and section-style advisories are not migration blockers.
