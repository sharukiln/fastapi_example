from fastapi import FastAPI, HTTPException, APIRouter
from app.db.database_config import database
from app.models.user_model import UserBase, UserCreate, UserResponse, UserUpdate

router = APIRouter()
# @router.post("/users/", response_model=UserResponse)
# async def create_user(user: UserCreate):
#     global user_id_counter
#     if user.username in fake_db:
#         raise HTTPException(status_code=400, detail="Username already taken")
#     new_user = {"id": user_id_counter, **user.dict()}
#     fake_db[user_id_counter] = new_user
#     user_id_counter += 1
#     return new_user

# @router.get("/users/{user_id}", response_model=UserResponse)
# async def read_user(user_id: int):
#     user = fake_db.get(user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @app.put("/users/{user_id}", response_model=UserResponse)
# async def update_user(user_id: int, user_update: UserUpdate):
#     user = fake_db.get(user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     updated_user = user.copy()
#     for key, value in user_update.dict(exclude_unset=True).items():
#         updated_user[key] = value
#     fake_db[user_id] = updated_user
#     return updated_user

# @app.delete("/users/{user_id}")
# async def delete_user(user_id: int):
#     if user_id in fake_db:
#         del fake_db[user_id]
#         return {"message": "User deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="User not found")