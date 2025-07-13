import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import feedback, reminders
from config import settings

app = FastAPI(title="Patient Feedback and Reminder API", version="1.0.0")

# CORS configuration for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(feedback.router, prefix="/api/v1", tags=["feedback"])
app.include_router(reminders.router, prefix="/api/v1", tags=["reminders"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)