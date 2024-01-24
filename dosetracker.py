import datetime
import os

# File to store dose information
dose_file = "dose_history.txt"

def save_dose(dose_size, dose_time):
    with open(dose_file, "a") as file:
        file.write(f"{dose_time.isoformat()},{dose_size}\n")

def read_dose_history():
    doses = []
    if os.path.exists(dose_file):
        with open(dose_file, "r") as file:
            for line in file:
                time_str, size = line.strip().split(",")
                doses.append((datetime.datetime.fromisoformat(time_str), int(size)))
    return doses

def display_dose_history(doses, hours=48):
    now = datetime.datetime.now()
    recent_doses = [d for d in doses if now - d[0] <= datetime.timedelta(hours=hours)]
    total_doses_24h = sum(d[1] for d in recent_doses if now - d[0] <= datetime.timedelta(hours=24))
    
    print("\nDose History (Last 48 hours):")
    for dose_time, size in recent_doses:
        print(f"- {size} mg at {dose_time}, {now - dose_time} ago")
    print(f"\nTotal mg in last 24 hours: {total_doses_24h} mg")

def main():
    print("Welcome to Dose Tracker!")
    
    doses = read_dose_history()
    display_dose_history(doses)
    
    if input("Would you like to record a dose? (yes/no) ").lower().startswith("y"):
        manual_time = input("Would you like to log it for a manual time? (yes/no) ").lower().startswith("y")
        if manual_time:
            hour = int(input("Enter the hour (0-23) you took the dose: "))
            now = datetime.datetime.now()
            dose_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if dose_time > now:
                dose_time -= datetime.timedelta(days=1)
        else:
            dose_time = datetime.datetime.now()
        
        dose_size = int(input("Enter the dose size in mg: "))
        save_dose(dose_size, dose_time)
        doses.append((dose_time, dose_size))
    
    display_dose_history(doses)

if __name__ == "__main__":
    main()
