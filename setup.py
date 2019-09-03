import setuptools
import unittest

exec(open('pysvd/version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysvd",
    version=__version__,
    description="System View Description parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="SVD CMSIS ARM",
    license="MIT",
    author="Benjamin Füldner",
    author_email="benjamin@fueldner.net",
    url="https://code.fueldner.net/opensource/pysvd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Embedded Systems",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
