#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import errno
import json
import os
import sys

from jinja2 import FileSystemLoader
from jinja2.environment import Environment

PY3 = sys.version > '3'
if PY3:
    import http.server as httpserver
    import socketserver
else:
    import SimpleHTTPServer as httpserver
    import SocketServer as socketserver


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def serve_static_site():
    # Serve the output directory
    os.chdir('output/')
    PORT = 9090
    Handler = httpserver.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    httpd.serve_forever()


def generate_html(pages, context=None, input_dir='input/'):
    context = context or {}
    env = Environment()
    env.loader = FileSystemLoader(input_dir)

    for page in pages:
        tmpl = env.get_template('{0}.html'.format(page))
        rendered_html = tmpl.render(**context)

        # Put index in the root. It's a special case.
        if page == 'index':
            with open('output/index.html', 'w') as fh:
                fh.write(rendered_html)

        # Put other pages in page/index.html, for better URL formatting.
        else:
            make_sure_path_exists('output/{0}/'.format(page))
            with open('output/{0}/index.html'.format(page), 'w') as fh:
                fh.write(rendered_html)


def generate_context(input_dir='input/'):
    """
    Generates the context for all complexity pages.

    Description:

        Iterates through the contents of the input_dir and finds all JSON files.
        Loads the JSON file as a Python object with the key being the JSON file name.

    Example:

        Assume the following files exist:

            input/names.json
            input/numbers.json

        Depending on their content, might generate a context as follows:

        contexts = {"names":
                        ['Audrey', 'Danny']
                    "numbers":
                        [1, 2, 3, 4]
                    }
    """
    context = {}

    # Loop through all the JSON files in the input directory
    for file_name in [f for f in os.listdir(input_dir) if f.endswith('json')]:

        # Open the JSON file and convert to Python object
        obj = json.load(open("{0}/{1}".format(input_dir, file_name)))

        # Add the Python object to the context dictionary
        context[file_name[:-5]] = obj

    return context


def command_line_runner():
    """ Entry point for the package, as defined in setup.py. """

    # List the stem of each HTML file in input/
    pages = [f.split('.')[0] for f in os.listdir('input/') if f.endswith('html')]

    context = generate_context()

    # Generate and serve the HTML site
    generate_html(pages, context)
    serve_static_site()


if __name__ == '__main__':
    command_line_runner()
