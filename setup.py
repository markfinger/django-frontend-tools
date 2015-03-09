from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(
    name='django-frontend-tools',
    version=VERSION,
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'django',
        'django-node',
    ],
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-node',
)