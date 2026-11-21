from abc import ABC, abstractmethod

from models.customer import Customer


class CustomerRepository(ABC):

    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def find_by_id(self, customer_id: str) -> Customer | None:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> Customer | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Customer]:
        pass

    @abstractmethod
    def update(self, customer: Customer) -> Customer | None:
        pass

    @abstractmethod
    def deactivate(self, customer_id: str) -> Customer | None:
        pass
