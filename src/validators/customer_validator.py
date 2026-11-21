import re

from exceptions.invalid_customer_data_exception import InvalidCustomerDataException


class CustomerValidator:

    NAME_MAX = 100
    ADDRESS_MAX = 255
    PHONE_PATTERN = re.compile(r"^\+?\d{10,15}$")

    @classmethod
    def validate_update(cls, request):
        """Validate an UpdateCustomerRequest; return normalized (name, phone, address)."""
        name = cls.validate_name(request.name)
        phone = cls.validate_phone(request.phone)
        address = cls.validate_address(request.address)
        return name, phone, address

    @classmethod
    def validate_name(cls, name):
        if not isinstance(name, str) or not name.strip():
            raise InvalidCustomerDataException("Name is required")
        name = name.strip()
        if len(name) > cls.NAME_MAX:
            raise InvalidCustomerDataException(
                f"Name must be at most {cls.NAME_MAX} characters"
            )
        return name

    @classmethod
    def validate_phone(cls, phone):
        if phone is None:
            return None
        if not isinstance(phone, str):
            raise InvalidCustomerDataException("Phone must be a string")
        phone = phone.replace(" ", "")
        if phone == "":
            return None
        if not cls.PHONE_PATTERN.match(phone):
            raise InvalidCustomerDataException(
                "Phone must be an optional + followed by 10 to 15 digits"
            )
        return phone

    @classmethod
    def validate_address(cls, address):
        if address is None:
            return None
        if not isinstance(address, str):
            raise InvalidCustomerDataException("Address must be a string")
        address = address.strip()
        if address == "":
            return None
        if len(address) > cls.ADDRESS_MAX:
            raise InvalidCustomerDataException(
                f"Address must be at most {cls.ADDRESS_MAX} characters"
            )
        return address
