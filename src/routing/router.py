import re
from src.exceptions.resource_not_found_exception import ResourceNotFoundException
from src.exceptions.method_not_allowed_exception import MethodNotAllowedException

class Router:
    def __init__(self):
        self.routes = []

    def register(self , method ,path ,handler):
        method = method.upper()
        path_parts = path.strip("/").split("/")
        regex_parts = []

        for part in path_parts:
            if part.startswith("<") and part.endswith(">"):
                parameter_name = part[1:-1]
                regex_parts.append(
                    f"(?P<{parameter_name}>[^/]f)"
                )
            else:
                regex_parts.append(re.escape(part))
        pattern = "^/" + "/".join(regex_parts)+"/?$"

        self.routes.append({
            "method": method,
            "path": path,
            "pattern": re.compile(pattern),
            "handler": handler
        })

    def dispatch (self, method, path, request):
        allowed_methods = []
        matched_route = None

        for route in self.routes:
            match = route["pattern"].match(path)
            if match:
                allowed_methods.append(route["method"])
                if route["method"] == method:
                    matched_route = route
                    request["path_params"] = match.groupdict()
                    break
        if matched_route is None:
            if allowed_methods:
                raise MethodNotAllowedException(
                    f"Method{method} is not allowed for this endpoint."
                )

            raise ResourceNotFoundException(
                f"Endpoint{path} not found."
            )
        return matched_route["handler"](request)
