from setuptools import setup, find_packages

setup(
    name='scrapy-dropbox',
    packages=find_packages(),
    install_requires=['scrapy', 'dropbox'],
    requires=['scrapy', 'dropbox'],
    extras_require={
        'test': ['pytest']
    }
)
