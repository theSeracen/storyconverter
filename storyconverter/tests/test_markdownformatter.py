#!/usr/bin/env python3

import pytest

from storyconverter import markdownformatter
from storyconverter.exceptions import ValidationError


@pytest.mark.parametrize(('test_string', 'expected'),
                         (('**teststring**', '[B]teststring[/B]'),
                          ('this is a **test string** for bbcode',
                           'this is a [B]test string[/B] for bbcode'),
                          ('this **is** multiple **bold** in a string',
                             'this [B]is[/B] multiple [B]bold[/B] in a string')))
def test_bold_markdown_to_BBcode(test_string: str, expected: str):
    result = markdownformatter.convert_markdown_to_BBcode(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['*teststring*',
                              'this is a *test string* for bbcode',
                              'this *is* multiple *italics * in a string'],
                             ['[I]teststring[/I]',
                              'this is a [I]test string[/I] for bbcode',
                              'this [I]is[/I] multiple [I]italics [/I] in a string']))
def test_italics_markdown_to_BBcode(test_string: str, expected: str):
    result = markdownformatter.convert_markdown_to_BBcode(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['***teststring***',
                              'this is a ***test string*** for bbcode',
                              'this has **unusual **spacing issues',
                              'this **is** a test with **multiple bold**.'],
                             ['[B][I]teststring[/I][/B]',
                              'this is a [B][I]test string[/I][/B] for bbcode',
                              'this has [B]unusual [/B]spacing issues',
                              'this [B]is[/B] a test with [B]multiple bold[/B].']))
def test_strong_markdown_to_BBcode(test_string: str, expected: str):
    result = markdownformatter.convert_markdown_to_BBcode(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['<testing.com/>',
                              '<testing.com>',
                              '<testing.com> <example.net>'],
                             ['[URL]testing.com/[/URL]',
                              '[URL]testing.com[/URL]',
                              '[URL]testing.com[/URL] [URL]example.net[/URL]']))
def test_link_simple_markdown_to_BBcode(test_string: str, expected: str):
    result = markdownformatter.convert_markdown_to_BBcode(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['[test link](example.com)',
                              '[test link](example.com)[other link](second.test)',
                              '[test link one](example1.com) then some text [test link 2](example2.com)'],
                             ['[URL=example.com]test link[/URL]',
                              '[URL=example.com]test link[/URL][URL=second.test]other link[/URL]',
                              '[URL=example1.com]test link one[/URL] then some text [URL=example2.com]test link 2[/URL]']))
def test_link_complex_markdown_to_BBcode(test_string: str, expected: str):
    result = markdownformatter.convert_markdown_to_BBcode(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['[test link](example.com)<test.net>'],
                             ['[URL=example.com]test link[/URL][URL]test.net[/URL]']))
def test_link_mixed_markdown_to_BBcode(test_string: str, expected: str):
    result = markdownformatter.convert_markdown_to_BBcode(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['This *is* a **complicated** string with ***many*** [BBcode](test.com) options like <example.net> for example'],
                             ['This [I]is[/I] a [B]complicated[/B] string with [B][I]many[/I][/B] [URL=test.com]BBcode[/URL] options like [URL]example.net[/URL] for example']))
def test_complex_strings_markdown_to_BBcode(test_string: str, expected: str):
    result = markdownformatter.convert_markdown_to_BBcode(test_string)
    assert result == expected


@pytest.mark.parametrize('test_string', ('*test',
                                         '**test',
                                         '***test',
                                         'test*',
                                         '*test**',
                                         '*test**test*',
                                         '**test* *'))
def test_markdown_validation_fail(test_string: str):
    with pytest.raises(ValidationError):
        markdownformatter.validate_markdown([test_string])


@pytest.mark.parametrize('test_string', ('*test*',
                                         '**test**',
                                         '*test* *test*',
                                         '*one* and *two*',
                                         '**one** and *two*'))
def test_markdown_validation_correct(test_string: str):
    markdownformatter.validate_markdown([test_string])
