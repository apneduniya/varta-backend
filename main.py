from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import DBConnection
from app import news, auth, users, subscription
import dotenv
import os


dotenv.load_dotenv()
ORIGINS = ["*"]
MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
db_connection = DBConnection(MONGO_CONNECTION_URL, DATABASE_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Up Event
    db_connection.connect()
    print("\nS E R V E R   S T A R T I N G . . . . . . . . . .\n")
    yield

    # Shut Down Event
    db_connection.disconnect()
    print("\nS E R V E R   S H U T D O W N . . . . . . . . . .\n")


app = FastAPI(
    title="Varta API",
    description="API for Varta",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  I N C L U D E   R O U T E R S

app.include_router(news.router, prefix="/news", tags=["news"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(subscription.router, prefix="/subscription", tags=["subscription"])



