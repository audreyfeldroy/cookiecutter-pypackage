from . import BaseTestCase

from {{cookiecutter.repo_name}} import {{cookiecutter.repo_name}}


class Test{{cookiecutter.repo_name|capitalize}}(BaseTestCase):

    def test_something(self):
        self.assertEquals(
            'Hello World!',
            {{cookiecutter.repo_name}}(),
        )

