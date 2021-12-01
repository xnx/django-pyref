from setuptools import setup, find_packages

long_description = """django-pyref is a Python package for managing, importing and searching bibliographic references to scientific articles.

Import of article metadata from DOI and Bibcode is supported.

See https://github.com/xnx/django-pyref for more information.
"""
# Read in dependencies list from requirements.txt
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name = 'django-pyref',
    version = '0.5.0',
    author = 'Frances Skinner, Iouli Gordon, Christian Hill, Robert Hargreaves, Kelly Lockhart',
    author_email = 'xn.hill@gmail.com',
    description = 'A package for managing bibliographic references',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url = 'https://github.com/xnx/django-pyref',
    packages = find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>=3.4',
)
