import sqlite3

connection = sqlite3.connect("nutrition.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS food(food_id INTEGER PRIMARY KEY, food_name TEXT, serving_size INTEGER, protein REAL, fiber REAL, calories INTEGER, cuisines TEXT, carbs REAL, sugar REAL, sodium REAL, fat REAL)")
cursor.execute("CREATE TABLE IF NOT EXISTS meal_log(log_id INTEGER PRIMARY KEY, food_name TEXT, meal_type TEXT, servings REAL, calories REAL, protein REAL, fiber REAL, carbs REAL, fat REAL, sodium REAL, date TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY, name TEXT, age INTEGER, weight INTEGER, height INTEGER, sex TEXT, activity_lvl TEXT, goal TEXT, goal_weight INTEGER, months_to_goal INTEGER)")
connection.commit()
connection.close()