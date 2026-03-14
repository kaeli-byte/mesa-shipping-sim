"""Minimal model base class."""

from random import Random


class Model:
    def __init__(self, seed: int | None = None) -> None:
        self.random = Random(seed)
