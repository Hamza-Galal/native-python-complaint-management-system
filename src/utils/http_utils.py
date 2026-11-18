from urllib.parse import urlparse , parse_qs
from src.utils.json_utils import JsonUtils
from src.exceptions.validation_exception import ValidationException


class HttpUtils:
    @staticmethod
    def read_request_body(handler):
        content_length = handler.headers.get("Content-Length")

        if content_length is None:
            return b""

        try:
            length = int(content_length)

        except ValueError:
            raise ValidationException("Invalid Content-Length header.")

        if length < 0 :
            raise ValidationException("Invalid Content-Length header.")
        return handler.rfile.read(length)

    @staticmethod
    def send_json_response(handler, status_code ,data):
        json_data = JsonUtils.to_json(data)
        response_body = json_data.encode("utf-8")
        handler.send_response(status_code)
        HttpUtils.set_response_headers(handler)

        handler.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
            )
        handler.send_header(
            "Content-length",
            str(len(response_body))
        )
        handler.end_headers()

        handler.wfile.write(response_body)

    @staticmethod
    def  send_empty_response(handler ,status_code):
        handler.send_response(status_code)
        HttpUtils.set_response_headers(handler)
        handler.send_header("Content-Length","0")
        handler.end_headers()

    @staticmethod
    def set_response_headers(handler):
        handler.send_header("Access-Control-Allow-Origin","*")
        handler.send_header(
            "Access-Control-Allow-Methods",
             "GET , POST , PUT , PATCH , DELETE , OPTIONS"
             )
        handler.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization"
        )

    @staticmethod
    def get_method(handler):
        return handler.command

    @staticmethod
    def get_path(handler):
        return urlparse(handler.path).path

    @staticmethod
    def get_header(handler , header_name):
        return handler.headers.get(header_name)

    @staticmethod
    def get_query_parameters(handler):
        query = urlparse(handler.path).query

        parsed_query = parse_qs(
            query,
            keep_blank_values= True
        )
        return{
            key: values[0] if len(values) == 1 else values
            for key, values in parsed_query.items()
        }