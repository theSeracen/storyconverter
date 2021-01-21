#!/usr/bin/env python3
# coding=utf-8

import argparse
from pathlib import Path

import pytest

import storyconverter.__main__ as storyconverter
from storyconverter.exceptions import ValidationError
from storyconverter.format import StoryFormat


@pytest.fixture()
def args() -> argparse.Namespace:
    args = argparse.Namespace()
    args.source = ['test_resources/bbcode_source.txt']
    args.format = 'markdown'
    args.source_format = None
    args.overwrite = False
    args.verbosity = 0
    args.stdout = False
    args.output = '.'
    args.validate = False
    return args


def test_bbcode_to_markdown_file(args: argparse.Namespace, capsys: pytest.CaptureFixture, tmp_path: Path):
    args.output = tmp_path / 'output.md'
    storyconverter.main(args)
    captured = capsys.readouterr()
    assert args.output.exists()
    assert 'Determined filetype BBCODE heuristically' in captured.out
    assert 'Output file written' in captured.out


def test_bbcode_to_markdown_stdout(args: argparse.Namespace, capsys: pytest.CaptureFixture):
    args.stdout = True
    storyconverter.main(args)
    captured = capsys.readouterr()
    assert 'This is a *sample* bit of BBcode text.\n\n' == captured.out


def test_markdown_to_bbcode_file(args: argparse.Namespace, capsys: pytest.CaptureFixture, tmp_path: Path):
    args.source = ['test_resources/markdown_source.md']
    args.format = 'bbcode'
    args.output = tmp_path / 'output.txt'
    storyconverter.main(args)
    captured = capsys.readouterr()
    assert args.output.exists()
    assert 'Determined filetype MARKDOWN heuristically' in captured.out
    assert 'Output file written' in captured.out


def test_markdown_to_bbcode_stdout(args: argparse.Namespace, capsys: pytest.CaptureFixture):
    args.stdout = True
    args.source = ['test_resources/markdown_source.md']
    args.format = 'bbcode'
    storyconverter.main(args)
    captured = capsys.readouterr()
    assert 'This is a [I]sample[/I] of markdown text.\n\n' == captured.out


def test_validate_bbcode_command(args: argparse.Namespace, capsys: pytest.CaptureFixture):
    args.format = 'bbcode'
    args.validate = True
    storyconverter.main(args)
    captured = capsys.readouterr()
    assert 'Successfully validated source as BBCODE' in captured.out


def test_validate_markdown_command(args: argparse.Namespace, capsys: pytest.CaptureFixture):
    args.format = 'markdown'
    args.source = ['test_resources/markdown_source.md']
    args.validate = True
    storyconverter.main(args)
    captured = capsys.readouterr()
    assert 'Successfully validated source as MARKDOWN' in captured.out


@pytest.mark.parametrize('test_string', ('test', 'test *2*', 'another **test** string'))
def test_validate_markdown_function_good(args: argparse.Namespace, capsys: pytest.CaptureFixture, test_string: str):
    args.format = StoryFormat.MARKDOWN
    storyconverter.validate(args, [test_string])


@pytest.mark.parametrize('test_string', ('*test', '**test* two', '*test* **test* test'))
def test_validate_markdown_function_bad(args: argparse.Namespace, capsys: pytest.CaptureFixture, test_string: str):
    args.format = StoryFormat.MARKDOWN
    with pytest.raises(ValidationError):
        storyconverter.validate(args, [test_string])


@pytest.mark.parametrize('test_string', ('test', '[I]bbcode[/I]', 'a [i]test[/i]'))
def test_validate_bbcode_function_good(args: argparse.Namespace, capsys: pytest.CaptureFixture, test_string: str):
    args.format = StoryFormat.BBCODE
    storyconverter.validate(args, [test_string])


@pytest.mark.parametrize('test_string', ('[b]test', '[B]test[/I]'))
def test_validate_bbcode_function_bad(args: argparse.Namespace, capsys: pytest.CaptureFixture, test_string: str):
    args.format = StoryFormat.BBCODE
    with pytest.raises(ValidationError):
        storyconverter.validate(args, [test_string])
