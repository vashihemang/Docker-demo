from fastapi import FastAPI 
from api.v1.endpoints.users import router  
import uvicorn as uv 

app = FastAPI(title = "Hospital management Api")
app.include_router(router)

# Health Check
@app.get("/health")
async def health_check():

    return {
        "status": "success",
        "message": "API is running"
    }


if __name__ == "__main__" : 
    uv.run(app=app)
    