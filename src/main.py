from routing.router import Router
from servers.http_server_manager import HTTPServerManager
from handlers.health_handler import HealthHandler
from exceptions.internal_server_exception import InternalServerException

def main():
    router = Router()

    router.register(
        "GET",
        "/api/health",
        HealthHandler.handle
    )
    server_manager = HTTPServerManager(
        router,
        host = "localhost",
        port = 8080
    )
    try:
        server_manager.start()

    except KeyboardInterrupt:
        print("\n Shutting Down HTTP server")

    except InternalServerException as exception:
        print(f"Server Startup failed: {exception.message}")

    finally:
        server_manager.stop()

if __name__ == "__main__":
    main()