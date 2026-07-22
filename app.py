import streamlit as st
import sqlite3
import os
import datetime
from src.tdee import calculate_tdee
from src.goals import calculate_goals
from src.recommendation import recommend
from src.logging import log_meal, get_progress
from src.food import search_food
DB_PATH = os.path.join(os.path.dirname(__file__), "nutrition.db")

def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS food(food_id INTEGER PRIMARY KEY, food_name TEXT, serving_size INTEGER, protein REAL, fiber REAL, calories INTEGER, cuisines TEXT, carbs REAL, sugar REAL, sodium REAL, fat REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS meal_log(log_id INTEGER PRIMARY KEY, food_name TEXT, meal_type TEXT, servings REAL, calories REAL, protein REAL, fiber REAL, carbs REAL, fat REAL, sodium REAL, date TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY, name TEXT, age INTEGER, weight INTEGER, height INTEGER, sex TEXT, activity_lvl TEXT, goal TEXT, goal_weight INTEGER, months_to_goal INTEGER)")
    connection.commit()
    connection.close()

init_db()

def seed_foods():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM food")
    count = cursor.fetchone()[0]
    connection.close()
    
    if count == 0:
        from src.food import add_food
        add_food("kontomire stew", 100, 30.5, 10.2, 350, "Ghanaian", 60.0, 2.4, 112.0, 45.0)
        add_food("Fufu and Light Soup", 100, 6.0, 1.4, 132, "Ghanaian", 16.5, 1.5, 360.0, 2.5)
        add_food("Ampesi (Boiled Yam) and Pavlava Sauce", 100, 5, 2.6, 167, "Ghanaian", 18.5, 1.3, 361, 9)
        add_food("Bofrot", 100, 7.8, 0, 291, "Ghanaian", 63.4, 11, 208, 2.6)
        add_food("Fried Yam and Meko", 100, 2.2, 2.5, 210, "Ghanaian", 31, 2.8, 245, 8.5)
        add_food("Tomato Stew", 100, 2.4, 1.8, 138, "Ghanaian", 8.6, 4.2, 395, 10.5)
        add_food("Tacos de Pollo", 100, 11.4, 1.8, 172, "Mexican", 16.5, 0.9, 324, 6.7)
        add_food("Sopa de Fideo", 100, 2.1, 0.8, 62, "Mexican", 8.8, 1.2, 280, 2.2)
        add_food("Tamal de Puerco en Salsa Roja", 100, 6.8, 2.3, 223, "Mexican", 21.8, 0.6, 492, 12.1)
        add_food("Elote", 100, 3.1, 2.0, 144, "Mexican", 15.6, 4.2, 295, 8.5)
        add_food("Carne Asada", 100, 24.8, 0.0, 210, "Mexican", 1.2, 0.4, 412, 11.6)
        add_food("Sumac Chicken and Onion Flatbread", 100, 12.5, 1.9, 234, "Palestinian", 18, 1.5, 380, 12.2)
        add_food("Maqluba", 100, 8.4, 1.4, 158, "Palestinian", 19.8, 1.1, 290, 5.5)
        add_food("Falafel", 100, 13.3, 4.9, 333, "Palestinian", 31.8, 2.4, 294, 17.8)
        add_food("Hummus", 100, 7.9, 6.0, 166, "Palestinian", 14.3, 0.3, 379, 9.6)
        add_food("Knafeh", 100, 7.1, 0.6, 318, "Palestinian", 41.5, 25.2, 195, 13.8)
        add_food("Bibimbap", 100, 6.1, 1.6, 135, "Korean", 19.5, 1.8, 285, 3.6)
        add_food("Kimchi", 100, 1.6, 1.8, 15, "Korean", 2.4, 1.1, 498, 0.2)
        add_food("Bulgogi", 100, 21.4, 0.3, 188, "Korean", 7.2, 5.4, 465, 7.8)
        add_food("Japchae", 100, 2.5, 1.5, 145, "Korean", 23.8, 4.1, 310, 4.4)
        add_food("Doenjang jjigae", 100, 4.2, 1.1, 48, "Korean", 4.5, 0.8, 415, 1.8)
        add_food("Couscous with vegetables", 100, 3.6, 2.2, 112, "Moroccan", 21.4, 1.9, 185, 1.4)
        add_food("Tagine with chicken", 100, 11.2, 1.1, 134, "Moroccan", 4.8, 1.5, 310, 7.8)
        add_food("Harira soup", 100, 4.1, 2.8, 78, "Moroccan", 11.5, 1.6, 265, 1.8)
        add_food("Bissara", 100, 6.4, 5.1, 118, "Moroccan", 16.5, 0.7, 210, 3.2)
        add_food("Msemen", 100, 7.2, 1.9, 324, "Moroccan", 52.4, 1.1, 345, 9.6)

seed_foods()

def get_todays_meals():
    date = datetime.date.today().isoformat()
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM meal_log WHERE date = ?", (date,))
    result = cursor.fetchall()
    connection.close()
    return result

def delete_meals(log_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM meal_log WHERE log_id = ?", (log_id,))
    connection.commit()
    connection.close()
    

def check_user():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user LIMIT 1")
    result = cursor.fetchone()
    connection.close()
    return result

st.title("Ethnic Calorie Tracker")
user = check_user()

if user is None:
    name = st.text_input("Please enter your full name: ")
    age = st.number_input("Please enter your age: ")
    height = st.number_input("Please enter your height (inches): ")
    weight = st.number_input("Please enter your weight (lbs): ")
    goal_weight = st.number_input("Please enter your goal weight (lbs): ")
    months_to_goal = st.number_input("Please enter how many months you want to spend toward this goal: ")
    sex = st.selectbox("Sex", ["Male", "Female"])
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Active", "Very Active"])
    goal = st.selectbox("Goal", ["Cut", "Bulk", "Maintain", "Body Recomposition"])

    if st.button("Create Profile"):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user(name, age, weight, height, sex, activity_lvl, goal, goal_weight, months_to_goal) VALUES(?,?,?,?,?,?,?,?,?)", 
                   (name, age, weight, height, sex, activity_level, goal, goal_weight, months_to_goal))
        connection.commit()
        connection.close()
        st.success("Profile Create!")
        st.rerun()

else:
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

    col1, col2, col3 = st.columns(3)
    col1.metric("Calories Remaining", round(progress["calories"]["remaining"]))
    col2.metric("Protein Remaining", f'{round(progress["protein"]["remaining"])}g')
    col3.metric("Fiber Remaining", f'{round(progress["fiber"]["remaining"])}g')


    col4, col5, col6 = st.columns(3)
    col4.metric("Carbs Remaining", f'{round(progress["carbs"]["remaining"])}g')
    col5.metric("Fat Remaining", f'{round(progress["fat"]["remaining"])}g')
    col6.metric("Sodium Remaining", f'{round(progress["sodium"]["remaining"])}mg')

    st.subheader("Recommended Foods")
    recommendations = recommend(
    progress["calories"]["remaining"],
    progress["protein"]["remaining"],
    progress["carbs"]["remaining"],
    progress["fiber"]["remaining"],
    progress["fat"]["remaining"],
    progress["sodium"]["remaining"]
    )

    for food in recommendations:
        st.write(f"**{food[0].title()}** — {food[2]}g protein | {food[3]}g fiber | {food[1]} cal")

    st.subheader("Log a Meal")
    food_name = st.text_input("Food Name")
    servings = st.number_input("Servings", min_value= 0.1, step=0.1)
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])

    if st.button("Log Meal"):
        result = search_food(food_name.lower())
        if result is None:
            st.error(f"'{food_name}' not found in database.")
        else:
            log_meal(food_name.lower(), servings, meal_type)
            st.success(f"{food_name.title()} logged successfully!")
            st.rerun()
    
    st.subheader("Today's Meals")
    todays_meals = get_todays_meals()

    if not todays_meals:
        st.write("No meals logged today.")
    else:
        for meal in todays_meals:
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{meal[1].title()}** — {meal[3]} servings | {meal[4]} cal | {meal[2]}")
            if col2.button("Delete", key=meal[0]):
                delete_meals(meal[0])
                st.rerun()
        
    st.divider()
    if st.button("Reset Profile"):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM user")
        cursor.execute("DELETE FROM meal_log")
        connection.commit()
        connection.close()
        st.rerun()
