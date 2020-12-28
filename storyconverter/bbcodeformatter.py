#!/usr/bin/env python3
# encoding=utf-8

"""Module for converting BBcode tags"""

import re

from storyconverter.commonfunctions import create_paragraph_breaks


def convert_BBcode_to_markdown(line: str) -> str:
    """Converts a string of BBcode to markdown formatting"""
    formatting_functions = [
        _bold_bbcode_to_markdown,
        _italics_bbcode_to_markdown,
        _links_bbcode_to_markdown]
    for formatfunc in formatting_functions:
        line = formatfunc(line)
    return line


def check_bbcode(line: str) -> str:
    """Check the passed string and validate all BBcode in it"""
    # TODO: add proper checks
    return line


def _italics_bbcode_to_markdown(line: str) -> str:
    line = re.sub(r'(?i)\[/?i]', '*', line)
    return line


def _bold_bbcode_to_markdown(line: str) -> str:
    line = re.sub(r'(?i)\[/?b]', '**', line)
    return line


def _links_bbcode_to_markdown(line: str) -> str:
    simple_link_pattern = re.compile(r'\[URL](.*?)\[/URL]')
    complex_link_pattern = re.compile(r'\[URL=(.*?)](.*?)\[/URL]')

    for simple_match in re.finditer(simple_link_pattern, line):
        line = line.replace(simple_match.group(0), '<{}>'.format(simple_match.group(1)))
    for complex_match in re.finditer(complex_link_pattern, line):
        line = line.replace(complex_match.group(0), '[{}]({})'.format(complex_match.group(2), complex_match.group(1)))

    return line
