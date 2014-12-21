import os

"""
Open additional data files using the absolute path,
otherwise it doesn't always find the file.
"""
# The absolute path of the directoy for this file:
_ROOT = os.path.abspath(os.path.dirname(__file__))


class Hello:
    def __init__(self):
        return None

    def say_hello(self):
        print "Hello, World!"