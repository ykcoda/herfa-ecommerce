from fastapi import APIRouter
from app.api.routes.users import users
from app.api.routes.category import categories


master = APIRouter()  # create a master router
master.include_router(users)  # added users router
master.include_router(categories)  # added categories router
