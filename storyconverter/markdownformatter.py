#!/usr/bin/env python3
# encoding=utf-8

"""Module for converting a markdown file"""

import re


def check_markdown(line: str) -> str:
    """Check the passed string and validate all markdown in it"""
    # TODO: add proper checks
    line = _double_paragraph_breaks(line)
    return line


def convert_markdown_to_BBcode(line: str) -> str:
    """Takes a string of markdown formatting and converts it to BBcode"""
    formatting_functions = [
        _link_markdown_to_BBcode,
        _strong_markdown_to_BBcode,
        _bold_markdown_to_BBcode,
        _italic_markdown_to_BBcode,
        _double_paragraph_breaks]
    for formatFunc in formatting_functions:
        line = formatFunc(line)
    return line


def _link_markdown_to_BBcode(line: str) -> str:
    simple_pattern = re.compile(r'<(.*?)>')
    complex_pattern = re.compile(r'\[(.*?)]\(((http|www)?.*?)\)')

    for simple_match in re.finditer(simple_pattern, line):
        line = line.replace(simple_match.group(0), '[URL]{}[/URL]'.format(simple_match.group(1)))
    for complex_match in re.finditer(complex_pattern, line):
        line = line.replace(complex_match.group(
            0), '[URL={}]{}[/URL]'.format(complex_match.group(2), complex_match.group(1)))

    return line


def _double_paragraph_breaks(line: str) -> str:
    """Doubles the new lines in the document, if there is not already a blank line between each paragraph"""
    # number 5 is completely arbitrary
    if len(re.findall(r'\n\n', line)) >= 5:
        return line
    else:
        return line.replace('\n', '\n\n')


def _bold_markdown_to_BBcode(line: str) -> str:
    line = re.sub(r'\*{2}(.*?)\*{2}', r'[B]\1[/B]', line)
    return line


def _strong_markdown_to_BBcode(line: str) -> str:
    line = re.sub(r'\*{3}(.*?)\*{3}', r'[B][I]\1[/I][/B]', line)
    return line


def _italic_markdown_to_BBcode(line: str) -> str:
    line = re.sub(r'\*(.*?)\*', r'[I]\1[/I]', line)
    return line