from fastapi import FastAPI 
from api.v1.endpoints.users import router 
from api.v2.endpoints.users import router_v2 
from api.v3.endpoints.users import router_v3
from api.v3.endpoints.tasks import router_task
import uvicorn as uv 

# API Version 1
app = FastAPI(title = "Hospital management Api",version="1.0.0")
app.include_router(router,prefix="/api/v1")


# API Version 2
app.include_router(router_v2,prefix="/api/v2")

# API Version 3
#  1. User Route : 
app.include_router(router_v3,prefix="/api/v3")
#  2. Task Route :
app.include_router(router_task,prefix="/tasks")

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
    