import pytest


def test_without_number(linker, parser_number, parser_linker, source_simple):
    assert linker.number is None

    with pytest.raises(ValueError):
        "".join(parser_linker.parse(source_simple))


def test_with_number(linker, number, parser_number, parser_linker, source_simple):
    list(parser_number.parse(source_simple))
    assert len(number.label_context) == 2
    linker.set_number(number)
    assert linker.number is number


def test_label_context(linker, parser_number, source_simple):
    assert linker.number is not None
    label_context = {
        "label-a": {
            "kind": "header",
            "number_list": [1],
            "id": "pheasant-number-label-a",
            "abs_src_path": ".",
        },
        "label-b": {
            "kind": "figure",
            "number_list": [2],
            "id": "pheasant-number-label-b",
            "abs_src_path": ".",
        },
    }
    assert linker.number.label_context == label_context


@pytest.fixture()
def source_parsed(linker, parser_number, source_simple):
    linker.number.reset()
    source = "".join(parser_number.parse(source_simple))
    return source


def test_render_linker(linker, parser_linker, source_parsed):
    assert "Linker_render_label" in parser_linker.patterns
    assert parser_linker.patterns["Linker_render_label"].startswith(
        "(?P<Linker_render_label>"
    )
    assert parser_linker.renders["Linker_render_label"] == linker.render_label

    splitter = parser_linker.splitter(source_parsed)
    next(splitter)
    cell = splitter.send(dict)
    assert cell["name"] is None
    assert cell["context"] == {}
    answer = 'begin\n<h1 id="pheasant-number-label-a">1. title</h1>\n' "text a Figure "
    assert cell["source"] == answer
    cell = splitter.send(dict)
    assert cell["name"] == "Linker_render_label"
    assert cell["context"] == {"label": "label-b", "_source": cell["source"]}
    assert cell["context"]["label"] in linker.number.label_context


def test_parse_linker(linker, parser_linker, source_parsed):
    source = "".join(parser_linker.parse(source_parsed))
    answer = (
        'begin\n<h1 id="pheasant-number-label-a">1. title</h1>\n'
        'text a Figure <a href=".#pheasant-number-label-b">2</a>\n'
        "<h2>1.1. section a</h2>\ntext b\n<h3>1.1.1. subsection</h3>\n"
        '<h2>1.2. section b</h2>\ntext c\n<div class="pheasant-number-figure">'
        "<p>figure content a1\nfigure content a2\ntext d</p>\n"
        "<p>Figure 1 figure title a</p></div>\n"
        '<div class="pheasant-number-figure" id="pheasant-number-label-b">'
        "<p>figure content b1\nfigure content b2</p>\n"
        '<p>Figure 2 figure title b Section <a href=".#pheasant-number-label-a">1'
        '</a></p></div>\nend <span style="color: red;">'
        "Unknown label: 'label-c'</span>"
    )
    assert source == answer
