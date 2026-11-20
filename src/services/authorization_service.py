from models.user_role import UserRole
from exceptions.forbidden_exception import ForbiddenException


class AuthorizationService:

    @staticmethod
    def require_roles(user, *roles):
        if user.role not in roles:
            raise ForbiddenException(
                "You do not have permission to perform this action"
            )

    @staticmethod
    def can_view_complaint(user, complaint):
        if user.role == UserRole.ADMIN:
            return True

        if user.role == UserRole.CUSTOMER:
            return (
                user.customer_id is not None
                and user.customer_id == complaint.customerId
            )

        if user.role == UserRole.AGENT:
            return (
                user.agent_id is not None
                and user.agent_id == complaint.assignedAgentId
            )

        return False

    @staticmethod
    def can_manage_complaint(user, complaint):
        if user.role == UserRole.ADMIN:
            return True

        if user.role == UserRole.AGENT:
            return (
                user.agent_id is not None
                and user.agent_id == complaint.assignedAgentId
            )

        return False