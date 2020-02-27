""" setup.py: see public setuptools docs for more detail """
from setuptools import setup, find_packages

# This should be a list of dependencies required for production use only
DEPENDENCIES = [
    'requests',
    'retry',
    'paramiko'
]

setup(
    name='f5-sdk-python',
    version='0.9.0',
    description='F5 SDK',
    url='https://***REMOVED***/automation-sdk/f5-sdk-python',
    author='F5 Ecosystems Group',
    author_email='solutionsfeedback@f5.com',
    license='Apache License 2.0',
    packages=find_packages(exclude=["test*", "tests*", "test_*", "test.*", "*.test"]),
    install_requires=DEPENDENCIES,
    package_data={'': ['*.json', '*.yaml', '*.md', '*.rst']}
)
