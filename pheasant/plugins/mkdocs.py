import logging
import os
from typing import Dict

import yaml
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from pheasant.core.converter import Converter

config_options  # to avoid linter error.

logger = logging.getLogger("mkdocs")


class PheasantPlugin(BasePlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config: Dict[str, Dict[str, str]] = {}
        self.served = False
        logger.debug("[Pheasant] Plugin created.")
        self.setup()

    def setup(self):
        self.converter = Converter()
        self.converter.register("script", "python")
        self.converter.register("markdown", ["jupyter", "number", "code"])
        self.converter.register("linker", "linker")
        logger.debug(f"[Pheasant] Converter created: {self.converter}.")
        logger.debug("[Pheasant] Parser registered.")
        for name, parser in self.converter.parsers.items():
            logger.debug(f"[Pheasant] Parser for '{name}' = {parser}.")
        logger.debug("[Pheasant] Renderer registered.")
        for name, renderers in self.converter.renderers.items():
            logger.debug(f"[Pheasant] Renderers for '{name}' = {renderers}.")

    def on_serve(self, server, config):
        self.served = True

        return server

    def on_config(self, config):
        logger.debug("[Pheasant] Plugin enabled.")

        from mkdocs.utils import markdown_extensions

        markdown_extensions.append(".py")
        logger.debug("[Pheasant] Python source files will be captured.")

        path = os.path.dirname(config["config_file_path"])
        path = os.path.join(path, "pheasant.yml")
        if os.path.exists(path):
            logger.debug(f"[Pheasant] Config file: {path}")
            with open(path, "r") as f:
                config_ = yaml.load(f)
            for renderer in self.converter.renderers:
                name = renderer.name
                if name in config_:
                    renderer.update_config(config_[name])
                for key, value in renderer.config.items():
                    logger.debug(
                        f"[Pheasant.{name}] Config value: '{key}' = {value}."
                    )
        return config

    def on_nav(self, nav, config, files):
        logger.debug(f"[Pheasant] Page order for numbering.")
        self.config["abs_src_paths"] = [page.file.abs_src_path for page in nav.pages]
        self.config["src_paths"] = [page.file.src_path for page in nav.pages]
        for k, srs_path in enumerate(self.config["src_paths"]):
            logger.debug(f"[Pheasant] Page number {k + 1}: {srs_path}")

        return nav

    def on_page_read_source(self, source, page, config):
        logger.info(f"[Pheasant] on_page_read_source: {page.file.src_path}")
        source = self.converter("markdown")(page.file.abs_src_path)
        return source

    def on_page_markdown(self, markdown, page, config, files):
        logger.info(f"[Pheasant] on_page_markdown: {page.file.src_path}")
        print(markdown)
        return

    def on_page_content(self, content, page, config, files):
        logger.info(f"[Pheasant] on_page_content: {page.file.src_path}")
        print(content)
        return

    def on_page_context(self, context, page, config, nav):
        logger.info(f"[Pheasant] on_page_context: {page.file.src_path}")
        print(page)
        print(dir(page))
        print(page.content)
        # update_page_config(config, page.file.abs_src_path)
        return context
