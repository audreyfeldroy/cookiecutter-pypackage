import pytest

from pywps import Service
from pywps.tests import assert_response_success

from {{ cookiecutter.project_slug }}.tests.common import client_for
from {{ cookiecutter.project_slug }}.processes.wps_wordcounter import WordCounter


@pytest.mark.online
def test_wps_wordcount():
    client = client_for(Service(processes=[WordCounter()]))
    datainputs = "text={0}".format(
        "https://en.wikipedia.org/wiki/Web_Processing_Service")
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='wordcounter',
        datainputs=datainputs)
    assert_response_success(resp)
