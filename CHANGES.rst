CHANGES
********

0.6.0
=====

Changes:

* Replace `search` by `parse` in the bumpversion config for `docs/conf.py` to support the `version|release` expression.

0.5.0 (2020-10-07)
==================

Changes:

* Easier to deploy new template to existing project using cruft (#85, #61).
* Use pip instead of setup.py (#97).
* Added conda forge, Python3.8, and osx build (#38).
* Backported fixes from birds (#86, #88, #89).
* Other fixes (#92, #93, #96, #100).

0.4.2 (2020-01-07)
==================

Changes:

* Fix conda environment for latest cookiecutter (#75).
* Pinned PyWPS 4.2 (#74).
* Updated links to developer guide (#73).
* Added setuptools to conda environment (#72).

0.4.1 (2019-09-27)
==================

This is the Bucharest release.

Changes:

* Skipped conda environment handling in makefile (#70).

0.4.0 (2019-04-17)
==================

This is the San Francisco release.

Changes:

* Skipped python 2.7 support (#67).
* Updated to pywps 4.2 (#66).
* Added `make spec` (#65).
* Fixed Emu references (#63).


0.3.1 (2018-12-05)
==================

Bugfixes for Washington release.

Changes:

* Raise Makefile errors (#57).
* Get version number without importing package (#56).
* Keep only a single *hello* process (#53).

0.3.0 (2018-09-05)
==================

Cookiecutter template prepared for Ansible deployment of PyWPS.

Changes:

* Updated to Ansible deployment (#14).
* Enabled PyWPS autodoc extension (#37).
* Updated PyWPS CLI (#8 and #33).
* Enabled Conda support for RTD (#51).
* Using ``bumpversion`` to update version (#9)
* numerous fixes.

0.2.0 (2018-05-22)
==================

Initial Cookiecutter Birdhouse release.

A Cookiecutter template for a minimal PyWPS server with example processes.

0.1.1 (2016-06-04)
==================

Original Cookiecutter:
https://github.com/audreyr/cookiecutter-pypackage/tree/v0.1.1
