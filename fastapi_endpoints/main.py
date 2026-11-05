from fastapi import FastAPI 
from api.v1.endpoints.users import router 
from api.v2.endpoints.users import router_v2 
import uvicorn as uv 

# API Version 1
app = FastAPI(title = "Hospital management Api",version="1.0.0")
app.include_router(router,prefix="/api/v1")


# API Version 2
app.include_router(router_v2,prefix="/api/v2")

# Health Check
@app.get("/health")
async def health_check():

    return {
        "status": "success",
        "message": "API is running"
    }

if __name__ == "__main__" : 
    uv.run(app=app)
    