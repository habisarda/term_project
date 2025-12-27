import json
from datetime import datetime, timedelta
import uuid
import os

def load_workouts(path = "Data/workouts.json"):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as jason_file:
            return json.load(jason_file)
    except json.JSONDecodeError:
        return []

def save_workouts(workouts:list , path="Data/workouts.json"):
    with open(path, "w", encoding="utf-8") as jason_file:
        json.dump(workouts, jason_file, ensure_ascii=False, indent=4)


def log_workout(workouts:list , workout_data: dict):
    w_id = "w" + str(uuid.uuid4())[:4]
    w_date = workout_data.get("date", datetime.today().strftime("%Y-%m-%d %H:%M"))

    new_workout = {
        "id": w_id,
        "date": w_date,
        "user_id": workout_data["user_id"],
        "type": workout_data["type"],
        "duration": int(workout_data.get("duration", 0)),
        "exercise": workout_data.get("exercise", []),
        "notes": workout_data.get("notes", ""),
    }
    workouts.append(new_workout)
    return new_workout

def update_workout(workouts:list , w_id: str ,updates: dict ):
    for workout in workouts:
        if workout["id"] == w_id:
            workout.update(updates)
            return workout
    return {}


def delete_workout(workouts:list , w_id: str):
    for i, workout in enumerate(workouts):
        if workout["id"] == w_id:
            del workouts[i]
            return True

    return False


def weekly_workout_summary(workouts:list , w_id , week_start: str):
    try:
        start_date = datetime.strptime(week_start, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    end_date = start_date + timedelta(days=7)

    total_workouts = 0
    total_duration = 0
    types_count = {}

    for w in workouts:
        if w.get("id") != id:
            continue
        w_date_str = w["date"].split(" ")[0]
        try:
            w_date_obj = datetime.strptime(w_date_str, "%Y-%m-%d")
        except ValueError:
            continue
        if start_date <= w_date_obj < end_date:
            total_workouts += 1
            total_duration += w.get("duration", 0)

            w_type = w.get("type", "Other")
            types_count[w_type] = types_count.get(w_type, 0) + 1

        return {
            "start_date": week_start,
            "end_date": end_date.strftime("%Y-%m-%d"),
            "total_workouts": total_workouts,
            "total_duration_minutes": total_duration,
            "types_breakdown": types_count
        }
    return None


def personal_records(workouts , u_id):
    records = {}

    for w in workouts:
        if w["id"] != u_id:
            continue

        for exercise in w.get("exercise", []):
            name = exercise.get("name", "")
            weight = exercise.get("weight", 0)

            if not name or not weight:
                continue

            try:
                weight_value = float(weight)
            except ValueError:
                continue

            if name not in records or weight_value > records[name]:
                records[name] = weight_value
    return records











