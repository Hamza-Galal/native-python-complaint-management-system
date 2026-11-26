from exceptions.invalid_category_data_exception import InvalidCategoryDataException


class CategoryValidator:

    NAME_MAX = 100
    DESCRIPTION_MAX = 255

    @classmethod
    def validate_request(cls, request):
        """Validate a create/update request; return normalized (name, description)."""
        name = cls.validate_name(request.name)
        description = cls.validate_description(request.description)
        return name, description

    @classmethod
    def validate_name(cls, name):
        if not isinstance(name, str) or not name.strip():
            raise InvalidCategoryDataException("Category name is required")
        name = name.strip()
        if len(name) > cls.NAME_MAX:
            raise InvalidCategoryDataException(
                f"Category name must be at most {cls.NAME_MAX} characters"
            )
        return name

    @classmethod
    def validate_description(cls, description):
        if description is None:
            return None
        if not isinstance(description, str):
            raise InvalidCategoryDataException("Description must be a string")
        description = description.strip()
        if description == "":
            return None
        if len(description) > cls.DESCRIPTION_MAX:
            raise InvalidCategoryDataException(
                f"Description must be at most {cls.DESCRIPTION_MAX} characters"
            )
        return description

    @staticmethod
    def validate_active(active):
        if not isinstance(active, bool):
            raise InvalidCategoryDataException(
                "Field 'active' must be true or false"
            )
        return active