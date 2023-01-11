# Tutorial

??? Note
    Did you find this article confusing? **Edit this file** and pull a request!

To start with, you will need [GitHub](https://github.com/), [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org/). If
you don't have one, please follow the links to apply one before you get started on this
tutorial.

If you are new to Git and GitHub, you should probably spend a few minutes on
some tutorials at the top of the page at [GitHub Help](https://help.github.com/).

## Step 1: Install Cookiecutter

Install cookiecutter:

``` bash
pip install cookiecutter
```

## Step 2: Generate Your Package

Now it's time to generate your Python package.

Run the following command and feed with answers, If you don’t know what to enter, stick with the defaults:

```bash
cookiecutter https://github.com/netbox-community/cookiecutter-netbox-plugin.git
```

Finally, a new folder will be created under current folder, the name is the answer you
provided to `project_slug`.

Go to this generated folder, the project layout should look like:

```
.
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── MANIFEST.in
├── Makefile
├── README.md
├── docs
│   ├── changelog.md
│   ├── contributing.md
│   └── index.md
├── mkdocs.yml
├── netbox_healthcheck_plugin
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── filtersets.cpython-310.pyc
│   │   ├── forms.cpython-310.pyc
│   │   ├── models.cpython-310.pyc
│   │   ├── navigation.cpython-310.pyc
│   │   ├── tables.cpython-310.pyc
│   │   ├── urls.cpython-310.pyc
│   │   └── views.cpython-310.pyc
│   ├── filtersets.py
│   ├── forms.py
│   ├── models.py
│   ├── navigation.py
│   ├── tables.py
│   ├── templates
│   │   └── netbox_healthcheck_plugin
│   │       └── healthcheck.html
│   ├── urls.py
│   └── views.py
├── requirements_dev.txt
├── setup.cfg
├── setup.py
└── tests
    ├── __init__.py
    └── test_netbox_healthcheck_plugin.py

```

Here the plugin_name is `HealthCheck`, when you generate yours, it could be other name.

## Step 3: Create a GitHub Repo

Go to your GitHub account and create a new repo named `netbox-healthcheck-plugin`, where
`netbox-healthcheck-plugin` matches the `project_slug` from your answers to running
cookiecutter.

Then go to repo > settings > secrets, click on 'New repository secret', add the following
 secrets:

- TEST_PYPI_API_TOKEN, see [How to apply TestPyPI token](https://test.pypi.org/manage/account/)
- PYPI_API_TOKEN, see [How to apply pypi token](https://pypi.org/manage/account/)
- PERSONAL_TOKEN, see [How to apply personal token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

## Step 4: Upload code to GitHub

Back to your develop environment, find the folder named after the `project_slug`.
Move into this folder, and then setup git to use your GitHub repo and upload the
code:

``` bash
cd my-package

git add .
git commit -m "Initial commit."
git branch -M main
git remote add origin git@github.com:myusername/my-package.git
git push -u origin main
```

Where `myusername` and `my-package` are adjusted for your username and
repo name.

You'll need a ssh key to push the repo. You can [Generate](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) a key or
[Add](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) an existing one.

???+ Warning

    if you answered 'yes' to the question if install pre-commit hooks at last step,
    then you should find pre-commit be invoked when you run `git commit`, and some files
     may be modified by hooks. If so, please add these files and **commit again**.

### Check result

After pushing your code to GitHub, goto GitHub web page, navigate to your repo, then
click on actions link, you should find screen like this:

![](http://images.jieyu.ai/images/202104/20210419170304.png)

There should be some workflows running. After they finished, go to [TestPyPI], check if a
new artifact is published under the name `project_slug`.

## Step 5. Check documentation

Documentation will be published and available at *https://{your_github_account}.github.io/{your_repo}* once:

1. the commit is tagged, and the tag name is started with 'v' (lower case)
2. build/testing executed by GitHub CI passed

## Step 6. Make official release

  After done with your phased development in a feature branch, make a pull request, following
  instructions at [release checklist](pypi_release_checklist.md), trigger first official release and check
  result at [PyPI].
