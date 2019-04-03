""" setup.py: see public setuptools docs for more detail """
from setuptools import setup, find_packages

# This should be a list of dependencies required for production use only
DEPENDENCIES = [
    'awscli==1.16.136',
    'azure-mgmt-compute==4.5.1',    
    'google-cloud==0.34.0'
]

setup(
    name='f5-cloud-sdk',
    version='0.9.0',
    description='F5 Cloud SDK',
    url='http://github.com/F5Networks/f5-cloud-sdk',
    author='F5 Ecosystems Group',
    author_email='solutionsfeedback@f5.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=DEPENDENCIES
)
