"""
This program is used to find all the functions in a file, to find the code of a specific function, and to replace the code of a specific function.
This enables verbal programming by allowing the user to say the name of the function and what it should do, and then the AI model will find the function in the file and replace the code with the new code based on what the user instructed the AI model to do.
"""

import os
import sys
import openai
import re


def find_functions(filename):
    """
    Finds all the functions in a file.
    :param filename: The name of the file to search in.
    :return: A list of all the functions in the file.
    """
    with open(filename, 'r') as file: # open the file
        code = file.read() # read the file
        functions = re.findall(r'\n\s*def\s+([a-zA-Z0-9_]+)\(', code) # find all the functions in the file and put them in a list.
        for function in functions: # print all the functions in the list
            print(function) # print the function
    return functions

get_function_code_

get_function_code_new()

replace_function_name_with_better_name


def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

is_int # Make this function more like the zen of python

digit_sum

'''
Write a recursive method that returns the sum of the digits in a given integer. Use the following method header:
'''

def digit_sum_recur(number):
    if number == 0:
        return 0
    else:
        return number % 10 + digit_sum_recur(number/10)

print digit_sum_recur(123)






def main():
    n = int(input("Enter number: "))
    print("Sum of digits", n, "is", digit_sum_recur(n))


if __name__ == "__main__":
    main()









def factorial(x):
    total = 1
    while x > 1:
        total *= x
        x -= 1
    return total


def is_prime(x):
    if x < 2:
        return False
    else:
        for n in range(2, x - 1):
            if x % n == 0:
                return False
        return True

def reverse(text):
    """Reverse a string iteratively."""
    text_list = list(text)
    idx = len(text_list) - 1
    reversed_list = []
    while idx >= 0:
        reversed_list.append(text_list[idx])
        idx -= 1
    reversed_text = ''.join(reversed_list)
    return reversed_text


def reverse2(text):
    """Reverse a string recursively."""
    text_list = list(text)
    if len(text_list) == 1:
        return text_list[0]
    else:
        return text_list[-1] + reverse2(text_list[:-1])


print reverse("hello")
print reverse2("hello")


def is_palindrome(word):
    return word == word[::-1]


def main():
    print(is_palindrome('racecar'))


if __name__ == '__main__':
    main()










def get_next_letter_in_sequence(my_string):
    """
    :param my_string:
    :return:
    """
    pass

censor
def censor(text,word):
  str = ""
  for i in range(len(word)):
    if i == 0 or i == len(word)-1:
      str+=word[i]
    else:
      str+="*"
  text=text.replace(word,str)
  return text



def count(sequence, item):
    found = 0
    for i in sequence:
        if i == item:
            found += 1
    return found


def purify(numbers):
    new_list = []
    for i in numbers:
        if i % 2 == 0:
            new_list.append(i)
    return new_list


def product(numbers):
    total = 1
    for i in numbers:
        total *= i
    return total


def remove_duplicates(numbers):
    new_list = []
    for i in numbers:
        if i not in new_list:
            new_list.append(i)
    return new_list


def median(numbers):
    numbers.sort()
    if len(numbers) % 2 == 0:
        middle_index_1 = int(len(numbers) / 2) - 1
        middle_index_2 = middle_index_1 + 1
        return (numbers[middle_index_1] + numbers[middle_index_2]) / 2.0
    else:
        middle_index = int(len(numbers) / 2)
        return numbers[middle_index]











def append_code_to_file(file_name, line_number, code):
    """
    Appends the code to the file at the given line number.
    :param file_name: The name of the file.
    :param line_number: The line number to append the code to.
    :param code: The code to append.
    :return: None
    """
    with open(file_name, 'r') as file_:
        file_code = file_.read()
    file_code = file_code.split('\n')
    file_code.insert(line_number, code)
    file_code = '\n'.join(file_code)

    with open(file_name, 'w') as file:
        file.write(file_code)
    return file_code




if __name__ == '__main__':

    function_name = input('Enter a function name: ')
    file_name= input('Enter a file name: ')
    replace_function(function_name, file_name, edit_code(get_function_code(function_name, file_name)))
    # append_code()































































































