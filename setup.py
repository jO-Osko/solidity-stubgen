# Copyright (C) 2021 Filip Koprivec
import pkg_resources
from setuptools import setup, find_packages
from pathlib import Path
import sys


assert sys.version_info >= (3, 7, 0), "Solidity typestub requires Python 3.7.0+"


CURRENT_DIR = Path(__file__).parent

with Path(Path("requirements") / "common.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]


def get_long_description() -> str:
    return (CURRENT_DIR / "README.md").read_text(encoding="utf8")


setup(
    name="solidity_typestub",
    version="0.0.1",  # Increase this on release
    description="Generate python typestubs for abi of solidity contracts",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="solidity abi workflow mypy typestubs",
    author="Filip Koprivec",
    author_email="koprivec.filip@gmail.com",
    url="https://github.com/jO-Osko/solidity-stubgen",
    license="MIT",
    ext_modules=[],
    packages=find_packages(),
    python_requires=">=3.7.0",
    zip_safe=True,
    install_requires=install_requires,
    extras_require={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": [
            "solidity_typestub=solidity_typestub:main",
        ]
    },
)
