
from dataclasses import dataclass
from datetime import datetime

from models.authenticated_user import AuthenticatedUser


@dataclass
class LoginResponse:
    token: str
    token_type: str
    expires_at: datetime
    user: AuthenticatedUser
