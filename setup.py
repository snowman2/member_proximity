#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="member_proximity",
    packages=find_packages(),
    version="0.0.1",
    description="Find members of the church who are closest to an address based on ward directory.",
    url="https://github.com/snowman2/member_proximity",
    author="Alan D. Snow",
    author_email="alansnow21@gmail.com",
    keywords=["geocode", "church", "ward", "members"],
    install_requires=["requests", "pandas", "geopy"],
    extras_require={"dev": ["pytest", "black"]},
)
