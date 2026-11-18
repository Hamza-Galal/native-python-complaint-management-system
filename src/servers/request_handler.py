from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse , parse_qs
from utils.http_utils import HTTPUtils
from utils.json_utils import JSONUtils
from exceptions.global_exception_handler import GlobalExceptionHandler

class RequestHandler(BaseHTTPRequestHandler):
    router = None

    @classmethod
    def create_handler(cls , router):
        class ConfiguredRequestHandler(cls):
            def __init__(self, *args, **kwargs):
                self.router = router

                super().__init__(*args , **kwargs)
        return ConfiguredRequestHandler

    def handle_request(self):
        path = HTTPUtils.get_path(self)
        try:
            method = HTTPUtils.get_method(self)

            body = HTTPUtils.read_request_body(self)

            request = {
                "method": method,
                "path": path,
                "query_params":HTTPUtils.get_query_parameters(self),
                "headers": self.headers,
                "body": body,
                "json": None,
                "path_params": {} 
            }
            status_code , response_data  = self.router.dispatch(
                method,
                path,
                request
            )
            if status_code == 204:
                HTTPUtils.send_empty_response(
                    self,
                    status_code
                )
            else:
                HTTPUtils.send_json_response(
                    self,
                    status_code,
                    response_data
                )
        except Exception as exception:
            status_code , error_data = (
                GlobalExceptionHandler.handle_exception(
                    exception,
                    path
                )
            )
            HTTPUtils.send_error_response(
                self,
                status_code,
                error_data
            )
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_PATCH(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def do_OPTIONS(self):
        HTTPUtils.send_empty_response(
            self,
            204,
        )