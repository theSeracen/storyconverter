#!/usr/bin/env python3
# coding=utf-8

import pytest

from storyconverter.commonfunctions import create_paragraph_breaks


@pytest.mark.parametrize(('test_string', 'expected'), ((['test'], 'test\n'),
                                                       (['test1', 'test2'], 'test1\n\ntest2\n'),
                                                       (['test1\n', 'test2', 'test3'], 'test1\n\ntest2\n\ntest3\n'),
                                                       (['test1\n\n\n', 'test2\n', 'test3'],
                                                        'test1\n\ntest2\n\ntest3\n')))
def test_simple_paragraph_breaks(test_string: list[str], expected: str):
    result = create_paragraph_breaks(test_string)
    result = ''.join(result)
    assert result == expected
