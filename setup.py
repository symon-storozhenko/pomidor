import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pomidor", # Replace with your own username
    version="0.0.2",
    author="Symon Storozhenko",
    author_email="symon.storozhenko@gmail.com",
    description="A BDD-style Selenium-driven browser automation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/symon-storozhenko/pomidor",
    packages=setuptools.find_packages(),
    install_requires=['selenium', 'pytest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)