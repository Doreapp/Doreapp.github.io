"""Main entrypoint"""

import argparse
import logging
import sys
from os import path

import yaml

from . import grammar, translator

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
    gram.check(data, "{}", logger, data)


def get_grammar() -> grammar.Type:
    """Return grammar to use"""
    file = path.join(path.dirname(__file__), "grammar.yml")
    return grammar.load(file)


def exit_based_on_log_level(handler: AggregationHandler, levelname: str):
    """
    Exit with 1 or 0 code based on the higher level message emitted
    (handled by the `handler`).
    The miniumum level at which a 1 code is used us defined by `levelname`.
    If levelname is `NONE`, return a 0 exit code.
    """
    level = NAME_TO_LEVEL.get(levelname)
    if level is None or handler.get_worst_level() < level:
        sys.exit(0)
    sys.exit(1)


def _get_parser():
    """Build CLI parser"""
    parser = argparse.ArgumentParser(
        "pyfolio",
        description="Program to manage a portfolio",
        epilog="Built by Antoine MANDIN",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        title="command", description="Program command", dest="command"
    )
    check_subparser = subparsers.add_parser(
        "check",
        help="Check the format of a yml file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    check_subparser.add_argument(
        "file", help="Path to the file to check", default="me.yml", nargs="?"
    )
    check_subparser.add_argument(
        "--fail-at",
        help="Minimum error level to return a non null exit code (NONE to never fail)",
        default="NONE",
        choices=("NONE", "INFO", "WARNING", "ERROR"),
    )
    translate_subparser = subparsers.add_parser(
        "translate",
        help="Translate a jekyll source folder, overriding some parts of the configuration",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    translate_subparser.add_argument("source", help="Path to jekyll source directory")
    translate_subparser.add_argument("dest", help="Path to destination directory")
    translate_subparser.add_argument("override", help="Path to overriding configuration directory")
    translate_subparser.add_argument(
        "--force", action="store_true", help="Whether to overriding existing destination directory"
    )
    return parser


def main(cli=None):
    """Main entrypoint from command line"""
    parser = _get_parser()
    args = parser.parse_args(cli)
    if args.command == "check":
        handler = AggregationHandler()
        check_file(get_grammar(), args.file, handler)
        exit_based_on_log_level(handler, args.fail_at)
    elif args.command == "translate":
        translator.translate(args.source, args.dest, args.override, args.force)
    else:
        raise argparse.ArgumentError("command", f"Unknown command '{args.command}'")


if __name__ == "__main__":
    main()
