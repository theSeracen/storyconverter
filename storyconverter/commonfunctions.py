#!/usr/bin/env python3
# encoding=utf-8

from typing import List


def concatenate_files(file_list: List[str]):
    file_contents = []
    for file_location in sorted(file_list):
        with open(file_location, 'r') as file:
            file_contents.append(file.read())

    return '\n-------------\n'.join(file_contents)
