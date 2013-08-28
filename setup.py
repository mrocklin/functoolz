from os.path import exists
from setuptools import setup

setup(name='functoolz',
      version='0.3',
      description='More function tools',
      url='http://github.com/mrocklin/functoolz/',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      license='BSD',
      packages=['functoolz'],
      long_description=open('README.md').read() if exists("README.md") else "",
      zip_safe=False)
