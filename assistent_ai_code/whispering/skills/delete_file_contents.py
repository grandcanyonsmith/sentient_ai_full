# this program deletes the contents of a file or directory
# 1. it imports the module from read_file_contents.py to get the directory contents
# 2. it asks the user to enter the number of the file or directory they want to delete. It accepts only numbers, but it can accept multiple numbers separated by a space
# 3. it checks if the user input is a number
# 4. it checks if the number is in the range of the directory contents
# 5. it gets the file name
# 6. it checks if the file name is a file
# 7. it deletes the file
# 8. it checks if the file name is a directory
# 9. it deletes the directory
# 10. it asks the user if they want to delete another file or directory
# 11. it checks if the user input is y or n


import os
import sys
import subprocess
from read_file_contents import get_directory_contents

def delete_file_contents():
    # get the current directory
    current_directory = os.getcwd()
    # get the contents of the current directory
    directory_contents = os.listdir(current_directory)
    # print the contents of the current directory
    for index, item in enumerate(directory_contents):
        if os.path.isdir(item):
            print("🗂", index, item)
        elif os.path.isfile(item):
            print("📄", index, item)
    print("\n\n")
    user_input = input("Enter the number of the file or directory you would like to delete: ")
    # check if the user input is a number
    if user_input.isdigit():
        # check if the number is in the range of the directory contents
        if int(user_input) in range(len(directory_contents)):
            # get the file name
            file_name = directory_contents[int(user_input)]
            # check if the file name is a file
            if os.path.isfile(file_name):
                # delete the file
                os.remove(file_name)
                print("The file has been deleted")
                print("\n")
            # check if the file name is a directory
            elif os.path.isdir(file_name):
                # delete the directory
                os.rmdir(file_name)
                print("The directory has been deleted")
                print("\n")
        else:
            print("That number is not in the range of the directory contents")
            delete_file_contents()
    else:
        print("That is not a number")
        delete_file_contents()
    print("\n\n")
    # ask the user if they want to delete another file or directory
    user_input = input("Would you like to delete another file or directory? (y/n): ")
    if user_input == "y":
        delete_file_contents()
    elif user_input == "n":
        return
    else:
        print("That is not a valid input")
        delete_file_contents()
    # get the contents of the current directory
    directory_contents = os.listdir(current_directory)
    # print the contents of the current directory
    for index, item in enumerate(directory_contents):
        if os.path.isdir(item):
            print("🗂", index, item)
        elif os.path.isfile(item):
            print("📄", index, item)
    print("\n\n")
# run the program
delete_file_contents()