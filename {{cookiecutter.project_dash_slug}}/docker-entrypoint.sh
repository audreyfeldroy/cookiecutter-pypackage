#!/bin/sh

main() {
  [ $# -lt 1 ] && run_cli
  case "$1" in
    -*) run_cli "$@";;
    *) exec "$@";;
  esac
}

run_cli() {
  export NEW_RELIC_CONFIG_FILE
  if [ -n "${NEW_RELIC_LICENSE_KEY}" ]; then
    echo "Running with New Relic monitoring..."
    exec newrelic-admin run-program {{cookiecutter.project_dash_slug}} "$@"
  else
    exec {{cookiecutter.project_dash_slug}} "$@"
  fi
}

main "$@"
