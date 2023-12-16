#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy', 'matplotlib', 'gcode_helpers', 'vpython'
]

test_requirements = [ ]

setup(
    author="Rodrigo Telles",
    author_email='rtelles@g.harvard.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Simple GCode Viewer",
    entry_points={
        'console_scripts': [
            'mecode_viewer=mecode_viewer.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description_content_type='text/x-rst',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mecode_viewer',
    name='mecode_viewer',
    packages=find_packages(include=['mecode_viewer', 'mecode_viewer.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rtellez700/mecode_viewer',
    version='0.2.5',
    zip_safe=False,
)
