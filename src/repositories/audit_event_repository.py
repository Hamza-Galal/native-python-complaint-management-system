
from abc import ABC, abstractmethod

from events.audit_event import AuditEvent


class AuditEventRepository(ABC):

    @abstractmethod
    def save(self, event: AuditEvent) -> AuditEvent:
        pass

    @abstractmethod
    def find_all(self) -> list[AuditEvent]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> list[AuditEvent]:
        pass
