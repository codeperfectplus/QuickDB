import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quickDB",
    version="0.0.1",
    author="Deepak Raj",
    author_email="deepak008@live.com",
    description="Simple python database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/py-contributors/python-db",
    keywords="python database",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.4",
    entry_points={
        "console_scripts": [],
    },
)
