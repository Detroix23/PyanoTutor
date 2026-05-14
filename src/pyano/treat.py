from mido import Message  # type: ignore[import-untyped]

from pyano.models import Note


def treat(
    held: frozenset[Note],
    added: frozenset[Note],
    removed: frozenset[Note],
) -> list[Message]:
    msgs: list[Message] = []
    for note in added:
        msgs.append(
            Message("note_on", note=note.pitch, velocity=note.velocity, channel=note.channel)
        )
    for note in removed:
        msgs.append(
            Message("note_off", note=note.pitch, velocity=0, channel=note.channel)
        )
    return msgs
