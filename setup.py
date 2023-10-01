from setuptools import setup, find_packages

setup(
    name='scrapy-dropbox',
    packages=find_packages(),
    install_requires=['scrapy', 'dropbox'],
    requires=['scrapy', 'dropbox'],
    setup_requires=['wheel'],
    extras_require={
        'test': ['pytest']
    }
)
