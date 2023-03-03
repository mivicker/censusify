import inspect
import ast


def sub_function():
    frame = inspect.currentframe()
    callframe = inspect.getouterframes(frame, 2)
    print(callframe[1])


def parent():
    return sub_function()

sub_function()
parent()
