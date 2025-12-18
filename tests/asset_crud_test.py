from tests.conftest import login

def test_admin_can_add_asset(client):
    login(client, "admin", "Password12345!")
    r = client.post("/admin/add", data={
        "name": "HP Laptop",
        "asset_tag": "Test",
        "asset_type": "Laptop",
        "location": "Hardman Square",
    }, follow_redirects=True)
    assert r.status_code == 200
