# setup.py

from setuptools import setup, find_packages

# Read the requirements from requirements.txt file
with open('requirements.txt', 'r') as file:
    requirements = file.read().splitlines()

setup(
    name='mail',
    version='0.1.0',
    description='Description of your package',
    author='Datalab Quinten',
    author_email='datalab@quinten-france.com',
    packages=find_packages(),
    install_requires=requirements,
)
