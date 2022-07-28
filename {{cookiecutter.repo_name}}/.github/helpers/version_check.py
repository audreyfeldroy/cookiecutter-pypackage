"""
Compare two Versions Using SemVer comparison
Make sure the `CURRENT_VERSION` and `MAIN_VERSION` environment variables are set
"""

import logging
from os import environ
from sys import argv

# noinspection PyPackageRequirements
from packaging.version import Version

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)8s]: %(message)s"
)

try:
    try:
        current_version = Version(argv[1])
        compared_version = Version(argv[2])
    except IndexError:
        current_version = Version(environ["CURRENT_VERSION"])
        compared_version = Version(environ["COMPARED_VERSION"])
    assert current_version > compared_version
except KeyError:
    raise EnvironmentError(
        f"You must set the `CURRENT_VERSION` and `MAIN_VERSION` "
        "environment variables or pass them in as arguments, "
        "respectively."
    )
except AssertionError:
    raise ValueError(
        f"Your current version ({current_version}) is not greater than "
        f"the `main` branch ({compared_version})"
    )

logger.info("Current Version: %s", current_version)
logger.info("Compared Version: %s", compared_version)
logger.info("Version check passed, proceeding")
