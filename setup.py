from setuptools import setup, find_packages

setup(
    name='scrapy-dropbox',
    packages=['scrapy_dropbox'],
    install_requires=['scrapy', 'dropbox'],
    requires=['scrapy', 'dropbox']
)
