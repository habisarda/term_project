import json
import os
import shutil
from datetime import datetime


def load_state(base_dir: str) -> tuple:
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    def load_json(filename):
        path = os.path.join(base_dir, filename)
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    users = load_json("users.json")
    workouts = load_json("workouts.json")
    meals = load_json("nutrition.json")
    metrics = load_json("metrics.json")

    return users, workouts, meals, metrics


def save_state(base_dir: str, users: list, workouts: list, meals: list, metrics: list) -> None:
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    def save_json(filename, data):
        path = os.path.join(base_dir, filename)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    save_json("users.json", users)
    save_json("workouts.json", workouts)
    save_json("nutrition.json", meals)
    save_json("metrics.json", metrics)


def backup_state(base_dir: str, backup_dir: str) -> list:
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_files = []

    files = ["users.json", "workouts.json", "nutrition.json", "metrics.json"]

    for filename in files:
        source = os.path.join(base_dir, filename)
        if os.path.exists(source):
            dest = os.path.join(backup_dir, f"{timestamp}_{filename}")
            shutil.copy2(source, dest)
            backup_files.append(dest)

    return backup_files


def validate_workout_entry(entry: dict) -> bool:
    if entry.get("duration", 0) <= 0:
        return False
    if not entry.get("type"):
        return False
    for ex in entry.get("exercises", []):
        if ex.get("exercise_weights", 0) < 0 or ex.get("exercise_reps", 0) < 0:
            return False
    return True