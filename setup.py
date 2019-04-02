from setuptools import setup, find_packages

setup(name='f5-cloud-sdk',
      version='0.9.0',
      description='F5 Cloud SDK',
      url='http://github.com/F5Networks/f5-cloud-sdk',
      author='F5 Ecosystems Group',
      author_email='solutionsfeedback@f5.com',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      zip_safe=False)
