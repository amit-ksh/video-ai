# GET /videos


def test_get_all_videos(client):
    response = client.get("/videos")
    assert response.status_code == 200
    assert b"videos" in response.data


# GET /video/<int:video_id>


def test_get_video(client):
    response = client.get("/video/1")
    assert response.status_code == 200
    assert b"id" in response.data


# GET /videos/<status>


def test_get_videos_by_status(client):
    status = "active"
    response = client.get(f"/videos/{status}")
    assert response.status_code == 200
    assert status in response.json


# CREATE /video


def test_create_video_without_auth_token(client):
    response = client.post(
        "/video",
        json={"title": "test", "description": "test"},
    )
    assert response.status_code == 401


def test_create_video(client):
    response = client.post(
        "/video",
        headers={"Authorization": client.token},
        json={"title": "test", "description": "test"},
    )
    assert response.status_code == 200
    assert b"id" in response.data
    assert "active" == response.json["status"]


def test_create_video_with_status_value(client):
    response = client.post(
        "/video",
        headers={"Authorization": client.token},
        json={"title": "test", "description": "test", "status": "archived"},
    )
    assert response.status_code == 200
    assert b"id" in response.data
    assert "archived" == response.json["status"]


def test_create_video_without_title_and_description(client):
    response = client.post("/video", headers={"Authorization": client.token}, json={})
    assert response.status_code == 400
    assert b"Title and description are required" in response.data


# UPDATE /video/<int:video_id>


def test_update_video(client):
    latest_video = client.get("/videos").json["videos"][-1]
    new_status = "archived" if latest_video['status'] == "active" else "active"
    response = client.put(
        f"/video/{latest_video["id"]}",
        headers={"Authorization": client.token},
        json={"title": latest_video['title'], "description": latest_video["description"], "status": new_status},
    )
    assert response.status_code == 200
    assert latest_video["id"] == response.json["id"]
    assert new_status == response.json["status"]


def test_update_video_without_payload(client):
    latest_video = client.get("/videos").json["videos"][-1]
    response = client.put(
        f"/video/{latest_video['id']}",
        headers={"Authorization": client.token},
        json={},
    )
    assert response.status_code == 400
    assert b"Title and description are required" in response.data


# DELETE /video/<int:video_id>


def test_delete_video(client):
    latest_video = client.get("/videos").json["videos"][-1]
    response = client.delete(
        f"/video/{latest_video["id"]}",
        headers={"Authorization": client.token},
    )

    assert response.status_code == 200
    assert latest_video["id"] == response.json["id"]


def test_delete_video_without_id(client):
    response = client.delete(
        "/video/",
        headers={"Authorization": client.token},
    )
    assert response.status_code == 404


def test_delete_video_with_invalid_id(client):
    response = client.delete(
        "/video/1000",
        headers={"Authorization": client.token},
    )
    assert response.status_code == 404
    assert b"Video not found" in response.data
