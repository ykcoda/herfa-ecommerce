from fastapi import APIRouter
from app.api.routes.users import users

master = APIRouter()  # create a master router
master.include_router(users)  # added users router
