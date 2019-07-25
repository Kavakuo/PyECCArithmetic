# coding=utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyECCArithmetic",
    version="1.0.2",
    author="Philipp Nieting",
    author_email="developer@nieting.de",
    description="Basic arithmetic operations for points on elliptic curves.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kavakuo/PyECCArithmetic",
    packages=setuptools.find_packages('src',exclude=['tests']),
    python_requires='>=3.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Security :: Cryptography"
    ],
    test_suite='tests',
    package_dir={'':'src'}
)
