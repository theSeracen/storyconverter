#!/usr/bin/env python3

import pytest

from storyconverter import bbcodeformatter
from storyconverter.exceptions import ValidationError


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['[B]teststring[/B]',
                              '[b]teststring[/b]',
                              'this is a [B]test string[/B] for bbcode',
                              'this [b]is[/b] multiple [B]bold [/b] in a string'],
                             ['**teststring**',
                              '**teststring**',
                              'this is a **test string** for bbcode',
                              'this **is** multiple **bold ** in a string']))
def test_bold_BBcode_to_markdown(test_string: str, expected: str):
    result = bbcodeformatter.convert_BBcode_to_markdown(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['[I]teststring[/I]',
                              '[i]teststring[/i]',
                              'this is a [I]test string[/I] for bbcode',
                              'this [I]is[/I] multiple [i]italics [/I] in a string'],
                             ['*teststring*',
                              '*teststring*',
                              'this is a *test string* for bbcode',
                              'this *is* multiple *italics * in a string']))
def test_italic_BBcode_to_markdown(test_string: str, expected: str):
    result = bbcodeformatter.convert_BBcode_to_markdown(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['[B][I]teststring[/I][/B]',
                              '[b][i]teststring[/i][/b]',
                              'this is a [B][I]test string[/I][/B] for bbcode'],
                             ['***teststring***',
                              '***teststring***',
                              'this is a ***test string*** for bbcode']))
def test_strong_BBcode_to_markdown(test_string: str, expected: str):
    result = bbcodeformatter.convert_BBcode_to_markdown(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['[URL]testing.com/[/URL]',
                              '[URL]testing.com[/URL]',
                              '[URL]testing.com[/URL] [URL]example.net[/URL]'],
                             ['<testing.com/>',
                              '<testing.com>',
                              '<testing.com> <example.net>']))
def test_link_simple_BBcode_to_markdown(test_string: str, expected: str):
    result = bbcodeformatter.convert_BBcode_to_markdown(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['[URL=example.com]test link[/URL]',
                              '[URL=example.com]test link[/URL][URL=second.test]other link[/URL]'],
                             ['[test link](example.com)',
                              '[test link](example.com)[other link](second.test)']))
def test_link_complex_BBcode_to_markdown(test_string: str, expected: str):
    result = bbcodeformatter.convert_BBcode_to_markdown(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['[URL=example.com]test link[/URL][URL]test.net[/URL]'],
                             ['[test link](example.com)<test.net>']))
def test_link_mixed_BBcode_to_markdown(test_string: str, expected: str):
    result = bbcodeformatter.convert_BBcode_to_markdown(test_string)
    assert result == expected


@pytest.mark.parametrize(('test_string', 'expected'),
                         zip(['This [I]is[/I] a [B]complicated[/B] string with [I][B]many[/B][/I] [URL=test.com]BBcode[/URL] options like [URL]example.net[/URL] for example'],
                             ['This *is* a **complicated** string with ***many*** [BBcode](test.com) options like <example.net> for example']))
def test_complex_string_BBcode_to_markdown(test_string: str, expected: str):
    result = bbcodeformatter.convert_BBcode_to_markdown(test_string)
    assert result == expected


@pytest.mark.parametrize('input_string', ('[B]test',
                                          '[I]test',
                                          '[i] test',
                                          '[b]test',
                                          'test[/b]',
                                          'test[/i]',
                                          'test[/I]',
                                          '[I][I]test[/I]',
                                          '[I]test[/B]',
                                          '[i]test[i]'))
def test_BBcode_validation_fail(input_string: str):
    with pytest.raises(ValidationError):
        bbcodeformatter.validate_bbCode([input_string])


@pytest.mark.parametrize('input_string', ('[I]This is a fine string.[/i]',
                                          '[B]This is a fine string.[/b]',
                                          '[B][I]This is a fine string.[/B][/I]',
                                          'This is [I]fine[/i] string.'))
def test_BBcode_validation_correct(input_string: str):
    bbcodeformatter.validate_bbCode([input_string])
