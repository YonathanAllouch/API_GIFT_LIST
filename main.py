from fastapi import FastAPI, HTTPException
from models import GiftList
import crud

app = FastAPI()

@app.post("/gift-lists/", response_model=int)
def create_gift_list(gift_list: GiftList):
    list_id = crud.create_gift_list(gift_list)
    return list_id

@app.get("/gift-lists/{list_id}")
def read_gift_list(list_id: int):
    items = crud.get_gift_list(list_id)
    if not items:
        raise HTTPException(status_code=404, detail="Gift list not found")
    return items
