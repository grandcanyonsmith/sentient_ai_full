import os

def print_tree(path, level=0):
    """
    Prints a tree of the given path.
    :param path: The path to print the tree of.
    :param level: The current level in the tree.
    :return: None
    """
    # first print the current file:
    print('\t' * level + '|- ' + path.split('/')[-1])
    # now check if it's a directory:
    if os.path.isdir(path):
        # if so, print all the files and subdirectories in it:
        for file in os.listdir(path):
            print_tree(path + '/' + file, level + 1)

# Now print the tree of the current directory:
print_tree('.')

# Now create a function that can print a file tree of any directory:
def print_tree_with_root(root_path):
    """
    Prints a tree of the given path.
    :param root_path: The path to print the tree of.
    :return: None
    """
    # first print the root directory:
    print(root_path)
    # now print all the files and subdirectories:
    for file in os.listdir(root_path):
        print_tree(root_path + '/' + file)



# Now create a function that can find all the files with the given extension:
import glob

def get_files_with_extension(extension, directory='.'):
    """
    Finds all the files with the given extension in the given directory.
    :param extension: The extension to find.
    :param directory: The directory to search in (defaults to the current directory).
    :return: A list of all the files with the given extension.
    """
    # First, get all the files in the directory:
    files = glob.glob(directory + '/*')
    # Now go through all the files and add the ones with the given extension to the list:
    files_with_extension = []
    for file in files:
        if file.endswith(extension):
            files_with_extension.append(file)
    return files_with_extension

print(get_files_with_extension('.py'))

print(print_tree('.'))
print(print_tree_with_root('.'))

def  get_user_input():
    """
    Asks the user what they would like to do to the file.
    :return:
    """
    # get the file name from the user:
    file_name = input('What file would you like to make changes to? (e.g. main.py)')
    # check if the file exists:
    if not os.path.isfile(file_name):
        raise Exception('File does not exist')

    # ask the user what they would like to do:
    print('What would you like to do?\n1. Find all functions\n2. Get the code of a function\n3. Replace the code of a function')
    # get the option from the user:
    option = input('Enter the number of the option you would like to do:')
    # if the option is find all functions:
    if option == '1':
        find_functions(file_name)
    # if the option is get the code of a function:
    elif option == '2':
        function_name = input('What function would you like to get the code of?')
        code = get_function_code(function_name, file_name)
        print(code)
    # if the option is replace the code of a function:
    elif option == '3':
        function_name = input('What function would you like to replace the code of?')
        new_code = input('What would you like the new code to be?')
        replace_function(function_name, file_name, new_code)
    # if the option is not valid:
    else:
        raise Exception('Option is not valid')
