from setuptools import setup, find_packages

long_description = """django-pyref is a Python package for managing, importing and searching bibliographic references to scientific articles.

Import of article metadata from DOI and Bibcode is supported.

See https://github.com/xnx/django-pyref for more information.
"""

setup(
    name = 'django-pyref',
    version = '0.4.0',
    author = 'Frances Skinner, Iouli Gordon, Christian Hill, Robert Hargreaves, Kelly Lockhart',
    author_email = 'xn.hill@gmail.com',
    description = 'A package for managing bibliographic references',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/xnx/django-pyref',
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>=3.4',
)
