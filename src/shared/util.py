import os


def get_data_dir():
    """
    Get the path to the history file
    """
    home = os.path.expanduser("~")
    dir = os.path.join(home, ".heyai")
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir
