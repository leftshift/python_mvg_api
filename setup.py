"""Library for fetching departure and route data from the Munich public transport organisation MVG

Github:
https://github.com/leftshift/python_mvg_api
Docs:
http://python-mvg-departures.readthedocs.io/en/latest/
"""

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mvg_api',
    version='1.2.7',
    description='Library for fetching departure and route data from the Munich public transport organisation MVG',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/leftshift/python_mvg_api',

    author='leftshift',
    author_email='leftshiftlp@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    packages=['mvg_api'],
    install_requires=['requests'],
)
