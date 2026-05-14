from __future__ import annotations

from collections.abc import Sequence

import mido  # type: ignore[import-untyped]

from pyano.models import Note


class MidiError(Exception):
    pass


class NoteTracker:
    """Tracks currently held notes from incoming MIDI note events."""

    def __init__(self) -> None:
        self._notes: dict[tuple[int, int], Note] = {}

    @property
    def held(self) -> frozenset[Note]:
        return frozenset(self._notes.values())

    def apply(self, msg: mido.Message) -> tuple[frozenset[Note], frozenset[Note]]:
        added: set[Note] = set()
        removed: set[Note] = set()

        if msg.type == "note_on" and msg.velocity > 0:
            note = Note(pitch=msg.note, velocity=msg.velocity, channel=msg.channel)
            self._notes[(msg.channel, msg.note)] = note
            added.add(note)
        elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
            key = (msg.channel, msg.note)
            old = self._notes.pop(key, None)
            if old is not None:
                removed.add(old)

        return frozenset(added), frozenset(removed)


class MidiManager(NoteTracker):
    """Opens real MIDI input and virtual output ports."""

    def __init__(self, input_port: str, virtual_output: str = "Pyano") -> None:
        super().__init__()
        try:
            self._in = mido.open_input(input_port)
            self._out = mido.open_output(virtual_output, virtual=True)
        except (OSError, SystemError) as exc:
            raise MidiError(
                "Cannot open MIDI ports. The ALSA sequencer kernel module "
                "(snd-seq) is required but not available on this system.\n"
                "  - On real Linux: install alsa-lib-devel and load snd-seq\n"
                "  - On WSL: the WSL kernel has no ALSA sequencer support\n"
                "  - To test without hardware: pass --simulate"
            ) from exc

    def poll(self) -> Sequence[mido.Message]:
        return list(self._in.iter_pending())

    def send(self, msg: mido.Message) -> None:
        self._out.send(msg)

    def close(self) -> None:
        self._in.close()
        self._out.close()

    def __enter__(self) -> MidiManager:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
