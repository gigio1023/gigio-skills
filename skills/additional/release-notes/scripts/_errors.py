"""Error types shared by the release-note scripts.

Every script exits with status 2 and prints the message when one of these
errors reaches its entry point. The message names the input that broke the
contract and what to change, so the caller can fix the input instead of
reading a traceback.
"""

from __future__ import annotations


class ReleaseNoteError(Exception):
    """Root of the errors the release-note scripts raise on purpose."""


class InputDataError(ReleaseNoteError):
    """A version export cannot be read as a list of keyed records."""


class NoteSourceError(ReleaseNoteError):
    """The note source (note.json) breaks its schema or cites a missing value."""


class EnvironmentSetupError(ReleaseNoteError):
    """A required tool, module, or font is missing from this machine."""
