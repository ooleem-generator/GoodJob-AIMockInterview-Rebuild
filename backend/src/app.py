# app.py

import os
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from pydantic import BaseModel

# class ChatRequest(BaseModel):
#     prompt: str # We expect a JSON body like {"prompt": "..."}

# class ChatResponse(BaseModel):
#     response: str # We'll return a JSON body like {"response": "..."}

app = FastAPI()

# CORS setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "GoodJob AI mock Interview API"}
