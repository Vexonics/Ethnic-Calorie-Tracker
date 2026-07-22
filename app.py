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
