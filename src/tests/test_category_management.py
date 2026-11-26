from app_container import AppContainer
from handlers.category_handler import CategoryHandler
from exceptions.application_exception import ApplicationException

app = AppContainer()
auth = app.authentication_service
handler = CategoryHandler(auth, app.category_service)


def req(token, body=None, category_id=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return {
        "headers": headers,
        "body": body,
        "path_params": {"categoryId": category_id},
    }


def status_of(fn, *args):
    try:
        return fn(*args)[0]
    except ApplicationException as e:
        return e.status_code


def check(label, ok):
    print(f"{label}: {'PASS' if ok else 'FAIL'}")


auth.register("Alice", "alice@example.com", "Password123")
cust = auth.login("alice@example.com", "Password123").token
admin = auth.login("admin@cms.local", "Admin@12345").token

# Seed data
s, cats = handler.get_all(req(admin))
names = {c["name"] for c in cats}
check("6 seeded categories", len(cats) == 6)
check("seed names correct", names == {
    "Technical Support", "Billing", "Delivery",
    "Account Issues", "Product Quality", "Other"})
check("all seeded active", all(c["active"] for c in cats))

# Create
s, created = handler.create(req(admin, b'{"name":"  Refunds  ","description":" Money back "}'))
cid = created["id"]
check("create -> 201", s == 201)
check("name/description trimmed", created["name"] == "Refunds" and created["description"] == "Money back")
check("new category active", created["active"] is True)
check("customer create -> 403", status_of(handler.create, req(cust, b'{"name":"X"}')) == 403)
check("no token create -> 401", status_of(handler.create, req(None, b'{"name":"X"}')) == 401)
check("empty name -> 400", status_of(handler.create, req(admin, b'{"name":"   "}')) == 400)
check("missing name -> 400", status_of(handler.create, req(admin, b'{}')) == 400)
check("name > 100 -> 400", status_of(handler.create, req(admin, ('{"name":"%s"}' % ("a" * 101)).encode())) == 400)
check("description > 255 -> 400", status_of(handler.create, req(admin, ('{"name":"Z","description":"%s"}' % ("a" * 256)).encode())) == 400)
check("duplicate name (case-insensitive) -> 409", status_of(handler.create, req(admin, b'{"name":"BILLING"}')) == 409)
check("invalid JSON -> 400", status_of(handler.create, req(admin, b'{bad')) == 400)

# Read
check("customer list ok", status_of(handler.get_all, req(cust)) == 200)
check("get by id ok", status_of(handler.get_by_id, req(cust, category_id=cid)) == 200)
check("unknown id 404", status_of(handler.get_by_id, req(admin, category_id="nope")) == 404)

# Update
s, upd = handler.update(req(admin, b'{"name":"Refunds & Returns","description":null}', cid))
check("update ok", s == 200 and upd["name"] == "Refunds & Returns" and upd["description"] is None)
check("update keep own name -> 200", status_of(handler.update, req(admin, b'{"name":"refunds & returns"}', cid)) == 200)
check("update to other's name -> 409", status_of(handler.update, req(admin, b'{"name":"Billing"}', cid)) == 409)
check("customer update -> 403", status_of(handler.update, req(cust, b'{"name":"Hack"}', cid)) == 403)
check("update unknown -> 404", status_of(handler.update, req(admin, b'{"name":"Q"}', "nope")) == 404)

# Status
check("customer patch -> 403", status_of(handler.update_status, req(cust, b'{"active":false}', cid)) == 403)
check("non-bool active -> 400", status_of(handler.update_status, req(admin, b'{"active":"no"}', cid)) == 400)
s, off = handler.update_status(req(admin, b'{"active":false}', cid))
check("deactivate ok", s == 200 and off["active"] is False)
check("deactivate again -> 200 unchanged", status_of(handler.update_status, req(admin, b'{"active":false}', cid)) == 200)

# Visibility of inactive
check("admin sees inactive in list", any(c["id"] == cid for c in handler.get_all(req(admin))[1]))
check("customer list hides inactive", all(c["id"] != cid for c in handler.get_all(req(cust))[1]))
check("customer GET inactive -> 404", status_of(handler.get_by_id, req(cust, category_id=cid)) == 404)
check("admin GET inactive -> 200", status_of(handler.get_by_id, req(admin, category_id=cid)) == 200)

# Service helper for complaint submission
from exceptions.inactive_category_exception import InactiveCategoryException
try:
    app.category_service.get_active_category(cid)
    check("inactive not usable for complaints", False)
except InactiveCategoryException:
    check("inactive not usable for complaints", True)

s, on = handler.update_status(req(admin, b'{"active":true}', cid))
check("reactivate ok", s == 200 and on["active"] is True)

# Audit
types = [e.event_type for e in app.audit_event_repository.find_all()]
check("audit events published",
      "CATEGORY_CREATED" in types and "CATEGORY_UPDATED" in types
      and "CATEGORY_DEACTIVATED" in types and "CATEGORY_ACTIVATED" in types)