from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import date


# User
class UserBase(BaseModel):
    name: str
    sex: SexEnum
    start_date : date
    date_of_birth: date
    department_id: Optional[int]
    position_id: Optional[int]

#
class SexEnum(str, Enum):
    Nam = "Nam"
    Nu = "Nu"
#
class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    position: Optional[Position]
    department: Optional[Department]
    class Config:
        from_attributes = True


# Position
class PositionBase(BaseModel):
    title: str

class PositionCreate(PositionBase):
    pass

class Position(PositionBase):
    id: int
    class Config:
        from_attributes = True

# Department
class DepartmentBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    children: List["Department"] = Field(default_factory=list)
    users: List[User] = Field(default_factory=list)

    class Config:
        from_attributes = True

User.model_rebuild()
UserCreate.model_rebuild()
UserBase.model_rebuild()
