
from app_container import AppContainer
from exceptions.invalid_credentials_exception import InvalidCredentialsException


app = AppContainer()
auth = app.authentication_service

user = auth.register(
    "Failed Login Test",
    "failed.login@example.com",
    "Password123"
)

login_result = "Not Rejected"

try:
    auth.login(user.email, "WrongPassword123")
except InvalidCredentialsException:
    login_result = "Rejected"

events = app.audit_event_repository.find_by_user_id(user.id)

login_events = [
    event
    for event in events
    if event.event_type == "USER_LOGGED_IN"
]

print("Wrong Password:", login_result)
print("Successful Login Events:", len(login_events))
