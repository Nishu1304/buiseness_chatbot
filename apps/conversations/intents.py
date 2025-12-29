from dataclasses import dataclass
from typing import Callable


@dataclass
class Intent:
    name: str
    keywords: set[str]
    priority: int
    handler: Callable
