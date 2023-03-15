"""
Translator of original webiste into another language (overriding some parts of the config)
"""

import os
import shutil


def _init_dest_dir(directory: str, force: bool = False):
    """Init the destination directory"""
    if os.path.exists(directory) and os.listdir(directory):
        if force:
            shutil.rmtree(directory)
        else:
            raise FileExistsError(
                f"Destination directory '{directory}' already exists. Use `force=True` to override"
            )
    os.makedirs(directory, exist_ok=True)


def _check_dir(directory: str):
    """Check correctness of source directory"""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' doesn't exist")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"'{directory}' doesn't point to a directory")


def translate(source: str, dest: str, overrides: str, force: bool = False):
    """
    Translate a full jekyll folder using overrides

    :param source: Path to the original jekyll source folder
    :param dest: Path to the directory that will contain the resulting jekyll source files.\
        Must not exist, except if `force` is True
    :param overrides: Path to the overriding configuration directory. Contains jekyll source that\
        will override the origin files.
    :param force: Whether to overwrite `dest` directory if it exists. Defaults to False.
    """
    _init_dest_dir(dest, force)
    _check_dir(source)
    _check_dir(overrides)
    shutil.copytree(source, dest, dirs_exist_ok=True)
    # TODO merge yml files rather than overriding them
    shutil.copytree(overrides, dest, dirs_exist_ok=True)
