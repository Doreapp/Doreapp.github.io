"""
Translator of original webiste into another language (overriding some parts of the config)
"""

import os
import shutil

import yaml


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


def load(filename: str) -> dict:
    """Load a YAML file"""
    with open(filename, "r", encoding="utf-8") as fis:
        data = yaml.safe_load(fis)
    return data


def _merge_objects(source_obj: dict, dest_obj: dict):
    """
    Update dest_obj to add attributes from source_obj and override existing keys in conflict
    """
    for key, value in source_obj.items():
        current = dest_obj.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            _merge_objects(current, value)
        else:
            dest_obj[key] = value


def _merge_yml_files(source_file: str, dest_file: str):
    """
    Merge yml files, putting additional attributes from source into dest and overriding existing
    keys
    """
    src_dict = load(source_file)
    dest_dict = load(dest_file)
    _merge_objects(src_dict, dest_dict)
    with open(dest_file, "w", encoding="utf-8") as fos:
        yaml.dump(dest_dict, fos, encoding="utf-8", allow_unicode=True)


def _merge_directories(source: str, dest: str):
    """
    Copy source directory into dest directory overriding most files with the same name
    but merging YAML files having the same name.
    """
    dest_files = os.listdir(dest)
    for filename in os.listdir(source):
        src_file, dest_file = os.path.join(source, filename), os.path.join(dest, filename)
        if os.path.isdir(src_file):
            if not filename in dest_files:
                os.mkdir(dest_file)
            _merge_directories(src_file, dest_file)
        elif (filename.endswith(".yml") or filename.endswith(".yaml")) and filename in dest_files:
            _merge_yml_files(src_file, dest_file)
        else:
            shutil.copy(src_file, dest_file)


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
    _merge_directories(source, dest)
