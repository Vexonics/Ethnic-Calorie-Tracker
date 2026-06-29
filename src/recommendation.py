import sqlite3

def recommend(calories, protein, carbs, fiber, fat, sodium):
    connection = sqlite3.connect("nutrition.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * from food")
    results = cursor.fetchall()

    score_list = []
    for i in results: 
        score = 1 / (abs(i[3] - protein) +1)
        if i[5] < calories:
            score_list.append((score, i))
    score_list.sort(key = lambda x : x[0], reverse = True)

    recommendation = []
    for i in score_list[:5]:
        food = i[1]
        food_name = food[1]
        food_protein = food[3]
        food_fiber = food[4]
        food_calories = food[5]
        recommendation.append((food_name, food_calories, food_protein, food_fiber))
    return recommendation
    
print(recommend(200, 68, 100, 15, 20, 800))