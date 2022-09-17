from fastapi import APIRouter
from .models import User

router = APIRouter()

@router.get(
    path="/users/",
    tags=["users"],
    response_model=User
)
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get(
    path="/users/me",
    tags=["users"],
    response_model=User
)
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get(
    path="/users/{username}",
    tags=["user"],
    response_model=User
)
async def read_user(username: str):
    return {"username": username}