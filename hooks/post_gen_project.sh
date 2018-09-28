#!/usr/bin/env bash


initialize_repo () {
    if [ -d .git ]
    then
         echo 'Leaving /git directory unchanged'
    else
        echo 'Initializing repository...'
        git init .

        echo 'Setting upstream origin to git@github.com:{{ cookiecutter.github_repo }}.git'
        git remote add origin 'git@github.com:{{ cookiecutter.github_repo }}.git'
    fi
}


configure_packagecloud () {
{% if 'generate' in cookiecutter.packagecloud_read_token | lower  %}
    # Prompt the user for a packagecloud API token if not set.

    local api_token="$PACKAGECLOUD_TOKEN"
    if [[ -z "$api_token" ]]
    then
        if ps -p $PPID -o args= | grep --silent -e --no-input
        then
            echo 'You must set the $PACKAGECLOUD_TOKEN environment variable to use the --no-input option.'
            exit 1
        fi
        echo 'No $PACKAGECLOUD_TOKEN environment variable. Get your token from '
        echo '    -> https://packagecloud.io/api_token'
        read -p 'And enter your packagecloud token: ' -r api_token
    fi

    local master_token="5a1f72e8a735582d8c435fc3429c1591cd869c657f9a94d7"
    local repo="syapse/General"
    local read_tokens_api="https://$api_token:@packagecloud.io/api/v1/repos/$repo/master_tokens/$master_token/read_tokens.json"

    echo "Creating a read token..."
    curl --silent --fail --output /dev/null -X POST -F "read_token[name]={{ cookiecutter.project_dash_slug }}" "$read_tokens_api" \
        || echo "A read token already exists for this project."

    echo "Fetching the read token for this project..."
    local read_token
    read_token=$(curl --silent --show-error --fail "$read_tokens_api" | python -c "import sys, json; print(next(t['value'] for t in json.load(sys.stdin).get('read_tokens', []) if t.get('name') == '{{cookiecutter.project_dash_slug}}') or '')")

    if [[ -z "$read_token" ]]
    then
        >&2 echo "There was a problem fetching the read token from packagecloud."
        exit 1
    fi

    sed -i '' -e "s=https://{{ cookiecutter.packagecloud_read_token }}:@packagecloud=https://${read_token}:@packagecloud=" Pipfile

    # ensure --replay works
    local replay_template=~/.cookiecutter_replay/cookiecutter-pypackage.json
    local old_value="\"packagecloud_read_token\": \"{{ cookiecutter.packagecloud_read_token }}\""
    local new_value="\"packagecloud_read_token\": \"${read_token}\""
    sed -i '' -e "s=${old_value}=${new_value}=" ${replay_template}

{% endif %}
    true
}


remove_cli_code () {
    if [[ '{{ cookiecutter.command_line_interface|lower }}' =~ no ]]
    then
        rm -f \
            'Dockerfile' \
            'bin/build' \
            'bin/run' \
            'docker-entrypoint.sh' \
            '{{ cookiecutter.project_slug }}/cli.py'
    fi
}


main () {
    initialize_repo
    remove_cli_code
    configure_packagecloud
}

main "$@"
