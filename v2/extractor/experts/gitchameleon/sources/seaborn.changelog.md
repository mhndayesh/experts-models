
# ===== SOURCE: https://raw.githubusercontent.com/mwaskom/seaborn/master/doc/whatsnew/v0.12.0.rst =====

v0.12.0 (September 2022)
------------------------

Introduction of the objects interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This release debuts the `seaborn.objects` interface, an entirely new approach to making plots with seaborn. It is the product of several years of design and 16 months of implementation work. The interface aims to provide a more declarative, composable, and extensible API for making statistical graphics. It is inspired by Wilkinson's grammar of graphics, offering a Pythonic API that is informed by the design of libraries such as `ggplot2` and `vega-lite` along with lessons from the past 10 years of seaborn's development.

For more information and numerous examples, see the :doc:`tutorial chapter </tutorial/objects_interface>` and :ref:`API reference <objects_api>`

This initial release should be considered "experimental". While it is stable enough for serious use, there are definitely some rough edges, and some key features remain to be implemented. It is possible that breaking changes may occur over the next few minor releases. Please be patient with any limitations that you encounter and help the development by reporting issues when you find behavior surprising.

Keyword-only arguments
~~~~~~~~~~~~~~~~~~~~~~

|API|

Seaborn's plotting functions now require explicit keywords for most arguments, following the deprecation of positional arguments in v0.11.0. With this enforcement, most functions have also had their parameter lists rearranged so that `data` is the first and only positional argument. This adds consistency across the various functions in the library. It also means that calling `func(data)` will do something for nearly all functions (those that support wide-form data) and that :class:`pandas.DataFrame` can be piped directly into a plot. It is possible that the signatures will be loosened a bit in future releases so that `x` and `y` can be positional, but minimal support for positional arguments after this change will reduce the chance of inadvertent mis-specification (:pr:`2804`).

Modernization of categorical scatterplots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This release begins the process of modernizing the :ref:`categorical plots <categorical_api>`, beginning with :func:`stripplot` and :func:`swarmplot`. These functions are sporting some enhancements that alleviate a few long-running frustrations (:pr:`2413`, :pr:`2447`):

- |Feature| The new `native_scale` parameter allows numeric or datetime categories to be plotted with their original scale rather than converted to strings and plotted at fixed intervals.

- |Feature| The new `formatter` parameter allows more control over the string representation of values on the categorical axis. There should also be improved defaults for some types, such as dates.

- |Enhancement| It is now possible to assign `hue` when using only one coordinate variable (i.e. only `x` or `y`).

- |Enhancement| It is now possible to disable the legend.

The updates also harmonize behavior with functions that have been more recently introduced. This should be relatively non-disruptive, although a few defaults will change:

- |Defaults| The functions now hook into matplotlib's unit system for plotting categorical data. (Seaborn's categorical functions actually predate support for categorical data in matplotlib.) This should mostly be transparent to the user, but it may resolve a few edge cases. For example, matplotlib interactivity should work better (e.g., for showing the data value under the cursor).

- |Defaults| A color palette is no longer applied to levels of the categorical variable by default. It is now necessary to explicitly assign `hue` to see multiple colors (i.e., assign the same variable to `x`/`y` and `hue`). Passing `palette` without `hue` will continue to be honored for one release cycle.

- |Defaults| Numeric `hue` variables now receive a continuous mapping by default, using the same rules as :func:`scatterplot`. Pass `palette="deep"` to reproduce previous defaults.

- |Defaults| The plots now follow the default property cycle; i.e. calling an axes-level function multiple times with the same active axes will produce different-colored artists.

- |API| Currently, assigning `hue` and then passing a `color` will produce a gradient palette. This is now deprecated, as it is easy to request a gradient with, e.g. `palette="light:blue"`.

Similar enhancements / updates should be expected to roll out to other categorical plotting functions in future releases. There are also several function-specific enhancements:

- |Enhancement| In :func:`stripplot`, a "strip" with a single observation will be plotted without jitter (:pr:`2413`)

- |Enhancement| In :func:`swarmplot`, the points are now swarmed at draw time, meaning that the plot will adapt to further changes in axis scaling or tweaks to the plot layout (:pr:`2443`).

- |Feature| In :func:`swarmplot`, the proportion of points that must overlap before issuing a warning can now be controlled with the `warn_thresh` parameter (:pr:`2447`).

- |Fix| In :func:`swarmplot`, the order of the points in each swarm now matches the order in the original dataset; previously they were sorted. This affects only the underlying data stored in the matplotlib artist, not the visual representation (:pr:`2443`).

More flexible errorbars
~~~~~~~~~~~~~~~~~~~~~~~

|API| |Feature|

Increased the flexibility of what can be shown by the internally-calculated errorbars for :func:`lineplot`, :func:`barplot`, and :func:`pointplot`.

With the new `errorbar` parameter, it is now possible to select bootstrap confidence intervals, percentile / predictive intervals, or intervals formed by scaled standard deviations or standard errors. The parameter also accepts an arbitrary function that maps from a vector to an interval. There is a new :doc:`user guide chapter </tutorial/error_bars>` demonstrating these options and explaining when you might want to use each one.

As a consequence of this change, the `ci` parameter has been deprecated. Note that :func:`regplot` retains the previous API, but it will likely be updated in a future release (:pr:`2407`, :pr:`2866`).

Other updates
~~~~~~~~~~~~~

- |Feature| It is now possible to aggregate / sort a :func:`lineplot` along the y axis using `orient="y"` (:pr:`2854`).

- |Feature| Made it easier to customize :class:`FacetGrid` / :class:`PairGrid` / :class:`JointGrid` with a fluent (method-chained) style by adding `apply`/ `pipe` methods. Additionally, fixed the `tight_layout` and `refline` methods so that they return `self` (:pr:`2926`).

- |Feature| Added :meth:`FacetGrid.tick_params` and :meth:`PairGrid.tick_params` to customize the appearance of the ticks, tick labels, and gridlines of all subplots at once (:pr:`2944`).

- |Enhancement| Added a `width` parameter to :func:`barplot` (:pr:`2860`).

- |Enhancement| It is now possible to specify `estimator` as a string in :func:`barplot` and :func:`pointplot`, in addition to a callable (:pr:`2866`).

- |Enhancement| Error bars in :func:`regplot` now inherit the alpha value of the points they correspond to (:pr:`2540`).

- |Enhancement| When using :func:`pairplot` with `corner=True` and `diag_kind=None`, the top left y axis label is no longer hidden (:pr:`2850`).

- |Enhancement| It is now possible to plot a discrete :func:`histplot` as a step function or polygon (:pr:`2859`).

- |Enhancement| It is now possible to customize the appearance of elements in a :func:`boxenplot` with `box_kws`/`line_kws`/`flier_kws` (:pr:`2909`).

- |Fix| Improved integration with the matplotlib color cycle in most axes-level functions (:pr:`2449`).

- |Fix| Fixed a regression in 0.11.2 that caused some functions to stall indefinitely or raise when the input data had a duplicate index (:pr:`2776`).

- |Fix| Fixed a bug in :func:`histplot` and :func:`kdeplot` where weights were not factored into the normalization (:pr:`2812`).

- |Fix| Fixed two edgecases in :func:`histplot` when only `binwidth` was provided (:pr:`2813`).

- |Fix| Fixed a bug in :func:`violinplot` where inner boxes/points could be missing with unpaired split violins (:pr:`2814`).

- |Fix| Fixed a bug in :class:`PairGrid` where an error would be raised when defining `hue` only in the mapping methods (:pr:`2847`).

- |Fix| Fixed a bug in :func:`scatterplot` where an error would be raised when `hue_order` was a subset of the hue levels (:pr:`2848`).

- |Fix| Fixed a bug in :func:`histplot` where dodged bars would have different widths on a log scale (:pr:`2849`).

- |Fix| In :func:`lineplot`, allowed the `dashes` keyword to set the style of a line without mapping a `style` variable (:pr:`2449`).

- |Fix| Improved support in :func:`relplot` for "wide" data and for faceting variables passed as non-pandas objects (:pr:`2846`).

- |Fix| Subplot titles will no longer be reset when calling :meth:`FacetGrid.map` or :meth:`FacetGrid.map_dataframe` (:pr:`2705`).

- |Fix| Added a workaround for a matplotlib issue that caused figure-level functions to freeze when `plt.show` was called (:pr:`2925`).

- |Fix| Improved robustness to numerical errors in :func:`kdeplot` (:pr:`2862`).

- |Fix| Fixed a bug where :func:`rugplot` was ignoring expand_margins=False (:pr:`2953`).

- |Defaults| The `patch.facecolor` rc param is no longer set by :func:`set_palette` (or :func:`set_theme`). This should have no general effect, because the matplotlib default is now `"C0"` (:pr:`2906`).

- |Build| Made `scipy` an optional dependency and added `pip install seaborn[stats]` as a method for ensuring the availability of compatible `scipy` and `statsmodels` libraries at install time. This has a few minor implications for existing code, which are explained in the Github pull request (:pr:`2398`).

- |Build| Example datasets are now stored in an OS-specific cache location (as determined by `appdirs`) rather than in the user's home directory. Users should feel free to remove `~/seaborn-data` if desired (:pr:`2773`).

- |Build| The unit test suite is no longer part of the source or wheel distribution. Seaborn has never had a runtime API for exercising the tests, so this should not have workflow implications (:pr:`2833`).

- |Build| Following `NEP29 <https://numpy.org/neps/nep-0029-deprecation_policy.html>`_, dropped support for Python 3.6 and bumped the minimally-supported versions of the library dependencies.

- |API| Removed the previously-deprecated `factorplot` along with several previously-deprecated utility functions (`iqr`, `percentiles`, `pmf_hist`, and `sort_df`).

- |API| Removed the (previously-unused) option to pass additional keyword arguments to :func:`pointplot`.

# ===== SOURCE: https://raw.githubusercontent.com/mwaskom/seaborn/master/doc/whatsnew/v0.13.0.rst =====

v0.13.0 (September 2023)
------------------------

This is a major release with a number of important new features and changes. The highlight is a major overhaul to seaborn's categorical plotting functions, providing them with many new capabilities and better aligning their API with the rest of the library. There is also provisional support for alternate dataframe libraries like `polars <https://www.pola.rs>`_, a new theme and display configuration system for :class:`objects.Plot`, and many smaller bugfixes and enhancements.

Updating is recommended, but users are encouraged to carefully check the outputs of existing code that uses the categorical functions, and they should be aware of some deprecations and intentional changes to the default appearance of the resulting plots (see notes below with |API| and |Defaults| tags).

Major enhancements to categorical plots
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Seaborn's :ref:`categorical functions <categorical_api>` have been completely rewritten for this release. This provided the opportunity to address some longstanding quirks as well as to add a number of smaller but much-desired features and enhancements.

Support for numeric and datetime data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|Feature|

The categorical functions have historically treated *all* data as categorical, even when it has a numeric or datetime type. This can now be controlled with the new `native_scale` parameter. The default remains `False` to preserve existing behavior. But with `native_scale=True`, values will be treated as they would by other seaborn or matplotlib functions. Element widths will be derived from the minimum distance between two unique values on the categorical axis.

Additionally, while seaborn previously determined the mapping from categorical values to ordinal positions internally, this is now delegated to matplotlib. The change should mostly be transparent to the user, but categorical plots (even with `native_scale=False`) will better align with artists added by other seaborn or matplotlib functions in most cases, and matplotlib's interactive machinery will work better.

Changes to color defaults and specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|API| |Defaults|

The categorical functions now act more like the rest of seaborn in that they will produce a plot with a single main color unless the `hue` variable is assigned. Previously, there would be an implicit redundant color mapping (e.g., each box in a boxplot would get a separate color from the default palette). To retain the previous behavior, explicitly assign a redundant `hue` variable (e.g., `boxplot(data, x="x", y="y", hue="x")`).

Two related idiosyncratic color specifications are deprecated, but they will continue to work (with a warning) for one release cycle:

- Passing a `palette` without explicitly assigning `hue` is no longer supported (add an explicitly redundant `hue` assignment instead).

- Passing a `color` while assigning `hue` to produce a gradient is no longer supported (use `palette="dark:{color}"` or `palette="light:{color}"` instead).

Finally, like other seaborn functions, the default palette now depends on the variable type, and a sequential palette will be used with numeric data. To retain the previous behavior, pass the name of a qualitative palette (e.g., `palette="deep"` for seaborn's default). Accordingly, the functions have gained a parameter to control numeric color mappings (`hue_norm`).

Other features, enhancements, and changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following updates apply to multiple categorical functions.

- |Feature| All functions now accept a `legend` parameter, which can be a boolean (to suppress the legend) or one of `{"auto", "brief", "full"}` to control the amount of information shown in the legend for a numerical color mapping.

- |Feature| All functions now accept a callable `formatter` parameter to control the string representation of the data.

- |Feature| All functions that draw a solid patch now accept a boolean `fill` parameter, which when set to `False` will draw line-art elements.

- |Feature| All functions that support dodging now have an additional `gap` parameter that can be set to a non-zero value to leave space between dodged elements.

- |Feature| The :func:`boxplot`, :func:`boxenplot`, and :func:`violinplot` functions now support a single `linecolor` parameter.

- |Enhancement| The default value for `dodge` has changed from `True` to `"auto"`. With `"auto"`, elements will dodge only when at least one set of elements would otherwise overlap.

- |Enhancement| When the value axis of the plot has a non-linear scale, the statistical operations (e.g. an aggregation in :func:`pointplot` or the kernel density fit in :func:`violinplot`) are now applied in that scale space.

- |Enhancement| All functions now accept a `log_scale` parameter. With a single argument, this will set the scale on the "value" axis (*opposite* the categorical axis). A tuple will set each axis directly (although setting a log scale categorical axis also requires `native_scale=True`).

- |Enhancement| The `orient` parameter now accepts `"x"/"y"` to specify the categorical axis, matching the objects interface.

- |Enhancement| The categorical functions are generally more deferential to the user's additional matplotlib keyword arguments.

- |API| Using `"gray"` to select an automatic gray value that complements the main palette is now deprecated in favor of `"auto"`.

The following updates are function-specific.

- |API| |Feature| In :func:`pointplot`, a single :class:`matplotlib.lines.Line2D` artist is now used rather than adding separate :class:`matplotlib.collections.PathCollection` artist for the points. As a result, it is now possible to pass additional keyword arguments for complete customization the appearance of both the lines and markers; additionally, the legend representation is improved. Accordingly, parameters that previously allowed only partial customization (`scale`, `join`, and `errwidth`) are now deprecated. The old parameters will now trigger detailed warning messages with instructions for adapting existing code.

- |API| |Feature| The bandwidth specification in :func:`violinplot` better aligns with :func:`kdeplot`, as the `bw` parameter is now deprecated in favor of `bw_method` and `bw_adjust`.

- |API| |Enhancement| In :func:`boxenplot`, the boxen are now drawn with separate patch artists in each tail. This may have consequences for code that works with the underlying artists, but it produces a better result for low-alpha / unfilled plots and enables proper area/density scaling.

- |API| |Enhancement| In :func:`barplot`, the `errcolor` and `errwidth` parameters are now deprecated in favor of a more general `err_kws`` dictionary. The existing parameters will continue to work for two releases.

- |API| In :func:`violinplot`, the `scale` and `scale_hue` parameters have been renamed to `density_norm` and `common_norm` for clarity and to reflect the fact that common normalization is now applied over both hue and faceting variables in :func:`catplot`.

- |API| In :func:`boxenplot`, the `scale` parameter has been renamed to `width_method` as part of a broader effort to de-confound the meaning of "scale" in seaborn parameters.

- |Defaults| |Enhancement| When passing a vector to the `data` parameter of :func:`barplot` or :func:`pointplot`, a bar or point will be drawn for each entry in the vector rather than plotting a single aggregated value. To retain the previous behavior, assign the vector to the `y` variable.

- |Defaults| |Enhancement| In :func:`boxplot`, the default flier marker now follows the matplotlib rcparams so that it can be globally customized.

- |Defaults| |Enhancement| When using `split=True` and `inner="box"` in :func:`violinplot`, a separate mini-box is now drawn for each split violin.

- |Defaults| |Enhancement| In :func:`boxenplot`, all plots now use a consistent luminance ramp for the different box levels. This leads to a change in the appearance of existing plots, but reduces the chances of a misleading result.

- |Defaults| |Enhancement| The `"area"` scaling in :func:`boxenplot` now approximates the density of the underlying observations, including for asymmetric distributions. This produces a substantial change in the appearance of plots with `width_method="area"`, although the existing behavior was poorly defined.

- |Feature| In :func:`countplot`, the new `stat` parameter can be used to apply a normalization (e.g to show a `"percent"` or `"proportion"`).

- |Feature| The `split` parameter in :func:`violinplot` is now more general and can be set to `True` regardless of the number of `hue` variable levels (or even without `hue`). This is probably most useful for showing half violins.

- |Feature| In :func:`violinplot`, the new `inner_kws` parameter allows additional control over the interior artists.

- |Enhancement| It is no longer required to use a `DataFrame` in :func:`catplot`, as data vectors can now be passed directly.

- |Enhancement| In :func:`boxplot`, the artists that comprise each box plot are now packaged in a `BoxPlotContainer` for easier post-plotting access.

Support for alternate dataframe libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- |Feature| Nearly all functions / objects now use the `dataframe exchange protocol <https://data-apis.org/dataframe-protocol/latest/index.html>`_ to accept `DataFrame` objects from libraries other than `pandas` (e.g. `polars`). Note that seaborn will still convert the data object to pandas internally, but this feature will simplify code for users of other dataframe libraries (:pr:`3369`).

Improved configuration for the objects interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- |Feature| Added control over the default theme to :class:`objects.Plot` (:pr:`3223`)

- |Feature| Added control over the default notebook display to :class:`objects.Plot` (:pr:`3225`).

- |Feature| Added the concept of a "layer legend" in :class:`objects.Plot` via the new `label` parameter in :meth:`objects.Plot.add` (:pr:`3456`).

- |Enhancement| In :meth:`objects.Plot.scale`, :meth:`objects.Plot.limit`, and :meth:`objects.Plot.label` the `x` / `y` parameters can be used to set a common scale / limit / label for paired subplots (:pr:`3458`).

Other updates
^^^^^^^^^^^^^

- |Enhancement| Improved the legend display for relational and categorical functions to better represent the user's additional keyword arguments (:pr:`3467`).

- |Enhancement| In :func:`ecdfplot`, `stat="percent"` is now a valid option (:pr:`3336`).

- |Enhancement| Data values outside the scale transform domain (e.g. non-positive values with a log scale) are now dropped prior to any statistical operations (:pr:`3488`).

- |Enhancement| In :func:`histplot`, infinite values are now ignored when choosing the default bin range (:pr:`3488`).

- |Enhancement| There is now generalized support for performing statistics in the appropriate space based on axes scales; previously support for this was spotty and at best worked only for log scales (:pr:`3440`).

- |Enhancement| Updated :func:`load_dataset` to use an approach more compatible with `pyiodide` (:pr:`3234`).

- |API| Support for array-typed palettes is now deprecated. This was not previously documented as supported, but it worked by accident in a few places (:pr:`3452`).

- |API| |Fix| In :func:`histplot`, treatment of the `binwidth` parameter has changed such that the actual bin width will be only approximately equal to the requested width when that value does not evenly divide the bin range. This fixes an issue where the largest data value was sometimes dropped due to floating point error (:pr:`3489`).

- |Fix| Fixed :class:`objects.Bar` and :class:`objects.Bars` widths when using a nonlinear scale (:pr:`3217`).

- |Fix| Worked around an issue in matplotlib that caused incorrect results in :func:`move_legend` when `labels` were provided (:pr:`3454`).

- |Fix| Fixed a bug introduced in v0.12.0 where :func:`histplot` added a stray empty `BarContainer` (:pr:`3246`).

- |Fix| Fixed a bug where :meth:`objects.Plot.on` would override a figure's layout engine (:pr:`3216`).

- |Fix| Fixed a bug introduced in v0.12.0 where :func:`lineplot` with a list of tuples for the keyword argument dashes caused a TypeError (:pr:`3316`).

- |Fix| Fixed a bug in :class:`PairGrid` that caused an exception when the input dataframe had a column multiindex (:pr:`3407`).

- |Fix| Improved a few edge cases when using pandas nullable dtypes (:pr:`3394`).
