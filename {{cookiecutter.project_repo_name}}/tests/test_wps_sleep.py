import pytest

from pywps import Service
from pywps.tests import assert_response_success

from . common import client_for
from {{ cookiecutter.project_slug }}.processes.wps_sleep import Sleep


@pytest.mark.slow
def test_wps_sleep():
    client = client_for(Service(processes=[Sleep()]))
    datainputs = "delay=0.1"
    resp = client.get(
        service='WPS', request='Execute', version='1.0.0', identifier='sleep',
        datainputs=datainputs)
    print(resp.data)
    assert_response_success(resp)
