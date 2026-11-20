
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from models.user_role import UserRole


@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: bytes
    salt: bytes
    role: UserRole
    is_active: bool = True
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    customer_id: Optional[str] = None
    agent_id: Optional[str] = None
