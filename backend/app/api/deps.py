# -*- coding: utf-8 -*-
from typing import Generator

from app.database import engine
from app.models import ServiceClient
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKey, APIKeyHeader, APIKeyQuery
from sqlmodel import Session
from starlette.status import HTTP_403_FORBIDDEN


def get_db() -> Generator:
    with Session(engine) as db:
        yield db


api_key_query = APIKeyQuery(name="api_key", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
):
    if api_key_query:
        return api_key_query
    else:
        return api_key_header


def api_auth(
    api_key: APIKey,
    db: Session,
    create: bool = False,
    read: bool = True,
    update: bool = False,
    delete: bool = False,
) -> ServiceClient:
    if api_key is not None:
        api_client = db.query(ServiceClient).filter(ServiceClient.api_key == api_key).first()
        if api_client is not None:
            if (
                (create is False or api_client.can_append)
                and (read is False or api_client.can_read)
                and (update is False or api_client.can_write)
                and (delete is False or api_client.can_delete)
            ):
                return api_client

    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials")
