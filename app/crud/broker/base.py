import json
from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel

from app.broker.broker_db import Broker
from app.utils import DTEncoder, dev_logs

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BrokerBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], tablename: str):
        self.model = model
        self.tablename = tablename

    def set(self, *, obj_in: ModelType) -> None:
        as_dict = {c.name: getattr(obj_in, c.name) for c in obj_in.__table__.columns}

        Broker.set(f"{self.tablename}:{obj_in.id}", json.dumps(as_dict, cls=DTEncoder))

    def set_specific_key(self, *, key: str, obj_in: ModelType) -> None:
        as_dict = {c.name: getattr(obj_in, c.name) for c in obj_in.__table__.columns}

        Broker.set(key, json.dumps(as_dict, cls=DTEncoder))

    def get(self, id: int) -> Optional[ModelType]:
        try:
            obj_broker = json.loads(Broker.get(f"{self.tablename}:{id}"))
            return self.model.from_json(obj_broker)
        except Exception as e:
            dev_logs(e)
            dev_logs("BrokerBase get e")
            dev_logs(ModelType)
            dev_logs(id)
            return None

    def get_specific_key(self, key: str) -> Optional[ModelType]:
        try:
            obj_broker = json.loads(Broker.get(key))
            return self.model(**obj_broker)
        except Exception as e:
            dev_logs(e)
            dev_logs("BrokerBase get_specific_key e")
            dev_logs(ModelType)
            dev_logs(id)
            return None

    def get_multi(self) -> List[ModelType]:
        try:
            obj_list = []
            for key in Broker.scan_iter(f"{self.tablename}:*", count=10000):
                try:
                    obj_broker = json.loads(Broker.get(key))
                    obj_list.append(self.model(**obj_broker))
                except Exception as e:
                    dev_logs("BrokerBase get_multi scan_iter e")
                    dev_logs(e)

            return obj_list
        except Exception as e:
            dev_logs("BrokerBase get_multi e")
            dev_logs(e)
            return []

    def delete(self, *, id: str) -> None:
        Broker.delete(f"{self.tablename}:{id}")
        Broker.delete(f"*{self.tablename}:{id}*")
