from typing import Annotated
from fastapi import  Depends, HTTPException, status, Response, APIRouter
from ..model import User, map_response_user
from ..db_conn.connection import *
from ..oauth2 import *


pool = None

def get_db():
     global pool
     if pool is None:
          pool = get_connection()
     return pool


router = APIRouter(
     prefix = "/users",
     tags=["Users"],
)

db = Annotated[dict, Depends(get_db)]


@router.get("/")
async def get_Users(dataBase: db, current_user: str = Depends(get_current_user)):
    cursor = dataBase["cursor"]
    cursor.execute(query = '''SELECT * FROM users ORDER BY id''')
    users = cursor.fetchall()
    print(current_user.email)
    response = []
    for user in users:
         x = dict(user)
         response.append(
              map_response_user(x)
         )
    return response

@router.post("/add", status_code= status.HTTP_201_CREATED)
async def post(payLoad: User, dataBase: db, user_email: str = Depends(get_current_user)):
    cursor = dataBase["cursor"]
    conn = dataBase["conn"]
    cursor.execute(query = '''INSERT INTO users (_name, age, phone_num) VALUES (%s, %s, %s) RETURNING *''',
                  vars = (payLoad.name, payLoad.age, payLoad.phoneNumber))
    new_user = cursor.fetchone()
    conn.commit()
    print(new_user)
    return {"new_user": new_user}

# @router.get("/users/latest")
# async def get_latest_user():
#     print(len(users) - 1)
#     new_user = users[len(users) - 1]
#     return {"User": new_user}

@router.get("/{id}")
async def get_user_with_Id(id: int,dataBase: db ):
     cursor = dataBase["cursor"]
     cursor.execute(query = '''SELECT * FROM users WHERE id = %s;''',vars = (id, ))
     user = cursor.fetchone()
     if not user:
              raise HTTPException(status_code=  status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
     
     return user

   

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_user_with_id(id: int, dataBase: db):
    cursor = dataBase["cursor"]
    conn = dataBase["conn"]
    cursor.execute(query = """DELETE FROM users WHERE id = %s RETURNING *""", vars = (id,))
    deleted_user = cursor.fetchone()
    conn.commit()

    if deleted_user == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"User with {id} not found.")

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
async def update_user(id: int, user: User, dataBase: db):
     cursor = dataBase["cursor"]
     conn = dataBase["conn"]
     cursor.execute(query = """UPDATE users SET _name = %s, age = %s, phone_num = %s WHERE id = %s returning *""", vars = (user.name, user.age, user.phoneNumber, id, ))
     updated_user = cursor.fetchone()
     conn.commit()

     if updated_user == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"User with {id} not found.")
  
     return updated_user


