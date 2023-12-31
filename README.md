# Сервис уведомлений

# Dev

## Стек

API
* FastAPI - 
* Pydantic - 
* SQLAlchemy - ORM
* Asyncpg - асинхронный драйвер для postgres

TaskManager
* Celery 

Database
* Postgres - sql база данных
* Redis - NoSql база данных (кэш)

* Testing
* Httpx
* Pytest async 

CI/CD
* Docker
* Docker compose

## Задача

Необходимо разработать сервис управления рассылками API администрирования и получения статистики.

## Описание

* Необходимо реализовать методы создания новой рассылки, просмотра созданных и получения статистики по выполненным
  рассылкам.
* Реализовать сам сервис отправки уведомлений на внешнее API.

## Основное задание

Спроектировать и разработать сервис, который по заданным правилам запускает рассылку по списку клиентов.

Сущность "рассылка" имеет атрибуты:

* уникальный id рассылки
* дата и время запуска рассылки
* текст сообщения для доставки клиенту
* фильтр свойств клиентов, на которых должна быть произведена рассылка (код мобильного оператора, тег)
* дата и время окончания рассылки: если по каким-то причинам не успели разослать все сообщения - никакие сообщения
  клиентам после этого времени доставляться не должны

Сущность "клиент" имеет атрибуты:

* уникальный id клиента
* номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)
* код мобильного оператора
* тег (произвольная метка)
* часовой пояс

Сущность "сообщение" имеет атрибуты:

* уникальный id сообщения
* дата и время создания (отправки)
* статус отправки
* id рассылки, в рамках которой было отправлено сообщение
* id клиента, которому отправили


Спроектировать и реализовать API для:

* добавления нового клиента в справочник со всеми его атрибутами
* обновления данных атрибутов клиента
* удаления клиента из справочника
* добавления новой рассылки со всеми её атрибутами
* получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по
  статусам
* получения детальной статистики отправленных сообщений по конкретной рассылке
* обновления атрибутов рассылки
* удаления рассылки
* обработки активных рассылок и отправки сообщений клиентам


