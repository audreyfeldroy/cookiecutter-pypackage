#!/bin/sh

# Entrypoint script

#!/bin/sh

main() {
  pipenv run "$@";
}

main "$@"
