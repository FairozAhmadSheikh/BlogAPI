from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException
import os

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRY")

oauth_schema=OAuth2PasswordBearer(tokenUrl="login")


def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_token(token:str=Depends(oauth_schema)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")