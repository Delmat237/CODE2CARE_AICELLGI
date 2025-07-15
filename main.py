import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import feedback, reminders, auth
from utils.auth import get_current_user


#app = FastAPI(title="Patient Feedback and Reminder API", version="1.0.0",dependencies=[Depends(get_current_user)])

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
app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"],    dependencies=[Depends(get_current_user)])
app.include_router(reminders.router, prefix="/api/reminder", tags=["reminders"],    dependencies=[Depends(get_current_user)])
app.include_router(auth.router,prefix="/api/auth", tags=["auth"])

if __name__ == "__main__":
    from config.settings import settings
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)