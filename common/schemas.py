import random
from enum import Enum
from typing import Annotated

from annotated_types import Ge, Le
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    x: Annotated[int, Ge(0), Le(100)] = Field(default_factory=lambda: random.randint(0, 100))
    y: Annotated[int, Ge(0), Le(100)] = Field(default_factory=lambda: random.randint(0, 100))


class TaxiStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
