
from types import SimpleNamespace

from models.user_role import UserRole
from services.authorization_service import AuthorizationService
from exceptions.forbidden_exception import ForbiddenException


service = AuthorizationService()

complaint = SimpleNamespace(
    customerId="C1",
    assignedAgentId="A1"
)

admin = SimpleNamespace(
    role=UserRole.ADMIN,
    customer_id=None,
    agent_id=None
)

customer_owner = SimpleNamespace(
    role=UserRole.CUSTOMER,
    customer_id="C1",
    agent_id=None
)

customer_other = SimpleNamespace(
    role=UserRole.CUSTOMER,
    customer_id="C2",
    agent_id=None
)

agent_assigned = SimpleNamespace(
    role=UserRole.AGENT,
    customer_id=None,
    agent_id="A1"
)

agent_other = SimpleNamespace(
    role=UserRole.AGENT,
    customer_id=None,
    agent_id="A2"
)

print("Admin Can View:", service.can_view_complaint(admin, complaint))
print("Admin Can Manage:", service.can_manage_complaint(admin, complaint))

print("Customer Owner Can View:", service.can_view_complaint(customer_owner, complaint))
print("Customer Other Can View:", service.can_view_complaint(customer_other, complaint))
print("Customer Can Manage:", service.can_manage_complaint(customer_owner, complaint))

print("Assigned Agent Can View:", service.can_view_complaint(agent_assigned, complaint))
print("Assigned Agent Can Manage:", service.can_manage_complaint(agent_assigned, complaint))
print("Other Agent Can View:", service.can_view_complaint(agent_other, complaint))
print("Other Agent Can Manage:", service.can_manage_complaint(agent_other, complaint))

try:
    service.require_roles(customer_owner, UserRole.ADMIN)
    print("Role Check: Failed")
except ForbiddenException:
    print("Role Check: Passed")
