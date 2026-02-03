# Troubleshooting

> **Note:** Can you help improve this file? [Edit this file](https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/main/docs/troubleshooting.md) and submit a pull request with your improvements!

## Windows Issues

- Some people have reported issues using git bash; try using the Command Terminal instead.
- Virtual environments can sometimes be tricky on Windows. If you have Python 3.6 or above installed (recommended), this should get you a virtualenv named `myenv` created inside the current folder:

    ```powershell
    > c:\Python35\python -m venv myenv
    ```
    Or:
    ```powershell
    > c:\Python35\python c:\Python35\Tools\Scripts\pyvenv.py myenv
    ```
- Some people have reported that they have to re-activate their virtualenv whenever they change directory, so you should remember the path to the virtualenv in case you need it.
