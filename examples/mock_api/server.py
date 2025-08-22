
# Mock vulnerable API (for demo only)
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Mock API with BOLA")

USERS = {
    "u1": {"id": "u1", "name": "Alice", "email": "alice@example.com"},
    "u2": {"id": "u2", "name": "Bob", "email": "bob@example.com"},
}

def user_from_token(auth: str | None) -> str | None:
    if not auth:
        return None
    token = auth.split(" ", 1)[1] if " " in auth else auth
    if token == "alice-token":
        return "u1"
    if token == "bob-token":
        return "u2"
    return None

@app.get("/users/{id}")
def get_user(id: str, authorization: str | None = Header(default=None, convert_underscores=False)):
    caller = user_from_token(authorization)
    if caller is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # VULN: no check that id == caller
    if id in USERS:
        return USERS[id]
    raise HTTPException(status_code=404, detail="Not found")
