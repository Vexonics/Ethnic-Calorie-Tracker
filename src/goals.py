def calculate_goals(weight, goal, sex, TDEE):
    if goal == "Cut":
        protein = weight * 0.7
    elif goal == "Bulk":
        protein = weight * 1
    elif goal == "Maintain": 
        protein = weight * 0.36
    else:
        protein = weight * 0.8
    carbs = TDEE * 0.1375
    fat = TDEE * 0.039
    sodium = 2300
    
    if sex == "Female":
        fiber = 25
    else:
        fiber = 38

    return round(protein), round(carbs), fiber, round(sodium), round(fat)

