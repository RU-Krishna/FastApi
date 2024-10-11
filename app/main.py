from fastapi import FastAPI, Depends

from .routers import guests, users, auth
from .db_conn.connection import *

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

get_connection()



app.include_router(users.router)
app.include_router(guests.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return "Hello, Welcome to our application"





