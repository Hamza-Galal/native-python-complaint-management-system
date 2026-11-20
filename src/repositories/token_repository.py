
from abc import ABC, abstractmethod

from models.auth_token import AuthToken


class TokenRepository(ABC):

    @abstractmethod
    def save(self, auth_token: AuthToken) -> AuthToken:
        pass

    @abstractmethod
    def find_by_token(self, token: str) -> AuthToken | None:
        pass

    @abstractmethod
    def delete(self, token: str) -> None:
        pass

    @abstractmethod
    def delete_all_by_user_id(self, user_id: str) -> None:
        pass
    
    @abstractmethod
    def exists(self, token: str) -> bool:
        pass