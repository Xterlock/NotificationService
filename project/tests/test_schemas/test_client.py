import pytest

from src.schemas.client import ClientSchemaAdd


async def test_client_schema_add_positive():
    """
    Позитивный тест на создание схемы
    :return:
    """
    schema = ClientSchemaAdd(
        phone_number="79179999999",
        operator_code="917",
        tag="Test",
        timezone="UTC+5"
    )
    assert schema.phone_number == "79179999999"


async def test_client_schema_add_phone_number_invalid():
    """
    Тест валидация номер телефона
    """
    with pytest.raises(ValueError):
        schema = ClientSchemaAdd(
            phone_number="791799999xx",
            operator_code="917",
            tag="Test",
            timezone="UTC+5"
        )


async def test_client_schema_add_phone_number_max_length():
    """
    Тест на максимальное кол-во символов в номере телефона
    """
    with pytest.raises(ValueError):
        schema = ClientSchemaAdd(
            phone_number="791799999999",
            operator_code="917",
            tag="Test",
            timezone="UTC+5"
        )
