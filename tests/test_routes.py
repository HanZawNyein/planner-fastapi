import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event
from tests.test_fixture import mock_event, access_token


@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = await default_client.get("/event/", headers=headers)
    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
    payload = {
        "title": "FastAPI Book Launch",
        "image": "https://linktomyimage.com/image.png",
        "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
        "tags": [
            "python",
            "fastapi",
            "book",
            "launch"
        ],
        "location": "Google Meet",
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {
        "message": "Event created Successfully."
    }
    response = await default_client.post("/event/new", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_events_count(default_client: httpx.AsyncClient, access_token: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = await default_client.get("/event/", headers=headers)
    events = response.json()
    assert response.status_code == 200
    assert len(events) == 2


@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    test_payload = {
        "title": "Updated FastAPI event"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.put(url, json=test_payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == test_payload["title"]


@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    test_response = {
        "message": "Event deleted successfully."
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/event/{mock_event.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_event_again(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    url = f"/event/{str(mock_event.id)}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    test_response = {
        'detail': "Event Supplied ID Doesn't Exist."
    }

    response = await default_client.get(url, headers=headers)
    assert response.status_code == 404
    assert response.json() == test_response
