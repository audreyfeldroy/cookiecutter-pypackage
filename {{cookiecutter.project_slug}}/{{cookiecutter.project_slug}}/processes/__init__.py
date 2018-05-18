from .wps_wordcounter import WordCounter
from .wps_inout import InOut
from .wps_sleep import Sleep

processes = [
    WordCounter(),
    InOut(),
    Sleep(),
]
