from handlers.auth_handler import AuthHandler
from mappers.customer_mapper import CustomerMapper
from utils.json_utils import JSONUtils
from exceptions.invalid_customer_data_exception import InvalidCustomerDataException


class CustomerHandler:

    def __init__(self, authentication_service, customer_service):
        self.authentication_service = authentication_service
        self.customer_service = customer_service

    def _authenticate(self, request):
        token = AuthHandler.get_bearer_token(request)
        return self.authentication_service.validate_token(token)

    @staticmethod
    def _body(request):
        data = JSONUtils.parse_request_body(request["body"])
        if not isinstance(data, dict):
            raise InvalidCustomerDataException(
                "Request body must be a JSON object"
            )
        return data

    def get_all(self, request):
        actor = self._authenticate(request)
        customers = self.customer_service.get_all(actor)
        return 200, [
            CustomerMapper.to_response(c).to_dict() for c in customers
        ]

    def get_by_id(self, request):
        actor = self._authenticate(request)
        customer = self.customer_service.get_by_id(
            actor, request["path_params"]["customerId"]
        )
        return 200, CustomerMapper.to_response(customer).to_dict()

    def update(self, request):
        actor = self._authenticate(request)
        update_request = CustomerMapper.from_update_dict(self._body(request))
        customer = self.customer_service.update(
            actor, request["path_params"]["customerId"], update_request
        )
        return 200, CustomerMapper.to_response(customer).to_dict()

    def update_status(self, request):
        actor = self._authenticate(request)
        data = self._body(request)
        customer = self.customer_service.set_status(
            actor, request["path_params"]["customerId"], data.get("active")
        )
        return 200, CustomerMapper.to_response(customer).to_dict()
