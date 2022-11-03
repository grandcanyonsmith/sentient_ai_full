import pandas as pd
import sys
import os
        
def read_from_file():
    with open('open_ai_responses.txt', 'r') as file:
        content = file.read()
        print(content)
    
# this function reads the contents of the file conversation_transcript.txt and prints it to the console


def write_to_file_and_delete():
    delete_file()
    write_to_file()
    

def write_to_file_and_read():
    write_to_file()
    read_file()

# create a function that will create a new folder
def create_new_folder():
    """
    This function creates a new folder
    """
    # ask the user for the name of the folder /Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/whispering/main_library.py
    folder_name = input('Enter a name for the folder: ')
    # create a new folder with the name that the user entered
    os.mkdir('/Users/canyonsmith/Desktop/sentient_ai/whispering' + folder_name)
    # print a message to the console
    print('The folder has been created\n')
    # return the folder name
    return folder_name

def create_new_file():
    """
    This function creates a new file
    """
    folder_name = input('Enter a name for the folder: ')
    file_name = input('Enter a name for the file: ')

    # create a new file in the folder that the user entered
    open('/Users/canyonsmith/Desktop/sentient_ai/whispering/' + folder_name + '/' + file_name + '.py', 'w').close()
    # print a message to the console
    print('The file has been created\n')

    
def move_file():
    """
    This function asks the user what file they want to move and then asks the user where they want to move it to.
    If it cannot find the file, it will print a message to the console and then ask the user to enter the file name again.
    """
    # ask the user for the name of the file that they want to move
    file_name = input('Enter the name of the file that you want to move: ')
    # verify that the file exists using fuzzy match
    if file_name in os.listdir():
        # ask the user for the name of the folder that they want to move the file to
        folder_name = input('Enter the name of the folder that you want to move the file to: ')
        # verify that the folder exists using fuzzy match
        if folder_name in os.listdir():
            # move the file to the folder
            os.rename(file_name, folder_name + '/' + file_name)
            # print a message to the console
            print('The file has been moved\n')
        else:
            # print a message to the console
            print('The folder does not exist\n')
            # ask the user to enter the folder name again
            move_file()


def rename_file():
    """
    This function renames the file. It asks the user for the name of the file that they want to rename and then asks the user for the new name of the file.
    After it changes the name of the file, it will adjust all of the imports in the other files.
    """
    # ask the user for the name of the file that they want to rename
    file_name = input('Enter the name of the file that you want to rename: ')
    # verify that the file exists using fuzzy match
    if file_name in os.listdir():
        # ask the user for the new name of the file
        new_file_name = input('Enter the new name of the file: ')
        # rename the file
        os.rename(file_name, new_file_name)
        # print a message to the console
        print('The file has been renamed\n')
        # adjust the imports in the other files
        adjust_imports(file_name, new_file_name)
    else:
        # print a message to the console
        print('The file does not exist\n')
        # ask the user to enter the file name again
        rename_file()

def adjust_imports(file_name, new_file_name):
    """
    If there is an import statement in the other files that imports the file that the user wants to rename, this function will change the name of the file in the import statement.
    """
    # loop through all of the files in the folder
    for file in os.listdir():
        # open the file
        with open(file, 'r') as f:
            # read the contents of the file
            content = f.read()
            # if the file name is in the content
            if file_name in content:
                # replace the file name with the new file name
                content = content.replace(file_name, new_file_name)
                # open the file
                with open(file, 'w') as f:
                    # write the new content to the file
                    f.write(content)


def delete_file():
    """
    This function deletes the file. It asks the user for the name of the file that they want to delete.
    """
    # ask the user for the name of the file that they want to delete
    file_name = input('Enter the name of the file that you want to delete: ')
    # verify that the file exists using fuzzy match
    if file_name in os.listdir():
        # delete the file
        os.remove(file_name)
        # print a message to the console
        print('The file has been deleted\n')
    else:
        # print a message to the console
        print('The file does not exist\n')
        # ask the user to enter the file name again
        delete_file()

from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")

model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")


def select_classification_label():
    text = "get Colby Smith's phone number"
    from transformers import pipeline
    classifier = pipeline("zero-shot-classification",
                        model="facebook/bart-large-mnli")


    sequence_to_classify = text

    # get the columns from the csv file database_info.csv
    #cd into database_info folder

    columns = pd.read_csv('phone_numbers.csv', nrows=1).columns
    #get all the rows from the csv file database_info.csv
    candidate_labels = columns
    print(candidate_labels)
    info_we_want = classifier(
        f"Based on this text, which info do we want: {sequence_to_classify}",
        candidate_labels,
    )

    # now we want out of the candidate labels, the one with the highest score
    # we can do this by creating a dictionary with the candidate labels as the keys and the scores as the values

    candidate_labels_scores = dict(zip(candidate_labels, info_we_want['scores']))
    # now we can sort the dictionary by the values
    sorted_candidate_labels_scores = sorted(candidate_labels_scores.items(), key=lambda x: x[1], reverse=True)
    # now we can get the first item in the list
    what_we_have = sorted_candidate_labels_scores[0][0]
    print(what_we_have)

    what_we_want = classifier(
        f"Based on this text, what info do we want: {sequence_to_classify}",
        candidate_labels,
    )

    # now we want out of the candidate labels, the one with the highest score
    # we can do this by creating a dictionary with the candidate labels as the keys and the scores as the values

    candidate_labels_scores = dict(zip(candidate_labels, what_we_want['scores']))
    # now we can sort the dictionary by the values
    new_sorted_candidate_labels_scores = sorted(candidate_labels_scores.items(), key=lambda x: x[1], reverse=True)
    # now we can get the first item in the list
    what_we_want = new_sorted_candidate_labels_scores[0][0]
    print("want:", what_we_want)
    print("have:", what_we_have)





    # now, using the column info we have, use the sequence to classify to find the info we want
    # for example, using the sequence to classify, "get colbys phone number", the columns are "name", "phone number", "email address"
    # the info we have is "name", and the info we want is "phone number"
    # so, we want to find the phone number for colby
    # we can do this by using the sequence to classify to find the name, and then using the name to find the phone number

    # get the name from the sequence to classify
    row_we_have = classifier(
        f"Based on this text: {sequence_to_classify}, what is the "
        + info_we_have['labels'][0]
        + "? ",
        candidate_labels,
    )

    print("row",row_we_have)

    info_we_have = row_we_have['labels'][0]
    print("info we have", info_we_have)
    info_we_want = info_we_want['labels'][0]
    print("info we want", info_we_want)

    value = get_value_from_database(info_we_have, info_we_want)
    # print the value to the console
    print(value)
    
def get_value_from_database(column, row):
    # get the value from the database
    df = pd.read_csv('phone_numbers.csv')
    return df.loc[df[column] == row, column].iloc[0]












if __name__ == '__main__':
    if len(sys.argv) > 1:  # if the user gives an argument, then use that as the command to run 
        globals()[sys.argv[1]]()
    else: # else just don't mind it and use the default which is nothing
        command = None










