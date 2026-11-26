from dataclasses import dataclass
from typing import Optional


@dataclass
class UpdateCategoryRequest:
    name: Optional[str]
    description: Optional[str] = None
    