# this file contains the variables that are used in controlling openai's behaviour

# this file gives the user the option to choose between the following commands:
# 1. read openai's variables settings
# 2. change openai's variables settings
# 3. exit

# the path to the file # path /Users/bottega/Desktop/sentient_ai/openai/environment_variables_openai.csv

# variables
'''
variable,value
temperature,0.1
top_p,0.9
top_k,0
frequency_penalty,0.0
presence_penalty,0.0

'''

# this function reads the contents of the file csv file, converts it to a list of dictionaries and returns it
def read_csv_file():
    with open('/Users/bottega/Desktop/sentient_ai/openai/environment_variables_openai.csv', 'r') as f:
        # read the contents of the file but don't include the first line
        contents = f.readlines()[1:]
        # convert the contents to a list of dictionaries
        contents = [dict(zip(['variable', 'value'], line.strip().split(','))) for line in contents]
        # return the contents
        return contents

# given a variable name, this function edits the value of the variable in the csv file
def edit_variable(variable_name, new_value):
    contents = read_csv_file()
    for i in range(len(contents)):
        if contents[i]['variable'] == variable_name:
            contents[i]['value'] = new_value
    with open('/Users/bottega/Desktop/sentient_ai/openai/environment_variables_openai.csv', 'w') as f:
        # write the first line
        f.write('variable,value\n')
        # loop through the contents
        for i in range(len(contents)):
            # write the contents to the file
            f.write(f'{contents[i]["variable"]},{contents[i]["value"]}\n')
        f.close()
        return contents

def print_variables():
    # read the contents of the csv file
    contents = read_csv_file()
    print('variable,value\n')
    # loop through the contents
    for i in range(len(contents)):
        # print the variable name and the value of the variable
        print(contents[i]['variable'] + ': ' + contents[i]['value'])


# this is a function that asks the user to enter a variable name and a new value for the variable
def change_variable():
    # ask the user to select a variable name from the list of variables in the terminal
    import os
    os.system('clear')
    print('Select a variable name from the list below:')
    # read the contents of the csv file
    print_variables()
    # allow the user to select a variable name using the keyboard
    variable_name = input('Enter a variable name: ')
    # ask the user to enter a new value for the variable
    new_value = input('Enter a new value for the variable: ')
    # edit the variable
    edit_variable(variable_name, new_value)
    # now print all the variables and their values
    print('The variables and their values are now:')
    # read the contents of the csv file
    print_variables()

change_variable()