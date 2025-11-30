if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

from fastapi import FastAPI
from app.routes.sign_route import router as sign_router

app = FastAPI(title="ASL Video API (Images->Video)")

app.include_router(sign_router)

@app.get("/")
def home():
    return {"message": "ASL Video API - use /api/video?letter=A"}