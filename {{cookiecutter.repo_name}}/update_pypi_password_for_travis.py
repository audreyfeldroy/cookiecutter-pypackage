#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Update encrypted deploy password in Travis config file
"""


from __future__ import print_function
import base64
import json
import os
import sys
from getpass import getpass
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

try:
    from urllib import urlopen
except:
    from urllib.request import urlopen

try:
    import yaml
except:
    print('Please install PyYAML first: pip install pyyaml')
    sys.exit(1)


GITHUB_REPO = '{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}'
TRAVIS_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '.travis.yml')


def encrypt(public_key, password):
    key = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(key)
    return base64.b64encode(cipher.encrypt(password))


def fetch_public_key(repo):
    keyurl = 'https://api.travis-ci.org/repos/{0}/key'.format(repo)
    data = json.loads(urlopen(keyurl).read())
    if 'key' not in data:
        errmsg = "Could not find public key for repo: {}.\n".format(repo)
        errmsg += "Have you already added your GitHub repo to Travis?"
        raise ValueError(errmsg)
    return data['key']


def update_travis_deploy_password(encrypted_password):
    with open(TRAVIS_CONFIG_FILE) as f:
        config = yaml.load(f)

    config['deploy']['password'] = dict(encrypted=encrypted_password)

    with open(TRAVIS_CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)


def main(args):
    public_key = fetch_public_key(args.repo)
    password = args.password or getpass('PyPI password: ')
    update_travis_deploy_password(encrypt(public_key, password))


if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default=GITHUB_REPO,
                        help='GitHub repo (default: %s)' % GITHUB_REPO)
    parser.add_argument('--password',
                        help='PyPI password (will prompt if not provided)')

    args = parser.parse_args()
    main(args)
