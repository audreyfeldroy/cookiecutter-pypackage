"""
Compare two Versions Using SemVer comparison
Make sure the `CURRENT_VERSION` and `MAIN_VERSION` environment variables are set
"""

import logging
from os import getenv

import click
import rich.traceback
from packaging.version import Version

rich.traceback.install(show_locals=True)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)8s]: %(message)s"
)

current_version_env = getenv("CURRENT_VERSION", None)
compared_version_env = getenv("COMPARED_VERSION", None)

if any([current_version_env is None, compared_version_env is None]):
    raise EnvironmentError(
        f"You must set the `CURRENT_VERSION` and `MAIN_VERSION` "
        "environment variables."
    )

current_version = Version(current_version_env)
compared_version = Version(compared_version_env)


@click.group()
def cli() -> None:
    """
    Version Helper CLI
    """


@cli.command()
@click.pass_context
def compare_versions(ctx: click.core.Context) -> None:
    """
    Compare two semantic versions
    """

    ctx.ensure_object(dict)
    if current_version <= compared_version:
        raise ValueError(
            f"Your current version ({current_version}) is not greater than "
            f"the `main` branch ({compared_version})"
        )
    else:
        logger.info("Current Version: %s", current_version)
        logger.info("Compared Version: %s", compared_version)
        logger.info("Version check passed, proceeding")


@cli.command()
@click.pass_context
def get_diff(ctx: click.core.Context):
    """
    Get the difference between two versions
    """
    major_difference = current_version.major - compared_version.major
    minor_difference = current_version.minor - compared_version.minor
    patch_difference = current_version.micro - compared_version.micro
    difference = sum([major_difference, minor_difference, patch_difference])
    if int(difference) != 1:
        logger.info("Current Version: %s", current_version)
        logger.info("Compared Version: %s", compared_version)
        raise RuntimeError(
            "You've specified an incompatible version change. Only one "
            "version can change between the Major, Minor, or Patch version levels."
        )
    else:
        if major_difference == 1:
            click.echo("major")
        elif minor_difference == 1:
            click.echo("minor")
        elif patch_difference == 1:
            click.echo("patch")
        else:
            raise NotImplementedError


if __name__ == "__main__":
    cli()
