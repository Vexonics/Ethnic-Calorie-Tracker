import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import datetime
from src.food import search_food

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "nutrition.db")

def log_meal(food_name, servings, meal_type):
    food = search_food(food_name)
    print(food)
    protein = food[3] * servings
    fiber = food[4] * servings
    calories = food[5] * servings
    carbs = food[7] * servings
    sodium = food[9] * servings
    fat = food[10] * servings
    date = datetime.date.today().isoformat()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO meal_log(food_name, meal_type, servings, calories, protein, fiber, carbs, fat, sodium, date) VALUES (?,?,?,?,?,?,?,?,?,?)", (food_name, meal_type, servings, calories, protein, fiber, carbs, fat, sodium, date))
    connection.commit()
    connection.close()

log_meal("kontomire stew", 1, "Breakfast")