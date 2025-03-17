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
            case default: print("Invalid choice.\n")
                
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
    pass

def delete_course():
    pass

def list_courses():
    pass

def add_student():
    pass

def delete_student():
    pass

def list_students():
    pass

def add_student_course():
    pass

def del_student_course():
    pass

def list_student_courses():
    pass

main()