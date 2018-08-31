###########################################################
# Demo WPS service for testing and debugging.
#
# See the werkzeug documentation on how to use the debugger:
# http://werkzeug.pocoo.org/docs/0.12/debug/
###########################################################

import os
import psutil
import click
from jinja2 import Environment, PackageLoader
from pywps import configuration

from . import wsgi
from six.moves.urllib.parse import urlparse

PID_FILE = os.path.abspath(os.path.join(os.path.curdir, "pywps.pid"))

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

template_env = Environment(
    loader=PackageLoader('{{ cookiecutter.project_slug }}', 'templates'),
    autoescape=True
)


def write_user_config(**kwargs):
    config_templ = template_env.get_template('pywps.cfg')
    rendered_config = config_templ.render(**kwargs)
    config_file = os.path.abspath(os.path.join(os.path.curdir, ".custom.cfg"))
    with open(config_file, 'w') as fp:
        fp.write(rendered_config)
    return config_file


def get_host():
    url = configuration.get_config_value('server', 'url')
    url = url or 'http://localhost:{{ cookiecutter.http_port }}/wps'

    click.echo("starting WPS service on {}".format(url))

    parsed_url = urlparse(url)
    if ':' in parsed_url.netloc:
        host, port = parsed_url.netloc.split(':')
        port = int(port)
    else:
        host = parsed_url.netloc
        port = 80
    return host, port


def run_process_action(action=None):
    """Run an action with psutil on current process
    and return a status message."""
    action = action or 'status'
    try:
        with open(PID_FILE, 'r') as fp:
            pid = int(fp.read())
            p = psutil.Process(pid)
            if action == 'stop':
                p.terminate()
                msg = "pid={}, status=terminated".format(p.pid)
            else:
                from psutil import _pprint_secs
                msg = "pid={}, status={}, created={}".format(
                    p.pid, p.status(), _pprint_secs(p.create_time()))
        if action == 'stop':
            os.remove(PID_FILE)
    except IOError:
        msg = 'No PID file found. Service not running? Try "netstat -nlp | grep :5000".'
    except psutil.NoSuchProcess as e:
        msg = e.msg
    click.echo(msg)


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
        use_debugger=False,
        use_reloader=False,
        threaded=True,
        # processes=2,
        use_evalex=not daemon,
        static_files=static_files)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
    """Command line to start/stop a PyWPS service.

    Do not use this service in a production environment.
    It's intended to be running in a test environment only!
    For more documentation, visit http://pywps.org/doc
    """
    pass


@cli.command()
def status():
    """Show status of PyWPS service"""
    run_process_action(action='status')


@cli.command()
def stop():
    """Stop PyWPS service"""
    run_process_action(action='stop')


@cli.command()
@click.option('--config', '-c', metavar='PATH', help='path to pywps configuration file.')
@click.option('--bind-host', '-b', metavar='IP-ADDRESS', default='127.0.0.1',
              help='IP address used to bind service.')
@click.option('--daemon', '-d', is_flag=True, help='run in daemon mode.')
@click.option('--hostname', metavar='HOSTNAME', default='localhost', help='hostname in PyWPS configuration.')
@click.option('--port', metavar='PORT', default='{{ cookiecutter.http_port }}', help='port in PyWPS configuration.')
@click.option('--maxsingleinputsize', default='200mb', help='maxsingleinputsize in PyWPS configuration.')
@click.option('--maxprocesses', metavar='INT', default='10', help='maxprocesses in PyWPS configuration.')
@click.option('--parallelprocesses', metavar='INT', default='2', help='parallelprocesses in PyWPS configuration.')
@click.option('--log-level', metavar='LEVEL', default='INFO', help='log level in PyWPS configuration.')
@click.option('--log-file', metavar='PATH', default='pywps.log', help='log file in PyWPS configuration.')
@click.option('--database', default='sqlite:///pywps-logs.sqlite', help='database in PyWPS configuration')
def start(config, bind_host, daemon, hostname, port,
          maxsingleinputsize, maxprocesses, parallelprocesses,
          log_level, log_file, database):
    """Start PyWPS service.
    This service is by default available at http://localhost:{{ cookiecutter.http_port }}/wps
    """
    if os.path.exists(PID_FILE):
        click.echo('PID file exists: "{}". Service still running?'.format(PID_FILE))
        os._exit(0)
    cfgfiles = []
    cfgfiles.append(write_user_config(
        wps_hostname=hostname,
        wps_port=port,
        wps_maxsingleinputsize=maxsingleinputsize,
        wps_maxprocesses=maxprocesses,
        wps_parallelprocesses=parallelprocesses,
        wps_log_level=log_level,
        wps_log_file=log_file,
        wps_database=database,
    ))
    if config:
        cfgfiles.append(config)
    app = wsgi.create_app(cfgfiles)
    # let's start the service ...
    # See:
    # * https://github.com/geopython/pywps-flask/blob/master/demo.py
    # * http://werkzeug.pocoo.org/docs/0.14/serving/
    if daemon:
        # daemon (fork) mode
        pid = None
        try:
            pid = os.fork()
            if pid:
                click.echo('forked process id: {}'.format(pid))
                with open(PID_FILE, 'w') as fp:
                    fp.write("{}".format(pid))
        except OSError as e:
            raise Exception("%s [%d]" % (e.strerror, e.errno))

        if pid == 0:
            os.setsid()
            _run(app, bind_host=bind_host, daemon=True)
        else:
            os._exit(0)
    else:
        # no daemon
        _run(app, bind_host=bind_host)
