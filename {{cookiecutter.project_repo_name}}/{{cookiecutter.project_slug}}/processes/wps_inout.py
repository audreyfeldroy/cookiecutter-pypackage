from pywps import Process
from pywps import LiteralInput, LiteralOutput
# from pywps import BoundingBoxInput
from pywps import BoundingBoxOutput
from pywps import ComplexInput, ComplexOutput
from pywps import Format, FORMATS
from pywps.app.Common import Metadata


import logging
LOGGER = logging.getLogger("PYWPS")


class InOut(Process):
    """
    This process defines several types of literal type of in- and outputs.

    TODO: add literal input with value range[(0,100)] ... see pywps doc
    """

    def __init__(self):
        inputs = [
            LiteralInput('string', 'String', data_type='string',
                         abstract='Enter a simple string.',
                         default="This is just a string"),
            LiteralInput('int', 'Integer', data_type='integer',
                         abstract='Choose an integer number from allowed values.',
                         default="7",
                         allowed_values=[1, 2, 3, 5, 7, 11]),
            LiteralInput('float', 'Float', data_type='float',
                         abstract='Enter a float number.',
                         default="3.14"),
            # TODO: boolean default is not displayed in phoenix
            LiteralInput('boolean', 'Boolean', data_type='boolean',
                         abstract='Make your choice :)',
                         default='1'),
            LiteralInput('time', 'Time', data_type='time',
                         abstract='Enter a time like 12:00:00',
                         default='12:00:00'),
            LiteralInput('date', 'Date', data_type='date',
                         abstract='Enter a date like 2012-05-01',
                         default='2012-05-01'),
            LiteralInput('datetime', 'Datetime', data_type='dateTime',
                         abstract='Enter a datetime like 2016-09-02T12:00:00Z',
                         default='2016-09-02T12:00:00Z'),
            LiteralInput('string_choice', 'String Choice', data_type='string',
                         abstract='Choose one item form list.',
                         allowed_values=['rock', 'paper', 'scissor'],
                         default='scissor'),
            LiteralInput('string_multiple_choice', 'String Multiple Choice',
                         abstract='Choose one or two items from list.',
                         metadata=[Metadata('Info')],
                         data_type='string',
                         allowed_values=['sitting duck', 'flying goose',
                                         'happy pinguin', 'gentle albatros'],
                         min_occurs=0, max_occurs=2,
                         default='gentle albatros'),
            # TODO: bbox is not supported yet by owslib
            # BoundingBoxInput('bbox', 'Bounding Box',
            #                  abstract='Bounding Box with EPSG:4326 and EPSG:3035.',
            #                  crss=['epsg:4326', 'epsg:3035'],
            #                  min_occurs=0),
            ComplexInput('text', 'Text',
                         abstract='Enter a URL pointing\
                            to a text document (optional)',
                         metadata=[Metadata('Info')],
                         min_occurs=0,
                         supported_formats=[Format('text/plain')]),
            ComplexInput('dataset', 'Dataset',
                         abstract="Enter a URL pointing to a NetCDF file (optional)",
                         metadata=[
                             Metadata('NetCDF Format', 'https://en.wikipedia.org/wiki/NetCDF',
                                      role='http://www.opengis.net/spec/wps/2.0/def/process/description/documentation')
                         ],
                         min_occurs=0,
                         supported_formats=[FORMATS.NETCDF]),
        ]
        outputs = [
            LiteralOutput('string', 'String', data_type='string'),
            LiteralOutput('int', 'Integer', data_type='integer'),
            LiteralOutput('float', 'Float', data_type='float'),
            LiteralOutput('boolean', 'Boolean', data_type='boolean'),
            LiteralOutput('time', 'Time', data_type='time'),
            LiteralOutput('date', 'Date', data_type='date'),
            LiteralOutput('datetime', 'DateTime', data_type='dateTime'),
            LiteralOutput('string_choice', 'String Choice',
                          data_type='string'),
            LiteralOutput('string_multiple_choice', 'String Multiple Choice',
                          data_type='string'),
            ComplexOutput('text', 'Text',
                          abstract='Copy of input text file.',
                          as_reference=True,
                          supported_formats=[Format('text/plain')]),
            ComplexOutput('dataset', 'Dataset',
                          abstract='Copy of input netcdf file.',
                          as_reference=True,
                          supported_formats=[FORMATS.NETCDF,
                                             FORMATS.TEXT]),
            BoundingBoxOutput('bbox', 'Bounding Box',
                              crss=['epsg:4326']),
        ]

        super(InOut, self).__init__(
            self._handler,
            identifier="inout",
            title="In and Out",
            version="1.0",
            abstract="Testing all WPS input and output parameters.",
            # profile=['birdhouse'],
            metadata=[
                Metadata('Birdhouse', 'http://bird-house.github.io/'),
                Metadata('User Guide', 'http://{{cookiecutter.project_slug}}.readthedocs.io/en/latest/',
                         role='http://www.opengis.net/spec/wps/2.0/def/process/description/documentation')],
            inputs=inputs,
            outputs=outputs,
            status_supported=True,
            store_supported=True)

    @staticmethod
    def _handler(request, response):
        response.outputs['string'].data = request.inputs['string'][0].data
        response.outputs['int'].data = request.inputs['int'][0].data
        response.outputs['float'].data = request.inputs['float'][0].data
        response.outputs['boolean'].data = request.inputs['boolean'][0].data
        response.outputs['time'].data = request.inputs['time'][0].data
        response.outputs['date'].data = request.inputs['date'][0].data
        response.outputs['datetime'].data = request.inputs['datetime'][0].data
        response.outputs['string_choice'].data = \
            request.inputs['string_choice'][0].data
        if 'string_multiple_choice' in request.inputs:
            response.outputs['string_multiple_choice'].data = ', '.join(
                [inpt.data for inpt in request.inputs['string_multiple_choice']])
        else:
            response.outputs['string_multiple_choice'].data = 'no value'
        # TODO: bbox is not working
        # response.outputs['bbox'].data = request.inputs['bbox'][0].data
        # TODO: how to copy file?
        response.outputs['text'].data_format = Format('text/plain')
        if 'text' in request.inputs:
            response.outputs['text'].file = request.inputs['text'][0].file
        else:
            response.outputs['text'].data = "request didn't have a text file."

        if 'dataset' in request.inputs:
            response.outputs['dataset'].data_format = FORMATS.NETCDF
            response.outputs['dataset'].file = request.inputs['dataset'][0].file
        else:
            response.outputs['dataset'].data_format = FORMATS.TEXT
            response.outputs['dataset'].data = "request didn't have a netcdf file."
        response.outputs['bbox'].data = [0, 0, 10, 10]
        return response
