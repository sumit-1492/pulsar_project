from setuptools import setup, find_packages
from typing import List

PROJECT_NAME = "pulsarclassification"
VERSION = "0.0.1"
AUTHOR = "sumit1492"
DESCRIPTION = "This is a complete end to end machine learning classification project on pulsar dataset"
REQUIREMENT_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirement_list() -> List[str]:

    with open(REQUIREMENT_FILE_NAME) as library_file:

        requirements_list = library_file.readlines()

        requirements_list = [ required_library.replace("\n", "") for required_library in requirements_list]

        if HYPHEN_E_DOT in requirements_list:

            requirements_list.remove(HYPHEN_E_DOT)

        return requirements_list

setup( 
    name = PROJECT_NAME,
    version = VERSION,
    author = AUTHOR,
    description = DESCRIPTION,
    package_dir={"": "src"},
    packages = find_packages(where="src"),
    install_requires = get_requirement_list()
    )