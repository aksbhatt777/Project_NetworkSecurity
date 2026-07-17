'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools to define the configuration 
of our project, such as its metadata, dependencies, and more
'''

from setuptools import find_packages,setup
from typing import List 

def get_requirements()->List[str]:
    """
    RETURNS LIST OF STRING 
    """ 
    requirement_list:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #Read lines from the file
            lines=file.readlines()
            ## Process each line
            for line in lines:
                requirement=line.strip()
                ## ignore empty lines and -e .
                if requirement and requirement!= '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    
    return requirement_list

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Akshat Bhatt",
    author_email="harshil65d@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)