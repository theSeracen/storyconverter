#!/usr/bin/env python3
# coding=utf-8

import pathlib
import re
from enum import Enum, auto
from typing import Optional


class StoryFormat(Enum):
    MARKDOWN = auto
    BBCODE = auto
    UNKNOWN = auto


def determine_source_markup(filename: pathlib.Path, file_contents: str) -> StoryFormat:
    if result := _determine_from_filename(filename):
        return result
    elif result := _determine_from_file_content(file_contents):
        return result
    else:
        return StoryFormat.UNKNOWN


def _determine_from_filename(filename: pathlib.Path) -> Optional[StoryFormat]:
    if filename.suffix.lower() in ['.md', '.mmd', '.markdown']:
        return StoryFormat.MARKDOWN
    else:
        return None


def _determine_from_file_content(content: str) -> Optional[StoryFormat]:
    if re.search(r'(?i)\[/?[bi]]', content):
        return StoryFormat.BBCODE
    elif re.search(r'\*{1,3}.*?\*{1,3}', content):
        return StoryFormat.MARKDOWN
