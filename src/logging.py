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

def get_progress(cal_goal, protein_goal, carbs_goal, fiber_goal, fat_goal, sodium_goal):
    date = datetime.date.today().isoformat()
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM meal_log WHERE date = ?", (date,))
    result = cursor.fetchall()
    connection.close()
    
    total_cal = 0
    total_protein = 0
    total_carbs = 0
    total_fiber = 0
    total_fat = 0
    total_sodium = 0
    
    for i in result:
       total_cal += i[4]
       total_protein += i[5]
       total_carbs += i[7]
       total_fiber += i[6]
       total_fat += i[8]
       total_sodium += i[9]
    
    return {
    "calories": {"eaten": total_cal, "remaining": cal_goal - total_cal},
    "protein": {"eaten": total_protein, "remaining": protein_goal - total_protein},
    "carbs": {"eaten": total_carbs, "remaining": carbs_goal - total_carbs},
    "fiber": {"eaten": total_fiber, "remaining": fiber_goal - total_fiber},
    "fat": {"eaten": total_fat, "remaining": fat_goal - total_fat},
    "sodium": {"eaten": total_sodium, "remaining": sodium_goal - total_sodium},
}

