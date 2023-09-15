import importlib
import os

def module_name():
    mod=importlib.import_module(input("Enter module name: "))
    return mod

module_name()

        

