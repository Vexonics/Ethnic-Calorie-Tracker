import sqlite3

connection = sqlite3.connect("nutrition.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE food(food_id INTEGER PRIMARY KEY, food_name TEXT, serving_size INTEGER, protein REAL, fiber REAL, calories INTEGER, cuisines TEXT, carbs REAL, sugar REAL, sodium REAL, fat REAL)")
connection.commit()
connection.close()