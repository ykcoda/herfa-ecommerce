from uuid import UUID
from fastapi import APIRouter
from app.api.common.dependencies import AUTHENTICATED_USER_DEP, PRODUCT_SERVICE_DEP
from app.database.schemas.product import CreateProduct, ReadProduct

products = APIRouter(prefix="/api/products", tags=["Products"])


# get all products
@products.get("/", response_model=list[ReadProduct])
async def get_all_products(
    authenticted_user: AUTHENTICATED_USER_DEP, service: PRODUCT_SERVICE_DEP
):
    return await service.get_all_products()


@products.post("/add", response_model=ReadProduct)
async def add_product(
    product: CreateProduct,
    authenticted_user: AUTHENTICATED_USER_DEP,
    service: PRODUCT_SERVICE_DEP,
):
    return await service.add_product(
        authenticted_user["user"]["id"], data=product  # type: ignore
    )
