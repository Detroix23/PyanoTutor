import argparse
import random
import time
from collections.abc import Sequence

import mido  # type: ignore[import-untyped]

from pyano.midi import MidiManager, MidiError, NoteTracker
from pyano.models import Note
from pyano.treat import treat


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pyano")
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Run with simulated note input (no MIDI hardware required)",
    )
    return parser


def _list_and_select_port() -> str:
    ports = mido.get_input_names()
    if not ports:
        print("No MIDI input ports found.")
        raise SystemExit(1)

    print("Available MIDI inputs:")
    for i, name in enumerate(ports):
        print(f"  [{i}] {name}")

    try:
        choice = int(input("Select port: "))
        selected: str = ports[choice]
        return selected
    except (ValueError, IndexError):
        print("Invalid selection.")
        raise SystemExit(1) from None


def _run_live(port_name: str) -> None:
    try:
        with MidiManager(port_name) as mgr:
            print(f"Listening on {port_name}. Press Ctrl+C to stop.")
            while True:
                msgs = mgr.poll()
                if msgs:
                    _process_batch(msgs, mgr)
                else:
                    time.sleep(0.001)
    except KeyboardInterrupt:
        print("\nStopped.")


def _run_simulate() -> None:
    tracker = NoteTracker()
    note_pool = [60, 64, 67, 72, 76]  # C E G C' E'

    print("Simulating MIDI input. Press Ctrl+C to stop.\n")
    try:
        while True:
            note = random.choice(note_pool)
            vel = random.randint(60, 120)
            on = mido.Message("note_on", note=note, velocity=vel, channel=0)
            _process_batch([on], tracker)

            time.sleep(random.uniform(0.8, 2.0))

            off = mido.Message("note_off", note=note, velocity=0, channel=0)
            _process_batch([off], tracker)

            time.sleep(random.uniform(0.3, 1.0))
    except KeyboardInterrupt:
        print("\nStopped.")


def _process_batch(
    msgs: Sequence[mido.Message],
    tracker: NoteTracker,
) -> None:
    all_added: set[Note] = set()
    all_removed: set[Note] = set()

    for msg in msgs:
        print(f"  IN:  {msg}")
        if msg.type in ("note_on", "note_off"):
            added, removed = tracker.apply(msg)
            all_added.update(added)
            all_removed.update(removed)

    if not all_added and not all_removed:
        return

    result = treat(
        held=tracker.held,
        added=frozenset(all_added),
        removed=frozenset(all_removed),
    )
    for out_msg in result:
        print(f"  OUT: {out_msg}")


def _main() -> int:
    args = _build_arg_parser().parse_args()

    if args.simulate:
        _run_simulate()
        return 0

    try:
        port_name = _list_and_select_port()
    except SystemExit:
        return 1

    try:
        _run_live(port_name)
    except MidiError as exc:
        print(f"MIDI error: {exc}")
        print("\nTip: run with --simulate to test without hardware.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
