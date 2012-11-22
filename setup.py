# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

for cmd in ('egg_info', 'develop'):
    import sys
    if cmd in sys.argv:
        from setuptools import setup

setup(
    name='django-multiuploader',
    version='0.1.0',
    author=u'Sinitsin Vladimir and Ivanov Vitaly',
    author_email='vs@llc.ac; vit@nlstar.com',
    packages=find_packages(),
    url='http://test.ru',
    license='BSD licence, see LICENCE.txt',
    description='Adds jQuery dynamic form for uploading multiple files',
    long_description=open('README.rst').read(),
    include_package_data=True,
    requires=['django (>= 1.3)','sorl_thumbnail'],
    zip_safe=False,
)
