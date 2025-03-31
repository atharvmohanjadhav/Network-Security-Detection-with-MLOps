"""
The setup.py file is an essential part of packaging and distributing Python projects. 
It is used by setup tools to define the congiguration of project, such as its metadata,dependencies and more.

"""
from setuptools import find_packages,setup
"""
find_packages module helps to find the packages mean the folder which have __init__.py file then
it consider that folder as package.
"""
from typing import List

def get_requirements()-> List[str]:
    """
    This function will return list of requirements

    """
    requirement_list:List[str] = []
    try:
        with open("requirements.txt","r") as file:
            lines = file.readlines() # read lines from file
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found!")

    return requirement_list

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Atharv Mohan Jadhav",
    author_email="atharvjadhav2910@gmail.com",
    packages=find_packages(),
    install_requires =get_requirements()
)