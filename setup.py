import setuptools
import unittest

exec(open('pysvd/version.py').read())

with open("README.rst", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="pysvd",
    version=__version__,
    description="System View Description parser",
    long_description=long_description,
    keywords="SVD CMSIS ARM",
    license="MIT",
    author="Benjamin Füldner",
    author_email="benjamin@fueldner.net",
    url="https://code.fueldner.net/opensource/pysvd",
    project_urls={
        'Bug Reports': 'https://github.com/bfueldner/pysvd/issues',
        'Source': 'https://github.com/bfueldner/pysvd',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Embedded Systems",
    ],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'svd2rst = scripts.svd2rst:main',
            'svd2register = scripts.svd2register:main',
        ],
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
