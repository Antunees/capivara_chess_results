from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from app.crud.broker.base import BrokerBase
from app.utils import dev_logs

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
CrudBroker = TypeVar("CrudBroker", bound=BrokerBase)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, CrudBroker]):
    def __init__(self, model: Type[ModelType], crudBroker: Type[CrudBroker]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.crudBroker = crudBroker(Type[ModelType], self.model.__tablename__)

    def create(self, dbSession: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        dbSession.add(db_obj)
        dbSession.commit()
        dbSession.refresh(db_obj)
        self.crudBroker.set(obj_in=db_obj)
        return db_obj

    def update(
        self,
        dbSession: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = obj_in.model_dump(mode="json", exclude_unset=True)
        db_obj.sqlmodel_update(obj_data)

        dbSession.add(db_obj)
        dbSession.commit()
        dbSession.refresh(db_obj)
        self.crudBroker.set(obj_in=db_obj)

        return db_obj

    def get_multi(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            dev_logs("CRUDBase get e")
            dev_logs(e)
            return None

    def delete(self, db: Session, *, db_obj: ModelType) -> None:
        db.delete(db_obj)
        db.commit()
        self.crudBroker.delete(id=db_obj.id)
