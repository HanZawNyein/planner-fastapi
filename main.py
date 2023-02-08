import uvicorn
from database.connection import Settings
from routes.events import router as events_router
from routes.users import router as user_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# origins
origins = ["*"]


app = FastAPI()
settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router, prefix="/user")
app.include_router(events_router, prefix="/event")


@app.on_event("startup")
async def init_db():
    await settings.initialize_database(default_database='test')

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True)
