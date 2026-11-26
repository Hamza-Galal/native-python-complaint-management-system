import uuid
from datetime import datetime, timezone

from events.audit_event import AuditEvent
from models.complaint_category import ComplaintCategory
from models.user_role import UserRole
from exceptions.forbidden_exception import ForbiddenException
from exceptions.category_not_found_exception import CategoryNotFoundException
from exceptions.duplicate_category_exception import DuplicateCategoryException
from exceptions.inactive_category_exception import InactiveCategoryException
from validators.category_validator import CategoryValidator


class CategoryService:

    def __init__(self, category_repository, audit_event_repository=None):
        self.category_repository = category_repository
        self.audit_event_repository = audit_event_repository

    def _audit(self, event_type, user_id, details):
        if self.audit_event_repository is None:
            return
        self.audit_event_repository.save(AuditEvent(
            event_type=event_type,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            details=details
        ))

    @staticmethod
    def _require_admin(actor):
        if actor.role != UserRole.ADMIN:
            raise ForbiddenException()

    def _ensure_name_available(self, name, own_id=None):
        existing = self.category_repository.find_by_name(name)
        if existing is not None and existing.id != own_id:
            raise DuplicateCategoryException()

    def create(self, actor, request) -> ComplaintCategory:
        self._require_admin(actor)
        name, description = CategoryValidator.validate_request(request)
        self._ensure_name_available(name)

        category = ComplaintCategory(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
        )
        self.category_repository.save(category)

        self._audit("CATEGORY_CREATED", actor.user_id, {
            "categoryId": category.id,
            "name": category.name
        })
        return category

    def get_all(self, actor) -> list[ComplaintCategory]:
        categories = self.category_repository.find_all()
        if actor.role == UserRole.ADMIN:
            return categories
        return [c for c in categories if c.is_active]

    def get_by_id(self, actor, category_id) -> ComplaintCategory:
        category = self.category_repository.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundException()
        # Non-admins must not even know an inactive category exists
        if not category.is_active and actor.role != UserRole.ADMIN:
            raise CategoryNotFoundException()
        return category

    def update(self, actor, category_id, request) -> ComplaintCategory:
        self._require_admin(actor)
        category = self.category_repository.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundException()

        name, description = CategoryValidator.validate_request(request)
        self._ensure_name_available(name, own_id=category.id)

        category.name = name
        category.description = description
        category.updated_at = datetime.now(timezone.utc)
        self.category_repository.update(category)

        self._audit("CATEGORY_UPDATED", actor.user_id, {
            "categoryId": category.id
        })
        return category

    def set_status(self, actor, category_id, active) -> ComplaintCategory:
        self._require_admin(actor)
        CategoryValidator.validate_active(active)

        category = self.category_repository.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundException()

        # Same state again: 200, nothing changes
        if category.is_active == active:
            return category

        if active:
            category.is_active = True
            category.updated_at = datetime.now(timezone.utc)
            self.category_repository.update(category)
            event_type = "CATEGORY_ACTIVATED"
        else:
            self.category_repository.deactivate(category.id)
            event_type = "CATEGORY_DEACTIVATED"

        self._audit(event_type, actor.user_id, {"categoryId": category.id})
        return category

    def get_active_category(self, category_id) -> ComplaintCategory:
        """Used by complaint submission (Assignment 5)."""
        category = self.category_repository.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundException()
        if not category.is_active:
            raise InactiveCategoryException()
        return category