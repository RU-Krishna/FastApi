import psycopg2
from psycopg2.extras import RealDictCursor
import time
from ..config import settings

def get_connection(): 
   while True:
      try:
         conn = psycopg2.connect(
            host=settings.database_host,
            database=settings.database_name,
            user= settings.database_username,
            password=settings.database_password,
            cursor_factory=RealDictCursor
            )
         cursor = conn.cursor()
         print("Database Connected Successfully")
         return {
            "conn": conn,
            "cursor": cursor
         }
      except Exception as error:
         print("Error connecting to database")
         print(error)
         time.sleep(3)




