def test_login_page_loads(client):
    r = client.get("/login")
    assert r.status_code == 200

def test_user_can_login(client):
    r = client.post("/login", data={"username": "alice", "password": "Password12345!"}, follow_redirects=True)
    assert r.status_code == 200

def test_assets_requires_login(client):
    r = client.get("/assets", follow_redirects=False)
    assert r.status_code in (302, 401)
