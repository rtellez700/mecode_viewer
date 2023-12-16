=============
mecode_viewer
=============


.. image:: https://img.shields.io/pypi/v/mecode_viewer.svg
   :target: https://pypi.python.org/pypi/mecode_viewer

.. image:: https://img.shields.io/travis/rtellez700/mecode_viewer.svg
   :target: https://travis-ci.com/rtellez700/mecode_viewer

.. image:: https://readthedocs.org/projects/mecode-viewer/badge/?version=latest
   :target: https://mecode-viewer.readthedocs.io/en/latest/?version=latest
   :alt: Documentation Status


Simple GCode Viewer
-------------------

* Free software: MIT license
* Documentation: https://mecode-viewer.readthedocs.io.


Features
--------

Installation
------------

.. code-block:: bash

   pip install git+https://github.com/rtellez700/mecode_viewer.git

Upgrading
---------

.. code-block:: bash

   pip install git+https://github.com/rtellez700/mecode_viewer.git --upgrade

Version Bump
------------

.. code-block:: bash

   bump2version --current-version <version> patch|minor|major
   git push origin <tag name>
   python setup.py sdist bdist_wheel
   twine check dist/*
   twine upload dist/* --verbose


Pushing to PyPi
---------------

   1. python3 -m pip install --upgrade build
   2. python3 -m build
   3. python3 -m pip install --upgrade twine
   4. python3 -m twine upload --repository testpypi dist/<file to upload>
Example
-------

.. code-block:: python

   import mecode_viewer.mecode_viewer as mecode_viewer

   mecode_viewer(<file_name_here>)

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
