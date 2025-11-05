from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional

class PositionBase(BaseModel):
    title: str

class PositionCreate(PositionBase):
    pass

class Position(PositionBase):
    id: int
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    department_id: Optional[int]
    position_id: Optional[int]

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    position: Optional[Position]
    class Config:
        from_attributes = True


class DepartmentBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    children: List["Department"] = []
    users: List[User] = []
    class Config:
        from_attributes = True
