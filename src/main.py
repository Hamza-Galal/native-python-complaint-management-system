
from routing.router import Router
from servers.http_server_manager import HTTPServerManager

from handlers.health_handler import HealthHandler
from handlers.auth_handler import AuthHandler
from handlers.customer_handler import CustomerHandler

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

    # Customer endpoints (all protected)
    customer_handler = CustomerHandler(
        app_container.authentication_service,
        app_container.customer_service
    )

    router.register("GET", "/api/customers", customer_handler.get_all)
    router.register(
        "GET", "/api/customers/<customerId>", customer_handler.get_by_id
    )
    router.register(
        "PUT", "/api/customers/<customerId>", customer_handler.update
    )
    router.register(
        "PATCH",
        "/api/customers/<customerId>/status",
        customer_handler.update_status
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
