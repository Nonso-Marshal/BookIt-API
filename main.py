from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routes.auth import auth_router
from routes.user import user_router
from routes.booking import booking_router
from routes.review import review_router
from routes.service import service_router
from database import get_db
from schemas.auth import UserLogin, Token
from routes.auth import login
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the BookIt API"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@app.post("/auth/login", response_model=Token, include_in_schema=False)
def custom_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_data = UserLogin(email=form_data.username, password=form_data.password)
    return login(user_data, db)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(service_router)
app.include_router(booking_router)
app.include_router(review_router)

logger.info("Application startup complete")