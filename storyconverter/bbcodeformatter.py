#!/usr/bin/env python3
# encoding=utf-8
"""Module for converting BBcode tags"""

import re


def convert_BBcode_to_markdown(line: str) -> str:
    """Converts a string of BBcode to markdown formatting"""
    formatting_functions = [
        _bold_bbcode_to_markdown,
        _italics_bbcode_to_markdown,
        _links_bbcode_to_markdown,
        _double_paragraph_breaks]
    for formatfunc in formatting_functions:
        line = formatfunc(line)
    return line


def check_bbcode(line: str) -> str:
    """Check the passed string and validate all BBcode in it"""
    line = _double_paragraph_breaks(line)
    return line


def _italics_bbcode_to_markdown(line: str) -> str:
    match_pattern = re.compile(r'(?i)\[/?i]')
    line = match_pattern.sub('*', line)
    return line


def _bold_bbcode_to_markdown(line: str) -> str:
    match_pattern = re.compile(r'(?i)\[/?b]')
    line = match_pattern.sub('**', line)
    return line


def _double_paragraph_breaks(line: str) -> str:
    """Doubles the new lines in the document, if there is not already a blank line between each paragraph"""
    # number 5 is completely arbitrary; just need to find if there's more than 5 empty lines
    if len(re.findall(r'\n\n', line)) >= 5:
        return line
    else:
        return line.replace('\n', '\n\n')


def _links_bbcode_to_markdown(line: str) -> str:
    simple_link_pattern = r'\[URL\](.*?)\[/URL\]'
    complex_link_pattern = r'\[URL=(.*?)\](.*?)\[/URL\]'

    substitutions = []

    for match in re.findall(r'({}|{})'.format(simple_link_pattern, complex_link_pattern), line):
        match = match[0]

        if re.search(complex_link_pattern, match):
            link = re.search(complex_link_pattern, match)
            substitutions.append(
                (re.sub(complex_link_pattern, '[' + link.group(2) + '](' + link.group(1) + ')', match),
                 match))

        elif re.search(simple_link_pattern, match):
            link = re.search(simple_link_pattern, match)
            substitutions.append((re.sub(simple_link_pattern, '<' + link.group(1) + '>', match), match))

    for (new, old) in substitutions:
        line = line.replace(old, new)
    return line
