#!/usr/bin/python3
import mcts_simple
import setuptools

# METADATA
NAME = "mcts-simple"
VERSION = mcts_simple.__version__
AUTHOR = "Lance Chin"
EMAIL = "denselance@gmail.com"
DESCRIPTION = "Python package that helps to quickly implement MCTS to solve reinforcement learning problems."
URL = "https://github.com/DenseLance/mcts-simple"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = None

# DEPENDENCIES
REQUIRED = ["json-pickle", "tqdm"]

with open("README.md", "r", encoding = "utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name = NAME,
    version = VERSION,
    author = AUTHOR,
    author_email = EMAIL,
    description = DESCRIPTION,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = URL,
    project_urls={
        "Bug Tracker": "https://github.com/DenseLance/mcts-simple/issues",
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages = setuptools.find_packages(where = "mcts_simple"),
    python_requires = REQUIRES_PYTHON,
)