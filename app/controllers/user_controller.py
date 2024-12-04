import datetime
from bcrypt import hashpw, gensalt, checkpw
from jwt import encode, decode
from bson import ObjectId
from app.services.user_service import fetch_user
from ..db.db import db
from config import JWT_SECRET
from ..services.validate_token import validateJWT


# -------- API FOR GETTING SINGLE USER ----------
# Refactored Code
async def get_user(user_id, Authtoken):
    try:
        # Validate the authentication token
        if not validateJWT(Authtoken):
            return {"error": "Invalid token"}

        # Validate and convert the user_id to ObjectId
        if not ObjectId.is_valid(user_id):
            return {"error": "Invalid user_id format"}
        
        object_id = ObjectId(user_id)

        # Fetch the user data
        user = await db.database.users.find_one({"_id": object_id})

        if not user:
            return {"error": "User not found"}
        
        user["_id"] = str(user["_id"])
        user.pop("password")
        return {"user_id": user_id, "user_data": user}
    
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


# -------- API FOR USER REGISTRATION ----------
async def create_user(user_data):
    try:
        # Hasing the pass before storing
        hashed_password = hashpw(user_data.password.encode("utf-8"), gensalt())

        # updating the original user_data with hash pass
        user_data.password = hashed_password

        # Creating a new user
        result = await db.database.users.insert_one(user_data.dict())

        # Fethcing the new user's data
        user = await db.database.users.find_one({"_id": result.inserted_id})

        if user:
            user["_id"] = str(user["_id"])
            return {"user_id": str(result.inserted_id), "user_data": user}
        else:
            return {"error": "User not found"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


# -------- API FOR LOGIN ----------
async def login_user(user_data):
    try:
        # Get user data by email
        user = await db.database.users.find_one({"email": user_data.email})

        if not user:
            return {"error": "User  not found"}

        print(f"Stored hash: {user['password']}")

        # Check User Password
        if not checkpw(user_data.password.encode("utf-8"), user["password"]):
            return {"error": "Invalid password"}

        # Token generation
        payload = {
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(hours=24),  # Token expiry
        }
        userData = {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "token": encode(payload, JWT_SECRET, algorithm="HS256"),
            "id": str(user["_id"]),
        }

        return {
            "message": "Login successful",
            "userData": userData,
        }

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
