from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime  import  datetime, timedelta, timezone

from app.model import TokenData
from app.config import settings
#SECRET
#Algorithm
#Expiration Time


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXXPIRATION_TIME = settings.access_token_expiry_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXXPIRATION_TIME)
    to_encode.update({"exp": expire})


    encoded_jwt = jwt.encode(to_encode, key = SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
    
         payload = jwt.decode(token, key = SECRET_KEY, algorithms = ALGORITHM)
         email: str = payload.get("user_email")
     
         if id is None:
             raise credentials_exception
         
         token_data = TokenData(email = email)
    except JWTError :
        raise credentials_exception
    
    return token_data
    


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                                         detail = "Could not validate credentials",
                                         headers = {"WWW-Authenticate": "Bearer"}
                                         )
    return verify_access_token(token, credential_exception)