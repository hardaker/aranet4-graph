import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aranet4-graph",
    version="0.2",
    author="Wes Hardaker",
    author_email="opensource@hardakers.net",
    description="Graph data file(s) from an aranet4 sensor.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hardaker/aranet4-graph",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "aranet4-graph = aranet4graph:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "seaborn",
        "matplotlib",
        "numpy",
        "dateparser",
    ],
    test_suite="nose.collector",
    tests_require=["nose"],
)
