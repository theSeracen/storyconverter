#!/usr/bin/env python3
# encoding=utf-8

from more_itertools import intersperse


def create_paragraph_breaks(lines: list[str]) -> list[str]:
    """Ensures that there is a spare line between each line of text"""
    halfway_lines_list = []
    for line in lines:
        line = line.strip('\n').split('\n')
        line = [sub_line + '\n' for sub_line in line]
        halfway_lines_list.append(line)

    flattened_lines = _flatten(halfway_lines_list)
    return list(intersperse('\n', flattened_lines))


def _flatten(passed_argument):
    rt = []
    for item in passed_argument:
        if isinstance(item, list):
            rt.extend(_flatten(item))
        else:
            rt.append(item)
    return rt


def concatenate_files(file_list: list[str]):
    file_contents = []
    for file_location in sorted(file_list):
        with open(file_location, 'r') as file:
            file_contents.append(file.read())

    return '\n-------------\n'.join(file_contents)
