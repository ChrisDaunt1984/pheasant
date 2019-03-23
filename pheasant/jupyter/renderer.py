import re
from typing import Iterator, List, Match

from pheasant.core.renderer import Renderer
from pheasant.jupyter.client import (execute, execution_report,
                                     find_kernel_names)
from pheasant.jupyter.display import (bokeh_extra_resources,
                                      holoviews_extra_resources,
                                      select_display_data)


class Jupyter(Renderer):

    FENCED_CODE_PATTERN = (
        r"^(?P<mark>`{3,})(?P<language>\w+) ?(?P<option>.*?)\n"
        r"(?P<code>.*?)\n(?P=mark)\n"
    )
    INLINE_CODE_PATTERN = r"\{\{(?P<code>.+?)\}\}"
    RE_INLINE_CODE_PATTERN = re.compile(INLINE_CODE_PATTERN)

    def __post_init__(self):
        super().__post_init__()
        self.register(Jupyter.FENCED_CODE_PATTERN, self.render_fenced_code)
        self.register(Jupyter.INLINE_CODE_PATTERN, self.render_inline_code)
        self.set_template(["fenced_code", "inline_code"])
        self.config["kernel_name"] = {
            key: values[0] for key, values in find_kernel_names().items()
        }
        self.reset()

    def setup(self):
        code = "\n".join(
            [
                "import pheasant.jupyter.display",
                "import pandas",
                "pandas.options.display.max_colwidth = 0",
            ]
        )
        self.execute(code, "python")

    def reset(self):
        for key in ["css", "javascript", "raw_css", "raw_javascript"]:
            self.meta[f"extra_{key}"] = []
        self.meta["extra_module"] = []

    def render_fenced_code(self, context, splitter, parser) -> Iterator[str]:
        if "display" in context["option"]:
            context["code"] = replace_for_display(context["code"], skip_equal=False)
        if "inline" in context["option"]:
            context["code"] = preprocess_fenced_code(context["code"])
        outputs = self.execute(code=context["code"], language=context["language"])
        output = super().render(
            "fenced_code", context, outputs=outputs, report=execution_report
        )
        yield output + "\n"

    def render_inline_code(self, context, splitter, parser) -> Iterator[str]:
        if context["code"].startswith("#"):
            yield context["_source"].replace(context["code"], context["code"][1:])
            return

        context["code"] = preprocess_inline_code(context["code"])
        if "language" not in context:
            context["language"] = "python"

        outputs = self.execute(code=context["code"], language=context["language"])
        for output in outputs:
            if "data" in output and "text/plain" in output["data"]:
                text = output["data"]["text/plain"]
                if (text.startswith('"') and text.endswith('"')) or (
                    text.startswith("'") and text.endswith("'")
                ):
                    output["data"]["text/plain"] = text[1:-1]
        for output in outputs:
            if output["type"] == "display_data":
                outputs = [
                    output for output in outputs if output["type"] == "display_data"
                ]
                break
        yield super().render("inline_code", context, outputs=outputs)

    def execute(self, code: str, language: str = "python") -> List:
        if language not in self.config["kernel_name"]:
            return []
        outputs = execute(code, self.config["kernel_name"][language])
        self.update_extra_resourse(outputs)
        select_display_data(outputs)
        return outputs

    def update_extra_resourse(self, outputs: List[dict]) -> None:
        module_dict = {
            "bokeh": bokeh_extra_resources,
            "holoviews": holoviews_extra_resources,
        }
        if len(self.meta["extra_module"]) == len(module_dict):
            return

        new_modules = []
        for output in outputs:
            if (
                "data" in output
                and "text/html" in output["data"]
                and "text/plain" in output["data"]
            ):
                module = output["data"]["text/plain"]
                if (
                    module in module_dict.keys()
                    and module not in self.meta["extra_module"]
                ):
                    new_modules.append(module)

        for module in new_modules:
            self.meta["extra_module"].append(module)
            resources = module_dict[module]()
            for key, values in resources.items():
                self.meta[key].extend(
                    value for value in values if value not in self.meta[key]
                )


def preprocess_fenced_code(code: str) -> str:
    def replace(match: Match) -> str:
        return replace_for_display(match.group(1), skip_equal=False)

    return Jupyter.RE_INLINE_CODE_PATTERN.sub(replace, code)


def preprocess_inline_code(code: str) -> str:
    return replace_for_display(code)


def replace_for_display(code: str, skip_equal: bool = True) -> str:
    """Replace a match object with `display` function.

    Parameters
    ----------
    code
        The code to be executed in the inline mode.
    skip_equal
        If True, skip the statement which contains equal character.

    Returns
    -------
    codes
        Replaced python code list.
    """
    if "=" in code and skip_equal:
        return code

    precode = None

    if code.startswith("^"):
        code = code[1:]
        output = "html"
    else:
        output = "markdown"

    code = code.replace(";", "\n")
    if "\n" not in code:
        precode = ""
    else:
        codes = code.split("\n")
        code = "_pheasant_dummy"
        match = re.match(r"(\w+) *?=", codes[-1])
        if match:
            codes.append(f"{code} = {match.group(1)}")
        else:
            codes[-1] = f"{code} = {codes[-1]}"
        precode = "\n".join(codes) + "\n"

    return f'{precode}pheasant.jupyter.display.display({code}, output="{output}")'
