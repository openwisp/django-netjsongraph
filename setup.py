#!/usr/bin/env python
import os
import sys

from django_netjsongraph import get_version
from setuptools import find_packages, setup


def get_install_requires():
    """
    parse requirements.txt, ignore links, exclude comments
    """
    requirements = []
    for line in open('requirements.txt').readlines():
        # skip to next iteration if comment or empty line
        if line.startswith('#') or line == '' or line.startswith('http') or line.startswith('git'):
            continue
        # add line to requirements
        requirements.append(line)
    return requirements


if sys.argv[-1] == 'publish':
    # delete any *.pyc, *.pyo and __pycache__
    os.system('find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload -s dist/*")
    os.system("rm -rf dist build")
    args = {'version': get_version()}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()


setup(
    name='django-netjsongraph',
    version=get_version(),
    license='MIT',
    author='Federico Capoano',
    author_email='nemesis@ninux.org',
    description='Reusable django app for collecting and visualizing network topology',
    long_description=open('README.rst').read(),
    url='http://netjson.org',
    download_url='https://github.com/interop-dev/django-netjsongraph/releases',
    platforms=['Platform Indipendent'],
    keywords=['django', 'netjson', 'mesh', 'networking'],
    packages=find_packages(exclude=['tests']),
    install_requires=get_install_requires(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Topic :: System :: Networking',
        'Programming Language :: Python :: 3',
    ]
)
