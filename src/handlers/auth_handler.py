
from utils.json_utils import JSONUtils
from exceptions.invalid_registration_exception import InvalidRegistrationException
from exceptions.invalid_token_exception import InvalidTokenException


class AuthHandler:

    def __init__(self, authentication_service):
        self.authentication_service = authentication_service

    @staticmethod
    def get_request_data(request):
        data = JSONUtils.parse_request_body(request["body"])

        if not isinstance(data, dict):
            raise InvalidRegistrationException(
                "Request body must be a JSON object"
            )

        return data

    @staticmethod
    def get_bearer_token(request):
        authorization = request["headers"].get("Authorization")

        if not authorization:
            raise InvalidTokenException()

        parts = authorization.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise InvalidTokenException()

        return parts[1]

    @staticmethod
    def serialize_user(user):
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "customerId": user.customer_id,
            "agentId": user.agent_id
        }
    @staticmethod
    def serialize_authenticated_user(user):
        return {
        "id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "customerId": user.customer_id,
        "agentId": user.agent_id
    }
    def register(self, request):
        data = self.get_request_data(request)

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not all(isinstance(value, str) for value in (name, email, password)):
            raise InvalidRegistrationException(
                "Name, email and password must be strings"
            )

        user = self.authentication_service.register(
            name,
            email,
            password
        )

        response_data = self.serialize_user(user)

        return 201, response_data
    
    def login(self, request):
        data = self.get_request_data(request)

        email = data.get("email")
        password = data.get("password")

        if not isinstance(email, str) or not isinstance(password, str):
            raise InvalidRegistrationException(
                "Email and password must be strings"
            )

        login_response = self.authentication_service.login(
            email,
            password
        )

        response_data = {
            "token": login_response.token,
            "tokenType": login_response.token_type,
            "expiresAt": login_response.expires_at.isoformat(),
            "user": self.serialize_authenticated_user(
                login_response.user
            )
        }

        return 200, response_data
    
    def get_current_user(self, request):
        token = self.get_bearer_token(request)

        authenticated_user = self.authentication_service.validate_token(
            token
        )

        response_data = self.serialize_authenticated_user(
             authenticated_user
       )
        return 200, response_data
    
    def logout(self, request):
        token = self.get_bearer_token(request)

        self.authentication_service.logout(token)

        return 204, None
