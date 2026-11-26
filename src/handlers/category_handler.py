from handlers.auth_handler import AuthHandler
from mappers.category_mapper import CategoryMapper
from utils.json_utils import JSONUtils
from exceptions.invalid_category_data_exception import InvalidCategoryDataException


class CategoryHandler:

    def __init__(self, authentication_service, category_service):
        self.authentication_service = authentication_service
        self.category_service = category_service

    def _authenticate(self, request):
        token = AuthHandler.get_bearer_token(request)
        return self.authentication_service.validate_token(token)

    @staticmethod
    def _body(request):
        data = JSONUtils.parse_request_body(request["body"])
        if not isinstance(data, dict):
            raise InvalidCategoryDataException(
                "Request body must be a JSON object"
            )
        return data

    def create(self, request):
        actor = self._authenticate(request)
        create_request = CategoryMapper.from_create_dict(self._body(request))
        category = self.category_service.create(actor, create_request)
        return 201, CategoryMapper.to_response(category).to_dict()

    def get_all(self, request):
        actor = self._authenticate(request)
        categories = self.category_service.get_all(actor)
        return 200, [
            CategoryMapper.to_response(c).to_dict() for c in categories
        ]

    def get_by_id(self, request):
        actor = self._authenticate(request)
        category = self.category_service.get_by_id(
            actor, request["path_params"]["categoryId"]
        )
        return 200, CategoryMapper.to_response(category).to_dict()

    def update(self, request):
        actor = self._authenticate(request)
        update_request = CategoryMapper.from_update_dict(self._body(request))
        category = self.category_service.update(
            actor, request["path_params"]["categoryId"], update_request
        )
        return 200, CategoryMapper.to_response(category).to_dict()

    def update_status(self, request):
        actor = self._authenticate(request)
        data = self._body(request)
        category = self.category_service.set_status(
            actor, request["path_params"]["categoryId"], data.get("active")
        )
        return 200, CategoryMapper.to_response(category).to_dict()