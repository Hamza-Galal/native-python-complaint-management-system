
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class AuditEvent:
    event_type: str
    user_id: str
    created_at: datetime
    details: dict[str, Any]
