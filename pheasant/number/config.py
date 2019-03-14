from typing import Any, Dict

config: Dict[str, Any] = {
    # Jinja2 template file for numbering.
    "header_template_file": "basic.jinja2",
    # List of numbered objects
    "kind": ["header", "figure", "table", "code", "file"],
    # Whether header's number ends with a period or not
    "header_period": True,
    # Numbering level. 0 for multiple pages, 2 for h2 etc.
    "level": 0,
    # Prefix for numbered object.
    "kind_prefix": {},
    # Label file of reference to record reference information.
    "label_file": ".pheasant-number.json",
    # Begin pattern
    "begin_pattern": "<!-- begin -->",
    # End pattern
    "end_pattern": "<!-- end -->",
    # <div> class name for numbered objects.
    "class": "pheasant-number-{kind}",
    # <div> id name for numbered objects.
    "id": "pheasant-number-{label}",
    # relpath function
    "relpath_function": None,
}
