from setuptools import find_packages, setup

setup(
    name="scrapy-dropbox",
    packages=find_packages(),
    version='0.2',
    install_requires=["scrapy", "dropbox"],
    requires=["scrapy", "dropbox"],
    setup_requires=["wheel"],
    extras_require={"test": ["pytest"]},
)
