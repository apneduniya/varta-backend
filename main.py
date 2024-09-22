from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app import news
import os


app = FastAPI(
#    docs_url=None, # Disable docs (Swagger UI)
#    redoc_url=None, # Disable redoc
    title="Varta API",
    description="API for Varta",
    version="1.0.0",
)

# Set the allowed origins, methods, headers, and other CORS options
# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router, prefix="/news", tags=["news"])


# Create an instance of DBConnection
# db_connection = DBConnection(MONGO_CONNECTION_URL, DATABASE_NAME)


@app.on_event("startup")
async def startup_event():
    # db_connection.connect()
    print("\nS E R V E R   S T A R T I N G . . . . . . . . . .\n")


@app.on_event("shutdown")
async def shutdown_event():
    # db_connection.disconnect()
    print("\nS E R V E R   S H U T D O W N . . . . . . . . . .\n")

