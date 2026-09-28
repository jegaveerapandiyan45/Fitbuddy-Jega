from fastapi import FastAPI
from .routes import router

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator", version="1.0.0")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
