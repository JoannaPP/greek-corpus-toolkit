from setuptools import setup, find_packages

setup(
    name="corpus_toolkit",
    version="0.1.0",
    description="A Python Corpus Linguistic Toolkit for Greek Text Analysis",
    author="Joanna Pepa",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0.0",
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "matplotlib>=3.5.0",
    ],
    python_requires=">=3.10",
)