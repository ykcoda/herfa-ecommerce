from fastapi import APIRouter
from app.api.routes.users import users
from app.api.routes.category import categories
from app.api.routes.products import products


master = APIRouter()  # create a master router
master.include_router(users)  # added users router
master.include_router(categories)  # added categories router
master.include_router(products)  # added products router
