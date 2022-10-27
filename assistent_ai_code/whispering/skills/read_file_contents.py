
# re write that import statement
import os
import sys
import subprocess
current_directory = os.getcwd()


from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")

model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")


def select_classification_label(text, labels):
    from transformers import pipeline
    classifier = pipeline("zero-shot-classification",
                        model="facebook/bart-large-mnli")
    sequence_to_classify = text
    # candidate_labels = ['Execute send text', 'Execute write python code', 'Do nothing', 'Send email', 'Create new file']
    labels.append("Get all code")
    candidate_labels = labels
    # candiate_labels = candiate_labels + ["Get all code"]
    # append the labels to the candidate labels
    
    results = classifier(sequence_to_classify, candidate_labels)
    confidence = results['scores'][0]
    best_label = results['labels'][0]
    print(best_label, confidence)
    # return whatever the best label is by what number it is in the list
    # should return a number
    label_index = candidate_labels.index(best_label)
    label_index = str(label_index)
    
    
    return best_label, confidence

# select_classification_label("Edit start_file in websocket client")



def get_directory_contents(command):
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
    # ask the user which file they want to read
    
    user_input = command
    best_label, confidence = select_classification_label(user_input, directory_contents)
    
    # check if the user input is a number


    
    # if best_label.isdigit():
    #     # check if the number is in the range of the directory contents
    #     if int(best_label) in range(len(directory_contents)):
    #         # get the file name
    #         try:
    #             file_name = directory_contents[int(best_label)]
    #         except:
    #             file_name = directory_contents[int(best_label)]
                
                
    #         # check if the file name is a file
    #         if os.path.isfile(file_name):
    #             # read the file
    #             # read_file(file_name)
    #             print("\n")
    #         # check if the file name is a directory
    #         elif os.path.isdir(file_name):
    #             # change the current directory to the new directory
    #             os.chdir(file_name)
    #             # get the contents of the new directory
    #             get_directory_contents()
    #             print("\n")
    #     else:
    #         print("That number is not in the range of the directory contents")
    #         get_directory_contents()
    # else:
    #     print("That is not a number")
    #     get_directory_contents()


    
    return directory_contents, best_label, confidence



    

def read_file(file_name):
    # open the file
    with open(file_name, "r") as f:
        # read the file
        file_contents = f.read()
        
        # ask the user if they want to read another file
        user_input = input("Do you want to read another file? (y/n) ")
        if user_input == "y":
            get_directory_contents()
        elif user_input == "n":
            print("file contents: ", file_contents)
            subprocess.run(["pbcopy"], universal_newlines=True, input=file_contents)
            return file_contents
            
        else:
            print("That is not a valid input")
            read_file(file_name)
        # return a list of the file contents split by line
        return file_contents.split("\n")



