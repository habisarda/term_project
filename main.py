import os
import sys
import profiles


data_file = "Data/users.json"


def screen():
    os.system("clear")

def main():
    print("Opening Fitness Tracking")
    users = profiles.load_users(data_file)

    current_user = None

    while True:
        print("\n=== FITNESS TRACKING ===")

        if current_user:
            print(f"Welcome,{current_user['username']}")
            print("1-) My Workouts ")
            print("2-) Nutrition")
            print("3-) Metrics")
            print("4) Logout")

            choice = input("Enter your choice: ")

            if choice == "4":
                current_user = None
                print("Logged Out")
        #Diğer özellikleri sonra ekliğeceğim

        else:
            print("1-) Sign In")
            print("2-) Sign Up")
            print("3-) Exit")

            choice_2 = input("Enter your choice: ")

            if choice_2 == "1":
                print("\n--- LOGIN ---")
                email = input("Enter your email: ")
                pw = input("Enter your password: ")
                registered_user = profiles.authenticate_user(users,email, pw)
                if registered_user:
                    print("Successfully logged in")
                    current_user = registered_user
                else:
                    print("Incorrect email or password!")





            elif choice_2 == "2":
                print("\n--- NEW MEMBER REGISTRATION ---")
                name = input("Username: ")
                mail = input("Email address: ")
                password = input("Password: ")
                age = int(input("Age: "))
                height_cm = int(input("Height: "))
                weight_kg = float(input("Weight: "))
                goal = input("Goal (Lose Weight / Gain Muscle ")
                goal_weight = float(input("Goal Weight: "))

                new_data = {
                    "username": name,
                    "email": mail,
                    "password": password,
                    "age": age,
                    "height_cm": height_cm,
                    "weight_kg": weight_kg,
                    "goal_type": goal,
                    "target_weight": goal_weight
                }
                profiles.register_user(users, new_data)
                profiles.save_users(users, data_file)
                print("User Registered Successfully,Please Login to continue")





            elif choice_2 == "3":
                print("Goodbye")
                break
            else:
                print("Invalid choice")


if __name__ == "__main__":
    main()