import os
import re

from setuptools import find_packages, setup

with open("README.md", "r") as readme:
    long_description = readme.read()

with open(os.path.join("dbfiles", "__init__.py"), "r") as src:
    version = re.match(r'.*__version__ = "(.*?)"', src.read(), re.S).group(1)

setup(
    name="django-dbfiles",
    version=version,
    description="Custom Database Storage for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imsweb/django-dbfiles",
    license="BSD",
    author="Dan Watson",
    author_email="watsond@imsweb.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="django database storage files",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
)
