import os
import sys
from datetime import datetime
import profiles
import workouts
import nutrition
import metrics
import storage

BASE_DATA_DIR = "Data"
BACKUP_DIR = "Backups"


def input_validation(prompt, data_type):
    while True:
        user_input = input(prompt)
        try:
            value = data_type(user_input)
            if isinstance(value, (int, float)) and value < 0:
                print("Please enter a number greater than 0")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")


def main():
    print("Opening Fitness Tracking Application...")

    users, workouts_list, nutrition_list, metrics_list = storage.load_state(BASE_DATA_DIR)

    current_user = None

    while True:
        print("\n=== FITNESS TRACKING ===")

        if current_user:
            print(f"Welcome, {current_user['username']}")
            print("1) Workouts")
            print("2) Nutrition")
            print("3) Metrics & Goals")
            print("4) Profile & System")
            print("5) Logout")

            choice = input("Enter your choice: ")

            if choice == "5":
                current_user = None
                print("Logged Out successfully.")

            elif choice == "1":
                while True:
                    print("\n--- WORKOUTS ---")
                    print("1) Log Workout")
                    print("2) Weekly Summary")
                    print("3) Personal Records")
                    print("4) Update/Delete Workout")
                    print("5) Return")

                    w_choice = input("Choice: ")
                    if w_choice == "5": break

                    if w_choice == "1":
                        w_type = input("Type (Cardio/Strength): ")
                        dur = input_validation("Duration (min): ", int)
                        note = input("Notes: ")

                        ex_list = []
                        while True:
                            nm = input("Exercise Name (q to finish): ")
                            if nm.lower() == 'q': break
                            sets = input_validation("Sets: ", int)
                            reps = input_validation("Reps: ", int)
                            wgt = input_validation("Weight (kg): ", float)
                            ex_list.append({"exercise_name": nm, "exercise_sets": sets, "exercise_reps": reps,
                                            "exercise_weights": wgt})

                        data = {"user_id": current_user["id"], "type": w_type, "duration": dur, "notes": note,
                                "exercises": ex_list}

                        if storage.validate_workout_entry(data):
                            workouts.log_workout(workouts_list, data)
                            storage.save_state(BASE_DATA_DIR, users, workouts_list, nutrition_list, metrics_list)
                            print("Saved!")
                        else:
                            print("Invalid Data, not saved.")

                    elif w_choice == "2":
                        date = input("Start Date (YYYY-MM-DD): ")
                        res = workouts.weekly_workout_summary(workouts_list, current_user["id"], date)
                        print(f"Summary: {res}")

                    elif w_choice == "3":
                        recs = workouts.personal_records(workouts_list, current_user["id"])
                        for k, v in recs.items():
                            print(f"{k}: {v} kg")

                    elif w_choice == "4":
                        print("--- DELETE WORKOUT ---")
                        d_id = input("Enter ID to delete: ")
                        if workouts.delete_workout(workouts_list, d_id):
                            storage.save_state(BASE_DATA_DIR, users, workouts_list, nutrition_list, metrics_list)
                            print("Deleted.")
                        else:
                            print("Not found.")

            elif choice == "2":
                while True:
                    print("\n--- NUTRITION ---")
                    print("1) Log Meal")
                    print("2) Daily Summary")
                    print("3) Macro Breakdown")
                    print("4) Return")

                    n_choice = input("Choice: ")
                    if n_choice == "4": break

                    if n_choice == "1":
                        m_type = input("Type (Breakfast/Lunch/Dinner): ")
                        cal = input_validation("Calories: ", float)
                        prot = input_validation("Protein (g): ", float)
                        carb = input_validation("Carbs (g): ", float)
                        fat = input_validation("Fats (g): ", float)

                        data = {
                            "user_id": current_user["id"], "meal_type": m_type, "calories": cal,
                            "macros": {"protein_g": prot, "carbs_g": carb, "fats_g": fat}
                        }
                        nutrition.log_meal(nutrition_list, data)
                        storage.save_state(BASE_DATA_DIR, users, workouts_list, nutrition_list, metrics_list)
                        print("Saved!")

                    elif n_choice == "2":
                        date = input("Date (YYYY-MM-DD): ")
                        res = nutrition.daily_calorie_summary(nutrition_list, current_user["id"], date)
                        print(f"Total Calories: {res['total_calories']}")

                    elif n_choice == "3":
                        start = input("Start (YYYY-MM-DD): ")
                        end = input("End (YYYY-MM-DD): ")
                        res = nutrition.macro_breakdown(nutrition_list, current_user["id"], (start, end))
                        print(f"P: {res['protein']}g, C: {res['carbs']}g, F: {res['fats']}g")

            elif choice == "3":
                while True:
                    print("\n--- METRICS & GOALS ---")
                    print("1) Log Metric")
                    print("2) Metric Summary")
                    print("3) Goal Progress")
                    print("4) ASCII Chart")
                    print("5) Return")

                    m_choice = input("Choice: ")
                    if m_choice == "5": break

                    if m_choice == "1":
                        wgt = input_validation("Weight (kg): ", float)
                        slp = input_validation("Sleep (hrs): ", float)
                        wtr = input_validation("Water (L): ", float)
                        mood = input("Mood: ")

                        data = {"user_id": current_user["id"], "weight": wgt, "sleep": slp, "water": wtr, "mood": mood}
                        metrics.log_metric(metrics_list, data)
                        storage.save_state(BASE_DATA_DIR, users, workouts_list, nutrition_list, metrics_list)
                        print("Saved!")

                    elif m_choice == "2":
                        m_type = input("Metric Type (weight/water/sleep): ")
                        start = input("Start (YYYY-MM-DD): ")
                        end = input("End (YYYY-MM-DD): ")
                        res = metrics.metrics_summary(metrics_list, current_user["id"], m_type, (start, end))
                        print(res)

                    elif m_choice == "3":
                        res = metrics.goal_progress(users, metrics_list, current_user["id"])
                        print(f"Current: {res['current_weight']} kg, Target: {res['target_weight']} kg")
                        print(f"Status: {res['status']}")

                    elif m_choice == "4":
                        my_metrics = [m.get("weight", 0) for m in metrics_list if m["user_id"] == current_user["id"]]
                        print(metrics.generate_ascii_chart(my_metrics))

            elif choice == "4":
                while True:
                    print("\n--- SYSTEM & PROFILE ---")
                    print("1) Update Goal")
                    print("2) Backup Data")
                    print("3) Delete Account")
                    print("4) Return")

                    p_choice = input("Choice: ")
                    if p_choice == "4": break

                    if p_choice == "1":
                        target = input_validation("New Target Weight: ", float)
                        profiles.update_goal(users, current_user["id"], {"target_weight": target})

                        if "goals" not in current_user:
                            current_user["goals"] = {}
                        current_user["goals"]["target_weight"] = target

                        storage.save_state(BASE_DATA_DIR, users, workouts_list, nutrition_list, metrics_list)
                        print("Goal updated.")

                    elif p_choice == "2":
                        files = storage.backup_state(BASE_DATA_DIR, BACKUP_DIR)
                        print("Backup created:")
                        for f in files: print(f)

                    elif p_choice == "3":
                        confirm = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirm.lower() == "yes":
                            if profiles.delete_user(users, current_user["id"]):
                                storage.save_state(BASE_DATA_DIR, users, workouts_list, nutrition_list, metrics_list)
                                print("Account deleted.")
                                current_user = None
                                break
                            else:
                                print("Error deleting account.")

        else:
            print("1) Sign In")
            print("2) Sign Up")
            print("3) Exit")

            choice_2 = input("Enter your choice: ")

            if choice_2 == "1":
                email = input("Email: ")
                pw = input("Password: ")
                user = profiles.authenticate_user(users, email, pw)
                if user:
                    current_user = user
                    print("Logged in!")
                else:
                    print("Failed.")

            elif choice_2 == "2":
                print("Registering...")
                name = input("Username: ")
                email = input("Email: ")
                pw = input("Password: ")
                age = input_validation("Age: ", int)

                new_u = {"username": name, "email": email, "password": pw, "age": age}
                profiles.register_user(users, new_u)
                storage.save_state(BASE_DATA_DIR, users, workouts_list, nutrition_list, metrics_list)
                print("Registered! Please login.")

            elif choice_2 == "3":
                print("Goodbye!")
                break


if __name__ == "__main__":
    main()