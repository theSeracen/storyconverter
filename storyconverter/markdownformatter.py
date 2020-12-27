"""Module for converting a markdown file"""

import os
import re


def find_files(directory: str):
    files = os.listdir(directory)
    # create list of all markdown files in directory
    markdown_files = [(directory + '\\' + file)
                      for file in files if file.endswith('.mmd')]
    for md_file in markdown_files:
        format_markdown_file_to_BBcode(md_file)


def check_markdown(line: str) -> str:
    """Check the passed string and validate all markdown in it"""
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
    simple_pattern = re.compile(r'\[(.*?)]\(((http|www)?.*?)\)')
    complex_pattern = re.compile(r'<(.*?)>')
    substitutions = []

    for match in re.findall(r'({}|{})'.format(simple_pattern, complex_pattern), line):
        match = match[0]

        if re.search(simple_pattern, match):
            link = re.search(simple_pattern, match)
            substitutions.append(
                (re.sub(simple_pattern, '[URL=' + link.group(2) + ']' + link.group(1) + '[/URL]', match), match))

        elif re.search(complex_pattern, match):
            link = re.search(complex_pattern, match)
            substitutions.append((re.sub(complex_pattern, '[URL]' + link.group(1) + '[/URL]', match), match))

    for (new, old) in substitutions:
        line = line.replace(old, new)
    return line


def _double_paragraph_breaks(line: str) -> str:
    """Doubles the new lines in the document, if there is not already a blank line between each paragraph"""
    # number 5 is completely arbitrary
    if len(re.findall(r'\n\n', line)) >= 5:
        return line
    else:
        return line.replace('\n', '\n\n')


def _bold_markdown_to_BBcode(line: str) -> str:
    """Takes a string and returns a single BBcode string with bold formatting"""
    # explode into bold parts
    bold_parts = re.split(r'(\*{2}.+?\*{2})', line)
    for part in range(len(bold_parts)):
        if bold_parts[part - 1].startswith('**'):
            bold_parts[part - 1] = '[B]' + bold_parts[part - 1].lstrip('**')
        if bold_parts[part - 1].endswith('**'):
            bold_parts[part - 1] = bold_parts[part - 1].rstrip('**') + '[/B]'
    return ''.join(bold_parts)


def _strong_markdown_to_BBcode(line: str) -> str:
    strong_parts = re.split(r'(\*{3}.+?\*{3})', line)
    for part in range(len(strong_parts)):
        if strong_parts[part - 1].startswith('***'):
            strong_parts[part - 1] = '[B][I]' + strong_parts[part - 1].lstrip('***')
        if strong_parts[part - 1].endswith('***'):
            strong_parts[part - 1] = strong_parts[part - 1].rstrip('***') + '[/I][/B]'
    return ''.join(strong_parts)


def _italic_markdown_to_BBcode(line: str) -> str:
    italic_parts = re.split(r'(\*.+?\*)', line)
    for part in range(len(italic_parts)):
        if italic_parts[part - 1].startswith('*'):
            italic_parts[part - 1] = '[I]' + italic_parts[part - 1].lstrip('*')
        if italic_parts[part - 1].endswith('*'):
            italic_parts[part - 1] = italic_parts[part - 1].rstrip('*') + '[/I]'
    return ''.join(italic_parts)


def format_markdown_file_to_BBcode(file: str):
    with open(file, 'r', encoding='utf-8') as markdown:
        lines = markdown.readlines()
        formatted = []
        for line in lines:
            # add double lines for each paragraph
            line = line.replace('\n', '\n\n')
            formatted.append(convert_markdown_to_BBcode(line))
    with open(file.rstrip('.mmd') + 'formatted.txt', 'w') as textfile:
        textfile.writelines(formatted)
