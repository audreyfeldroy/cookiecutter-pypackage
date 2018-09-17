#!/usr/bin/env bash


initialize_repo () {
    echo 'Initializing repository...'
    git init .

    echo 'Setting upstream origin to git@github.com:{{ cookiecutter.github_repo }}.git'
    git remote add origin 'git@github.com:{{ cookiecutter.github_repo }}.git'
}


remove_cli_code () {
    if [[ '{{ cookiecutter.command_line_interface|lower }}' =~ no ]]
    then
        rm -f '{{ cookiecutter.project_slug }}/cli.py'
    fi
}


main () {
    initialize_repo
    remove_cli_code
}

main "$@"
