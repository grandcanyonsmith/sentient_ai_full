import os

print_tree


# This line is added
def print_tree(self, node=None, prefix="", is_left=True):
    if node is None:
        print(self.root)
        node = self.root
    if node.left != None:
        left = node.left.value
    else:
        left = "None"

    if node.right != None:
        right = node.right.value
    else:
        right = "None"
    print(prefix + ("├──" if is_left else "└──" + str(node.value)))
    print_tree(self, node.left, prefix + ("|   " if is_left else "    "), True)
    print_tree(self, node.right, prefix + ("|   " if is_left else "    "), False)

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

from os import listdir

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Get all file paths with the given extension.

This function returns a list of all the file paths with the given
extension. This is done recursively.

Args:
    path (str): The path to search in.
    extension (str): The file extension to look for.

Returns:
    list: List of file paths with the given extension found in the given path.

"""

__author__ = 'bryan'

from os import listdir, path

import os

[Dockerfile]


