import os, sys

def sys_path_append_parent_dir(n_up):
    here = os.path.abspath(__file__)
    ups = ""
    if n_up:
        ups = os.path.join(*([".."] * n_up))
    parent_dir = os.path.join(os.path.dirname(here), ups)
    sys.path.append(parent_dir)
