import json
from datetime import datetime
import uuid
import os

def load_nutrition(path = "Data/nutrition.json"):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as jason_file:
            return json.load(jason_file)
    except json.JSONDecodeError:
        return []



def save_nutrition(meals , path = "Data/nutrition.json"):
    with open(path, "w", encoding="utf-8") as jason_file:
        json.dump(meals, jason_file, ensure_ascii=False, indent=4)


def log_meal(meals: list, meal_data: dict):
    n_id = "n" + str(uuid.uuid4())[:4]
    n_date = meal_data.get("date", datetime.today().strftime("%Y-%m-%d"))

    new_meal = {
        "id": n_id,
        "date": n_date,
        "meal_type": meal_data["meal_type"],
        "user_id": meal_data["user_id"],
        "foods": meal_data.get("foods", []),
        "calories": meal_data.get("calories", 0),

        "macros":{
            "protein_g": float(meal_data.get("protein_g", 0)),
            "carbs_g": float(meal_data.get("carbs_g", 0)),
            "fats_g": float(meal_data.get("fats_g", 0),)
        }
    }
    meals.append(new_meal)
    return new_meal


def update_meal(meals : list, n_id : str, updates: dict):
    for meal in meals:
        if meal["id"] == n_id:
            meal.update(updates)
            return meal
    return {}

def delete_meal(meals : list, n_id : str):
    for i, meal in enumerate(meals):
        if meal["id"] == n_id:
            del meals[i]
            return True
    return False

def daily_calorie_summary(meals : list, user_id : str, date : str):
    try:
        start_date_2 = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    end_date_2 = start_date_2 + timedelta(hours=24)

    total_calories = 0
    total_protein_g = 0
    total_carbs_g = 0
    total_fats_g = 0

    for meal in meals:
        if meal.get("user_id") != user_id:
            continue

        if meal.get("date") == date:
            total_calories += meal.get("calories", 0)
            macros = meal.get("macros", {})
            total_protein_g += macros.get("protein_g", 0)
            total_carbs_g += macros.get("carbs_g", 0)
            total_fats_g += macros.get("fats_g", 0)
    return {
        "date": date,
        "user_id": user_id,
        "total_calories": total_calories,
        "total_macros":{
            "protein_g": total_protein_g,
            "carbs_g": total_carbs_g,
            "fats_g": total_fats_g
        }
    }

def macro_breakdown(meals : list, user_id : str, date_range : tuple):

    start_date = date_range[0]
    end_date = date_range[1]

    total_protein_g = 0
    total_carbs_g = 0
    total_fats_g = 0
    for meal in meals:
        if meal.get("user_id") != user_id:
            continue

        meal_date = meal.get("date")
        if start_date <= meal_date <= end_date:
            macros = meal.get("macros", {})
            total_protein_g += macros.get("protein_g", 0)
            total_carbs_g += macros.get("carbs_g", 0)
            total_fats_g += macros.get("fats_g", 0)
    return {
        "start_date": start_date,
        "end_date": end_date,
        "protein": total_protein_g,
        "carbs": total_carbs_g,
        "fats": total_fats_g
    }
