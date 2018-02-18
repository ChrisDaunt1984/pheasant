import pytest

from pheasant.jupyter.converter import initialize
from pheasant.jupyter.markdown import convert, fenced_code_splitter
from pheasant.utils import read


@pytest.fixture
def stream_input():
    return read(__file__, 'mkdocs/docs/markdown_stream_input.md')


@pytest.fixture
def stream_output():
    return read(__file__, 'mkdocs/docs/markdown_stream_output.md')


def test_fenced_code_splitter(stream_input):
    nodes = fenced_code_splitter(stream_input)
    assert next(nodes) == '# Title\n\nText1\n\n'
    assert next(nodes) == ('python', 'def func(x):\n    return 2 * x\n', [])
    assert next(nodes) == '\nText2\n\n'
    assert next(nodes) == ('python', 'func(1)\n', [])
    assert next(nodes) == '\n'
    assert next(nodes) == ('python', 'func(2)\n', ['hide-input'])
    assert next(nodes) == '\n'
    assert next(nodes) == ('python', 'func(3)\n', ['hide-output'])
    assert next(nodes) == '\n'
    assert next(nodes) == ('python', 'func(4)\n', ['hide'])
    assert next(nodes) == '\nText3\n\n'


def test_execute_and_export_stream(stream_input, stream_output):
    initialize()
    output = convert(stream_input)
    assert isinstance(output, str)
    lines = zip(output.split('\n'), stream_output.split('\n'))
    for markdown_line, stream_output_line in lines:
        pass
        # assert markdown_line == stream_output_line
