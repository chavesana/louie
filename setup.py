import os
from setuptools import setup, find_packages
import louie

#Grab the README.md for the long description
with open('README.md', 'r') as f:
    long_description = f.read()

VERSION = louie.__version__

def setup_package():
    setup(
        name = "louie",
        version = VERSION,
        author = "Kelvin Rodriguez, Tyler Thatcher",
        author_email = "kr788@nau.edu",
        description = ("Chatbot supporting general use queries"),
        long_description = long_description,
        license = "Public Domain",
        keywords = "chat bot smart city",
        url = "http://packages.python.org/louie",
        packages=find_packages(),
        install_requires=[
            'pandas',
            'psycopg2',
            'pymongo',
            'requests',
            'bottle',
            'wit',
            'python-google-places',
            'wolframalpha',
            'fuzzywuzzy'
            ],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "License :: Public Domain",
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
        ],
    )

if __name__ == '__main__':
    setup_package()
