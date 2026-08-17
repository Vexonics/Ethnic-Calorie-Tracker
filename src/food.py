import sqlite3
import os
from src.api import search_open_food_facts

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "nutrition.db")

def add_food(food_name, serving_size, protein, fiber, calories, cuisines, carbs, sugar, sodium, fat):
   connection = sqlite3.connect(DB_PATH)
   cursor = connection.cursor()
   cursor.execute("INSERT INTO food(food_name, serving_size, protein, fiber, calories, cuisines, carbs, sugar, sodium, fat) VALUES(?,?,?,?,?,?,?,?,?,?)", (food_name, serving_size, protein, fiber, calories, cuisines, carbs, sugar, sodium, fat))
   connection.commit()
   connection.close()  

def search_food(food_name):
   connection = sqlite3.connect(DB_PATH)
   cursor = connection.cursor()
   cursor.execute("SELECT * from food WHERE LOWER(food_name) = LOWER(?)", (food_name,))
   result = cursor.fetchone()
   connection.close()

   if result is not None:
       return result

   api_result = search_open_food_facts(food_name)
   if api_result is None:
       return None

   add_food(
    food_name,
    api_result["serving_size"],
    api_result["protein"],
    api_result["fiber"],
    api_result["calories"],
    api_result["cuisines"],
    api_result["carbs"],
    api_result["sugar"],
    api_result["sodium"],
    api_result["fat"],
)

   connection = sqlite3.connect(DB_PATH)
   cursor = connection.cursor()
   cursor.execute("SELECT * from food WHERE LOWER(food_name) = LOWER(?)", (food_name,))
   result = cursor.fetchone()
   connection.close()
   return result