import codecs
from collections import OrderedDict
from functools import partial
from typing import Callable, Iterable, Optional, Union

from pheasant.core.parser import Parser
from pheasant.core.renderer import Renderer
from pheasant.core.renderers import Renderers


class Converter:
    def __init__(self, name: str = ""):
        self.name = name or self.__class__.__qualname__.lower()
        self.parsers: OrderedDict[str, Parser] = OrderedDict()
        self.renderers = Renderers()

    def __repr__(self):
        parsers = ", ".join(f"'{name}'" for name in self.parsers)
        return f"<{self.__class__.__qualname__}#{self.name}[{parsers}]>"

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.parsers[item]
        elif isinstance(item, tuple):
            return self.renderers[item]

    def register(
        self,
        name: str,
        renderers: Union[Union[Renderer, str], Iterable[Union[Renderer, str]]],
    ):
        """Register renderer's processes

        Parameters
        ----------
        name
            The name of Parser
        renderers
            List of Renderer's instance or name of Renderer
        """
        if name in self.parsers:
            raise ValueError(f"Duplicated parser name '{name}'")
        parser = Parser(name)
        self.parsers[name] = parser
        self.renderers.register(name, renderers)
        for renderer in self.renderers[name]:
            for pattern, render in renderer.renders.items():
                parser.register(pattern, render)

    def convert(
        self, source: str, names: Optional[Union[str, Iterable[str]]] = None
    ) -> str:
        """Convert source text.

        Parameters
        ----------
        source
            The text string to be converted.
        names
            Parser names to be used. If not specified. all of the registered
            parsers will be used.

        Returns
        -------
        Converted source text.
        """
        if isinstance(names, str):
            names = [names]
        names = names or self.parsers
        for name in names:
            parser = self.parsers[name]
            source = "".join(parser.parse(source))

        return source

    def convert_from_file(
        self, path: str, names: Optional[Iterable[str]] = None
    ) -> str:
        """Convert source text from file.

        Parameters
        ----------
        source
            The text string to be converted.
        names
            Parser names to be used. If not specified. all of the registered
            parsers will be used.

        Returns
        -------
        converted source text.
        """
        with codecs.open(path, "r", "utf8") as file:
            source = file.read()
        source = source.replace("\r\n", "\n").replace("\r", "\n")
        return self.convert(source, names)

    def __call__(self, *names: str) -> Callable[[str], str]:
        return partial(self.convert_from_file, names=names)
