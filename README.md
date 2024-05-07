# Video API

## Development Setup

1. Clone the repo
    `git clone https://github.com/amit-ksh/video-api.git`

1. `cd video-api`

1. Copy `.env.example` file, rename to `.env`

1. Build and run the server: `docker compose up`

1. Run database migrations

    ```bash
    docker compose exec api flask db upgrade
    -OR-
    scripts\migrate.sh
    ```

1. Server Running At: `http://localhost:5000/` (open `http://localhost:5000/videos`)

## How to run tests

```bash
docker compose exec api python -m pytest
-OR-
scripts\test.sh
```

## API

### User

1. User Registration

    **Request**

    ```bash
    curl --location 'http://127.0.0.1:5000/user/register' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "email": "john@mail.com",
        "password": "password"
    }'
    ```

    **Response**

    ```bash
    {
        "created_at": "2024-05-06T12:25:08.840470",
        "email": "john@mail.com",
        "id": 1
    }
    ```

1. User Login

    **Request**

    ```bash
    curl --location 'http://127.0.0.1:5000/user/login' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "email": "john@mail.com",
        "password": "password"
    }'
    ```

    **Response**

    ```bash
    {
        "access_token": "<TOKEN>"
    }
    ```

### Video

1. Get All Videos

    **Request**

    ```bash
    curl --location 'http://127.0.0.1:5000/videos'
    ```

    **Response**

    ```bash
    {
        "videos": [
            {
                "title": "Video",
                "description": "video description",
                "status": "ACTIVE"
            }
        ]
    }
    ```

1. Get Video by ID

    **Request**

    ```bash
    curl --location 'http://127.0.0.1:5000/video/1'
    ```

    **Response**

    ```bash
    {
        "created_at": "2024-05-06T12:28:43.180936",
        "description": "video description",
        "id": 1,
        "status": "active",
        "title": "Brand new video"
    }
    ```

1. Get Videos By Status

    **Request**

    ```bash
    curl --location 'http://127.0.0.1:5000/videos/archived'
    ```

    **Response**

    ```bash
    {
        "archived": [
            {
                "created_at": "2024-05-06T12:30:39.934096",
                "description": "video description",
                "id": 2,
                "status": "archived",
                "title": "Brand new video"
            }
        ]
    }
    ```

1. Create Video

    **Request**

    ```bash
    curl --location 'http://127.0.0.1:5000/video' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <TOKEN>' \
    --data '{
        "title": "Brand new video",
        "description": "video description"
    }'
    ```

    **Response**

    ```bash
    {
        "created_at": "2024-05-06T12:28:43.180936",
        "description": "video description",
        "id": 1,
        "status": "active",
        "title": "Brand new video"
    }
    ```

1. Get Update Video By ID

    **Request**

    ```bash
    curl --location --request PUT 'http://127.0.0.1:5000/video/1' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <TOKEN>' \
    --data '{
        "title": "Updated Video",
        "description": "updated video description",
        "status": "ARCHIVED"
    }'
    ```

    **Response**

    ```bash
    {
        "title": "Updated Video",
        "description": "updated video description",
        "status": "ARCHIVED"
    }
    ```

1. Delete Video

    **Request**

    ```bash
    curl --location --request DELETE 'http://127.0.0.1:5000/video/3' \
    --header 'Authorization: Bearer <TOKEN>'
    ```

    **Response**

    ```bash
    {
        "title": "Video",
        "description": "video description",
        "status": "ARCHIVED"
    }
    ```
