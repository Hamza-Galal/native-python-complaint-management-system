
from events.audit_event import AuditEvent
from repositories.audit_event_repository import AuditEventRepository


class InMemoryAuditEventRepository(AuditEventRepository):

    def __init__(self):
        self.events = []

    def save(self, event: AuditEvent) -> AuditEvent:
        self.events.append(event)
        return event

    def find_all(self) -> list[AuditEvent]:
        return list(self.events)

    def find_by_user_id(self, user_id: str) -> list[AuditEvent]:
        return [
            event
            for event in self.events
            if event.user_id == user_id
        ]
