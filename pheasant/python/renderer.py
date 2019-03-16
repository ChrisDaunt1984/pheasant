from typing import Iterable, Optional

from pheasant.core.parser import Parser
from pheasant.core.renderer import Config, Context, Renderer
from pheasant.python.formatter import Formatter
from pheasant.python.splitter import splitter


class Python(Renderer):

    PYTHON_CODE_PATTERN = r"^(?P<source>.+)"  # Entire source!

    def __init__(self, config: Optional[Config] = None):
        super().__init__(config)
        self.register(Python.PYTHON_CODE_PATTERN, self.render_python_code)

    def render_python_code(self, context: Context, parser: Parser) -> Iterable[str]:
        formatter = Formatter(context["source"])
        for cell_type, begin, end in splitter(context["source"]):
            yield formatter(cell_type, begin, end)
