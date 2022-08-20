from os import read
from setuptools import setup, find_packages

from mecode_viewer.main import mecode_viewer

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

INFO = {'name': 'mecode_viewer',
        'version': '0.0.2',
        'description': 'Simple GCode Viewer',
        'author': 'Rodrigo Telles',
        'author_email': 'rtelles@g.harvard.edu',
        }

setup(
    name=INFO['name'],
    version=INFO['version'],
    description=INFO['description'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=INFO['author'],
    author_email=INFO['author_email'],
    packages=find_packages(include=['mecode_viewer', 'mecode_viewer.*']),
    python_requires='>=3.6',
    url='https://github.com/rtellez700/mecode_viewer.git',
    download_url='https://github.com/rtellez700/mecode_viewer/tarball/master',
    keywords=['gcode', '3dprinting', 'cnc', 'reprap', 'additive'],
    zip_safe=False,
    package_data = {
        '': ['*.txt', '*.md'],
    },
    license="MIT license",
    install_requires=[
        'numpy',
        'matplotlib',
        # 'solidpython',
        # 'vpython',
    ],
)