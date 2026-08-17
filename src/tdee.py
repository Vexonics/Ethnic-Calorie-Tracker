def calculate_tdee(weight, height, age, sex, activity_lvl, goal, goal_weight, months_to_goal):
    weeks_to_goal = months_to_goal * 4
    weight = weight * 0.453592
    goal_weight = goal_weight * 0.453592
    height = height * 2.54

    if sex == "Female":
        BMR = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else: 
        BMR = (10 * weight) + (6.25 * height) - (5 * age) + 5

    activity_multipliers = {
        "Sedentary" : 1.2,
        "Lightly Active" : 1.375,
        "Moderately Active" : 1.55,
        "Active" : 1.725,
        "Very Active" : 1.9
    }

    TDEE = BMR * activity_multipliers[activity_lvl]

    weight_change = abs(weight - goal_weight)
    weekly_rate = weight_change / weeks_to_goal
    daily_deficit = weekly_rate * 500

    if goal == "Cut":
        TDEE = TDEE - daily_deficit
    elif goal == "Bulk":
        TDEE = TDEE + daily_deficit
    else: 
        TDEE = TDEE
    return round(TDEE)