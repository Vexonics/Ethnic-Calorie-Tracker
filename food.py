import sqlite3

def add_food(food_name, serving_size, protein, fiber, calories, cuisines, carbs, sugar, sodium, fat):
   connection = sqlite3.connect("nutrition.db")
   cursor = connection.cursor()
   cursor.execute("INSERT INTO food(food_name, serving_size, protein, fiber, calories, cuisines, carbs, sugar, sodium, fat) VALUES(?,?,?,?,?,?,?,?,?,?)", (food_name, serving_size, protein, fiber, calories, cuisines, carbs, sugar, sodium, fat))
   connection.commit()
   connection.close()  

def search_food(food_name):
   connection = sqlite3.connect("nutrition.db")
   cursor = connection.cursor()
   cursor.execute("SELECT * from food WHERE food_name = ?", (food_name,))
   result = cursor.fetchone()
   connection.close()
   return result

