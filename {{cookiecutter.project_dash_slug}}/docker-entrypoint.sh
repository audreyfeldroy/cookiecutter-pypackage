#!/bin/sh

# Entrypoint script

main() {
  [ $# -lt 1 ] && pipenv_shell
  case "$1" in
    -*) pipenv_shell "$@";;
    *) exec "$@";;
  esac
}

pipenv_shell() {
  pipenv shell
}

main "$@"
