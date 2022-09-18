from fastapi import APIRouter
from fastapi import status, Path, Body
from fastapi import Response, HTTPException

from .models import Write

from app.works.send_action import SendDBAction

def execute_db_action(key, method, *args, **kwargs):
    sender = SendDBAction()
    return sender.run(key, method, *args, **kwargs)

router = APIRouter(
    prefix="/db",
    tags = ["Database Actions"],
    responses={404: {"description": "Not found"}}
)


@router.get(
    path="/{key}",
    status_code=status.HTTP_200_OK,
)
def get(key: str = Path(...)):
    response = execute_db_action(key, 'get')
    return response.json()

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
def insert(obj: Write = Body(...)):
    obj = obj.dict()
    execute_db_action(method="post", **obj)
    return { "result": "OK" }

@router.put(
    path="/{key}",
    status_code=status.HTTP_200_OK,
)
def update(obj: Write = Body(...)):
    obj = obj.dict()
    execute_db_action(method="put", **obj)
    return { "result": "OK" }

@router.delete(
    path="/{key}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(key: str = Path(...)):
    execute_db_action(key, 'delete')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
