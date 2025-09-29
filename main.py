from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from routes.auth import auth_router
from routes.user import user_router
from routes.booking import booking_router
from routes.review import review_router
from routes.service import service_router
from database import get_db
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
@app.head("/")
async def root():
    return {"message": "Welcome to the BookIt API"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(service_router)
app.include_router(booking_router)
app.include_router(review_router)

logger.info("Application startup complete")