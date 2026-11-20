from models.user import User
from repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self.users = {}

    def save(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def find_by_email(self, email: str) -> User | None:
        normalized_email = email.strip().lower()

        for user in self.users.values():
            if user.email.strip().lower() == normalized_email:
                return user

        return None

    def find_by_id(self, user_id: str) -> User | None:
        return self.users.get(user_id)

    def find_all(self) -> list[User]:
        return list(self.users.values())

    def update(self, user: User) -> User | None:
        if user.id not in self.users:
            return None

        self.users[user.id] = user
        return user

    def deactivate(self, user_id: str) -> User | None:
        user = self.find_by_id(user_id)

        if user is None:
            return None

        user.is_active = False
        return self.update(user)

    def delete(self, user_id: str) -> None:
        self.users.pop(user_id, None)