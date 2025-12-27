import json
import uuid
import os
from datetime import datetime

def load_users(path= "Data/users.json" ):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as jason_file:
            return json.load(jason_file)
    except json.JSONDecodeError:
        return []


def save_users(users, path="Data/users.json"):
    with open(path, "w", encoding="utf-8") as jason_file:
        json.dump(users, jason_file, ensure_ascii=False, indent=4)

def register_user(users_list, user_data):
    u_id = str(uuid.uuid4())
    today_date = datetime.today().strftime('%d-%m-%Y')

    new_user = {
        "id": u_id,
        "username": user_data["username"],
        "email": user_data["email"],
        "password": user_data["password"],

        "Profile":{
            "age": int(user_data["age"]),
            "height_cm": int(user_data["height_cm"]),
            "weight_kg": float(user_data["weight_kg"]),
            "activity_level": user_data.get("activity_level", "None"),
            },
        "Goals":{
            "goal_type": user_data["goal_type"],
            "target_weight": float(user_data["target_weight"]),
            "start_date": today_date,
            "end_date": user_data.get("end_date", "Not Specified"),
        },

        "created_at": datetime.now().isoformat()
    }
    users_list.append(new_user)
    return new_user

def authenticate_user(users_list, email, password):
    email_user = email.strip().lower()
    password_user = password.strip()
    for user in users_list:
        db_email = user.get("email", "").strip().lower()
        db_password = user.get("password", "").strip()

        if db_email == email_user and db_password == password_user:
            return user
    return None


def delete_user(users_list, u_id):
    for i, user in enumerate(users_list):
        if user["id"] == u_id:
            del users_list[i]
            return True
    return False


def update_goal(users, user_id, goal_data):
    for user in users:
        if user["id"] == user_id:
            if "goals" not in user:
                user["goals"] = {}
            user["goals"].update(goal_data)
            return user["goals"]
    return {}