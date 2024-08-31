from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from typing import List

app = FastAPI()

# MongoDB connection URI
MONGO_DETAILS = "mongodb://localhost:27017"

# MongoDB client
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.my_database  # Replace with your database name