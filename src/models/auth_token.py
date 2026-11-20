
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuthToken:
    token: str
    user_id: str
    created_at: datetime
    expires_at: datetime
