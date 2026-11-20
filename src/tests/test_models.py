
from models.user import User
from models.user_role import UserRole
from models.authenticated_user import AuthenticatedUser

user = User(
    id="1",
    name="Eman",
    email="eman@example.com",
    password_hash=b"test_hash",
    salt=b"test_salt",
    role=UserRole.CUSTOMER
)

print(user)
print(user.role.value)
print(user.is_active)
print(user.created_at)
authenticated_user = AuthenticatedUser(
    user_id=user.id,
    name=user.name,
    email=user.email,
    role=user.role
)

print(authenticated_user)