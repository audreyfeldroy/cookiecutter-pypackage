import nox


@nox.session(python=['2.7', '3.6', '3.7'], reuse_venv=True)
def prep(session):
  with open('requirements_dev.txt', 'r') as reqs_file:
    reqs = reqs_file.readlines()
  session.install(**reqs)

@nox.session(python=['2.7', '3.6', '3.7'], reuse_venv=True)
def tests(session):
  session.run('pytest')

@nox.session(python='3.7', reuse_venv=True)
def lint(session):
  session.run('pylint')

@nox.session(python='3.7', reuse_venv=True)
def docs(session):
  sphinx-build -b html -d {envtmpdir}/doctrees . {envtmpdir}/html