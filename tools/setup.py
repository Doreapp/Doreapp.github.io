"""The setup script."""

import os
from typing import List

from setuptools import find_packages, setup

PROJECT_SLUG = "pyfolio"
VERSION = os.environ["VERSION"]


def read_requirements(path: str) -> List[str]:
    """Parse a list of requirements from the file at ``path``"""
    with open(path, "r", encoding="utf8") as req_file:
        result = [
            line.replace(" ", "")
            for line in req_file.readlines()
            if not line.lstrip().startswith("#")
        ]
    return result


with open("README.md", "r", encoding="utf8") as readme_file:
    readme = readme_file.read()

requirements = read_requirements("requirements.txt")
requirements_dev = read_requirements("requirements-dev.txt")

setup(
    author="Antoine Mandin",
    author_email="doreapp.contact@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="Tool to check the format of portfolio/resume data",
    entry_points={
        "console_scripts": [
            f"{PROJECT_SLUG}={PROJECT_SLUG}.__main__:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=[PROJECT_SLUG, "portfolio", "resume", "me.yml"],
    name=PROJECT_SLUG,
    packages=find_packages(include=[PROJECT_SLUG, f"{PROJECT_SLUG}.*"]),
    test_suite="tests",
    tests_require=requirements_dev,
    url=f"https://github.com/Doreapp/Doreapp.github.io/tree/main/tools",
    version=VERSION,
    zip_safe=False,
)
