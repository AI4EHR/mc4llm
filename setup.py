from setuptools import setup, find_packages

setup(
    name="medical_calculators",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=1.8.2",
        "pint>=0.17",
        "pytest>=6.0.0",
    ],
) 