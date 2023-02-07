from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event
from typing import List

router = APIRouter(tags=['Events'])

events = []


@router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events


@router.get("/{id}",    response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event Supplied ID Doesn't Exist."
    )


@router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    events.append(body)
    return {
        "message": "Event created Successfully."
    }


@router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {"message": "Event delete Successfully."}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID doesn't Exist."
    )


@router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {"message": "Events deleted successfully."}
