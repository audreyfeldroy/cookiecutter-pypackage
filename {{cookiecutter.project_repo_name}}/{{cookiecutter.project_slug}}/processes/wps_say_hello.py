from pywps import Process, LiteralInput, LiteralOutput, UOM
from pywps.app.Common import Metadata

import logging
LOGGER = logging.getLogger("PYWPS")


class SayHello(Process):
    """A nice process saying 'hello'."""
    def __init__(self):
        inputs = [
            LiteralInput('name', 'Your name',
                         abstract='Please enter your name.',
                         keywords=['name', 'firstname'],
                         data_type='string')]
        outputs = [
            LiteralOutput('output', 'Output response',
                          abstract='A friendly Hello from us.',
                          keywords=['output', 'result', 'response'],
                          data_type='string')]

        super(SayHello, self).__init__(
            self._handler,
            identifier='hello',
            title='Say Hello',
            abstract='Just says a friendly Hello.'
                     'Returns a literal string output with Hello plus the inputed name.',
            keywords=['hello', 'demo'],
            metadata=[
                Metadata('Birdhouse', 'http://bird-house.github.io/'),
                Metadata('PyWPS Demo', 'https://pywps-demo.readthedocs.io/en/latest/'),
            ],
            version='1.5',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    @staticmethod
    def _handler(request, response):
        LOGGER.info("say hello")
        response.outputs['output'].data = 'Hello ' + request.inputs['name'][0].data
        response.outputs['output'].uom = UOM('unity')
        return response
