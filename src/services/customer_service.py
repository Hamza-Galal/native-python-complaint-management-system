import uuid
from datetime import datetime, timezone

from events.audit_event import AuditEvent
from models.customer import Customer
from models.user_role import UserRole
from exceptions.forbidden_exception import ForbiddenException
from exceptions.customer_not_found_exception import CustomerNotFoundException
from exceptions.customer_access_denied_exception import CustomerAccessDeniedException
from exceptions.customer_already_inactive_exception import CustomerAlreadyInactiveException
from exceptions.invalid_customer_data_exception import InvalidCustomerDataException
from validators.customer_validator import CustomerValidator


class CustomerService:

    def __init__(
        self,
        customer_repository,
        user_repository,
        token_repository,
        audit_event_repository=None
    ):
        self.customer_repository = customer_repository
        self.user_repository = user_repository
        self.token_repository = token_repository
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

    def create_profile_for_user(self, user) -> Customer:
        customer = Customer(
            id=str(uuid.uuid4()),
            user_id=user.id,
            name=user.name,
            email=user.email,
        )
        return self.customer_repository.save(customer)

    def _get_accessible(self, actor, customer_id) -> Customer:
        customer = self.customer_repository.find_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundException()

        if actor.role == UserRole.ADMIN:
            return customer
        if actor.role == UserRole.CUSTOMER and actor.customer_id == customer.id:
            return customer
        raise CustomerAccessDeniedException()

    def get_all(self, actor) -> list[Customer]:
        if actor.role != UserRole.ADMIN:
            raise ForbiddenException()
        return self.customer_repository.find_all()

    def get_by_id(self, actor, customer_id) -> Customer:
        return self._get_accessible(actor, customer_id)

    def update(self, actor, customer_id, request) -> Customer:
        customer = self._get_accessible(actor, customer_id)
        name, phone, address = CustomerValidator.validate_update(request)

        customer.name = name
        customer.phone = phone
        customer.address = address
        customer.updated_at = datetime.now(timezone.utc)
        self.customer_repository.update(customer)

        self._audit("CUSTOMER_UPDATED", actor.user_id, {
            "customerId": customer.id
        })
        return customer

    def set_status(self, actor, customer_id, active) -> Customer:
        if actor.role != UserRole.ADMIN:
            raise ForbiddenException()

        if not isinstance(active, bool):
            raise InvalidCustomerDataException(
                "Field 'active' must be true or false"
            )

        customer = self.customer_repository.find_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundException()

        if active == customer.is_active:
            if not active:
                raise CustomerAlreadyInactiveException()
            return customer

        user = self.user_repository.find_by_id(customer.user_id)

        if active:
            customer.is_active = True
            customer.updated_at = datetime.now(timezone.utc)
            self.customer_repository.update(customer)
            if user is not None:
                user.is_active = True
                self.user_repository.update(user)
            event_type = "CUSTOMER_REACTIVATED"
        else:
            self.customer_repository.deactivate(customer.id)
            if user is not None:
                self.user_repository.deactivate(user.id)
                self.token_repository.delete_all_by_user_id(user.id)
            event_type = "CUSTOMER_DEACTIVATED"

        self._audit(event_type, actor.user_id, {"customerId": customer.id})
        return customer
