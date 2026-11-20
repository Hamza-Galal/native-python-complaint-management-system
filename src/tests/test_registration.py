
from services.authentication_service import AuthenticationService
from repositories.in_memory_user_repository import InMemoryUserRepository
from repositories.in_memory_token_repository import InMemoryTokenRepository
from exceptions.invalid_registration_exception import InvalidRegistrationException
from exceptions.duplicate_email_exception import DuplicateEmailException


user_repository = InMemoryUserRepository()
token_repository = InMemoryTokenRepository()

service = AuthenticationService(user_repository, token_repository)

test_cases = [
    ("Empty name", "", "a@test.com", "Password123"),
    ("Invalid email", "Eman", "invalid-email", "Password123"),
    ("Short password", "Eman", "b@test.com", "123")
]

for label, name, email, password in test_cases:
    try:
        service.register(name, email, password)
        print(label, "FAILED")
    except InvalidRegistrationException:
        print(label, "PASS")

service.register("Eman", "eman@test.com", "Password123")

try:
    service.register("Another User", "EMAN@test.com", "Password456")
    print("Duplicate email FAILED")
except DuplicateEmailException:
    print("Duplicate email PASS")
