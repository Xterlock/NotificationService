from typing import Optional, List

from fastapi import APIRouter
from starlette import status

from src.dependencies import ClientService
from ..schemas.client import (
    ClientSchemaAdd,
    ClientSchemaUpdate,
    ClientSchemaResponse,
)
from ..schemas.response import IdResponse, ResponseStatus

router = APIRouter(prefix="/client", tags=["Client"])


@router.get("", response_model=List[ClientSchemaResponse])
async def find_clients(service: ClientService, tag: Optional[str] = None, operator_code: Optional[str] = None):
    clients = await service.find_clients(tag, operator_code)
    return clients


@router.post("", response_model=IdResponse, status_code=status.HTTP_201_CREATED)
async def added_client(client: ClientSchemaAdd, service: ClientService):
    """Добавления нового клиента в справочник со всеми его атрибутами"""
    client_id = await service.added_client(client)
    return IdResponse(id=client_id)


@router.delete("", response_model=ResponseStatus, status_code=status.HTTP_202_ACCEPTED)
async def delete_client(client_id: int, service: ClientService):
    await service.delete_client(client_id)
    return ResponseStatus(status="OK")


@router.patch("/{client_id}", response_model=IdResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_client_attributes(client_id: int, attributes: ClientSchemaUpdate, service: ClientService):
    """Обновления данных атрибутов клиента"""
    client_id = await service.update_client_attributes(client_id, attributes)
    return IdResponse(id=client_id)


@router.get("/{client_id}", response_model=ClientSchemaResponse)
async def get_client(client_id: int, service: ClientService):
    """Получить клиента по id"""
    client = await service.get_client(client_id)
    return client
