from subprocess import run
from pathlib import Path
from venv import create
import os

print(Path.cwd())
exit(0)
env = Path.cwd().joinpath(Path('{{cookiecutter.project_name}}/env'))
create(env, with_pip=True)

run([str(Path(env).joinpath('bin')) + 'activate'])
os.chdir()
run(["pip", "install", "-e", "."])
