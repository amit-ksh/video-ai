# Register tests


def test_user_register(client):
    response = client.post(
        "/user/register", json={"email": "amit@mail.com", "password": "password"}
    )
    assert response.status_code == 200
    assert b"email" in response.data
    assert b"id" in response.data


def test_user_register_without_email_and_password(client):
    response = client.post("/user/register", json={})
    assert response.status_code == 400
    assert b"Email and password are required" in response.data


def test_user_register_without_password(client):
    response = client.post("/user/register", json={"email": "some@mail"})
    assert response.status_code == 400
    assert b"Email and password are required" in response.data


def test_user_register_without_email(client):
    response = client.post("/user/register", json={"password": "password"})
    assert response.status_code == 400
    assert b"Email and password are required" in response.data


def test_existing_user_register(client):
    response = client.post(
        "/user/register", json={"email": "test@mail.com", "password": "password"}
    )
    assert response.status_code == 400
    assert b"User already exists" in response.data


# login tests


def test_user_login(client):
    response = client.post(
        "/user/login", json={"email": "test@mail.com", "password": "password"}
    )
    assert response.status_code == 200
    assert b"access_token" in response.data


def test_user_login_without_credentials(client):
    response = client.post("/user/login", json={})
    assert response.status_code == 400
    assert b"Email and password are required" in response.data


def test_invalid_user_login(client):
    response = client.post(
        "/user/login", json={"email": "noindb@mail.com", "password": "password"}
    )
    assert response.status_code == 400
    assert b"Invalid credentials" in response.data
