from app_container import AppContainer
from handlers.customer_handler import CustomerHandler
from mappers.customer_mapper import CustomerMapper
from exceptions.application_exception import ApplicationException
from exceptions.invalid_credentials_exception import InvalidCredentialsException
from exceptions.invalid_token_exception import InvalidTokenException

app = AppContainer()
auth = app.authentication_service
handler = CustomerHandler(auth, app.customer_service)


def req(token, body=None, customer_id=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return {
        "headers": headers,
        "body": body,
        "path_params": {"customerId": customer_id},
    }


def status_of(fn, *args):
    try:
        return fn(*args)[0]
    except ApplicationException as e:
        return e.status_code


def check(label, ok):
    print(f"{label}: {'PASS' if ok else 'FAIL'}")


u1 = auth.register("Alice", "alice@example.com", "Password123")
u2 = auth.register("Bob", "bob@example.com", "Password123")
t1 = auth.login("alice@example.com", "Password123").token
t2 = auth.login("bob@example.com", "Password123").token
admin = auth.login("admin@cms.local", "Admin@12345").token

check("register sets customer_id", u1.customer_id is not None)
c1, c2 = u1.customer_id, u2.customer_id
profile = app.customer_repository.find_by_user_id(u1.id)
check("profile copies name/email, empty phone/address",
      profile.name == "Alice" and profile.email == "alice@example.com"
      and profile.phone is None and profile.address is None)

check("admin lists all", len(handler.get_all(req(admin))[1]) == 2)
check("customer list -> 403", status_of(handler.get_all, req(t1)) == 403)
check("no token -> 401", status_of(handler.get_all, req(None)) == 401)

check("own profile 200", status_of(handler.get_by_id, req(t1, customer_id=c1)) == 200)
check("other profile 403", status_of(handler.get_by_id, req(t1, customer_id=c2)) == 403)
check("admin any profile 200", status_of(handler.get_by_id, req(admin, customer_id=c2)) == 200)
check("unknown id 404", status_of(handler.get_by_id, req(admin, customer_id="nope")) == 404)

s, body = handler.update(req(
    t1,
    b'{"name":" Alice B ","phone":"+1 234 567 8901","address":"1 Main St",'
    b'"email":"hack@x.com","role":"ADMIN","id":"zzz","userId":"zzz"}',
    c1))
check("update ok, extras ignored",
      s == 200 and body["name"] == "Alice B" and body["phone"] == "+12345678901"
      and body["email"] == "alice@example.com" and body["id"] == c1)
check("update other -> 403",
      status_of(handler.update, req(t1, b'{"name":"X"}', c2)) == 403)
check("empty name -> 400",
      status_of(handler.update, req(t1, b'{"name":"  "}', c1)) == 400)
check("bad phone -> 400",
      status_of(handler.update, req(t1, b'{"name":"A","phone":"12ab"}', c1)) == 400)
check("invalid JSON -> 400",
      status_of(handler.update, req(t1, b'{bad', c1)) == 400)

check("customer cannot set status",
      status_of(handler.update_status, req(t1, b'{"active":false}', c1)) == 403)
check("non-bool active -> 400",
      status_of(handler.update_status, req(admin, b'{"active":"no"}', c2)) == 400)
check("deactivate 200",
      status_of(handler.update_status, req(admin, b'{"active":false}', c2)) == 200)
check("deactivate twice 409",
      status_of(handler.update_status, req(admin, b'{"active":false}', c2)) == 409)
check("user inactive + tokens deleted",
      not app.user_repository.find_by_id(u2.id).is_active
      and not app.token_repository.exists(t2))
try:
    auth.login("bob@example.com", "Password123")
    check("deactivated login rejected", False)
except InvalidCredentialsException:
    check("deactivated login rejected", True)
check("reactivate 200",
      status_of(handler.update_status, req(admin, b'{"active":true}', c2)) == 200)
check("reactivate again 200 unchanged",
      status_of(handler.update_status, req(admin, b'{"active":true}', c2)) == 200)
check("login after reactivation", auth.login("bob@example.com", "Password123").token is not None)

types = [e.event_type for e in app.audit_event_repository.find_all()]
check("audit events", all(t in types for t in
      ("CUSTOMER_UPDATED", "CUSTOMER_DEACTIVATED", "CUSTOMER_REACTIVATED")))
check("response has no password data",
      "password" not in str(CustomerMapper.to_response(profile).to_dict()).lower())
