from tests.conftest import login

def test_non_admin_cannot_access_admin(client):
    login(client, "alice", "Password12345!")
    r = client.get("/admin/", follow_redirects=False)
    assert r.status_code in (302, 403)

def test_admin_can_access_admin(client):
    login(client, "admin", "Password12345!")
    r = client.get("/admin/", follow_redirects=False)
    assert r.status_code == 200
