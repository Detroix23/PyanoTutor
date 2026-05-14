from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Note:
    pitch: int
    velocity: int
    channel: int
