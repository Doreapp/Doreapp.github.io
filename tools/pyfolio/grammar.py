"""
Grammar to analyse the file
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import Logger
from typing import Dict as TDict

import yaml

URL_REGEX = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}"
    r"\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)


@dataclass
class Type(ABC):
    """Abstract representation of a type in the grammar"""

    @abstractmethod
    def check(self, node, location: str, logger: Logger) -> bool:
        """
        Check whether the node matches this type

        :param node: Instance to check
        :param location: Position of the instance
        :param logger: Logger instance to broadcast issues to
        :return: False whenever the type isn't matched at all, else true
        """


@dataclass
class String(Type):
    """String type"""

    url: bool = False
    """Whether the string represents a URL"""

    def check(self, node, location: str, logger: Logger) -> bool:
        if not isinstance(node, str):
            logger.error("`%s` is not a string but a %s: '%s'", location, type(node).__name__, node)
            return False
        if self.url and not URL_REGEX.fullmatch(node):
            logger.error("`%s` is not a URL string: '%s'", location, node)
            return False
        return True


@dataclass
class List(Type):
    """List node"""

    children_type: Type
    """Type of the list elements"""

    must_have_a_single_child: bool = False
    """Whether the list must contain exactly one element"""

    def check(self, node, location: str, logger: Logger) -> bool:
        if not isinstance(node, list):
            logger.error("`%s` is not a list but a %s: '%s'", location, type(node).__name__, node)
            return False
        if self.must_have_a_single_child and len(node) != 1:
            logger.warning("`%s` should have a single child, but got %s", location, len(node))
        result = True
        for i, child in enumerate(node):
            result = result and self.children_type.check(child, f"{location}[{i}]", logger)
        return result


@dataclass
class Dict(Type):
    """Dict node"""

    needed: TDict[str, Type]
    optional: TDict[str, Type]

    def check(self, node, location: str, logger: Logger) -> bool:
        if not isinstance(node, dict):
            logger.error(
                "`%s` is not a dictionary but a %s: '%s'", location, type(node).__name__, node
            )
            return False
        needed_missing, optional_missing = set(self.needed), set(self.optional)
        for key, value in node.items():
            if key in self.needed:
                self.needed[key].check(value, f"{location}.{key}", logger)
                needed_missing.remove(key)
            elif key in self.optional:
                self.optional[key].check(value, f"{location}.{key}", logger)
                optional_missing.remove(key)
            else:
                logger.warning("`%s` contains an unused attribute: '%s'", location, key)
        if len(optional_missing) > 0:
            logger.info(
                "`%s` doesn't have some optional attributes: %s", location, optional_missing
            )
        if len(needed_missing) > 0:
            for missing in needed_missing:
                logger.error(
                    "`%s` doesn't have the attribute '%s' which is required", location, missing
                )
            return False
        return True


def _parse(location: str, element) -> Type:
    """Parse a subelement of the grammar"""
    if isinstance(element, dict):
        result = Dict({}, {})
        for key, value in element.items():
            vtype = _parse(f"{location}.{key}", value)
            if key.endswith("(1)") and isinstance(vtype, List):
                vtype.must_have_a_single_child = True
                key = key[:-3]
            if key.endswith("(o)"):
                result.optional[key[:-3]] = vtype
            else:
                result.needed[key] = vtype
        return result
    if isinstance(element, list):
        if len(element) != 1:
            raise Exception(
                "Lists must contain a single child. " f"{location} contains {len(element)}."
            )
        return List(_parse(f"{location}[0]", element[0]))
    if isinstance(element, str):
        if element == "str":
            return String()
        if element == "url":
            return String(url=True)
        raise Exception(f"{location} is an unknown str '{element}'")
    raise Exception(f"{location} has an unhandled type '{type(element).__name__}'.")


def load(filepath: str) -> Type:
    """Load a grammar from a YAML file"""
    with open(filepath, "r", encoding="utf8") as fis:
        raw = yaml.safe_load(fis)
    return _parse("", raw)
