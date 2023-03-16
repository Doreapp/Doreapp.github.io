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


def merge_arrays(source_arr: list, dest_arr: list):
    """
    Update dest_arr to match source_arr content, while merging some of the children.

    The correspondance between a child element of `source_arr` and one of `dest_arr` can be
    made using an attribute `_xxx` in `source_arr` having the exact same value as the `xxx`
    attribute in `dest_arr`.

    However, if no `_xxx` attribute is found for a children from `dest_arr`, then it will be
    removed.
    All the elements from `source_arr` will be moved to `dest_arr` anyway.
    """
    mapping = {}
    copied_source = list(source_arr)
    for element in copied_source:
        if isinstance(element, dict):
            for key, value in element.items():
                if key.startswith("_"):
                    prev = mapping.get(key[1:], {})
                    prev[value] = element
                    mapping[key[1:]] = prev
                    break
    result = []
    for element in dest_arr:
        if isinstance(element, dict):
            source_value, match_key = None, None
            for key, value in element.items():
                source_value = mapping.get(key)
                if source_value is None:
                    continue
                source_value = source_value.get(value)
                if source_value is not None:
                    match_key = key
                    break
            if source_value is not None:
                merge_objects(source_value, element)
                del element[f"_{match_key}"]
                result.append(element)
                copied_source.remove(source_value)
                continue
    dest_arr.clear()
    dest_arr.extend(result)
    dest_arr.extend(copied_source)


def merge_objects(source_obj: dict, dest_obj: dict):
    """
    Update dest_obj to add attributes from source_obj and override existing keys in conflict
    """
    for key, value in source_obj.items():
        current = dest_obj.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merge_objects(value, current)
        elif isinstance(current, list) and isinstance(value, list):
            merge_arrays(value, current)
        else:
            dest_obj[key] = value


def _merge_yml_files(source_file: str, dest_file: str):
    """
    Merge yml files, putting additional attributes from source into dest and overriding existing
    keys
    """
    src_dict = load(source_file)
    dest_dict = load(dest_file)
    merge_objects(src_dict, dest_dict)
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
    _merge_directories(overrides, dest)
