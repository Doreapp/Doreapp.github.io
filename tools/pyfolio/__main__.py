"""Main entrypoint"""

import argparse
import logging
import sys
from os import path

import yaml

from . import grammar

logging.basicConfig(format="[%(name)s] %(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)

NAME_TO_LEVEL = logging._nameToLevel  # pylint: disable=protected-access


class AggregationHandler(logging.Handler):
    """Logging handler to find the higher level message emitted"""

    _max_level = None

    def emit(self, record: logging.LogRecord) -> None:
        level = NAME_TO_LEVEL[record.levelname]
        if self._max_level is None or level > self._max_level:
            self._max_level = level

    def get_worst_level(self) -> int:
        """Retrun the maxuimum level for which at least a message was emitted"""
        return self._max_level or 0


def check_file(gram: grammar.Type, file: str, handler: logging.Handler):
    """Check the grammar of the file"""
    with open(file, "r", encoding="utf8") as fis:
        data = yaml.safe_load(fis)
    logger = logging.getLogger(path.basename(file))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    gram.check(data, "{}", logger)


def get_grammar() -> grammar.Type:
    """Return grammar to use"""
    file = path.join(path.dirname(__file__), "grammar.yml")
    return grammar.load(file)


def exit_based_on_log_level(handler: AggregationHandler, levelname: str):
    """
    Exit with 1 or 0 code based on the higher level message emitted
    (handled by the `handler`).
    The miniumum level at which an 1 code id used us defined by `levelname`.
    If levelname is `NONE`, return a 0 exit code.
    """
    level = NAME_TO_LEVEL.get(levelname)
    if level is None or handler.get_worst_level() < level:
        sys.exit(0)
    sys.exit(1)


def main(cli=None):
    """Main entrypoint from command line"""
    parser = argparse.ArgumentParser("pyfolio")
    parser.add_argument("file", help="Path to the file to check", default="me.yml", nargs="?")
    parser.add_argument(
        "--fail-at",
        help="Minimum error level to return a non null exit code (NONE to never fail)",
        default="NONE",
        choices=("NONE", "INFO", "WARNING", "ERROR"),
    )
    args = parser.parse_args(cli)
    handler = AggregationHandler()
    check_file(get_grammar(), args.file, handler)
    exit_based_on_log_level(handler, args.fail_at)


if __name__ == "__main__":
    main()
