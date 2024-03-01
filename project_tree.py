import os
from icecream import ic
from directory_tree import display_tree
current_dir = os.getcwd()

git_root_dir = os.chdir("..")

string_representation = display_tree(
    git_root_dir,
    string_rep=True,
    show_hidden=False)

ic(string_representation)
