import sqlite3
import datetime
from food import search_food

def log_meal(food_name, servings, meal_type):
    print(f"Searching for: {food_name}")

    food = search_food(food_name)
    protein = food[3] * servings
    fiber = food[4] * servings
    calories = food[5] * servings
    carbs = food[7] * servings
    sodium = food[9] * servings
    fat = food[10] * servings
    date = datetime.date.today().isoformat()

    connection = sqlite3.connect("nutrition.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO meal_log(food_name, meal_type, servings, calories, protein, fiber, carbs, fat, sodium, date) VALUES (?,?,?,?,?,?,?,?,?,?)", (food_name, meal_type, servings, calories, protein, fiber, carbs, fat, sodium, date))
    connection.commit()
    connection.close()

print(log_meal("kontomire stew", 1, "Breakfast"))