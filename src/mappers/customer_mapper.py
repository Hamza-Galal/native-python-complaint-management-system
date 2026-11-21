from dtos.customer_response import CustomerResponse
from dtos.update_customer_request import UpdateCustomerRequest


class CustomerMapper:

    @staticmethod
    def to_response(customer) -> CustomerResponse:
        return CustomerResponse(
            id=customer.id,
            user_id=customer.user_id,
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            address=customer.address,
            active=customer.is_active,
            created_at=customer.created_at.isoformat(),
            updated_at=customer.updated_at.isoformat(),
        )

    @staticmethod
    def from_update_dict(data: dict) -> UpdateCustomerRequest:
        # Only name, phone and address are accepted; everything else is ignored.
        return UpdateCustomerRequest(
            name=data.get("name"),
            phone=data.get("phone"),
            address=data.get("address"),
        )
