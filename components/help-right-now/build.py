from html import escape
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
TOKEN_RE = re.compile(r"{{([a-zA-Z0-9_.-]+)}}")


def load_json(name):
    with (HERE / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def render(template, values):
    missing = sorted({key for key in TOKEN_RE.findall(template) if key not in values})
    if missing:
        raise SystemExit("Missing template values: " + ", ".join(missing))

    def replace(match):
        return escape(str(values[match.group(1)]), quote=True)

    rendered = TOKEN_RE.sub(replace, template)
    leftover = TOKEN_RE.findall(rendered)
    if leftover:
        raise SystemExit("Unresolved template values: " + ", ".join(sorted(set(leftover))))
    return rendered


copy_values = load_json("copy.json")
data_values = load_json("data.json")
values = {**copy_values, **data_values}
template = (HERE / "prototype.template.html").read_text(encoding="utf-8")
output = render(template, values)
(HERE / "prototype.html").write_text(output, encoding="utf-8")
