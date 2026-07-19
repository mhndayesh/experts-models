# Volatility 2 to Volatility 3 migration (memory forensics / DFIR)

Source 1: Volatility 3 official docs — "Changes between Volatility 2 and Volatility 3"
(https://volatility3.readthedocs.io/en/latest/vol2to3.html)

## Changes between Volatility 2 and Volatility 3

### Library and Context

Volatility 3 has been designed from the ground up to be a library, this means the components are independent and all state required to run a particular plugin at a particular time is self-contained in an object derived from a `ContextInterface`.

The context contains the two core components that make up Volatility, layers of data and the available symbols.

### Symbols and Types

Volatility 3 no longer uses profiles, it comes with an extensive library of symbol tables, and can generate new symbol tables for most windows memory images, based on the memory image itself. This allows symbol tables to include specific offsets for locations (symbol locations) based on that operating system in particular. This means it is easier and quicker to identify structures within an operating system, by having known offsets for those structures provided by the official debugging information.

### Object Model changes

The object model has changed as well, objects now inherit directly from their Python counterparts, meaning an integer object is actually a Python integer (and has all the associated methods, and can be used wherever a normal int could). In Volatility 2, a complex proxy object was constructed which tried to emulate all the methods of the host object, but ultimately it was a different type and could not be used in the same places (critically, it could make the ordering of operations important, since x + y might not work, but y + x might work fine).

Volatility 3 has also had significant speed improvements, where Volatility 2 was designed to allow access to live memory images and situations in which the underlying data could change during the run of the plugin, in Volatility 3 the data is now read once at the time of object construction, and will remain static, even if the underlying layer changes. This was because live memory analysis was barely ever used, and this feature could cause a particular value to be re-read many times over for no benefit (particularly since each re-read could result in many additional image reads from following page table translations).

Further, in order to provide Volatility specific information without impact on the ability for structures to have members with arbitrary names, all the metadata about the object (such as its layer or offset) have been moved to a read-only `vol()` dictionary.

Finally, the distinction between a `Template` (the thing that constructs an object) and the `Object` itself has been made more explicit. In Volatility 2, some information (such as size) could only be determined from a constructed object, leading to instantiating a template on an empty buffer, just to determine the size. In Volatility 3, templates contain information such as their size, which can be queried directly without constructing the object.

### Layer and Layer dependencies

Address spaces in Volatility 2, are now more accurately referred to as Translation Layers, since each one typically sits atop another and can translate addresses between the higher logical layer and the lower physical layer. Address spaces in Volatility 2 were strictly limited to a stack, one on top of one other. In Volatility 3, layers can have multiple "dependencies" (lower layers), which allows for the integration of features such as swap space.

### Automagic

In Volatility 2, we often tried to make this simpler for both users and developers. This resulted in something referred to as automagic, in that it was magic that happened automatically. We've now codified that more, so that the automagic processes are clearly defined and can be enabled or disabled as necessary for any particular run. We also included a stacker automagic to emulate the most common feature of Volatility 2, automatically stacking address spaces (now translation layers) on top of each other.

By default the automagic chosen to be run are determined based on the plugin requested, so that Linux plugins get Linux specific automagic and Windows plugins get Windows specific automagic. This should reduce unnecessarily searching for Linux kernels in a Windows image, for example. At the moment this is not user configurable.

### Searching and Scanning

Scanning is very similar to scanning in Volatility 2, a scanner object (such as a `BytesScanner` or `RegExScanner`) is primed with the data to be searched for, and the `scan()` method is called on the layer to be searched.

### Output Rendering

This is extremely similar to Volatility 2, because we were developing it for Volatility 3 when we added it to Volatility 2. We now require that all plugins produce output in a `TreeGrid` object, which ensure that the library can be used regardless of which interface is driving it. An example web GUI is also available called Volumetric which allows all the plugins that can be run from the command line to be run from a webpage, and offers features such as automatic formatting and sorting of the data, which previously couldn't be provided easily from the CLI. There is also the ability to provide file output such that the user interface can provide a means to render or save those files.

---

Source 2: JPCERT/CC — "Migrate Volatility Plugins 2 to 3" by Shusei Tomonaga, July 1, 2020
(https://blogs.jpcert.or.jp/en/2020/07/how-to-convert-vol-plugin.html)

## Migrate Volatility Plugins 2 to 3

The Volatility Foundation released Volatility 3 Public Beta, a new version of Volatility Framework in October 2019. The version not only offers compatibility with Python 3 but also has a lot of functional updates from Volatility 2. Particularly, creating plugins is much easier with Volatility 3 compared to the previous version.

Volatility 3's official release is planned for August 2020, and the support for Volatility 2 will end in August 2021. With this change, the environment for Volatility plugin development will shift to Volatility 3. In addition, Volatility plugins that were developed for Volatility 2 will not run on Volatility 3, and so it is necessary to update such plugins.

To make a Volatility 2 plugin compatible with Volatility 3, it is important not only to make sure it works on Volatility 3 but also to consider the following differences between the two versions:

- Volatility plugin execution flow
- Class inheritance
- Options
- Symbol and Memory Layer
- Result output

### Volatility Plugin execution flow

In Volatility 2, the first function to be called is `calculate()`, and then `render_text()` is executed. It is a complicated structure; `render_text()` is not called by `calculate()`, but rather it is executed with a return value of `calculate()`.

On the other hand, Volatility 3 has a simpler system. It executes `run()` first, and then `TreeGrid()` is called to output the result.

### Class inheritance

A newly defined Volatility plugin basically inherits an existing class. In Volatility 2, plugin developers need to choose the appropriate classes from several existing ones according to their purpose of plugin.

From Volatility 3, a new class `interfaces.plugins.PluginInterface` has been defined with the aim of integrating the plugin interface. Now developers inherit this class to develop their plugins.

To access the existing plugin functions and data, import them by using the class method `requirements` (for example `requirements.PluginRequirement`).

### Options

Options to set upon Volatility plugin execution can be added to config with `argparse` (a Python module) in Volatility 2. In Volatility 3, this can be done by the `requirements` function as in the previous section.

In Volatility 3, `short_option` is no longer available. Also, while options are all inherited together with a class in Volatility 2, options need to be set in Volatility 3. For example, `pid`, an option to specify process to analyse which works on many plugins, is not inherited, and rather needs to be written in the `requirements`.

### Symbol and Memory Layer

In Volatility 2, the OS information of the memory image to analyse has to be set with the `profile` option. This process is no longer necessary in Volatility 3, but instead it has to be set with the `requirements` function. (If it is Windows OS, use `nt_symbols`.)

Volatility 3 handle memory images by each `Memory Layer`, and this needs to be defined in `requirements`. Normally, one Memory Layer is sufficient, but multiple Memory Layers need to be defined when analysing multiple memory images. Memory architecture can also be set in Memory Layer, but this is optional.

### Result output

Volatility plugin has functions to display results. These are `table_header()` and `table_row()` in Volatility 2, replaced by `TreeGrid()` in Volatility 3.

With `TreeGrid()`, table size does not have to be set, but Type does. `format_hints` modules can be used for Hex and binary display. Result output of `TreeGrid()` can be exported in different formats such as CSV and JSON by using a command line option `renderer`.

As the current Volatility 3 is a beta version, the features introduced in this article may change. Changing the settings should be done carefully as some default plugins that worked in Volatility 2 do not work in Volatility 3.

---

Source 3: Existing curated seed (previously validated facts for the netsec expert)

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
