from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .config import settings
from .routers import post, user, auth, vote


# Connections
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",  # specific origin
    "http://localhost:8080",  # specific origin
    # Use any of one
    "*"  # for all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
