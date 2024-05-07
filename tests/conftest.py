import pytest
from app.app import create_app, db


@pytest.fixture(scope="session", autouse=True)
def app():
    app = create_app()

    yield app


@pytest.fixture(scope="session")
def client(app):
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables in the test database
            # Insert test data into the test database
            client.post(
                "/user/register",
                json={"email": "test@mail.com", "password": "password"},
            )
            response = client.post(
                "/user/login", json={"email": "test@mail.com", "password": "password"}
            )

            # Check if the login was successful
            assert response.status_code == 200
            access_token = f"Bearer {response.json['access_token']}"

            # Save the access token in the client object
            client.token = access_token

            # Create 5 videos
            for i in range(5):
                client.post(
                    "/video",
                    headers={"Authorization": access_token},
                    json={
                        "title": f"video {i+1}",
                        "description": f"description {i+1}",
                        "status": "active" if i % 2 == 0 else "archived",
                    },
                )

        yield client
        # Drop all tables after the test
        db.drop_all()
