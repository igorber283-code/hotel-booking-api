async def test_register_and_login_user(ac):

    r1 = await ac.post(
        "/authx/register",
        json={"email": "test@example.com", "password": "password123"},
    )

    assert r1.status_code == 201, r1.text

    r2 = await ac.post(
        "/authx/login",
        json={"email": "test@example.com", "password": "password123"},
    )

    assert r2.status_code == 200, r2.text
    assert "access_token" in r2.json()
