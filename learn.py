# Initialize a dictionary to store student names and their attendance counts
attendance_record = {}

def register():
    """
    Register students by inputting their names separated by spaces.
    Each student is added to the attendance_record with an initial attendance count of 0.
    """
    print("Enter student names to register, separated by spaces:")
    input_str = input().lower()  # Convert input to lowercase for consistency
    # Split input into a list, strip whitespace, and remove empty entries
    student_names = [name.strip() for name in input_str.split() if name.strip()]
    for name in student_names:
        if name not in attendance_record:
            attendance_record[name] = 0  # Add student with initial count of 0
            print(f"{name} registered successfully")
        else:
            print(f"{name} is already registered")

def daily_attendance():
    """
    Record daily attendance by inputting names of students who attended, separated by spaces.
    For each unique student, if they are registered, increment their attendance count.
    """
    print("Enter names of students who attended today, separated by spaces:")
    input_str = input().lower()  # Convert input to lowercase
    # Use a set to avoid duplicate attendance records in one session
    attended_names = set([name.strip() for name in input_str.split() if name.strip()])
    for name in attended_names:
        if name in attendance_record:
            attendance_record[name] += 1  # Increment attendance count
            print(f"Attendance recorded for {name}")
        else:
            print(f"{name} is not registered")

def view_attendance():
    """
    Display the current attendance record, sorted alphabetically by student name.
    """
    print("Current attendance record:")
    for student in sorted(attendance_record):  # Sort for readability
        print(f"{student}: {attendance_record[student]}")

def main():
    """
    Main function to control the program flow with a menu.
    Allows multiple actions until the user chooses to exit.
    """
    while True:
        print("\nChoose an action:")
        print("1. Register students")
        print("2. Record attendance")
        print("3. View attendance")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register()
        elif choice == '2':
            daily_attendance()
        elif choice == '3':
            view_attendance()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

# Start the program
main()