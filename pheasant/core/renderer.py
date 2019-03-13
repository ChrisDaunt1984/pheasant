import importlib
import logging
import os
import re
from typing import Any, Dict, Iterable, List, Match, Optional, Union

from jinja2 import Environment, FileSystemLoader, select_autoescape

from pheasant.core.parser import Parser

Context = Dict[str, str]
Config= Dict[str, Any]


def update_config(config: Config, update: Config) -> None:
    for key, value in update.items():
        if key not in config:
            config[key] = value
        elif isinstance(value, list):
            config[key].extend(value)
        elif isinstance(value, dict):
            config[key].update(value)
        else:
            config[key] = value


class Renderer:
    def __init__(self, parser: Parser, config: Optional[Config] = None):
        self.parser = parser
        self.config: Dict[str, Any] = {}
        config_module = ".".join(self.__module__.split(".")[:-1]) + ".config"
        try:
            module = importlib.import_module(config_module)
            if hasattr(module, "config"):
                self.config = getattr(module, "config")
        except Exception:
            pass
        if config:
            update_config(self.config, config)

    def set_template(self, prefix: Union[str, List[str]] = "") -> None:
        module = importlib.import_module(self.__module__)
        default_directory = os.path.join(os.path.dirname(module.__file__), "templates")
        if isinstance(prefix, str):
            prefix = [prefix]
        for prefix_ in [f"{p}_" if p else "" for p in prefix]:
            template = f"{prefix_}template"
            template_file = f"{template}_file"
            if template in self.config:
                continue
            abspath = os.path.abspath(self.config[template_file])
            template_directory, template_file = os.path.split(abspath)
            loader = FileSystemLoader([template_directory, default_directory])
            env = Environment(loader=loader, autoescape=select_autoescape(["jinja2"]))
            self.config[template] = env.get_template(template_file)
