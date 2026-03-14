"""Minimal Mesa-compatible interfaces for local development tests.

If the real `mesa` package is installed, it should be preferred in production.
"""

from .agent import Agent
from .model import Model

__all__ = ["Agent", "Model"]
