from fastapi import FastAPI, APIRouter

# Import from setup folder
from setup.users.user import router as user_router
from setup.project.project import router as project_router

# Import from application folder
from application.po.purchase_order import router as purchase_order_router
# Purchase Requisition
from application.pr.purchase_requisition import router as purchase_requisition_router

# สร้าง FastAPI app หลัก
app = FastAPI(title="Workflow Management System")

# สร้าง router หลัก
main_router = APIRouter()

# สร้าง API operations
@main_router.get("/")
async def index():
    return {"message": "Welcome to Workflow Management System"}

@main_router.get("/health") 
async def check_health():
    return {"status": "healthy"}

# เพิ่ม routers เข้ากับ app หลัก
app.include_router(main_router, prefix="/api/v1", tags=["Index"])

# Setup routers
app.include_router(user_router, prefix="/api/v1/users", tags=["Users Management"])
app.include_router(project_router, prefix="/api/v1/projects", tags=["Setup Projects"])

# Application routers
app.include_router(purchase_order_router, prefix="/api/v1/purchase_order", tags=["Purchase Order Management"])
app.include_router(purchase_requisition_router, prefix="/api/v1/purchase_requisition", tags=["Purchase Requisition Management"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
