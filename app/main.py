from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

# initiating fast api
app = FastAPI()


# api home page
@app.get("/api")
async def home():
    return {"message": "Herfa-Ecommerce"}


# scalar docs
@app.get("/api/docs", include_in_schema=False)
async def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, title="Herfa-Ecommerce API"
    )
