import httpx
import pytest


@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "testuser@packt.com",
        "password": "testpassword",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    test_response = {
        "message": "User successfull registerd."
    }

    response = await default_client.post("/user/signup", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_sign_new_user_again(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "testuser@packt.com",
        "password": "testpassword",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    test_response = {
        'detail': 'User with supplied username exists'
    }

    response = await default_client.post("/user/signup", json=payload, headers=headers)

    assert response.status_code == 409
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testuser@packt.com",
        "password": "testpassword"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = await default_client.post("/user/signin", data=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_sign_user_in_without(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "wronguser@packt.com",
        "password": "testpassword"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    test_response = {"detail": "Users does not exist."}

    response = await default_client.post("/user/signin", data=payload, headers=headers)

    assert response.status_code == 404
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_sign_user_in_wrong_pass(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testuser@packt.com",
        "password": "wrong"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    test_response = {"detail": "Wrong Credentials Passed."}

    response = await default_client.post("/user/signin", data=payload, headers=headers)

    assert response.status_code == 401
    assert response.json() == test_response
