from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.service.base_service import BaseService
from app.database.model.product import Product
from app.database.schemas.product import CreateProduct
from app.utils import logging_service, LogType, LogServiceType


class ProductService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)
        self.session = session

    # get all products
    async def get_all_products(self):
        return await self._get_all()

    # add new product
    async def add_product(self, user_id: UUID, data: CreateProduct):
        new_product = Product(**data.model_dump(), user_id=user_id)
        # log
        logging_service.set_log(
            f"{data.name} has been added to products.",
            log_type=LogType.INFO,
            log_service_type=LogServiceType.DATABASE,
        )
        return await self._create(new_product)
