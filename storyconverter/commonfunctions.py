#!/usr/bin/env python3
# encoding=utf-8

import pathlib
from typing import Any

from more_itertools import intersperse


def create_paragraph_breaks(lines: list[str]) -> list[str]:
    """Ensures that there is a spare line between each line of text"""
    halfway_lines_list = []
    for line in lines:
        line = line.split('\n')
        line = [sub_line.replace('\n', '').strip() for sub_line in line]
        line = [sub_line + '\n' for sub_line in line if sub_line != '']
        halfway_lines_list.append(line)

    flattened_lines = _flatten(halfway_lines_list)
    return list(intersperse('\n', flattened_lines))


def _flatten(passed_argument: list[Any]) -> list:
    out = []
    for item in passed_argument:
        if isinstance(item, list):
            out.extend(_flatten(item))
        else:
            out.append(item)
    return out


def concatenate_files(file_list: list[pathlib.Path]) -> list[str]:
    file_contents = []
    for file_location in sorted(file_list):
        with open(file_location, 'r') as file:
            file_contents.append(file.read())

    # TODO: make this file separator configurable
    return _flatten(list(intersperse(['\n-------------\n'], file_contents)))
