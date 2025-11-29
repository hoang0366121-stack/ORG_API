from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Position as PositionModel
from schemas import Position as PositionSchema, PositionCreate
from database import get_db

router = APIRouter(prefix="/positions", tags=["Positions"])

@router.post("/", response_model=PositionSchema)
def create_position(pos: PositionCreate, db: Session = Depends(get_db)):
    new_pos = PositionModel(title=pos.title)
    db.add(new_pos)
    db.commit()
    db.refresh(new_pos)
    return new_pos

@router.get("/", response_model=List[PositionSchema])
def get_positions(db: Session = Depends(get_db)):
    return db.query(PositionModel).all()

@router.delete("/{pos_id}")
def delete_position(pos_id: int, db: Session = Depends(get_db)):
    pos = db.query(PositionModel).filter(PositionModel.id == pos_id).first()
    if not pos:
        raise HTTPException(status_code=404, detail="Position not found")
    db.delete(pos)
    db.commit()
    return {"message": "Deleted successfully"}
