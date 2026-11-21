from datetime import datetime, timezone

from models.customer import Customer
from repositories.customer_repository import CustomerRepository


class InMemoryCustomerRepository(CustomerRepository):

    def __init__(self):
        self.customers = {}

    def save(self, customer: Customer) -> Customer:
        self.customers[customer.id] = customer
        return customer

    def find_by_id(self, customer_id: str) -> Customer | None:
        return self.customers.get(customer_id)

    def find_by_user_id(self, user_id: str) -> Customer | None:
        for customer in self.customers.values():
            if customer.user_id == user_id:
                return customer
        return None

    def find_all(self) -> list[Customer]:
        return list(self.customers.values())

    def update(self, customer: Customer) -> Customer | None:
        if customer.id not in self.customers:
            return None
        self.customers[customer.id] = customer
        return customer

    def deactivate(self, customer_id: str) -> Customer | None:
        customer = self.find_by_id(customer_id)
        if customer is None:
            return None
        customer.is_active = False
        customer.updated_at = datetime.now(timezone.utc)
        return self.update(customer)
