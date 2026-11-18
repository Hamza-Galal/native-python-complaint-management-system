import json
from src.exceptions.invalid_json_exception import InvalidJsonException
from src.exceptions.internal_server_exception import InternalServerException

class JsonUtils:
    @staticmethod
    def to_json(data):
        try:
            return json.dumps(
                data,
                ensure_ascii= False,
                allow_nan= False
            )
        except (TypeError , ValueError) as exception:
            raise InternalServerException("Unable to serialize response data.") from exception

    @staticmethod
    def from_json(json_data):
        if not json_data or not json_data.strip():
            return None

        try:
            return json.loads(json_data)

        except(json.JSONDecodeError , ValueError) as exception:
            raise InvalidJsonException() from exception

    @staticmethod
    def parse_request_body(body):
        if not body:
            return None

        try:
            if isinstance(body , bytes):
                body = body.decode("utf-8")

            return JsonUtils.from_json(body)

        except UnicodeDecodeError as exception:
            raise InvalidJsonException("Request Body must use UTF-8 encoding.") from exception