"""Installs document classification training package"""
from setuptools import find_packages, setup

setup(
    name="sentiment-classification-service",
    version="1.0",
    packages=find_packages(),
    python_requires="==3.8.*",
    install_requires=["grpcio", "grpcio-tools"],
    extras_require={
        "dev": [
            "rich",
        ],
    },
)
