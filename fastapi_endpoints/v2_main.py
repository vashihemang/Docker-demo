from fastapi import FastAPI 
from api.v2.endpoints.users import router  
import uvicorn as uv 

app = FastAPI(title = "Hospital management Api",version="1.1.0")
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
    