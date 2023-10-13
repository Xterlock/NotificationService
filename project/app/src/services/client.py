from typing import Optional, List

from fastapi import HTTPException
from loguru import logger
from starlette import status

from src.repositories.client import ClientRepository
from src.schemas.client import (
    ClientSchemaAdd,
    ClientSchemaUpdate,
    ClientSchemaResponse,
)
from src.utils.requests import Request


class ClientServices:
    repository = ClientRepository()
    request = Request()
    time_zone_api_endpoint = "https://nums.hanumi.net/api/get_info?phone={0}"

    async def get_client(self, client_id: int) -> ClientSchemaResponse:
        client_model = await self.repository.find_one(id=client_id)
        if not client_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден")
        return client_model.read_to_schema()

    async def find_clients(self, tag: Optional[str], operator_code: Optional[str]) -> List[ClientSchemaResponse] | List:
        filer = {}
        if tag:
            filer["tag"] = tag
        if operator_code:
            filer["operator_code"] = operator_code
        client_models = await self.repository.find_all(**filer)
        return [model.read_to_schema() for model in client_models] if client_models else []

    async def added_client(self, client: ClientSchemaAdd) -> int:
        """Добавления нового клиента в справочник"""
        data = client.model_dump()
        time_zone = await self.__get_timezone(client.phone_number)
        data["operator_code"] = client.phone_number[1:4]
        data["timezone"] = f"UTC+{time_zone}"
        try:
            client_id = await self.repository.add_one(data)
            return client_id
        except Exception as ex:
            logger.error(f"Ошибка при добавление нового клиента: {ex}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    async def update_client_attributes(self, client_id: int, attributes: ClientSchemaUpdate) -> int:
        """
        Обновления данных атрибутов клиента
        :param client_id: идентификатор клиента
        :param attributes: обновляемы значение
        :return: ид клиента
        """
        data = attributes.get_values_dict()
        try:
            _client_id = await self.repository.edit_one(data, id=client_id)
            return _client_id
        except Exception as ex:
            logger.error(f"Ошибка при обновление атрибутов клиента: {ex}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    async def delete_client(self, client_id: int) -> None:
        """
        Удаления клиента
        :param client_id: идентификатор клиента
        """
        try:
            await self.repository.delete_one(id=client_id)
        except Exception as ex:
            logger.error(f"Ошибка при удаления клиента: {ex}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    async def __get_timezone(self, phone: str) -> int:
        url = self.time_zone_api_endpoint.format(phone)
        response = await self.request.execute("GET", url)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            return data["time_zone"]
