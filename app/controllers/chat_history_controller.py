from datetime import datetime
from bcrypt import hashpw, gensalt, checkpw
from jwt import encode, decode
from bson import ObjectId
from app.services.user_service import fetch_user
from ..db.db import db
from config import JWT_SECRET
from ..services.validate_token import validateJWT
from pydantic import BaseModel


class ChatHistoryDist(BaseModel):
    title: str
    description: str


async def CreateChatHistory(chatHistory):
    try:
        if not chatHistory:
            return {"error": "No chat history provided"}

        chatExists = await db.database.ChatHistory.find_one({"chatId": chatHistory.chatId, "userId": chatHistory.userId})

        if chatExists:
            try:
                if isinstance(chatHistory.chatHistory, list):
                    chat_history_dicts = [item.dict() for item in chatHistory.chatHistory]
                else:
                    chat_history_dicts = [chatHistory.chatHistory.dict()]

                result = await db.database.ChatHistory.update_one(
                    {"_id": chatExists["_id"]},
                     {
                        "$set": {"lastUpdated": datetime.now()},
                        "$push": {"chatHistory": {"$each": chat_history_dicts}}
                    }
                )

                chatHistory = await db.database.ChatHistory.find_one({"_id": chatExists["_id"]})

                if chatHistory:
                    chatHistory["_id"] = str(chatHistory["_id"])
                    return {"chatId": str(chatExists["_id"]), "chatHistory": chatHistory}
                else:
                    return {"error": "Chat history not found"}

            except Exception as e:
                return {"error": f"An error occurred while updating: {str(e)}"}

        # Add New Chat History
        chatHistory.lastUpdated = datetime.now()
        print(chatHistory.dict())
        try:
            result = await db.database.ChatHistory.insert_one(chatHistory.dict())
        except Exception as e:
            return {"error": f"An error occurred while inserting: {str(e)}"}

        chatHistory = await db.database.ChatHistory.find_one({"_id": result.inserted_id})

        if chatHistory:
            chatHistory["_id"] = str(chatHistory["_id"])
            return {"chatId": str(result.inserted_id), "chatHistory": chatHistory}
        else:
            return {"error": "Chat history not found"}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
    
    
async def FetchChatHistory(chatId,userId ):
    try:

        if not chatId or not userId:
            return {"error": "Invalid chatId or userId"}

        chatHistory = await db.database.ChatHistory.find_one({"chatId": chatId, "userId": userId})

        if chatHistory:
            chatHistory["_id"] = str(chatHistory["_id"])
            return {"data": chatHistory}
        else:
            return {"error": "Chat history not found"}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
    
    
async def FetchRecentChats(userId):
    if not userId:
        return {"error": "Invalid userId"}

    try:
        chatHistory = (
            await db.database.ChatHistory.find({"userId": userId})
            .sort("lastUpdated", -1)
            .limit(3)
            .to_list(length=3)
        )

        if not chatHistory:
            return {"error": "Chat history not found"}

        for chat in chatHistory:
            chat["_id"] = str(chat["_id"])

        return {"data": chatHistory}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
