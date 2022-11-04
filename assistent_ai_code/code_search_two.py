from utils import *
import os
from glob import glob
import pandas as pd
import openai
openai.api_key = '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'

def get_function_name(code):
    """
    Extract function name from a line beginning with "def "
    """
    assert code.startswith("def ")
    return code[len("def "): code.index("(")]

def get_until_no_space(all_lines, i) -> str:
    """
    Get all lines until a line outside the function definition is found.
    """
    ret = [all_lines[i]]
    for j in range(i + 1, i + 10000):
        if j < len(all_lines):
            if len(all_lines[j]) == 0 or all_lines[j][0] in [" ", "\t", ")"]:
                ret.append(all_lines[j])
            else:
                break
    return "\n".join(ret)

def get_functions(filepath):
    """
    Get all functions in a Python file.
    """
    all_funcs = []
    whole_code = open(filepath).read().replace("\r", "\n")
    all_lines = whole_code.split("\n")
    for i, l in enumerate(all_lines):
        if l.startswith("def "):
            code = get_until_no_space(all_lines, i)
            function_name = get_function_name(code)
            yield {"code": code, "function_name": function_name, "filepath": filepath}
    
    

# get user root directory
# path = input("Enter the path to the directory you want to search: ")
# get the file path from os
# path = '/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/' + 

# get all the files in the directory


path = '/U/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/codeguru_repo.py'
# REMOVE THE FILE FROM THE PATH
def remove_file_from_path(path):
    return path[:path.rfind('/')]

# folder = remove_file_from_path(path)
# print(folder)
root_dir = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/whispering/codeguru_repo.py"

    




    # split everything after the last / to get the file name
    

print("Enter the path to the file you want to search: ")
print(root_dir)


# path to code repository directory
code_root = root_dir
# print(code_root)
# code_files = [y for x in os.walk(code_root) for y in glob(os.path.join(x[0], '*.py'))]
# # only look at files in serverless folder, stipulations folder, and utils folder
# # code_files = [y for x in os.walk(code_root) for y in glob(os.path.join(x[0], '*.py')) if any([i in x[0] for i in ['serverless', 'stipulations', 'utils']])]

# print("Total number of py files:", len(code_files))
all_funcs = []
# for code_file in code_files:
funcs = list(get_functions("/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/code_search_two.py"))
for func in funcs:
    all_funcs.append(func)

print("Total number of functions extracted:", len(all_funcs))

from openai.embeddings_utils import get_embedding

def create_data_frame(all_funcs):

    df = pd.DataFrame(all_funcs)
    df['code_embedding'] = df['code'].apply(lambda x: get_embedding(x, engine='code-search-babbage-code-001'))
    df['filepath'] = df['filepath'].apply(lambda x: x.replace(code_root, ""))
    df.to_csv("assistent_ai_code/output/code_search_openai-python.csv", index=False)
    df.head()

    return df
# def getfunction_path(path):
#     all_funcs = []
#     funcs = list(get_functions(path))
#     for func in funcs:
#         all_funcs.append(func)
#     df = pd.DataFrame(all_funcs)
#     df['code_embedding'] = df['code'].apply(lambda x: get_embedding(x, engine='code-search-babbage-code-001'))
#     df['filepath'] = df['filepath'].apply(lambda x: x.replace(code_root, ""))
#     df.to_csv("assistent_ai_code/output/code_search_openai-python.csv", index=False)
#     df.head()
    
  

from openai.embeddings_utils import cosine_similarity

def search_functions(df, code_query, n=1, pprint=True,n_lines=1000):

    # from openai.embeddings_utils import cosine_similarity    
    # embedding = get_embedding(code_query, engine='code-search-babbage-text-001')
    from openai.embeddings_utils import cosine_similarity    
    embedding = get_embedding(code_query, engine='code-search-babbage-text-001')
    df['similarities'] = df['code_embedding'].apply(lambda x: cosine_similarity(x, embedding))
    res = df.sort_values('similarities', ascending=False).head(n)
    
    
    
    
    if pprint:
        for r in res.iterrows():
            print(r[1].filepath+":"+r[1].function_name + "  score=" + str(round(r[1].similarities, 3)))
            print("\n".join(r[1].code.split("\n")[:n_lines]))
            print('-'*70)
    # i loc
    # print(res.iloc[0].function_name)
        name = res.iloc[0].function_name
        code = res.iloc[0].code
    return name, code
    
    # print(res)
    # return res 

# search_functions("stipulations/_title/", n=1, pprint=True, n_lines=100)


def get_line(path, line_number):
    # this gets the line before the line number, the line number, and the line after the line number
    # then puts them all together and returns them
    with open(path) as f:
    
        data = f.readlines()
    number_above = line_number - 5
    number_two_above = line_number - 4
    number_below = line_number + 1
    number_two_below = line_number + 5
    data[line_number] = data[line_number] + "\n"

    # lines between number_two_above and number_two_below
    lines = data[number_two_above:number_two_below]
    # convert into a string
    lines = "".join(lines)
    #
    return lines
    
    

    

        
        
    
    
    


            
    
        
    

# line = get_line('/Users/canyonsmith/Desktop/enium/stipulations/_title/verify_title.py', input("Enter the line number: "))
# path = '/Users/canyonsmith/Desktop/enium/' + input("Enter the path: ")
# line = get_line(search_dir, int(input("Enter the line number: ")))
# print(line)
# search_functions(line, n=1, pprint=True, n_lines=1000)
# # return the name of the function
# function_name = search_functions(line, n=1, pprint=True, n_lines=1000)['function_name']
# # print(function_name)
# '''1    handler
# Name: function_name, dtype: object
# '''
# # just return the name of the function
# function_name = function_name.to_string(index=False)
# print(function_name)
# file_name = search_functions(line, n=1, pprint=True, n_lines=1000)['filepath']
# command = "format this"

# replace_function(function_name, file_name, edit_code(get_function_code(function_name, file_name),command))


# def get_function_code(function_name, file_name):
#     """
#     Gets the code of a function in a file.
#     :param function_name: The name of the function to get the code of.
#     :param file_name: The name of the file to search in.
#     :return: The code of the function.
#     """
#     with open(file_name, 'r') as file:
#         code = file.read()
#     # first find the function definition:
#     function_def = re.search(r'\n\s*def\s+' + function_name + r'\(', code, re.MULTILINE)
#     if not function_def:
#         raise ValueError("Could not find function definition for " + function_name)
#     function_def = function_def.group()
#     # now find the beginning and end of the function code:
#     function_begin = code.find(function_def)
#     function_end = function_begin + len(function_def)
#     # to find the end, we need to find the next function definition (or the end of the file):
#     next_function_def = re.search(r'\n\s*def\s+[a-zA-Z0-9_]+\(', code[function_end:], re.MULTILINE)
#     if next_function_def:
#         indentation_level = function_def.count('\t') + 1
#         # now get the indentation level, we don't want any lines that have a lesser indentation
#         while code[function_end:].startswith('\t' * indentation_level):
#             function_end += 1
#         function_end += next_function_def.start() - 1
#     else:
#         function_end = len(code)
#     # now get the function code:
#     return code[function_begin:function_end]


# def get_function_code(function_name, file_name):
#     """
#     Gets the code of a function in a file.
#     :param function_name: The name of the function to get the code of.
#     :param file_name: The name of the file to search in.
#     :return: The code of the function.
#     """
#     with open(file_name, 'r') as file:
#         code = file.read()
#     # first find the function definition:
#     function_def = re.search(r'\n\s*def\s+' + function_name + r'\(', code, re.MULTILINE)
#     if not function_def:
#         raise ValueError("Could not find function definition for " + function_name)
#     function_def = function_def.group()
#     # now find the beginning and end of the function code:
#     function_begin = code.find(function_def)
#     function_end = function_begin + len(function_def)
#     # to find the end, we need to find the next function definition (or the end of the file):
#     next_function_def = re.search(r'\n\s*def\s+[a-zA-Z0-9_]+\(', code[function_end:], re.MULTILINE)
#     if next_function_def:
#         indentation_level = function_def.count('\t') + 1
#         # now get the indentation level, we don't want any lines that have a lesser indentation
#         while code[function_end:].startswith('\t' * indentation_level):
#             function_end += 1
#         function_end += next_function_def.start() - 1
#     else:
#         function_end = len(code)
#     # now get the function code:
#     return code[function_begin:function_end]



# def get_files_with_extension(extension, directory='.'):
#     """
#     Finds all the files with the given extension in the given directory.
#     :param extension: The extension to find.
#     :param directory: The directory to search in (defaults to the current directory).
#     :return: A list of all the files with the given extension.
#     """
#     # First, get all the files in the directory:
#     files = glob.glob(directory + '/*')
#     # Now go through all the files and add the ones with the given extension to the list:
#     files_with_extension = []
#     for file in files:
#         if file.endswith(extension):
#             files_with_extension.append(file)
#     return files_with_extension

# def get_files_with_extension(extension, directory='.'):
#     """
#     Finds all the files with the given extension in the given directory.
#     :param extension: The extension to find.
#     :param directory: The directory to search in (defaults to the current directory).
#     :return: A list of all the files with the given extension.
#     """
#     if not directory:
#         raise ValueError('directory cannot be empty')
#     # First, get all the files in the directory:
#     files = glob.glob(directory + '/*')
#     # Now go through all the files and add the ones with the given extension to the list:
#     files_with_extension = []
#     for file in files:
#         if file.endswith(extension):
#             files_with_extension.append(file)
#     return files_with_extension