from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from utils import save_to_file

router = APIRouter(prefix="/departments", tags=["Departments"])

# 🟢 Thêm phòng ban
@router.post("/", response_model=schemas.Department)
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    new_dept = models.Department(name=dept.name, parent_id=dept.parent_id)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    print(f"✅ Created Department: {new_dept.name}")
    # 🔥 Lưu tất cả department ra file JSON
    departments = db.query(models.Department).all()
    data = [{"id": d.id, "name": d.name, "parent_id": d.parent_id} for d in departments]
    save_to_file("departments_backup.json", data)
    
    return new_dept

# 🟢 Lấy tất cả phòng ban
@router.get("/", response_model=List[schemas.Department])
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

# 🟢 Sửa phòng ban
@router.put("/{dept_id}", response_model=schemas.Department)
def update_department(dept_id: int, dept_data: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    dept.name = dept_data.name
    dept.parent_id = dept_data.parent_id
    db.commit()
    db.refresh(dept)
    print(f"✏️ Updated Department ID {dept_id}")
    return dept

# 🟢 Xóa phòng ban
@router.delete("/{dept_id}")
def delete_department(dept_id: int, db: Session = Depends(get_db)):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(dept)
    db.commit()
    print(f"🗑️ Deleted Department ID {dept_id}")
    return {"message": "Deleted successfully"}

# 🌳 Lấy sơ đồ tổ chức dạng cây
def build_tree(departments, parent_id=None):
    tree = []
    for dept in [d for d in departments if d.parent_id == parent_id]:
        node = {
            "id": dept.id,
            "name": dept.name,
            "users": [{"id": u.id, "name": u.name} for u in dept.users],
            "children": build_tree(departments, dept.id)
        }
        tree.append(node)
    return tree

@router.get("/tree")
def get_department_tree(db: Session = Depends(get_db)):
    departments = db.query(models.Department).all()
    return build_tree(departments)
