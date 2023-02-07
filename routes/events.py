from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event, EventUpdate
from typing import List

from beanie import PydanticObjectId
from database.connection import Database

event_database = Database(Event)

router = APIRouter(tags=['Events'])


@router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@router.get("/{id}",response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event Supplied ID Doesn't Exist."
        )
    return event


@router.post("/new")
async def create_event(body: Event) -> dict:
    await event_database.save(body)
    return {
        "message": "Event created Successfully."
    }


@router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event


@router.delete("/{id}")
async def delete_event(id: int) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID doesn't Exist."
        )
    return {"message": "Event delete Successfully."}


@router.delete("/")
async def delete_all_events() -> dict:
    event = await event_database.delete
    return {"message": "Events deleted successfully."}
