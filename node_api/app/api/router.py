from fastapi import APIRouter
from fastapi import status, Path, Body
from fastapi import Response, HTTPException

from .models import Read, Write
from app.db import Database
from app.db import NoSuchKeyError
from app.db import KeyAlreadyExistsError


router = APIRouter(
    prefix="/db",
    tags = ["Database Actions"],
    responses={404: {"description": "Not found"}}
)

def execute_db_action(action, *args, **kwargs):
    try:
        db = Database()
        task = getattr(db, action)
        return task(*args, **kwargs)
    except NoSuchKeyError as nske:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(nske)
        )
    except KeyAlreadyExistsError as kaee:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(kaee)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
def get_all():
    return {
        "keys": execute_db_action("get_keys")
    }

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
def insert(obj: Write = Body(...)):
    obj = obj.dict()
    execute_db_action("save", **obj)
    return { "result": "OK" }

@router.get(
    path="/{key}",
    status_code=status.HTTP_200_OK,
)
def get(key: str = Path(...)):
    return {
        "value": execute_db_action("get", key=key)
    }

@router.put(
    path="/{key}",
    status_code=status.HTTP_200_OK,
)
def update(obj: Write = Body(...)):
    obj = obj.dict()
    execute_db_action("update", **obj)
    return { "result": "OK" }

@router.delete(
    path="/{key}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(key: str = Path(...)):
    execute_db_action("delete", key=key)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
