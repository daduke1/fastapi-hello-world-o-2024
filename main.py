from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Security
from pydantic import BaseModel
from fastapi.security.api_key import APIKeyQuery
import os

_ = load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "access_token" # Definir el nombre al parámetro de query
api_key_query = APIKeyQuery(name=API_KEY_NAME) #  Dice que esto es un parámetro de query


async def get_api_key(api_key: str = Security(api_key_query)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        )


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# Cada uno de los decoradores es un endpoint, tiene URL y el método que estamos utilizando
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None, api_key: str = Depends(get_api_key)):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(item: Item, api_key: str = Depends(get_api_key)): # Se necesita api_key que depende de esa función
    return {"name": item.name, "price": item.price}
