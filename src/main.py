
from routing.router import Router
from servers.http_server_manager import HTTPServerManager

from handlers.health_handler import HealthHandler
from handlers.auth_handler import AuthHandler

from app_container import AppContainer

from exceptions.internal_server_exception import InternalServerException


def main():
    router = Router()

    # Initialize application dependencies
    app_container = AppContainer()

    # Initialize authentication handler
    auth_handler = AuthHandler(
        app_container.authentication_service
    )

    # Public endpoints
    router.register(
        "GET",
        "/api/health",
        HealthHandler.handle
    )

    router.register(
        "POST",
        "/api/auth/register",
        auth_handler.register
    )

    router.register(
        "POST",
        "/api/auth/login",
        auth_handler.login
    )

    # Protected endpoints
    router.register(
        "GET",
        "/api/auth/me",
        auth_handler.get_current_user
    )

    router.register(
        "POST",
        "/api/auth/logout",
        auth_handler.logout
    )

    server_manager = HTTPServerManager(
        router,
        host="localhost",
        port=8090
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
