from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional

# Position
class PositionBase(BaseModel):
    title: str

class PositionCreate(PositionBase):
    pass

class Position(PositionBase):
    id: int
    class Config:
        from_attributes = True

# User
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
