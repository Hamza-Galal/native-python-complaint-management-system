import os
import uuid

from repositories.in_memory_user_repository import InMemoryUserRepository
from repositories.in_memory_token_repository import InMemoryTokenRepository

from services.authentication_service import AuthenticationService
from services.authorization_service import AuthorizationService
from services.customer_service import CustomerService
from services.category_service import CategoryService
from repositories.in_memory_category_repository import InMemoryCategoryRepository
from models.complaint_category import ComplaintCategory
from repositories.in_memory_customer_repository import InMemoryCustomerRepository

from models.user import User
from models.user_role import UserRole

from repositories.in_memory_audit_event_repository import InMemoryAuditEventRepository

class AppContainer:

    ADMIN_EMAIL = "admin@cms.local"
    ADMIN_NAME = "System Administrator"
    DEFAULT_ADMIN_PASSWORD = "Admin@12345"

    DEFAULT_CATEGORIES = [
        "Technical Support",
        "Billing",
        "Delivery",
        "Account Issues",
        "Product Quality",
        "Other",
    ]

    def __init__(self):

        self.user_repository = InMemoryUserRepository()
        self.token_repository = InMemoryTokenRepository()
        self.audit_event_repository = InMemoryAuditEventRepository()

        self.customer_repository = InMemoryCustomerRepository()

        self.customer_service = CustomerService(
            self.customer_repository,
            self.user_repository,
            self.token_repository,
            self.audit_event_repository
        )

        # Registration hook provided by Assignment 3
        self.customer_profile_creator = (
            self.customer_service.create_profile_for_user
        )

        self.authentication_service = AuthenticationService(
            self.user_repository,
            self.token_repository,
            self.customer_profile_creator,
            self.audit_event_repository
        )
        self.authorization_service = AuthorizationService()

        # Category management (Assignment 4)
        self.category_repository = InMemoryCategoryRepository()
        self.category_service = CategoryService(
            self.category_repository,
            self.audit_event_repository
        )

        self.seed_admin_user()
        self.seed_categories()

    def seed_categories(self):
        for name in self.DEFAULT_CATEGORIES:
            if self.category_repository.find_by_name(name) is None:
                self.category_repository.save(ComplaintCategory(
                    id=str(uuid.uuid4()),
                    name=name
                ))

    def seed_admin_user(self):

        existing_admin = self.user_repository.find_by_email(
            self.ADMIN_EMAIL
        )

        if existing_admin is not None:
            if existing_admin.role != UserRole.ADMIN:
                raise ValueError(
                    "The admin email is already used by a non-admin user."
                )
            return existing_admin

        admin_password = os.getenv(
            "CMS_ADMIN_PASSWORD",
            self.DEFAULT_ADMIN_PASSWORD
        )

        if len(admin_password) < 8:
            raise ValueError(
                "CMS_ADMIN_PASSWORD must be at least 8 characters."
            )

        password_hash, salt = self.authentication_service.hash_password(
            admin_password
        )

        admin_user = User(
            id=str(uuid.uuid4()),
            name=self.ADMIN_NAME,
            email=self.ADMIN_EMAIL,
            password_hash=password_hash,
            salt=salt,
            role=UserRole.ADMIN
        )

        return self.user_repository.save(admin_user)