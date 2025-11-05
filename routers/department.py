from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Department
from schemas import Department, DepartmentCreate
from database import get_db

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=Department)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    new_dept = Department(name=dept.name, parent_id=dept.parent_id)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

@router.get("/", response_model=List[Department])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.delete("/{dept_id}")
def delete_department(dept_id: int, db: Session = Depends(get_db)):
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(dept)
    db.commit()
    return {"message": "Deleted successfully"}

# 🔥 API lấy sơ đồ tổ chức dạng TREE
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
    departments = db.query(Department).all()
    return build_tree(departments)
