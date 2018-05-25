import re
from collections import Counter

from pywps import Process
from pywps import ComplexInput, ComplexOutput, FORMATS
from pywps.app.Common import Metadata

import logging
LOGGER = logging.getLogger("PYWPS")


class WordCounter(Process):
    """
    Notes
    -----

    Counts ocurrences of all words in a document.
    """
    def __init__(self):
        inputs = [
            ComplexInput('text', 'Text document',
                         abstract='URL pointing to a text document, for example "Alice in Wonderland":'
                                  ' http://www.gutenberg.org/cache/epub/19033/pg19033.txt',
                         supported_formats=[FORMATS.TEXT]), ]
        outputs = [
            ComplexOutput('output', 'Word counter result',
                          as_reference=True,
                          supported_formats=[FORMATS.JSON]), ]

        super(WordCounter, self).__init__(
            self._handler,
            identifier='wordcounter',
            title='Word Counter',
            abstract="Counts words in a given text.",
            version='1.0',
            metadata=[
                Metadata('User Guide', 'http://{{cookiecutter.project_slug}}.readthedocs.io/en/latest/'),
                Metadata('Free eBooks at Gutenberg', 'http://www.gutenberg.org/'),
                Metadata('Example: Alice in Wonderland', 'http://www.gutenberg.org/cache/epub/19033/pg19033.txt'),
            ],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True)

    @staticmethod
    def _handler(request, response):
        wordre = re.compile(r'\w+')

        def words(f):
            for line in f:
                for word in wordre.findall(line):
                    yield word

        counts = Counter(words(request.inputs['text'][0].stream))
        sorted_counts = sorted([(v, k) for (k, v) in counts.items()],
                               reverse=True)
        with open('out.txt', 'w') as fout:
            fout.write(str(sorted_counts))
            response.outputs['output'].file = fout.name
        return response
