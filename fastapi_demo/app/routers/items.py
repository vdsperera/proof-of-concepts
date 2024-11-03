"""_summary_
"""

from fastapi import APIRouter, HTTPException
from fastapi_demo.app.models import Item
from fastapi_demo.app.services.item_service import create_item, get_item

router = APIRouter()

@router.post(path="/items/", response_model=Item)
async def create_item_endpoint(item: Item):
    """_summary_
    """
    try:
        return create_item(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(path="/items/{item_id}", response_model=Item)
async def get_item_endpoint(item_id):
    """_summary_
    """
    try:
        print(f"get_item_endpoint : {item_id}")
        return get_item(int(item_id))
    except ValueError as e:
        print(f"get_item_endpoint error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
