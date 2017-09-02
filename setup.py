# -*- encoding:utf8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='nlp-utils',
    version='0.1',
    author='sonas',
    author_email='guolinsen123@gmail.com',
    py_modules=[],
    packages=find_packages('../nlp-utils'),
    package_dir={'nlp-utils':'nlp-utils'}
    )
