
from models.auth_token import AuthToken
from repositories.token_repository import TokenRepository


class InMemoryTokenRepository(TokenRepository):

    def __init__(self):
        self.tokens = {}

    def save(self, auth_token: AuthToken) -> AuthToken:
        self.tokens[auth_token.token] = auth_token
        return auth_token

    def find_by_token(self, token: str) -> AuthToken | None:
        return self.tokens.get(token)

    def delete(self, token: str) -> None:
        self.tokens.pop(token, None)

    def delete_all_by_user_id(self, user_id: str) -> None:
        tokens_to_delete = []

        for token, auth_token in self.tokens.items():
            if auth_token.user_id == user_id:
                tokens_to_delete.append(token)

        for token in tokens_to_delete:
            del self.tokens[token]
     
    def exists(self, token: str) -> bool:
      return token in self.tokens