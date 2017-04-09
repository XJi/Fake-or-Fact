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

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
