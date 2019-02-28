"""
A module processes inline code.

IMPORTANT: `display` function is called from jupyter kernel.
"""
import base64
import html
import io
from typing import Any

from pheasant.jupyter.config import config
from pheasant.jupyter.renderer import delete_style
from pheasant.markdown.converter import markdown_convert


def display(obj: Any, **kwargs: Any) -> str:
    # FIXME: how to determine the function for conversion.
    if hasattr(obj, '__module__'):
        module = obj.__module__
        if module.startswith('matplotlib.'):
            source = matplotlib_to_base64(obj, **kwargs)
        elif module.startswith('pandas.'):
            source = pandas_to_html(obj)
        elif module.startswith('bokeh.'):
            source = bokeh_to_html(obj)
        elif module.startswith('holoviews.'):
            source = holoviews_to_html(obj)
        elif module.startswith('sympy.'):
            source = sympy_to_latex(obj)
        else:
            source = str(obj)
    else:
        is_str = isinstance(obj, str)
        if not is_str:
            obj = str(obj)

        if 'html' == kwargs.get('output'):
            source = markdown_convert(obj)
        elif is_str:
            source = obj
        else:
            source = html.escape(obj)

    return source


def matplotlib_to_base64(obj, output='markdown') -> str:
    """Convert a Matplotlib's figure into base64 string."""
    fmt = config['matplotlib_format']
    buf = io.BytesIO()

    if not hasattr(obj, 'savefig'):
        obj = obj.figure  # obj is axes.

    obj.savefig(buf, fmt=fmt, bbox_inches='tight', transparent=True)
    buf.seek(0)
    binary = buf.getvalue()

    return base64image(binary, fmt, output)


def base64image(binary, fmt: str, output: str) -> str:
    data = base64.b64encode(binary).decode('utf8')
    data = f'data:image/{fmt};base64,{data}'

    if output == 'markdown':
        return f'![{fmt}]({data})'
    elif output == 'html':
        return f'<img alt="{fmt}" src="{data}"/>'
    else:
        raise ValueError(f'Unknown output: {output}')


def pandas_to_html(dataframe) -> str:
    """Convert a pandas.DataFrame into a <table> tag."""
    html = dataframe.to_html(escape=False)
    html = delete_style(html)
    return html


def bokeh_to_html(figure) -> str:
    """Convert a Bokeh's figure into <script> and <div> tags."""
    from bokeh.embed import components
    script, div = components(figure)
    return script + div


def holoviews_to_html(figure, output='markdown', fmt=None) -> str:
    import holoviews as hv
    backend = config['holoviews_backend']
    if fmt is None:
        fmt = config[f'{backend}_format']
    renderer = hv.renderer(backend)
    html, info = renderer(figure, fmt=fmt)

    if fmt == 'png':
        return base64image(html, fmt, output)
    else:
        return html


def sympy_to_latex(obj) -> str:
    """Convert a Sympy's object into latex string."""
    import sympy as sp
    return sp.latex(obj)
