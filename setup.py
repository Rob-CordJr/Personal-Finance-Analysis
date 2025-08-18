from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:

    requirements = list()
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements



setup(
    name = 'Personal Finance Analysis',
    version = '0.0.1',
    author = 'Roberto Cordeiro',
    author_email = 'robertodossantos747@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)