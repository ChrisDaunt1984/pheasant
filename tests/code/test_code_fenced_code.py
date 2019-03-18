import re
from typing import Pattern

import pytest

from pheasant.code.renderer import Code


@pytest.fixture()
def source_simple():
    source_simple = "\n".join(
        [
            "begin\n~~~python\na=1\nb=1\n~~~\ntext",
            "begin\n~~~ruby inline\na=1\nb=1\n~~~\ntext",
        ]
    )
    return source_simple


def test_complile_pattern():
    assert isinstance(re.compile(Code.FENCED_CODE_PATTERN), Pattern)
    assert isinstance(re.compile(Code.INLINE_CODE_PATTERN), Pattern)


def test_renderer(code):
    assert code.config["fenced_code_template"] is not None


def test_render_fenced_code(parser, code, source_simple):
    assert "code__fenced_code" in parser.patterns
    assert "code__inline_code" in parser.patterns

    splitter = parser.split(source_simple)
    context = next(splitter)
    assert context.source == "begin\n"
    context = next(splitter)
    assert context.render_name == "code__fenced_code"
    assert context.group.source == "a=1\nb=1"
    next(splitter)
    context = next(splitter)
    assert context.group.option == "inline"
