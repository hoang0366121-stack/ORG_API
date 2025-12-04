from fastapi import FastAPI
from database import Base, engine
from routers import department, user, position

# Tạo database nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Organization Management API",
    description="""
Hệ thống API quản lý sơ đồ tổ chức gồm **Phòng ban**, **Chức danh**, và **Nhân viên**.

### 🧱 Module:
- `/departments` – Quản lý phòng ban & sơ đồ tổ chức (tree)
- `/users` – Quản lý người dùng (thêm, sửa, xóa, xem)
- `/positions` – Quản lý chức danh (vị trí công việc)

### 🌳 API nổi bật:
- `GET /departments/tree` – Lấy sơ đồ tổ chức dạng cây (tree)
    """,
    version="1.0.0",
    contact={
        "name": "Hiep Hoang",
        "url": "https://pro.io.vn",
        "email": "admin@pro.io.vn",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Ẩn models bên phải
        "displayRequestDuration": True,  # Hiển thị thời gian xử lý API
        "docExpansion": "none",          # Ẩn các API theo nhóm
        "filter": True                   # Cho phép lọc API
    },
)

# Gắn các router
app.include_router(department.router)
app.include_router(user.router)
app.include_router(position.router)

# ✅ Cho phép chạy trực tiếp bằng: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)