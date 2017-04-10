from setuptools import setup
import os

setup(
    name='fake',
    packages=['fake'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
