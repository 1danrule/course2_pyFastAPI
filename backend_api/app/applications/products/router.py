from fastapi import APIRouter

products_router = APIRouter()


@products_router.post('')
async def create_product():
    return