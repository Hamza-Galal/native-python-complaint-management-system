from services.authentication_service import AuthenticationService
from repositories.in_memory_user_repository import InMemoryUserRepository
from repositories.in_memory_token_repository import InMemoryTokenRepository
from exceptions.invalid_credentials_exception import InvalidCredentialsException


user_repository = InMemoryUserRepository()
token_repository = InMemoryTokenRepository()

service = AuthenticationService(user_repository, token_repository)

service.register(
    "Eman",
    "eman@example.com",
    "Password123"
)

response = service.login(
    " EMAN@example.com ",
    "Password123"
)

print("Token exists:", bool(response.token))
print("Token type:", response.token_type)
print("User name:", response.user.name)
print("User role:", response.user.role.value)
print("Token saved:", token_repository.find_by_token(response.token) is not None)

try:
    service.login("eman@example.com", "WrongPassword")
    print("Wrong password: FAILED")
except InvalidCredentialsException:
    print("Wrong password: PASS")