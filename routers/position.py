from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/positions", tags=["Positions"])

@router.get("/", response_model=list[schemas.Position])
def get_positions(db: Session = Depends(get_db)):
    return db.query(models.Position).all()

@router.get("/{position_id}", response_model=schemas.Position)
def get_position(position_id: int, db: Session = Depends(get_db)):
    position = db.query(models.Position).filter(models.Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position

@router.post("/", response_model=schemas.Position)
def create_position(position: schemas.PositionCreate, db: Session = Depends(get_db)):
    new_position = models.Position(**position.dict())
    db.add(new_position)
    db.commit()
    db.refresh(new_position)
    print(f"✅ Created Position: {new_position.title}")
    return new_position

@router.put("/{position_id}", response_model=schemas.Position)
def update_position(position_id: int, updated_position: schemas.PositionCreate, db: Session = Depends(get_db)):
    position = db.query(models.Position).filter(models.Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    for key, value in updated_position.dict().items():
        setattr(position, key, value)
    db.commit()
    db.refresh(position)
    print(f"✏️ Updated Position ID {position_id}")
    return position

@router.delete("/{position_id}")
def delete_position(position_id: int, db: Session = Depends(get_db)):
    position = db.query(models.Position).filter(models.Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    db.delete(position)
    db.commit()
    print(f"🗑️ Deleted Position ID {position_id}")
    return {"message": "Position deleted successfully"}
