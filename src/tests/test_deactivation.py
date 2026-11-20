
from app_container import AppContainer
from exceptions.invalid_credentials_exception import InvalidCredentialsException


app = AppContainer()
auth = app.authentication_service

user = auth.register(
    "Deactivation Test",
    "deactivation.test@example.com",
    "Password123"
)

login_1 = auth.login(user.email, "Password123")
login_2 = auth.login(user.email, "Password123")

print("Tokens Before:", app.token_repository.exists(login_1.token)
      and app.token_repository.exists(login_2.token))

deactivated_user = auth.deactivate_user(user.id)

print("User Deactivated:", deactivated_user.is_active is False)
print("First Token Deleted:", not app.token_repository.exists(login_1.token))
print("Second Token Deleted:", not app.token_repository.exists(login_2.token))

login_result = "Not Rejected"

try:
    auth.login(user.email, "Password123")
except InvalidCredentialsException:
    login_result = "Rejected"

print("Login After Deactivation:", login_result)
