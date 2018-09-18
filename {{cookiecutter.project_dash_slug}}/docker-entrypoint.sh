#!/bin/sh

main() {
  [ $# -lt 1 ] && run_tests
  case "$1" in
    -*) run_tests "$@";;
    *) exec "$@";;
  esac
}

run_tests() {
  exec echo TBD
}

main "$@"
