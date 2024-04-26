import os
import re
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request, status
#from sqlalchemy.ext.asyncio import AsyncSession
#from src.database.db import get_db
import uvicorn


app = FastAPI()





@app.get("/")
def index():
    return {'message':'PhotoShare Application'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    
    

