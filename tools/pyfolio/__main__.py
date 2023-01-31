"""Main entrypoint"""

import argparse
import logging
from os import path

import yaml

from . import grammar

logging.basicConfig(format="%(levelname)s:%(message)s")
LOGGER = logging.getLogger(__name__)


def check_file(gram: grammar.Type, file: str):
    """Check the grammar of the file"""
    with open(file, "r", encoding="utf8") as fis:
        data = yaml.safe_load(fis)
    gram.check(data, "<root>", logging.getLogger(file))


def get_grammar() -> grammar.Type:
    """Return grammar to use"""
    file = path.join(path.dirname(__file__), "grammar.yml")
    return grammar.load(file)


def main(cli=None):
    """Main entrypoint from command line"""
    parser = argparse.ArgumentParser("pyfolio")
    parser.add_argument("file", help="Path to the file to check", default="me.yml", nargs="?")
    args = parser.parse_args(cli)
    check_file(get_grammar(), args.file)


if __name__ == "__main__":
    main()
