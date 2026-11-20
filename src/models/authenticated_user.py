from dataclasses import dataclass
from typing import Optional

from models.user_role import UserRole


@dataclass
class AuthenticatedUser:
    user_id: str
    name: str
    email: str
    role: UserRole
    customer_id: Optional[str] = None
    agent_id: Optional[str] = None