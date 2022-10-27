import sys
import os


def hello_world():
    print("Hello World!")


def goodbye_world():
    print("Goodbye World!")

if __name__ == '__main__':
    if len(sys.argv) > 1:  # if the user gives an argument, then use that as the command to run 
        globals()[sys.argv[1]]()
    else: # else just don't mind it and use the default which is nothing
        command = None

        

    

    







