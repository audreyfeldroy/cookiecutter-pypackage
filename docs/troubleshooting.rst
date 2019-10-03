.. _troubleshooting:

===============
Troubleshooting
===============

.. note:: Can you help improve this file? `Edit this file`_
          and submit a pull request with your improvements!

.. _`Edit this file`: https://github.com/audreyr/cookiecutter-pypackage/blob/master/docs/troubleshooting.rst


Windows Issues
--------------

* Some people have reported issues using git bash; try using the Command Terminal instead.

* Virtual environments can sometimes be tricky on Windows. If you have Python 3.5 or above installed (recommended), this should get you a virtualenv named ``myenv`` created inside the current folder:

.. code-block:: powershell

    > c:\Python35\python -m venv myenv

Or:

.. code-block:: powershell

    > c:\Python35\python c:\Python35\Tools\Scripts\pyvenv.py myenv

* Some people have reported that they have to re-activate their virtualenv whenever they change directory, so you should remember the path to the virtualenv in case you need it.


MacOS Issues
------------

* Some people have reported issues with MacOS El Capitan and cryptography dependency (when running ``pip install cryptography``). To fix it, install ``openssl`` and link it like below:

.. code-block:: bash

    brew install openssl
    cd /usr/local/include
    ln -s ../opt/openssl/include/openssl .

For further information visit https://solitum.net/openssl-os-x-el-capitan-and-brew/.

