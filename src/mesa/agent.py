"""Minimal agent base class."""


class Agent:
    def __init__(self, unique_id: int, model: object) -> None:
        self.unique_id = unique_id
        self.model = model

    def step(self) -> None:  # pragma: no cover
        return
