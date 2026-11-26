from dtos.category_response import CategoryResponse
from dtos.create_category_request import CreateCategoryRequest
from dtos.update_category_request import UpdateCategoryRequest


class CategoryMapper:

    @staticmethod
    def to_response(category) -> CategoryResponse:
        return CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            active=category.is_active,
            created_at=category.created_at.isoformat(),
            updated_at=category.updated_at.isoformat(),
        )

    @staticmethod
    def from_create_dict(data: dict) -> CreateCategoryRequest:
        # Only name and description are accepted; everything else is ignored.
        return CreateCategoryRequest(
            name=data.get("name"),
            description=data.get("description"),
        )

    @staticmethod
    def from_update_dict(data: dict) -> UpdateCategoryRequest:
        return UpdateCategoryRequest(
            name=data.get("name"),
            description=data.get("description"),
        )