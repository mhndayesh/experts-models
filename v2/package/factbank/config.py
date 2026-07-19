"""factbank.toml support. Precedence: CLI flags > config file > defaults.

Implementation: the toml's [serve] table becomes argparse DEFAULTS before
parsing, so anything typed on the command line still wins, and --help
always shows the effective source of truth.
"""

import os
import tomllib

CONFIG_ENV = "FACTBANK_CONFIG"
DEFAULT_NAME = "factbank.toml"


def find_config(explicit: str | None = None) -> str | None:
    if explicit:
        return explicit if os.path.exists(explicit) else None
    env = os.environ.get(CONFIG_ENV)
    if env and os.path.exists(env):
        return env
    if os.path.exists(DEFAULT_NAME):
        return DEFAULT_NAME
    return None


def apply_config(parser, section: str, path: str | None):
    """Set toml values as parser defaults. Unknown keys are refused loudly
    (a silently ignored typo in a config file is a debugging tax)."""
    if not path:
        return
    with open(path, "rb") as fh:
        data = tomllib.load(fh)
    table = data.get(section, {})
    known = {a.dest for a in parser._actions}
    values = {}
    for k, v in table.items():
        dest = k.replace("-", "_")
        if dest not in known:
            raise SystemExit(f"factbank.toml [{section}]: unknown key "
                             f"{k!r} (known: {sorted(known)})")
        values[dest] = v
    parser.set_defaults(**values)
