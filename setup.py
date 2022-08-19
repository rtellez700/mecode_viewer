from setuptools import setup, find_packages

INFO = {'name': 'mecode_viewer',
        'version': '0.0.1',
        'description': 'Simple GCode Viewer',
        'author': 'Rodrigo Telles',
        'author_email': 'rtelles@g.harvard.edu',
        }

setup(
    name=INFO['name'],
    version=INFO['version'],
    description=INFO['description'],
    author=INFO['author'],
    author_email=INFO['author_email'],
    packages=find_packages(),
    url='https://github.com/rtellez700/mecode_viewer.git',
    download_url='https://github.com/rtellez700/mecode_viewer/tarball/master',
    keywords=['gcode', '3dprinting', 'cnc', 'reprap', 'additive'],
    zip_safe=False,
    package_data = {
        '': ['*.txt', '*.md'],
    },
    install_requires=[
        'numpy',
        'matplotlib',
        # 'solidpython',
        # 'vpython',
    ],
)