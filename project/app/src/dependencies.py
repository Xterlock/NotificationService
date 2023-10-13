from typing import Annotated
from fastapi import Depends

from src.services.client import ClientServices
from src.services.mailing import MailingServices
from src.services.message import MessageServices


def get_client_service() -> ClientServices:
    return ClientServices()


def get_mailing_service() -> MailingServices:
    return MailingServices()


def get_message_service() -> MessageServices():
    return MessageServices()


ClientService = Annotated[ClientServices, Depends(get_client_service)]
MailingService = Annotated[MailingServices, Depends(get_mailing_service)]
MessageService = Annotated[MessageServices, Depends(get_message_service)]
