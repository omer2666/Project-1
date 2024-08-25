from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import os
import logging

# Initialize FastAPI
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB Configuration
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = MongoClient(MONGO_DETAILS)
database = client.my_database
collection = database.my_collection

# Pydantic model for the data
class Item(BaseModel):
    name: str
    description: str 
    price: float
    available: bool = True

# Convert MongoDB ObjectId to string
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item["price"],
        "available": item["available"],
    }

# Create an item in MongoDB
@app.post("/items/", response_model=dict)
async def create_item(item: Item):
    try:
        new_item = item.dict()
        result = collection.insert_one(new_item)
        created_item = collection.find_one({"_id": result.inserted_id})
        return item_helper(created_item)
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get an item from MongoDB by ID
@app.get("/items/{item_id}", response_model=dict)
async def get_item(item_id: str):
    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
        if item:
            return item_helper(item)
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error retrieving item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get all items from MongoDB
@app.get("/items/", response_model=list)
async def get_items():
    try:
        items = []
        for item in collection.find():
            items.append(item_helper(item))
        return items
    except Exception as e:
        logger.error(f"Error retrieving items: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Update an item in MongoDB by ID
@app.put("/items/{item_id}", response_model=dict)
async def update_item(item_id: str, item: Item):
    try:
        updated_item = collection.find_one_and_update(
            {"_id": ObjectId(item_id)},
            {"$set": item.dict()},
            return_document=True
        )
        if updated_item:
            return item_helper(updated_item)
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error updating item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Delete an item from MongoDB by ID
@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
        if item:
            collection.delete_one({"_id": ObjectId(item_id)})
            return item_helper(item)
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
