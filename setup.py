import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pii-data-generator",
    version="1.0.2",
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
        'console_scripts': ['pii = pii_generator.command_line'],
    },
    install_requires=[
            "bleach==4.1.0",
            "certifi==2021.10.8",
            "charset-normalizer==2.0.8",
            "colorama==0.4.4",
            "docutils==0.18.1",
            "Faker==9.8.3",
            "idna==3.3",
            "importlib-metadata==4.8.2",
            "keyring==23.4.0",
            "mongoengine==0.23.1",
            "numpy==1.21.4",
            "packaging==21.3",
            "pandas==1.3.4",
            "pkginfo==1.8.1",
            "Pygments==2.10.0",
            "pymongo==3.12.1",
            "pyparsing==3.0.6",
            "python-dateutil==2.8.2",
            "pytz==2021.3",
            "readme-renderer==30.0",
            "requests==2.26.0",
            "requests-toolbelt==0.9.1",
            "rfc3986==1.5.0",
            "six==1.16.0",
            "text-unidecode==1.3",
            "tqdm==4.62.3",
            "urllib3==1.26.7",
            "webencodings==0.5.1",
            "zipp==3.6.0"

    ],

)