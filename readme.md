# FastAPI MongoDB CRUD API

This is a simple FastAPI application for managing items in a MongoDB database. The application allows you to create, retrieve, update, and delete items using a RESTful API.

## Features

- Create an item in the database
- Retrieve an item by its ID
- Retrieve all items
- Update an item by its ID
- Delete an item by its ID

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git



cd yourproject
pip install -r requirements.txt
export MONGO_DETAILS="your_mongo_connection_string"
uvicorn main:app --reload
