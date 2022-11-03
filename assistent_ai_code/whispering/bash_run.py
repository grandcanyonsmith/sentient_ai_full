# a python script to run bash.sh 

import os
import subprocess
import sys
import time


# this function runs that deletes the file hello_world.py and then creates a new file with the same name
# make it print hello oklahoma

def edit_hello_world():
    os.remove('/Users/bottega/Desktop/sentient_ai/hello_world.py')

    open('/Users/bottega/Desktop/sentient_ai/hello_world.py', 'w').close()

    with open('/Users/bottega/Desktop/sentient_ai/hello_world.py', 'a') as f:

        f.write('print(\'Hello Oklahoma\')')
        f.close()
edit_hello_world()

new_file_name = input('Enter a new file name: ')
# this function renames the file hello_world.py to the name that the user entered



# this function deletes the bash.sh file and then creates a new file with the same name

def rename_file(new_file_name):
    """
    This function renames the file.
    """
    
    os.rename(
        '/Users/bottega/Desktop/sentient_ai/hello_world.py',
        f'/Users/bottega/Desktop/sentient_ai/{new_file_name}.py',
    )


    print('The file has been renamed')

    run_bash_script(new_file_name)



def delete_bash_script(new_file_name):
    # remove the file bash.sh
    os.remove('/Users/bottega/Desktop/sentient_ai/bash.sh')
    # create a new file with the same name
    open('/Users/bottega/Desktop/sentient_ai/bash.sh', 'w').close()
    # open the file bash.sh in append mode
    with open('/Users/bottega/Desktop/sentient_ai/bash.sh', 'a') as f:
        # write the contents to the file
        f.write(f'python3 /Users/bottega/Desktop/sentient_ai/{new_file_name}.py& exit')
        # close the file
        f.close()
        # print a message
        print('The bash.sh file has been deleted and a new file has been created\n')
        # print a message
        # run the python script


# this function runs the bash script

def run_bash_script(new_file_name):
    # run the bash script
    subprocess.call(['bash', '/Users/bottega/Desktop/sentient_ai/bash.sh', new_file_name])
    # print a message to the terminal
    print('The bash script has been run')
    # run the python script

    



new_file_name = input('Enter a new file name: ')
rename_file(new_file_name)
delete_bash_script(new_file_name)
run_bash_script(new_file_name)











