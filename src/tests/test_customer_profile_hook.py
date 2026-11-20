from app_container import AppContainer


app = AppContainer()

created_profile = type(
    "CustomerProfile",
    (),
    {"id": "CUST-001"}
)()

app.authentication_service.customer_profile_creator = (
    lambda user: created_profile
)

user = app.authentication_service.register(
    "Test User",
    "test.hook@example.com",
    "Password123"
)

print(
    "SUCCESS TEST:",
    user.customer_id == "CUST-001",
    app.user_repository.find_by_id(user.id) is not None
)


def failing_profile_creator(user):
    raise RuntimeError("Profile creation failed")


app.authentication_service.customer_profile_creator = (
    failing_profile_creator
)

try:
    app.authentication_service.register(
        "Fail User",
        "test.fail@example.com",
        "Password123"
    )
except RuntimeError:
    rollback_success = (
        app.user_repository.find_by_email(
            "test.fail@example.com"
        ) is None
    )

    print("ROLLBACK TEST:", rollback_success)