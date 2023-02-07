from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.users import router as user_router
from routes.events import router as events_router
from database.connection import conn

import uvicorn

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(events_router, prefix="/event")


@app.on_event("startup")
def on_startup():
    conn()


@app.get("/")
def home():
    return RedirectResponse(url="/event/")


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True)
