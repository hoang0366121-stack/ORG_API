from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import User as UserModel
from schemas import User as UserSchema, UserCreate
from database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserModel(
        name=user.name,
        department_id=user.department_id,
        position_id=user.position_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "Deleted successfully"}
