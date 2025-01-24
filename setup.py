# setup.py
from setuptools import setup, find_packages

setup(
    name="pytestcoder",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "pytest",
        "httpx",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "pytest-asyncio",
        "pytest-cov"
    ],
)