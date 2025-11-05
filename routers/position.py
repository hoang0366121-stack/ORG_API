from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/positions",
    tags=["Positions"]
)

# 🟢 Lấy tất cả chức danh
@router.get("/", response_model=list[schemas.Position])
def get_positions(db: Session = Depends(get_db)):
    return db.query(models.Position).all()

# 🟢 Lấy 1 chức danh theo id
@router.get("/{position_id}", response_model=schemas.Position)
def get_position(position_id: int, db: Session = Depends(get_db)):
    position = db.query(models.Position).filter(models.Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position

# 🟢 Tạo mới chức danh
@router.post("/", response_model=schemas.Position)
def create_position(position: schemas.PositionCreate, db: Session = Depends(get_db)):
    new_position = models.Position(**position.dict())
    db.add(new_position)
    db.commit()
    db.refresh(new_position)
    return new_position

# 🟢 Cập nhật chức danh
@router.put("/{position_id}", response_model=schemas.Position)
def update_position(position_id: int, updated_position: schemas.PositionCreate, db: Session = Depends(get_db)):
    position = db.query(models.Position).filter(models.Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    for key, value in updated_position.dict().items():
        setattr(position, key, value)
    db.commit()
    db.refresh(position)
    return position

# 🟢 Xóa chức danh
@router.delete("/{position_id}")
def delete_position(position_id: int, db: Session = Depends(get_db)):
    position = db.query(models.Position).filter(models.Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    db.delete(position)
    db.commit()
    return {"message": "Position deleted successfully"}
