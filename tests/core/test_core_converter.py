import re

import pytest

from pheasant.core.converter import Converter
from pheasant.renderers.number.number import Header


def test_converter_init(jupyter):
    converter = Converter()
    assert converter.convert("abc") == "abc"

    converter.register("markdown", [jupyter, Header()])
    assert len(converter.parsers) == 1


def test_converter(jupyter):
    converter = Converter()
    converter.register("markdown", [jupyter, Header()])
    output = converter.convert("abd\n# a\n## b\n```python\n2*3\n```\n")
    output = re.sub(r"(\<.*?\>)|\n", "", output)
    assert output == "abd# 1 a## 1.1 b2*36"

    with pytest.raises(ValueError):
        converter.register("markdown", [jupyter])

    converter.update_config({"jupyter": {"a": "b"}})
    assert jupyter.config["a"] == "b"


def test_converter_special_function(converter):
    assert repr(converter) == "<Converter#converter['preprocess', 'postprocess']>"
    assert repr(converter["preprocess"]) == "<Parser#preprocess[3]>"
    assert repr(converter["preprocess", "jupyter"]) == "<Jupyter#jupyter[2]>"
    with pytest.raises(KeyError):
        converter["preprocess", "abc"]


def test_multiple_parser(converter):
    source = "# title {#a#}\ntext {#a#}\n## section\n```python\n1/0\n```\n"
    header = converter["preprocess", "header"]
    anchor = converter["postprocess", "anchor"]
    anchor.header = header
    output = converter.convert(source, "preprocess")
    output = re.sub(r"(\<.*?\>)|\n", "", output)
    answer = (
        "# 1 titletext {#a#}## 1.1 " "section1/0ZeroDivisionError: division by zero"
    )
    assert output == answer
    header.reset()
    output = converter.convert(source, ["preprocess", "postprocess"])
    output = re.sub(r"(\<.*?\>)|\n", "", output)
    answer = (
        "# 1 titletext [1](.#a)## 1.1 " "section1/0ZeroDivisionError: division by zero"
    )
    assert output == answer
    header.reset()
    output = converter.convert(source)
    output = re.sub(r"(\<.*?\>)|\n", "", output)
    assert output == answer
