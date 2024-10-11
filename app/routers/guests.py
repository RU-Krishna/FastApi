from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from ..model import CreateGuest
from ..utils import hash
from ..db_conn.connection import *

pool = None

def get_db():
     global pool
     if pool is None:
          pool = get_connection()
     return pool


router = APIRouter(
     prefix = "/guests",
     tags=["Guests"],
)

db = Annotated[dict, Depends(get_db, use_cache= True)]



@router.get("/")
async def get_guests(dataBase: db):
    #  conn = db["conn"]
     cursor = dataBase["cursor"]
     cursor.execute("""SELECT email FROM guests""")
     guests = cursor.fetchall()
     return guests

@router.post("/add", status_code= status.HTTP_201_CREATED)
async def create_guest(guest: CreateGuest,dataBase: db):
     try: 
         cursor = dataBase["cursor"]
         conn = dataBase["conn"]

         cursor.execute("INSERT INTO guests (email, password) VALUES (%s, %s) RETURNING email",
                        vars = (guest.email, hash(guest.password)))
         new_guest = dict(cursor.fetchone())
         conn.commit()
     except Exception as error:
          raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Duplicate Value")
     return {"detail": f"Guest with {new_guest['email']} created"}
     

@router.get("/{id}")
async def get_usr_with_id(id: int, dataBase: db):
     cursor = dataBase["cursor"]
     cursor.execute("""SELECT * FROM guests WHERE id = %s""",
                    vars = (id, ))
     user = cursor.fetchone()
     print(user)
     if user == None:
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"Guest with userId {id} not found")
     
     return user['email']
