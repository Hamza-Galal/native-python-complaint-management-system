from dataclasses import dataclass
from typing import Optional


@dataclass
class CustomerResponse:
    id: str
    user_id: str
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    active: bool
    created_at: str
    updated_at: str

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "active": self.active,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }
