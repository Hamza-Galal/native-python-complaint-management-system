
import hashlib
import hmac
import secrets
import re
import uuid

from datetime import datetime, timezone, timedelta

from models.user import User
from models.user_role import UserRole
from models.auth_token import AuthToken
from models.authenticated_user import AuthenticatedUser

from dtos.login_response import LoginResponse

from repositories.user_repository import UserRepository
from repositories.token_repository import TokenRepository

from exceptions.duplicate_email_exception import DuplicateEmailException
from exceptions.invalid_registration_exception import InvalidRegistrationException
from exceptions.invalid_credentials_exception import InvalidCredentialsException
from exceptions.invalid_token_exception import InvalidTokenException

from events.audit_event import AuditEvent
class AuthenticationService:

    HASH_ALGORITHM = "sha256"
    HASH_ITERATIONS = 100000
    SALT_LENGTH = 16
    TOKEN_EXPIRATION_HOURS = 24

    def __init__(
        self,
        user_repository: UserRepository,
        token_repository: TokenRepository,
        customer_profile_creator=None,
        audit_event_repository=None
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.customer_profile_creator = customer_profile_creator
        self.audit_event_repository = audit_event_repository


    def publish_audit_event(
        self,
        event_type: str,
        user_id: str,
        details: dict | None = None
    ) -> None:

        if self.audit_event_repository is None:
            return

        event = AuditEvent(
            event_type=event_type,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            details=details or {}
        )

        self.audit_event_repository.save(event)
    @staticmethod
    def hash_password(password: str) -> tuple[bytes, bytes]:
        salt = secrets.token_bytes(AuthenticationService.SALT_LENGTH)

        password_hash = hashlib.pbkdf2_hmac(
            AuthenticationService.HASH_ALGORITHM,
            password.encode("utf-8"),
            salt,
            AuthenticationService.HASH_ITERATIONS
        )

        return password_hash, salt

    @staticmethod
    def verify_password(password: str, password_hash: bytes, salt: bytes) -> bool:
        new_hash = hashlib.pbkdf2_hmac(
            AuthenticationService.HASH_ALGORITHM,
            password.encode("utf-8"),
            salt,
            AuthenticationService.HASH_ITERATIONS
        )

        return hmac.compare_digest(new_hash, password_hash)

    def register(self, name: str, email: str, password: str) -> User:

        name = name.strip()
        email = email.strip().lower()

        if not name:
            raise InvalidRegistrationException("Name is required")

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(email_pattern, email):
            raise InvalidRegistrationException("Invalid email address")

        if len(password) < 8:
            raise InvalidRegistrationException(
                "Password must be at least 8 characters"
            )

        if self.user_repository.find_by_email(email):
            raise DuplicateEmailException()

        password_hash, salt = self.hash_password(password)

        user = User(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            password_hash=password_hash,
            salt=salt,
            role=UserRole.CUSTOMER
        )

        self.user_repository.save(user)

        try:
            if self.customer_profile_creator is not None:
                customer_profile = self.customer_profile_creator(user)

                user.customer_id = customer_profile.id
                self.user_repository.update(user)

        except Exception:
            self.user_repository.delete(user.id)
            raise

        self.publish_audit_event(
            event_type="USER_REGISTERED",
            user_id=user.id,
            details={
                "email": user.email,
                "role": user.role.value
            }
        )

        return user

    def login(self, email: str, password: str) -> LoginResponse:

        email = email.strip().lower()

        user = self.user_repository.find_by_email(email)

        if (
            user is None
            or not user.is_active
            or not self.verify_password(
                password,
                user.password_hash,
                user.salt
            )
        ):
            raise InvalidCredentialsException()

        token = secrets.token_urlsafe(32)

        created_at = datetime.now(timezone.utc)

        expires_at = created_at + timedelta(
            hours=self.TOKEN_EXPIRATION_HOURS
        )

        auth_token = AuthToken(
            token=token,
            user_id=user.id,
            created_at=created_at,
            expires_at=expires_at
        )

        self.token_repository.save(auth_token)

        authenticated_user = AuthenticatedUser(
           user_id=user.id,
           name=user.name,
           email=user.email,
           role=user.role,
           customer_id=user.customer_id,
           agent_id=user.agent_id
        )
        self.publish_audit_event(
            event_type="USER_LOGGED_IN",
            user_id=user.id,
            details={
                "email": user.email,
                "role": user.role.value
            }
        )
        return LoginResponse(
            token=token,
            token_type="Bearer",
            expires_at=expires_at,
            user=authenticated_user
        )
    def validate_token(self, token: str) -> AuthenticatedUser:

        auth_token = self.token_repository.find_by_token(token)

        if auth_token is None:
            raise InvalidTokenException()

        if auth_token.expires_at <= datetime.now(timezone.utc):
            self.token_repository.delete(token)
            raise InvalidTokenException()

        user = self.user_repository.find_by_id(auth_token.user_id)

        if user is None or not user.is_active:
            self.token_repository.delete(token)
            raise InvalidTokenException()

        return AuthenticatedUser(
           user_id=user.id,
           name=user.name,
           email=user.email,
           role=user.role,
           customer_id=user.customer_id,
           agent_id=user.agent_id
        )
    def logout(self, token: str) -> None:

        authenticated_user = self.validate_token(token)

        self.token_repository.delete(token)

        self.publish_audit_event(
            event_type="USER_LOGGED_OUT",
            user_id=authenticated_user.user_id,
            details={
                "email": authenticated_user.email,
                "role": authenticated_user.role.value
            }
        )

    def deactivate_user(self, user_id: str) -> User | None:

        user = self.user_repository.deactivate(user_id)

        if user is None:
            return None

        self.token_repository.delete_all_by_user_id(user_id)

        return user   