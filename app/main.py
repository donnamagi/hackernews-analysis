from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import hackernews

app = FastAPI()

origins = [
  "http://localhost:3000",
  "https://hackernews.news",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(hackernews.app)

@app.get("/")
async def root():
  return {"message": "Hello World"}
