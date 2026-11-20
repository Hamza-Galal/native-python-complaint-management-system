
from datetime import datetime, timezone, timedelta

from app_container import AppContainer
from exceptions.invalid_token_exception import InvalidTokenException


app = AppContainer()
auth = app.authentication_service

user = auth.register(
    "Expiration Test",
    "expiration.test@example.com",
    "Password123"
)

login_result = auth.login(user.email, "Password123")
token = login_result.token

print("Token Before Expiration:", app.token_repository.exists(token))

auth_token = app.token_repository.find_by_token(token)
auth_token.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)

validation_result = "Not Rejected"

try:
    auth.validate_token(token)
except InvalidTokenException:
    validation_result = "Rejected"

print("Expired Token:", validation_result)
print("Expired Token Deleted:", not app.token_repository.exists(token))
