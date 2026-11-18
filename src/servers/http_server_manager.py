from http.server import ThreadingHTTPServer
from servers.request_handler import RequestHandler
from exceptions.internal_server_exception import InternalServerException

class HTTPServerManager:
    def __init__(self,router,host="localhost",port = 8080):
        self.router = router
        self.host = host
        self.port = port

        self.server = None
        self.is_running = False
        self.has_started = False
    def start(self):
        if self.has_started:
            raise RuntimeError(
                "Server has already started."
            )

        try:
            handler_class = RequestHandler.create_handler(
                self.router
            )
            self.server = ThreadingHTTPServer(
                (self.host , self.port),
                handler_class
            )

            self.server.daemon_threads = True

            self.has_started = True
            self.is_running = True
            print(
                f"HTTP Server Started On http://{self.host}:{self.port}"
            )    
            self.server.serve_forever()
        except OSError as exception:
            raise InternalServerException(
                "Unable to start HTTP server"
            ) from exception
        finally:
            self.is_running = False
    def stop(self):
        if self.server is None:
            return
        
        if self.is_running:
            self.server.shutdown()

        self.server.server_close()

        self.is_running = False

        print("HTTP Server stopped Successfully")
