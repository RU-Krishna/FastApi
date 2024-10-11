from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm, oauth2

from ..model import UserCredentials
from ..db_conn.connection import get_connection
from ..utils import verifyUser
from ..oauth2 import *
from ..model import Token

pool = None

def  get_db():
    global pool
    if pool is None:
        pool = get_connection()
    return pool


router = APIRouter(
    tags = ["Authentication"],
    prefix = "/auth"
)

db = Annotated[dict, Depends(get_db, use_cache= True)]


@router.post("/login", response_model= Token)
def login(dataBase: db, userCredentials: OAuth2PasswordRequestForm = Depends()):
    conn = dataBase["conn"]
    cursor = dataBase['cursor']
    cursor.execute("""SELECT email, password from guests WHERE email = %s""", 
                   vars = (userCredentials.username, ))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"User with email {userCredentials.email} not found.")

    if not verifyUser(userCredentials.password, user['password']):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Wrong Password")
    

    token = create_access_token({"user_email": user['email']})
    
    return {'access_token': token, "token_type": "bearer"}