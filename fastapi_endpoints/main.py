from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.auth import router_auth
from api.v1.endpoints.users import router 
from api.v2.endpoints.users import router_v2 
from api.v3.endpoints.users import router_v3
from api.v3.endpoints.tasks import router_task
from core.security import validate_security_settings
import uvicorn as uv 


@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_security_settings()
    yield


app = FastAPI(
    title="PMS Task Manager API",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(router,prefix="/api/v1")
app.include_router(router_v2,prefix="/api/v2")
app.include_router(router_v3,prefix="/api/v3")
app.include_router(router_task,prefix="/tasks")
app.include_router(router_auth, prefix="/auth")

# Health Check
@app.get("/health")
async def health_check():
    return {
            "status": "success",
            "message": "API is running",
            "versions": {
                "v1": {
                    "status": "active",
                    "message": "V1 API is running"
                },
                "v2": {
                    "status": "active",
                    "message": "V2 API is running"
                },
                "v3": {
                    "status": "active",
                    "message": "V3 API is running"
                }
            }
        }



if __name__ == "__main__" : 
    uv.run("main:app",host="127.0.0.1", port=8000, reload=True)
    