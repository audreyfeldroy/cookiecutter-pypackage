###########################################################
# Demo WPS service for testing and debugging.
#
# See the werkzeug documentation on how to use the debugger:
# http://werkzeug.pocoo.org/docs/0.12/debug/
###########################################################

import os

from pywps import configuration

from . import wsgi
from ._compat import urlparse

import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)
LOGGER = logging.getLogger('DEMO')


def get_host():
    url = configuration.get_config_value('server', 'url')
    url = url or 'http://localhost:5000/wps'

    LOGGER.warn("starting WPS service on %s", url)

    parsed_url = urlparse(url)
    if ':' in parsed_url.netloc:
        host, port = parsed_url.netloc.split(':')
        port = int(port)
    else:
        host = parsed_url.netloc
        port = 80
    return host, port


def _run(application, bind_host=None, daemon=False):
    from werkzeug.serving import run_simple
    # call this *after* app is initialized ... needs pywps config.
    host, port = get_host()
    bind_host = bind_host or host
    # need to serve the wps outputs
    static_files = {
        '/outputs': configuration.get_config_value('server', 'outputpath')
    }
    run_simple(
        hostname=bind_host,
        port=port,
        application=application,
        use_debugger=True,
        use_reloader=True,
        use_evalex=not daemon,
        static_files=static_files)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="""Script for starting a demo WPS instance.
                       This service is by default available at http://localhost:5000/wps""",
        epilog="""Do not use this service in a production environment.
         It's intended to be running in a test environment only!
         For more documentation, visit http://bird-house.github.io/
        """
    )
    parser.add_argument('--debug',
                        action="store_true", help="enable debug logging mode")
    parser.add_argument('-c', '--config',
                        help="path to pywps configuration file")
    parser.add_argument('-a', '--all-addresses',
                        action='store_true', help="run service using IPv4 0.0.0.0 (all network interfaces), "
                        "otherwise bind to 127.0.0.1 (localhost).")
    parser.add_argument('-d', '--daemon',
                        action='store_true', help="run in daemon mode")
    args = parser.parse_args()
    cfgfiles = []
    if args.config:
        cfgfiles.append(args.config)
        LOGGER.warn('using pywps configuration: %s', args.config)
    if args.debug:
        cfgfiles.append(os.path.join(os.path.dirname(__file__), 'debug.cfg'))
    if args.all_addresses:
        bind_host = '0.0.0.0'
    else:
        bind_host = '127.0.0.1'
    app = wsgi.create_app(cfgfiles)
    # let's start the service ...
    if args.daemon:
        # daemon (fork) mode
        pid = None
        try:
            pid = os.fork()
            if pid:
                LOGGER.warn('forked process id: %s', pid)
        except OSError as e:
            raise Exception("%s [%d]" % (e.strerror, e.errno))

        if (pid == 0):
            os.setsid()
            _run(app, bind_host=bind_host, daemon=True)
        else:
            os._exit(0)
    else:
        # no daemon
        _run(app, bind_host=bind_host)


if __name__ == '__main__':
    main()
