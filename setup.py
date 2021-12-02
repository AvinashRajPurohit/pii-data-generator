import pathlib
from setuptools import setup
from os import  path
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
print(HERE)
requirementPath = str(HERE / "requirements.txt")
print(requirementPath)
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
print(path.isfile(requirementPath))
if path.isfile(requirementPath):
    print(requirementPath)
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
# This call to setup() does all the work
print(install_requires)
setup(
    name="pii-data-generator",
    version="1.0.5",
    description="It generats the dummy 'Personally identifiable information' data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AvinashRajPurohit/pii-data-generator",
    author="Deepak Rajpurohit",
    author_email="deepakrajpurohit945@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

    ],
    packages=["pii_generator"],
    include_package_data=True,
    entry_points = {
        'console_scripts': ['pii = pii_generator.command_line:main'],
    },
    install_requires=install_requires,

)