#!/usr/bin/env bash

echo 'Initializing repository...'
git init .

echo 'Setting upstream origin to git@github.com:{{ cookiecutter.github_repo }}.git'
git remote add origin 'git@github.com:{{ cookiecutter.github_repo }}.git'

if [[ '{{ cookiecutter.command_line_interface|lower }}' =~ no ]]
then
   rm '{{ cookiecutter.project_slug }}/cli.py'
fi

if [[ '{{ cookiecutter.packagecloud|lower }}' =~ enable ]]
then
   # Get packagecloud API token
   if [ -z "${PACKAGECLOUD_TOKEN}" ]
   then
      echo '${PACKAGECLOUD_TOKEN} is not set, please find your token at'
      echo '    https://packagecloud.io/api_token'
      read -p 'and enter it here: ' PACKAGECLOUD_TOKEN
   fi
   echo "Using ${PACKAGECLOUD_TOKEN} package cloud api token"

   # Get or create read token

   # python subroutine for parsing read_tokens result from packagecloud
   pythontmpfile=$(mktemp /tmp/parse_json.XXXXXX)
   cat > $pythontmpfile <<EOF
import sys
import json

for token in json.load(sys.stdin).get('read_tokens', []):
    if token['name'] == '{{ cookiecutter.project_dash_slug }}':
        sys.stdout.write(token['value'])
        sys.exit(0)
sys.stderr.write('Could not find read token\n')
sys.exit(1)
EOF

   # When copy/pasting this code into a different cookie cutter please create a new master token.

   MASTER_TOKEN=5a1f72e8a735582d8c435fc3429c1591cd869c657f9a94d7

   # NB: the MASTER_TOKEN is not secret. The package cloud documentation says:
   #
   # That means that you can safely give master tokens to customers, embed them in
   # configuration management manifests, or otherwise distribute them to untrusted parties.

   READ_TOKENS_API=api/v1/repos/syapse/General/master_tokens/${MASTER_TOKEN}/read_tokens.json
   # Creating read token may fail if the script is called twice, with error response json, but 0 bash status code)
   # We ignore result.
   curl -o /dev/null -X POST -F "read_token[name]={{ cookiecutter.project_dash_slug }}" https://${PACKAGECLOUD_TOKEN}:@packagecloud.io/${READ_TOKENS_API}
   # Get read tokens (either freshly created or old one)
   READ_TOKEN=$(curl https://${PACKAGECLOUD_TOKEN}:@packagecloud.io/${READ_TOKENS_API} | python $pythontmpfile)

   rm $pythontmpfile

   # Edit Pipfile
   sed -i '' -e 's/[$]{READ_TOKEN}/'${READ_TOKEN}/ Pipfile

fi
