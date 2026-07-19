# Volatility 2 to Volatility 3 plugin migration (API changes)

The plugin entry point `calculate()` is removed; a Volatility 3 plugin implements `run()` instead.
The `render_text()` method is replaced; Volatility 3 returns a `TreeGrid()` from `run()`.
The `table_header()` and `table_row()` output functions are removed; build a `TreeGrid()` with typed columns instead.
Plugins now inherit from `interfaces.plugins.PluginInterface` instead of the Volatility 2 base classes.
The `--profile` option is removed; Volatility 3 auto-detects the OS and configures symbols via the `get_requirements()` function (e.g. `nt_symbols` for Windows).
Direct `addrspace` access is replaced by a Memory Layer declared in `get_requirements()` and accessed through `context.layers`.
Plugin options are no longer defined by class inheritance/argparse config; they are declared in `get_requirements()` as `requirements.*` objects.
The `short_option` for arguments is no longer available.
Volatility 3 is written in Python 3; Volatility 2 was Python 2.7.
Output format is selected with a renderer option supporting CSV and JSON; Volatility 2 had manual table construction.
Volatility 3 supports multiple Memory Layers instead of a single profile-based address space.
