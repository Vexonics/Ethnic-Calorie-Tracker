import sqlite3
import os
from src.tdee import calculate_tdee
from src.goals import calculate_goals
from src.recommendation import recommend
from src.logging import log_meal, get_progress
DB_PATH = os.path.join(os.path.dirname(__file__), "nutrition.db")


def check_user():
   connection = sqlite3.connect(DB_PATH)
   cursor = connection.cursor()
   cursor.execute("SELECT * from user LIMIT 1")
   result = cursor.fetchone()
   connection.close()
   return result

def setup_user():
   name = input("Enter your name: ")
   age = int(input("Enter your age: "))
   sex = input("Enter your sex: ")
   height = float(input("Enter your height(inches): "))
   weight = float(input("Enter your weight(lbs): "))
   activity_level = input("Enter your activity level (Sedentary, Lightly Active, Moderately Active, Highly Active): ")
   goal = input("Enter your goal (bulk, cut, maintain, body recomposition): ")
   goal_weight = float(input("Enter your goal weight: "))
   months_to_goal = int(input("Enter how many months until you want to reach your goal: "))

   connection = sqlite3.connect(DB_PATH)
   cursor = connection.cursor()
   cursor.execute("INSERT INTO user(name, age, weight, height, sex, activity_lvl, goal, goal_weight, months_to_goal) VALUES(?,?,?,?,?,?,?,?,?)", (name, age, weight, height, sex, activity_level, goal, goal_weight, months_to_goal))
   connection.commit()
   connection.close()
   return (name, age, weight, height, sex, activity_level, goal, goal_weight, months_to_goal)   

def main():
   user = check_user()
   if user is None:
      user = setup_user()
   age = user[2]
   weight = float(user[3])
   height = float(user[4])
   sex = user[5]
   activity_level = user[6]
   goal = user[7]
   goal_weight = float(user[8])
   months_to_goal = int(user[9])
   tdee = calculate_tdee(weight, height, age, sex, activity_level, goal, goal_weight, months_to_goal)  
   
   goals = calculate_goals(weight, sex, goal, tdee) 
   protein_goal, carbs_goal, fiber_goal, sodium_goal, fat_goal = goals
   progress = get_progress(tdee, protein_goal, carbs_goal, fiber_goal, fat_goal, sodium_goal)

   print(f"\nHello {user[1]}! Here's your progress for today: ")
   print(progress)

   recommendations = recommend(
    progress["calories"]["remaining"],
    progress["protein"]["remaining"],
    progress["carbs"]["remaining"],
    progress["fiber"]["remaining"],
    progress["fat"]["remaining"],
    progress["sodium"]["remaining"]
)
   
   print("\nRecommended foods:")
   print(recommendations)

   while True:
      log = input("\n Do you want to log a meal (yes/no): ")
      if log.lower() == "no":
         break 
      food_name = input("Enter food name: ")
      servings = float(input("Enter servings: "))
      meal_type = input("Enter meal type (Breakfast/Lunch/Dinner/Snack): ")
      log_meal(food_name, servings, meal_type)
      progress = get_progress(tdee, protein_goal, carbs_goal, fiber_goal, fat_goal, sodium_goal)
      print("\nUpdated progress: ")
      print(progress)

if __name__ == "__main__":
    main()