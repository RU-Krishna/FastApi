from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    age: int
    phoneNumber: str


class ReturnUser(BaseModel):
    name: str
    age: int
    phoneNumber: str



class CreateGuest(BaseModel):
    email: EmailStr
    password: str


class ReturnGuest(BaseModel):
    email: str


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None


def map_response_guest(dict):
    return ReturnGuest(
        email = dict['email']
    )



def map_response_user(dict):
    return ReturnUser(
        name=dict['_name'],
        age = dict['age'],
        phoneNumber = dict['phone_num']
    )
