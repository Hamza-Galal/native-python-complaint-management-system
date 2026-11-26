from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateCategoryRequest:
    name: Optional[str]
    description: Optional[str] = None