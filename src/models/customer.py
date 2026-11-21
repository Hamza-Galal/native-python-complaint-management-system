from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


def _now():
    return datetime.now(timezone.utc)


@dataclass
class Customer:
    id: str
    user_id: str
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)
