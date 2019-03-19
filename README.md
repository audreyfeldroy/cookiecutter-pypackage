# cookiecutter
[cookiecutter](https://cookiecutter.readthedocs.io/) is a python utility by @audreyr to create python skeleton for new Python apps

# cookiecutter-appbase
[cookiecutter-appbase](https://github.com/scrolltech/cookiecutter-appbase) a application boilerplate for scroll style Python apps.
It is based on cookiecutter by audreyr.

## What does it do?
It builds envioronment for common scroll python project requirements

For example if we are creating a new project with the name **Our New App** and slug is our_new_app ..
- It copies files directories in {{cookiecutter.project_slug}} directory to `our_new_app`
- It has ability to use variables declared in cookiecutter.json in naming file/directory names and in template. 
    - eg. {{cookiecutter.project_slug}} directory will be renamed our_new_app
    - any files with text {{cookiecutter.<variable>}} will be replaced with it's corresponding value defined in cookiecutter.json

# Usage instructions for creating new project based on cookiecutter-appbase

```
cookiecutter cookiecutter-appbase
```

# Guide for creating new project boilerplate like this one

I couldn't quickly figure out cookiecutter inspite of it's simplicity and good documentation. 
So here 

- `pip install cookiecutter`
- Fork github.com/audreyr/cookiecutter-pypackage
- Rename cookiecutter-appbase
- `git clone git@github.com:<gituser>/cookiecutter-appbase.git`
- `vi cookiecutter.json`
