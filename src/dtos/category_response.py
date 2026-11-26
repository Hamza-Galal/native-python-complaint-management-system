from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryResponse:
    id: str
    name: str
    description: Optional[str]
    active: bool
    created_at: str
    updated_at: str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "active": self.active,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }