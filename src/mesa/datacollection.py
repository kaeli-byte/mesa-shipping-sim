"""Minimal DataCollector implementation."""

from __future__ import annotations

from typing import Callable, Dict


class _SimpleFrame:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows
        self.columns = list(rows[0].keys()) if rows else []

    def tail(self, n: int) -> "_SimpleFrame":
        return _SimpleFrame(self._rows[-n:])

    def to_string(self, index: bool = False) -> str:  # noqa: ARG002
        if not self._rows:
            return ""
        header = " | ".join(self.columns)
        values = " | ".join(str(self._rows[-1][c]) for c in self.columns)
        return f"{header}\n{values}"


class DataCollector:
    def __init__(self, model_reporters: Dict[str, Callable[[object], object]]) -> None:
        self.model_reporters = model_reporters
        self._model_rows: list[dict] = []

    def collect(self, model: object) -> None:
        row = {name: fn(model) for name, fn in self.model_reporters.items()}
        self._model_rows.append(row)

    def get_model_vars_dataframe(self) -> _SimpleFrame:
        return _SimpleFrame(self._model_rows)
