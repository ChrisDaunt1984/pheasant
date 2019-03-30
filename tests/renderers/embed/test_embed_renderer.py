from pheasant.renderers.embed.embed import (get_language_from_path, inspect,
                                            resolve_path)
from pheasant.renderers.jupyter.client import get_kernel_name


def test_renderer(embed):
    output = embed.parse("~~~\nabc\n~~~\n")
    assert 'class="markdown"' in output

    output = embed.parse("{%setup.py[1:2]%}")
    assert '<code class="python">import re</code>' in output

    output = embed.parse("{%abc.py%}")
    assert output == '<p style="font-color:red">File not found: abc.py</p>\n'


def test_get_languate_from_path():
    assert get_language_from_path("a.py") == "python"
    assert get_language_from_path("a.yml") == "yaml"
    assert get_language_from_path("a.txt") == "text"


def test_inspect_error():
    kernel_name = get_kernel_name("python")
    assert inspect("ABC", kernel_name) == "inspect error"


def test_resolve_path():
    assert resolve_path("abc.py?python")["language"] == "python"