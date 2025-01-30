from setuptools import setup, find_packages

setup(
    name="movies-searcher",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'ujson==5.10.0'
    ],
    author="Felipe Santos",
    author_email="felipe.dossantos.dev@gmail.com",
    description="A movie searcher",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/felipe-dossantos-dev/movies-searcher",
    python_requires=">=3.6",
)
