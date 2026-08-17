import os
import requests
from dotenv import load_dotenv

load_dotenv()

USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
USDA_API_KEY = os.environ.get("USDA_API_KEY", "")

def _query_usda(food_name, data_types):
    params = {
        "query": food_name,
        "dataType": data_types,
        "pageSize": 1,
        "api_key": USDA_API_KEY,
    }

    try:
        response = requests.get(USDA_BASE_URL, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        print("Network error:", e)
        return None

    if response.status_code != 200:
        return None

    data = response.json()
    foods = data.get("foods", [])

    if not foods:
        return None

    food = foods[0]
    nutrients = {n["nutrientName"]: n["value"] for n in food.get("foodNutrients", [])}

    calories = nutrients.get("Energy (Atwater General Factors)", 0) or nutrients.get("Energy", 0)
    sugar = nutrients.get("Sugars, total including NLEA", 0) or nutrients.get("Total Sugars", 0)

    if calories == 0:
        return None

    return {
        "food_name": food.get("description", food_name.title()),
        "serving_size": 100,
        "protein": nutrients.get("Protein", 0),
        "fiber": nutrients.get("Fiber, total dietary", 0),
        "calories": calories,
        "cuisines": "Unknown",
        "carbs": nutrients.get("Carbohydrate, by difference", 0),
        "sugar": sugar,
        "sodium": nutrients.get("Sodium, Na", 0),
        "fat": nutrients.get("Total lipid (fat)", 0),
    }

def search_open_food_facts(food_name):
    result = _query_usda(food_name, ["Foundation", "SR Legacy"])
    if result is not None:
        return result

    return _query_usda(food_name, ["Branded"])