# !/usr/bin/python3
# type: ignore

# ** info: python imports
from datetime import datetime

# ** info: typing imports
from typing import Self
from typing import Any

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: users entity
from src.modules.collect_request.adapters.database_providers_entities.collect_request_entity import (
    CollectRequest,
)

# ** info: artifacts imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider
from src.sidecards.artifacts.uuid_provider import UuidProvider
from src.sidecards.artifacts.env_provider import EnvProvider

# ** info: session managers imports
from src.sidecards.database_managers.mysql_manager import MySQLManager

__all__: list[str] = ["CollectRequestProvider"]


class CollectRequestProvider:
    def __init__(self: Self) -> None:
        self._env_provider: EnvProvider = EnvProvider()
        self._uuid_provider: UuidProvider = UuidProvider()
        self._datetime_provider: DatetimeProvider = DatetimeProvider()
        self._session_manager: MySQLManager = MySQLManager(
            password=self._env_provider.database_password,
            database=self._env_provider.database_name,
            username=self._env_provider.database_user,
            host=self._env_provider.database_host,
            port=self._env_provider.database_port,
            drivername=r"mysql+pymysql",
            query={"charset": "utf8"},
        )

    def search_collect_request_by_id(self: Self, uuid: str) -> CollectRequest:
        session: Session = self._session_manager.obtain_session()
        query: Any = select(CollectRequest).where(CollectRequest.uuid == uuid)
        search_collect_request_by_id_result: CollectRequest = session.exec(statement=query).first()
        return search_collect_request_by_id_result

    def store_collect_request(self: Self, collect_date: str, production_center_id: int) -> CollectRequest:
        session: Session = self._session_manager.obtain_session()
        uuid: str = self._uuid_provider.get_str_uuid()
        date_time: datetime = self._datetime_provider.get_current_time()
        new_collect_request: CollectRequest = CollectRequest(
            uuid=uuid,
            collect_date=collect_date,
            process_status=9,
            production_center_id=production_center_id,
            create=date_time,
            update=date_time,
        )
        session.add(new_collect_request)
        session.commit()
        session.refresh(new_collect_request)
        return new_collect_request

    def find_collects_requests_by_state(self: Self, process_status: int) -> list[CollectRequest]:
        session: Session = self._session_manager.obtain_session()
        query: Any = select(CollectRequest).where(CollectRequest.process_status == process_status)
        find_collect_request_by_state_result: list[CollectRequest] = session.exec(statement=query).all()
        return find_collect_request_by_state_result

    def modify_collect_request_by_id(self: Self, uuid: str, process_status: int) -> CollectRequest:
        session: Session = self._session_manager.obtain_session()
        query: Any = select(CollectRequest).where(CollectRequest.uuid == uuid)
        CollectRequest_data: CollectRequest = session.exec(statement=query).first()
        if CollectRequest_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collect Request not found")
        CollectRequest_data.update = self._datetime_provider.get_current_time()
        CollectRequest_data.process_status = process_status
        session.add(CollectRequest_data)
        session.commit()
        session.refresh(CollectRequest_data)
        return CollectRequest_data
