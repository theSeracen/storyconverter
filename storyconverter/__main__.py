#!/usr/bin/env python3
# encoding=utf-8

import argparse
import logging
import pathlib
import re
import sys

from storyconverter.bbcodeformatter import convert_BBcode_to_markdown
from storyconverter.commonfunctions import (concatenate_files,
                                            create_paragraph_breaks)
from storyconverter.markdownformatter import convert_markdown_to_BBcode

logger = logging.getLogger()
parser = argparse.ArgumentParser()


def _setup_arguments():
    parser.add_argument('source', type=str, nargs='+')
    parser.add_argument('format', choices=['markdown', 'bbcode'], type=str)
    parser.add_argument('--source-format', choices=['markdown', 'bbcode'], default=None)
    parser.add_argument('-O', '--output', type=str, default='.')
    parser.add_argument('--overwrite', action='store_true', default=False)


def _determine_source_format(filename: pathlib.Path, file_contents: str) -> str:
    if filename.suffix.lower() in ['.md', '.mmd', '.markdown']:
        return 'markdown'

    if re.search(r'(?i)\[/?[bi]]', file_contents):
        return 'bbcode'
    elif re.search(r'\*{1,3}.*?\*{1,3}', file_contents):
        return 'markdown'


if __name__ == '__main__':
    logger.setLevel(1)
    stream = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    _setup_arguments()
    args = parser.parse_args()

    args.output = pathlib.Path(args.output).resolve()
    args.source = [pathlib.Path(s).resolve() for s in args.source]

    if not all([s.exists() for s in args.source]):
        raise Exception('Source file does not exist')

    if args.output.is_dir():
        if not args.output.exists():
            raise Exception('Destination directory does not exist')
        args.output /= args.source[0].stem

    source_data = concatenate_files(args.source)
    for file in args.source:
        logger.info('Loading {}'.format(file))

    if not args.source_format:
        args.source_format = _determine_source_format(args.source[0], ''.join(source_data[0]))
        logger.info('Determined filetype {} heuristically'.format(args.source_format))

    if args.source_format == args.format:
        raise Exception('Source and wanted formats are the same')

    converted_data = create_paragraph_breaks(source_data)
    if args.format == 'markdown' and args.source_format == 'bbcode':
        logger.info('Converting BBcode to markdown')
        converted_data = [convert_BBcode_to_markdown(line) for line in converted_data]
        args.output = pathlib.Path(str(args.output) + '.md')

    elif args.format == 'bbcode' and args.source_format == 'markdown':
        logger.info('Converting Markdown to BBcode')
        converted_data = [convert_markdown_to_BBcode(line) for line in converted_data]
        args.output = pathlib.Path(str(args.output) + '.txt')

    if args.output.exists() and args.overwrite is False:
        raise Exception('Output file exists and overwriting disabled')

    with open(args.output, 'w') as file:
        file.write(''.join(converted_data))
