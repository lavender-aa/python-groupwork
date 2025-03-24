# Program: Assignment 3
# Authors: Group 8
#       - Brianna Dulik
#       - Lavender Wilson
#       - Nik Roebuck


# notes:
# 
# - courses: dictionary (key=code, val=title)
# - students: dictionary of dictionaries (use IDs as key for parent)

# global variables (dicts)
courses = {}
students = {}

# main loop (menu)
def main():

    get_data_from_files()
    while True:
        print_menu()
        try: choice = input("\nSelect an option: ")
        except KeyboardInterrupt: return
        
        try: choice = int(choice)
        except ValueError:
            print("Invalid choice.")
            continue
        
        match(choice):
            case 0:
                print("Quitting program.")
                store_data()
                return
            case 1: add_course()
            case 2: delete_course()
            case 3: list_courses()
            case 4: add_student()
            case 5: delete_student()
            case 6: list_students()
            case 7: add_student_course()
            case 8: del_student_course()
            case 9: list_student_courses()
            case _: print("Invalid choice.\n")

# read data from file (if it exists)
# file: CMSC3380_Assignment3_8.dat
def get_data_from_files():
    pass

# save the data to a binary file
# file: CMSC3380_Assignment3_8.dat
def store_data():
    pass
                
def print_menu():
    print("\nOptions:\n--------")
    print("\t[0] Quit")
    print("\t[1] Add a course")
    print("\t[2] Delete a course")
    print("\t[3] List all courses")
    print("\t[4] Add a student")
    print("\t[5] Delete a student")
    print("\t[6] List all students")
    print("\t[7] Add course to student")
    print("\t[8] Delete course from student")
    print("\t[9] List a student's courses")
    
def add_course():
    code = input("Enter course code: ")
    name = input("Enter course name: ")
    courses[code] = name

def delete_course():
    code = input("Enter the code of the course to delete: ")
    
    if code in courses.keys():
        del courses[code]
        print("Removed course.")
    else:
        print("Course " + code + " does not exist.")

def list_courses():
    for code, name in courses.items():
        print(code, name)

# student dict: name, major, email, course codes
# main dict: IDs, students
def add_student():
    id = input("Enter the student's ID: ")
    while id in students.keys():
        print("A student with this ID already exists.")
    name = input("Enter the student's name: ")
    major = input("Enter the student's major: ")
    email = input("Enter the student's email: ")
    student = {"name":name, "major":major, "email":email, "courses":[]}
    students[id] = student
    

def delete_student():
    id = input("Enter ID of student to remove: ")
    if id in students.keys():
        del students[id]
        print("Removed student.")
    else:
        print("No student has that ID.")

def list_students():
    for id, student in students.items():
        print("ID: " + id)
        print("Name: " + student["name"])
        print("Major: " + student["major"])
        print("Email: " + student["email"])
        print()

def add_student_course():
    id = input("ID of student to add course to: ")
    if id in students.keys():
        code = input("Enter course code to add: ")
        if code in courses.keys():
            students[id]["courses"].append(code)
        else:
            print("Course does not exist.")
    else:
        print("No student has that ID.")

def del_student_course():
    id = input("ID of student to remove course from: ")
    if id in students.keys():
        code = input("Enter code of course to remove: ")
        if code in courses.keys():
            students[id]["courses"].remove(code)
        else:
            print("Course does not exist.")
    else:
        print("No student has that ID.")

def list_student_courses():
    id = input("Enter ID of student to show courses: ")
    if id in students.keys():
        for code in students[id]["courses"]:
            print(code, courses[code])
    else:
        print("No student has that ID.")

main()