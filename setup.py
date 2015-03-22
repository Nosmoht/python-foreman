""" package setup
"""

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()

def requirements():
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()

setup(name='python-foreman',
      version='0.11.1',
      description='Python class to communicate with Foreman via API v2',
      long_description=readme(),
      keywords=['foreman'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
      author='Thomas Krahn',
      author_email='ntbc@gmx.net',
      license='MIT',
      url='https://github.com/Nosmoht/python-foreman',
      packages=['foreman'],
      install_requires=requirements(),
      )
