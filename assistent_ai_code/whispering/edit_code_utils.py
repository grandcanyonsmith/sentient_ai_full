"""
This program is used to find all the functions in a file, to find the code of a specific function, and to replace the code of a specific function.
This enables verbal programming by allowing the user to say the name of the function and what it should do, and then the AI model will find the function in the file and replace the code with the new code based on what the user instructed the AI model to do.
"""
from skills.read_file_contents import get_directory_contents, select_classification_label
# from assistent_ai_code.whispering.classify_text import classify_text
import os
import sys
import openai
import re




import os.path
import re

import macro

if __name__ == "__main__":
    print("Hello World!")

import os

def get_files_list(path):
    """This function get a list of files. This function
    can only access files in its directory and not the
    sub directories.

    Args:
        path(str): string containing the path

    Returns:
        files(list): a list of files
    """
    import os
    files = [file for file in os.listdir(path) if os.path.isfile(path + "/" + file)]
    return files

if __name__ == "__main__":
    print get_files_list("path/to/directory")




def get_comments(self, max_results=None):
    """
    List all the comments for the public section of your talk

    Example:

    >>> for comment in talk.get_comments():
    ...     print comment.content

    :rtype: list of :class:`Comment`
    """

url = self.comments_api_url

comments = []

while True:
    response = self._get(url)

    comments.extend(Comment(comment) for comment in response.get('comments', []))

    if response.get('next_page') is None or max_results and len(comments) >= max_results:
        break

    url = response['next_page']

    return comments[:max_results]



def function():
    """Docstring
    """

def replace_function(A):
    """
    Returns value A.
    
    >>> replace_function('A')
    'A'

    """
    return A

if __name__ == '__main__':
    import doctest
    import os
    os.environ['TERM'] = 'linux' # Suppress ^[[?1034h
    doctest.testmod()
"main"

def main():
	"""Function definition is here"""
	pass

"""
function to ask user for a float and return the float
"""

def return_float():
    """
    Ask user for a float and return the float
    """
    while True:
        try:
            return float(input("Please enter a number: "))
        except ValueError:
            print("That was not a number")

if __name__ == "__main__":
    print("\n", return_float())



def calc_function(function, value_1, value_2):
    """
    :param function: function
    :param value_1: int
    :param value_2: int
    :return: result of function applied to two values
    """
    return function(value_1, value_2)


def add(value_1, value_2):
    """
    :param value_1: int
    :param value_2: int
    :return: addition result of two values
    """
    return value_1 + value_2


def subtract(value_1, value_2):
    """
    :param value_1: int
    :param value_2: int
    :return: subtraction result of two values
    """
    return value_1 - value_2


def multiply(value_1, value_2):
    """
    :param value_1: int
    :param value_2: int
    :return: multiplication result of two values
    """
    return value_1 * value_2


def divide(value_1, value_2):
    """
    :param value_1: int
    :param value_2: int
    :return: division result of two values
    """
    return value_1 / value_2








