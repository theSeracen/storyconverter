#!/usr/bin/env python3
# encoding=utf-8

"""Module for converting BBcode tags"""

import re

from storyconverter.exceptions import ValidationError


def convert_BBcode_to_markdown(line: str) -> str:
    """Converts a string of BBcode to markdown formatting"""
    formatting_functions = [
        _bold_bbcode_to_markdown,
        _italics_bbcode_to_markdown,
        _links_bbcode_to_markdown]
    for formatfunc in formatting_functions:
        line = formatfunc(line)
    return line


def validate_bbCode(lines: list[str]):
    """Check the passed string and validate all BBcode in it"""
    # Convert all to uppercase so flags are easier to catch
    lines = ''.join(lines).upper()
    for markdown_pair in (('[B]', '[/B]'), ('[I]', '[/I]')):
        pair1 = lines.count(markdown_pair[0])
        pair2 = lines.count(markdown_pair[1])
        try:
            assert pair1 == pair2
        except AssertionError:
            raise ValidationError(
                f'BBCode pairs are unequal: {markdown_pair[0]} {pair1}, {markdown_pair[1]} {pair2}')
    return True


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
        line = line.replace(simple_match.group(0), f'<{simple_match.group(1)}>')
    for complex_match in re.finditer(complex_link_pattern, line):
        line = line.replace(complex_match.group(0), f'[{complex_match.group(2)}]({complex_match.group(1)})')

    return line
