from fastapi import FastAPI
from app.routes import user_routes
from .db.db import connect_to_mongo, close_mongo_connection
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (replace with specific origins for more security)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include the user routes
app.include_router(user_routes.router)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    
@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
    

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}
