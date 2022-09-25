from fastapi import APIRouter
from fastapi import status, Path, Body
from fastapi import Response, HTTPException

from .models import Read, Replication, Write
from app.db import Database, ReplicationDatabase
from app.db import NoSuchKeyError
from app.db import KeyAlreadyExistsError
from app.restore import main as restore_process


router = APIRouter(
    prefix="/db",
    tags = ["Database Actions"],
    responses={404: {"description": "Not found"}}
)

def execute_db_action(action, db_type, *args, **kwargs):
    try:

        db = db_type()
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
        "keys": execute_db_action("get_keys", Database)
    }

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
def insert(obj: Write = Body(...)):
    obj = obj.dict()
    execute_db_action("save", Database, **obj)
    return { "result": "OK" }

@router.get(
    path="/{key}",
    status_code=status.HTTP_200_OK,
)
def get(key: str = Path(...)):
    return {
        "value": execute_db_action("get", Database, key=key)
    }

@router.put(
    path="/{key}",
    status_code=status.HTTP_200_OK,
    deprecated=True
)
def update(obj: Write = Body(...)):
    obj = obj.dict()
    execute_db_action("update", Database, **obj)
    return { "result": "OK" }

@router.delete(
    path="/{key}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(key: str = Path(...), rep: Replication = Body(...)):
    execute_db_action("delete", Database, key = key, **(rep.dict()))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ===================REPLICATION=====================================

@router.get(
    path="/replication/",
    status_code=status.HTTP_200_OK,
)
def rep_get_all():
    return {
        "keys": execute_db_action("get_keys", ReplicationDatabase)
    }

@router.post(
    path="/replication",
    status_code=status.HTTP_201_CREATED,
)
def rep_insert(obj: Write = Body(...)):
    obj = obj.dict()
    execute_db_action("save", ReplicationDatabase, **obj)
    return { "result": "OK" }

@router.get(
    path="/replication/{key}",
    status_code=status.HTTP_200_OK,
)
def rep_get(key: str = Path(...)):
    return {
        "value": execute_db_action("get", ReplicationDatabase, key=key)
    }

@router.put(
    path="/replication/{key}",
    status_code=status.HTTP_200_OK,
    deprecated=True
)
def rep_update(obj: Write = Body(...)):
    obj = obj.dict()
    execute_db_action("update", ReplicationDatabase, **obj)
    return { "result": "OK" }

@router.delete(
    path="/replication/{key}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def rep_delete(key: str = Path(...), rep: Replication = Body(...)):
    execute_db_action("delete", ReplicationDatabase, key = key, **(rep.dict()))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    path="/replication/restore/",
    status_code=status.HTTP_200_OK
)
def restore(rep: Replication = Body(...)):
    restore_process(rep.node_url)