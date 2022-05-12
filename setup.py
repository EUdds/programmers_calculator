from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

with open("LICENSE", "r") as fh:
    license = fh.read()

setup(
    name="dev_calc",
    version="0.0.1",
    description="A Programmers calculator that lives in the command line!",
    long_description=readme,
    author="Eric Udlis",
    author_email="udlis.eric@gmail.com",
    url="https://github.com/EUdds/programmers_calculator",
    license=license,
    packages=find_packages(exclude=("tests")),
    entry_points={
        "console_scripts": [
            "dev_calc=dev_calc.dev_calc:main",
        ],
    }
)