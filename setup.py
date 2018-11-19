# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '5.1.11'

setup(
    name='plone.app.locales',
    version=version,
    description='Translation files for Plone',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'Framework :: Zope2',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='plone i18n locale translation',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://github.com/collective/plone.app.locales',
    license='GPL version 2',
    packages=find_packages(),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
)
