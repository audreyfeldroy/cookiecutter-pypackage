{% if cookiecutter.include_cli == 'yes' %}
import {{cookiecutter.repo_name}}.cli
{{cookiecutter.repo_name}}.cli.main()
{% else %}
from {{cookiecutter.repo_name}} import {{cookiecutter.repo_name}}
{{cookiecutter.repo_name}}()
{% endif %}
