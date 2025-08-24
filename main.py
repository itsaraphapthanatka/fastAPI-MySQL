from fastapi import FastAPI, APIRouter, Depends
from fastapi.openapi.utils import get_openapi
from setup.users.auth import verify_token

# Import from setup folder
from setup.users.user import router as user_router
from setup.users.login import router as login_router
from setup.company.company import router as company_router
from setup.project.project import router as project_router

# Import from application folder
from application.po.purchase_order import router as purchase_order_router
# Purchase Requisition
from application.pr.purchase_requisition import router as purchase_requisition_router
from fastapi.middleware.cors import CORSMiddleware
from setup.users.auth import verify_token
import os
from dotenv import load_dotenv

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request


# สร้าง FastAPI app หลัก
app = FastAPI(title="Workflow Management System", version="1.0.0", description="API for Workflow Management System")

load_dotenv()

APP_URL_DEV = os.getenv("APP_URL_DEV")
APP_URL_STAGING = os.getenv("APP_URL_STAGING")
APP_URL_PRODUCTION = os.getenv("APP_URL_PRODUCTION")

# กำหนดค่า OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Workflow Management System",
        version="1.0.0",
        description="API for Workflow Management System",
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        { "url": APP_URL_DEV, "description": "Local server"  },
        { "url": APP_URL_STAGING, "description": "Staging server" },
        { "url": APP_URL_PRODUCTION, "description": "Production server" }
    ]
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# สร้าง router หลัก
main_router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List allowed origins
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)

@main_router.get("/secure-data")
async def secure_data(payload: dict = Depends(verify_token)):
    return {"msg": f"Authorized user", "payload": payload}
# สร้าง API operations
@main_router.get("/")
async def index():
    version = str(app.version) if app.version else "1.0.0"
    return {"Version": version,"message": "Welcome to Workflow Management System"}

@main_router.get("/health") 
async def check_health():
    return {"status": "healthy"}

# เพิ่ม routers เข้ากับ app หลัก
app.include_router(main_router, prefix="/api/v1", tags=["Index"])

# Setup routers
app.include_router(login_router, prefix="/api/v1/login", tags=["Login"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users Management"],dependencies=[Depends(verify_token)])
app.include_router(company_router, prefix="/api/v1/company", tags=["Company Management"],dependencies=[Depends(verify_token)])
app.include_router(project_router, prefix="/api/v1/projects", tags=["Setup Projects"],dependencies=[Depends(verify_token)])

# Application routers
app.include_router(purchase_order_router, prefix="/api/v1/purchase_order", tags=["Purchase Order Management"],dependencies=[Depends(verify_token)])
app.include_router(purchase_requisition_router, prefix="/api/v1/purchase_requisition", tags=["Purchase Requisition Management"],dependencies=[Depends(verify_token)])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body
        },
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
