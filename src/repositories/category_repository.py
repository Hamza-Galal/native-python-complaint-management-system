from abc import ABC, abstractmethod

from models.complaint_category import ComplaintCategory


class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category: ComplaintCategory) -> ComplaintCategory:
        pass

    @abstractmethod
    def find_by_id(self, category_id: str) -> ComplaintCategory | None:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> ComplaintCategory | None:
        pass

    @abstractmethod
    def find_all(self) -> list[ComplaintCategory]:
        pass

    @abstractmethod
    def update(self, category: ComplaintCategory) -> ComplaintCategory | None:
        pass

    @abstractmethod
    def deactivate(self, category_id: str) -> ComplaintCategory | None:
        pass