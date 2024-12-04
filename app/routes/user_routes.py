from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.controllers.user_controller import get_user, create_user, login_user
from app.controllers.llm_controller import chatWithLLM
from app.controllers.chat_history_controller import CreateChatHistory,FetchChatHistory, FetchRecentChats
from typing import List
from datetime import datetime

router = APIRouter()


@router.get("/user/{user_id}")
async def read_user(user_id, authorization=Header(None)):
    if authorization is None:
        raise HTTPException(status_code=400, detail="Authorization token is missing")

    user = await get_user(user_id, authorization)
    return user


# Define a Pydantic model for the user data
class UserCreateRequest(BaseModel):
    name: str
    email: str
    is_active: bool
    password: str
    role: str
    orgCode: str


@router.post("/register")
async def createUser(user_data: UserCreateRequest):
    user = await create_user(user_data)
    return user


# Define a Pydantic model for the user data
class UserLoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def loginFunc(user_data: UserLoginRequest):
    user = await login_user(user_data)
    return user



class UserMessageRequest(BaseModel):
    message: str
@router.post("/chat")
async def chatLLM(user_msg: UserMessageRequest):
    return await chatWithLLM(user_msg.message)






class ChatHistoryDist(BaseModel):
    title: str
    description: str

class ChatHistory(BaseModel):
    chatId: str
    userId: str
    chatHistory: List[ChatHistoryDist]
    lastUpdated: datetime = datetime.now()
    isActive: bool = True
    


@router.post("/chatHistory")
async def createChatHistory(Chat_History: ChatHistory):
    try:
        response = await CreateChatHistory(Chat_History)
        return response
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


class FetchChatHistoryClass(BaseModel):
    chatId: str
    userId: str

@router.post("/fetchChatHistory")
async def fetchChatHistoryFunc(fetchChatHistoryData: FetchChatHistoryClass):
    try:
        response = await FetchChatHistory(fetchChatHistoryData.chatId, fetchChatHistoryData.userId)
        return response
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
    

class FetchRecentChatsClass(BaseModel):
    userId: str

@router.post("/fetchRecentChats")
async def fetchRecentChatFunc(fetchRecentChatsData: FetchRecentChatsClass):
    try:
        response = await FetchRecentChats(fetchRecentChatsData.userId)
        return response
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
    
