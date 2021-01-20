#!/usr/bin/env python3
# coding=utf-8

from pathlib import Path

import pytest

import storyconverter.format as formatter


@pytest.mark.parametrize(('file_name', 'file_contents'), ((Path('test.md'), ''),
                                                          (Path('test.txt'), 'test *string*')))
def test_determine_markdown(file_name: Path, file_contents: str):
    result = formatter.determine_source_markup(file_name, file_contents)
    assert result is formatter.StoryFormat.MARKDOWN


@pytest.mark.parametrize(('file_name', 'file_contents'), ((Path('test.txt'), '[B]test[/B]'),
                                                          (Path('test.txt'), 'other [I]test[/I]'),
                                                          (Path('test.txt'), '[i]test[/i]')))
def test_determine_BBcode(file_name: Path, file_contents: str):
    result = formatter.determine_source_markup(file_name, file_contents)
    assert result is formatter.StoryFormat.BBCODE


@pytest.mark.parametrize(('file_name', 'file_contents'), ((Path('test.txt'), ''),
                                                          (Path('test.txt'), 'random')))
def test_determine_ambiguous(file_name: Path, file_contents: str):
    result = formatter.determine_source_markup(file_name, file_contents)
    assert result is formatter.StoryFormat.UNKNOWN
