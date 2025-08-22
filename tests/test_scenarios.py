
from authscope.loaders.openapi_loader import make_scenarios, guess_path_vars
from authscope.core.safe_eval import safe_eval

def test_guess_vars():
    assert guess_path_vars("/users/{id}") == ["id"]
    assert guess_path_vars("/orgs/{orgId}/orders/{orderId}") == ["orgId", "orderId"]

def test_make_scenarios_self_other():
    eps = [{"method":"GET","path":"/users/{id}"}]
    scs = make_scenarios(eps)
    methods = [s.method for s in scs]
    paths = [s.path for s in scs]
    params = [s.path_params for s in scs]
    assert len(scs) == 2
    assert {"id":"SELF"} in params
    assert {"id":"OTHER"} in params

def test_safe_eval_basic():
    expr = "subject.claims.sub == path.id or 'admin' in subject.claims.roles"
    subject = type("S", (), {"claims": {"sub":"u1", "roles":["user"]}})()
    assert safe_eval(expr, {"subject":subject, "path":{"id":"u1"}}) is True
    assert safe_eval(expr, {"subject":subject, "path":{"id":"u2"}}) is False
