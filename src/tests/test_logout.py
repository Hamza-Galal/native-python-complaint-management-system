from services.authentication_service import AuthenticationService
from repositories.in_memory_user_repository import InMemoryUserRepository
from repositories.in_memory_token_repository import InMemoryTokenRepository
from exceptions.invalid_token_exception import InvalidTokenException


user_repository = InMemoryUserRepository()
token_repository = InMemoryTokenRepository()

service = AuthenticationService(user_repository, token_repository)

service.register("Eman", "eman@example.com", "Password123")

response = service.login("eman@example.com", "Password123")

token = response.token

service.logout(token)

print(
    "Token deleted:",
    token_repository.find_by_token(token) is None
)

try:
    service.validate_token(token)
    print("Reused token: FAILED")
except InvalidTokenException:
    print("Reused token: PASS")