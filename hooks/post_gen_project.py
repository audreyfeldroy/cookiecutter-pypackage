#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

module_dir = os.getcwd()
metadata = dict(re.findall(
    "([a-z]+)='([^']+)'",
    open('%s/setup.py' % module_dir).read()
))
print(metadata)

with open('requirements.txt', 'r') as f:
    if 'docopt' not in f.read():
        os.remove('%s/%s/cli.py' % (module_dir, metadata['name']))
