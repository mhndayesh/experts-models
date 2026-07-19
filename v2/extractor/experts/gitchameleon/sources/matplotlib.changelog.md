
# ===== SOURCE: https://raw.githubusercontent.com/matplotlib/matplotlib/v3.8.0/doc/users/prev_whats_new/whats_new_3.2.0.rst =====

.. _whats-new-3-2-0:

What's new in Matplotlib 3.2 (Mar 04, 2020)
===========================================

For a list of all of the issues and pull requests since the last
revision, see the :ref:`github-stats`.

.. contents:: Table of Contents
   :depth: 4

.. toctree::
   :maxdepth: 4


Unit converters recognize subclasses
------------------------------------
Unit converters now also handle instances of subclasses of the class they have
been registered for.

`~.pyplot.imsave` accepts metadata and PIL options
--------------------------------------------------
`~.pyplot.imsave` has gained support for the ``metadata`` and ``pil_kwargs``
parameters. These parameters behave similarly as for the `.Figure.savefig()`
method.

`.cbook.normalize_kwargs`
-------------------------
`.cbook.normalize_kwargs` now presents a convenient interface to normalize
artist properties (e.g., from "lw" to "linewidth"):

>>> cbook.normalize_kwargs({"lw": 1}, Line2D)
{"linewidth": 1}

The first argument is the mapping to be normalized, and the second argument can
be an artist class or an artist instance (it can also be a mapping in a
specific format; see the function's docstring for details).

`.FontProperties` accepts `os.PathLike`
---------------------------------------
The *fname* argument to `.FontProperties` can now be an `os.PathLike`,
e.g.

>>> FontProperties(fname=pathlib.Path("/path/to/font.ttf"))

Gouraud-shading alpha channel in PDF backend
--------------------------------------------
The pdf backend now supports an alpha channel in Gouraud-shaded
triangle meshes.

.. _whats-new-3-2-0-kerning:

Kerning adjustments now use correct values
------------------------------------------
Due to an error in how kerning adjustments were applied, previous versions of
Matplotlib would under-correct kerning. This version will now correctly apply
kerning (for fonts supported by FreeType). To restore the old behavior (e.g.,
for test images), you may set :rc:`text.kerning_factor` to 6 (instead of 0).
Other values have undefined behavior.

.. plot::

   import matplotlib.pyplot as plt

   # Use old kerning values:
   plt.rcParams['text.kerning_factor'] = 6
   fig, ax = plt.subplots()
   ax.text(0.0, 0.05, 'BRAVO\nAWKWARD\nVAT\nW.Test', fontsize=56)
   ax.set_title('Before (text.kerning_factor = 6)')

Note how the spacing between characters is uniform between their bounding boxes
(above). With corrected kerning (below), slanted characters (e.g., AV or VA)
will be spaced closer together, as well as various other character pairs,
depending on font support (e.g., T and e, or the period after the W).

.. plot::

   import matplotlib.pyplot as plt

   # Use new kerning values:
   plt.rcParams['text.kerning_factor'] = 0
   fig, ax = plt.subplots()
   ax.text(0.0, 0.05, 'BRAVO\nAWKWARD\nVAT\nW.Test', fontsize=56)
   ax.set_title('After (text.kerning_factor = 0)')


bar3d lightsource shading
-------------------------
:meth:`~.Axes3D.bar3d` now supports lighting from different angles when the *shade*
parameter is ``True``, which can be configured using the ``lightsource``
parameter.

Shifting errorbars
------------------
Previously, `~.Axes.errorbar()` accepted a keyword argument *errorevery* such
that the command ``plt.errorbar(x, y, yerr, errorevery=6)`` would add error
bars to datapoints ``x[::6], y[::6]``.

`~.Axes.errorbar()` now also accepts a tuple for *errorevery* such that
``plt.errorbar(x, y, yerr, errorevery=(start, N))`` adds error bars to points
``x[start::N], y[start::N]``.

Improvements in Logit scale ticker and formatter
------------------------------------------------
Introduced in version 1.5, the logit scale didn't have an appropriate ticker and
formatter. Previously, the location of ticks was not zoom dependent, too many labels
were displayed causing overlapping which broke readability, and label formatting
did not adapt to precision.

Starting from this version, the logit locator has nearly the same behavior as the
locator for the log scale or the linear
scale, depending on used zoom. The number of ticks is controlled. Some minor
labels are displayed adaptively as sublabels in log scale. Formatting is adapted
for probabilities and the precision adapts to the scale.

rcParams for axes title location and color
------------------------------------------
Two new rcParams have been added: :rc:`axes.titlelocation` denotes the default axes title
alignment, and :rc:`axes.titlecolor` the default axes title color.

Valid values for ``axes.titlelocation`` are: left, center, and right.
Valid values for ``axes.titlecolor`` are: auto or a color. Setting it to auto
will fall back to previous behaviour, which is using the color in ``text.color``.

3-digit and 4-digit hex colors
------------------------------
Colors can now be specified using 3-digit or 4-digit hex colors, shorthand for
the colors obtained by duplicating each character, e.g. ``#123`` is equivalent to
``#112233`` and  ``#123a`` is equivalent to ``#112233aa``.



Added support for RGB(A) images in pcolorfast
---------------------------------------------

`.Axes.pcolorfast` now accepts 3D images (RGB or RGBA) arrays.

# ===== SOURCE: https://raw.githubusercontent.com/matplotlib/matplotlib/v3.8.0/doc/users/prev_whats_new/whats_new_3.4.0.rst =====

.. _whats-new-3-4-0:

=============================================
What's new in Matplotlib 3.4.0 (Mar 26, 2021)
=============================================

For a list of all of the issues and pull requests since the last revision, see
the :ref:`github-stats`.

.. contents:: Table of Contents
   :depth: 4

.. toctree::
   :maxdepth: 4

Figure and Axes creation / management
=====================================

New subfigure functionality
---------------------------

New `.figure.Figure.add_subfigure` and `.figure.Figure.subfigures`
functionalities allow creating virtual figures within figures. Similar nesting
was previously done with nested gridspecs (see
:doc:`/gallery/subplots_axes_and_figures/gridspec_nested`). However, this did
not allow localized figure artists (e.g., a colorbar or suptitle) that only
pertained to each subgridspec.

The new methods `.figure.Figure.add_subfigure` and `.figure.Figure.subfigures`
are meant to rhyme with `.figure.Figure.add_subplot` and
`.figure.Figure.subplots` and have most of the same arguments.

See :doc:`/gallery/subplots_axes_and_figures/subfigures` for further details.

.. note::

  The subfigure functionality is experimental API as of v3.4.

.. plot::

    def example_plot(ax, fontsize=12, hide_labels=False):
        pc = ax.pcolormesh(np.random.randn(30, 30))
        if not hide_labels:
            ax.set_xlabel('x-label', fontsize=fontsize)
            ax.set_ylabel('y-label', fontsize=fontsize)
            ax.set_title('Title', fontsize=fontsize)
        return pc

    np.random.seed(19680808)
    fig = plt.figure(constrained_layout=True, figsize=(10, 4))
    subfigs = fig.subfigures(1, 2, wspace=0.07)

    axsLeft = subfigs[0].subplots(1, 2, sharey=True)
    subfigs[0].set_facecolor('#eee')
    for ax in axsLeft:
        pc = example_plot(ax)
    subfigs[0].suptitle('Left plots', fontsize='x-large')
    subfigs[0].colorbar(pc, shrink=0.6, ax=axsLeft, location='bottom')

    axsRight = subfigs[1].subplots(3, 1, sharex=True)
    for nn, ax in enumerate(axsRight):
        pc = example_plot(ax, hide_labels=True)
        if nn == 2:
            ax.set_xlabel('xlabel')
        if nn == 1:
            ax.set_ylabel('ylabel')
    subfigs[1].colorbar(pc, shrink=0.6, ax=axsRight)
    subfigs[1].suptitle('Right plots', fontsize='x-large')

    fig.suptitle('Figure suptitle', fontsize='xx-large')

    plt.show()

Single-line string notation for ``subplot_mosaic``
--------------------------------------------------

`.Figure.subplot_mosaic` and `.pyplot.subplot_mosaic` now accept a single-line
string, using semicolons to delimit rows. Namely, ::

    plt.subplot_mosaic(
        """
        AB
        CC
        """)

may be written as the shorter:

.. plot::
    :include-source:

    plt.subplot_mosaic("AB;CC")

Changes to behavior of Axes creation methods (``gca``, ``add_axes``, ``add_subplot``)
-------------------------------------------------------------------------------------

The behavior of the functions to create new Axes (`.pyplot.axes`,
`.pyplot.subplot`, `.figure.Figure.add_axes`, `.figure.Figure.add_subplot`) has
changed. In the past, these functions would detect if you were attempting to
create Axes with the same keyword arguments as already-existing Axes in the
current Figure, and if so, they would return the existing Axes. Now,
`.pyplot.axes`, `.figure.Figure.add_axes`, and `.figure.Figure.add_subplot`
will always create new Axes. `.pyplot.subplot` will continue to reuse an
existing Axes with a matching subplot spec and equal *kwargs*.

Correspondingly, the behavior of the functions to get the current Axes
(`.pyplot.gca`, `.figure.Figure.gca`) has changed. In the past, these functions
accepted keyword arguments. If the keyword arguments matched an
already-existing Axes, then that Axes would be returned, otherwise new Axes
would be created with those keyword arguments. Now, the keyword arguments are
only considered if there are no Axes at all in the current figure. In a future
release, these functions will not accept keyword arguments at all.

``add_subplot``/``add_axes`` gained an *axes_class* parameter
-------------------------------------------------------------

In particular, ``mpl_toolkits`` Axes subclasses can now be idiomatically used
using, e.g., ``fig.add_subplot(axes_class=mpl_toolkits.axislines.Axes)``

Subplot and subplot2grid can now work with constrained layout
-------------------------------------------------------------

``constrained_layout`` depends on a single `.GridSpec` for each logical layout
on a figure. Previously, `.pyplot.subplot` and `.pyplot.subplot2grid` added a
new ``GridSpec`` each time they were called and were therefore incompatible
with ``constrained_layout``.

Now ``subplot`` attempts to reuse the ``GridSpec`` if the number of rows and
columns is the same as the top level GridSpec already in the figure, i.e.,
``plt.subplot(2, 1, 2)`` will use the same GridSpec as ``plt.subplot(2, 1, 1)``
and the ``constrained_layout=True`` option to `~.figure.Figure` will work.

In contrast, mixing *nrows* and *ncols* will *not* work with
``constrained_layout``: ``plt.subplot(2, 2, 1)`` followed by ``plt.subplots(2,
1, 2)`` will still produce two GridSpecs, and ``constrained_layout=True`` will
give bad results. In order to get the desired effect, the second call can
specify the cells the second Axes is meant to cover:  ``plt.subplots(2, 2, (2,
4))``, or the more Pythonic ``plt.subplot2grid((2, 2), (0, 1), rowspan=2)`` can
be used.


Plotting methods
================

``axline`` supports *transform* parameter
-----------------------------------------

`~.Axes.axline` now supports the *transform* parameter, which applies to the
points *xy1*, *xy2*. The *slope* (if given) is always in data coordinates.

For example, this can be used with ``ax.transAxes`` for drawing lines with a
fixed slope. In the following plot, the line appears through the same point on
both Axes, even though they show different data limits.

.. plot::
    :include-source:

    fig, axs = plt.subplots(1, 2)

    for i, ax in enumerate(axs):
        ax.axline((0.25, 0), slope=2, transform=ax.transAxes)
        ax.set(xlim=(i, i+5), ylim=(i, i+5))

New automatic labeling for bar charts
-------------------------------------

A new `.Axes.bar_label` method has been added for auto-labeling bar charts.

.. figure:: /gallery/lines_bars_and_markers/images/sphx_glr_bar_label_demo_001.png
   :target: ../../gallery/lines_bars_and_markers/bar_label_demo.html

   Example of the new automatic labeling.

A list of hatches can be specified to `~.axes.Axes.bar` and `~.axes.Axes.barh`
------------------------------------------------------------------------------

Similar to some other rectangle properties, it is now possible to hand a list
of hatch styles to `~.axes.Axes.bar` and `~.axes.Axes.barh` in order to create
bars with different hatch styles, e.g.

.. plot::

    fig, ax = plt.subplots()
    ax.bar([1, 2], [2, 3], hatch=['+', 'o'])
    plt.show()

Setting ``BarContainer`` orientation
------------------------------------

`.BarContainer` now accepts a new string argument *orientation*. It can be
either ``'vertical'`` or ``'horizontal'``, default is ``None``.

Contour plots now default to using ScalarFormatter
--------------------------------------------------

Pass ``fmt="%1.3f"`` to the contouring call to restore the old default label
format.

``Axes.errorbar`` cycles non-color properties correctly
-------------------------------------------------------

Formerly, `.Axes.errorbar` incorrectly skipped the Axes property cycle if a
color was explicitly specified, even if the property cycler was for other
properties (such as line style). Now, `.Axes.errorbar` will advance the Axes
property cycle as done for `.Axes.plot`, i.e., as long as all properties in the
cycler are not explicitly passed.

For example, the following will cycle through the line styles:

.. plot::
    :include-source:

    x = np.arange(0.1, 4, 0.5)
    y = np.exp(-x)
    offsets = [0, 1]

    plt.rcParams['axes.prop_cycle'] = plt.cycler('linestyle', ['-', '--'])

    fig, ax = plt.subplots()
    for offset in offsets:
        ax.errorbar(x, y + offset, xerr=0.1, yerr=0.3, fmt='tab:blue')

``errorbar`` *errorevery* parameter matches *markevery*
-------------------------------------------------------

Similar to the *markevery* parameter to `~.Axes.plot`, the *errorevery*
parameter of `~.Axes.errorbar` now accept slices and NumPy fancy indexes (which
must match the size of *x*).

.. plot::

    x = np.linspace(0, 1, 15)
    y = x * (1-x)
    yerr = y/6

    fig, ax = plt.subplots(2, constrained_layout=True)
    ax[0].errorbar(x, y, yerr, capsize=2)
    ax[0].set_title('errorevery unspecified')

    ax[1].errorbar(x, y, yerr, capsize=2,
                   errorevery=[False, True, True, False, True] * 3)
    ax[1].set_title('errorevery=[False, True, True, False, True] * 3')

``hexbin`` supports data reference for *C* parameter
----------------------------------------------------

As with the *x* and *y* parameters, `.Axes.hexbin` now supports passing the *C*
parameter using a data reference.

.. plot::
    :include-source:

    data = {
        'a': np.random.rand(1000),
        'b': np.random.rand(1000),
        'c': np.random.rand(1000),
    }

    fig, ax = plt.subplots()
    ax.hexbin('a', 'b', C='c', data=data, gridsize=10)

Support callable for formatting of Sankey labels
------------------------------------------------

The `format` parameter of `matplotlib.sankey.Sankey` can now accept callables.

This allows the use of an arbitrary function to label flows, for example
allowing the mapping of numbers to emoji.

.. plot::

    from matplotlib.sankey import Sankey
    import math


    def display_in_cats(values, min_cats, max_cats):
        def display_in_cat_scale(value):
            max_value = max(values, key=abs)
            number_cats_to_show = \
                max(min_cats, math.floor(abs(value) / max_value * max_cats))
            return str(number_cats_to_show * '🐱')

        return display_in_cat_scale


    flows = [35, 15, 40, -20, -15, -5, -40, -10]
    orientations = [-1, 1, 0, 1, 1, 1, -1, -1]

    # Cats are good, we want a strictly positive number of them
    min_cats = 1
    # More than four cats might be too much for some people
    max_cats = 4

    cats_format = display_in_cats(flows, min_cats, max_cats)

    sankey = Sankey(flows=flows, orientations=orientations, format=cats_format,
                    offset=.1, head_angle=180, shoulder=0, scale=.010)

    diagrams = sankey.finish()

    diagrams[0].texts[2].set_text('')

    plt.title(f'Sankey flows measured in cats \n'
              f'🐱 = {max(flows, key=abs) / max_cats}')

    plt.show()

``Axes.spines`` access shortcuts
--------------------------------

``Axes.spines`` is now a dedicated container class `.Spines` for a set of
`.Spine`\s instead of an ``OrderedDict``. On top of dict-like access,
``Axes.spines`` now also supports some ``pandas.Series``-like features.

Accessing single elements by item or by attribute::

    ax.spines['top'].set_visible(False)
    ax.spines.top.set_visible(False)

Accessing a subset of items::

    ax.spines[['top', 'right']].set_visible(False)

Accessing all items simultaneously::

    ax.spines[:].set_visible(False)

New ``stairs`` method and ``StepPatch`` artist
----------------------------------------------

`.pyplot.stairs` and the underlying artist `~.matplotlib.patches.StepPatch`
provide a cleaner interface for plotting stepwise constant functions for the
common case that you know the step edges. This supersedes many use cases of
`.pyplot.step`, for instance when plotting the output of `numpy.histogram`.

For both the artist and the function, the x-like edges input is one element
longer than the y-like values input

.. plot::

    np.random.seed(0)
    h, edges = np.histogram(np.random.normal(5, 2, 5000),
                            bins=np.linspace(0,10,20))

    fig, ax = plt.subplots(constrained_layout=True)

    ax.stairs(h, edges)

    plt.show()

See :doc:`/gallery/lines_bars_and_markers/stairs_demo` for examples.

Added *orientation* parameter for stem plots
--------------------------------------------

By default, stem lines are vertical. They can be changed to horizontal using
the *orientation* parameter of `.Axes.stem` or `.pyplot.stem`:

.. plot::

    locs = np.linspace(0.1, 2 * np.pi, 25)
    heads = np.cos(locs)

    fig, ax = plt.subplots()
    ax.stem(locs, heads, orientation='horizontal')

Angles on Bracket arrow styles
------------------------------

Angles specified on the *Bracket* arrow styles (``]-[``, ``]-``, ``-[``, or
``|-|`` passed to *arrowstyle* parameter of `.FancyArrowPatch`) are now
applied. Previously, the *angleA* and *angleB* options were allowed, but did
nothing.

.. plot::

    import matplotlib.patches as mpatches

    fig, ax = plt.subplots()
    ax.set(xlim=(0, 1), ylim=(-1, 4))

    for i, stylename in enumerate((']-[', '|-|')):
        for j, angle in enumerate([-30, 60]):
            arrowstyle = f'{stylename},angleA={angle},angleB={-angle}'
            patch = mpatches.FancyArrowPatch((0.1, 2*i + j), (0.9, 2*i + j),
                                             arrowstyle=arrowstyle,
                                             mutation_scale=25)
            ax.text(0.5, 2*i + j, arrowstyle,
                    verticalalignment='bottom', horizontalalignment='center')
            ax.add_patch(patch)

``TickedStroke`` patheffect
---------------------------

The new `.TickedStroke` patheffect can be used to produce lines with a ticked
style. This can be used to, e.g., distinguish the valid and invalid sides of
the constraint boundaries in the solution space of optimizations.

.. figure:: /gallery/misc/images/sphx_glr_tickedstroke_demo_002.png
   :target: ../../gallery/misc/tickedstroke_demo.html


Colors and colormaps
====================

Collection color specification and mapping
------------------------------------------

Reworking the handling of color mapping and the keyword arguments for
*facecolor* and *edgecolor* has resulted in three behavior changes:

1. Color mapping can be turned off by calling ``Collection.set_array(None)``.
   Previously, this would have no effect.
2. When a mappable array is set, with ``facecolor='none'`` and
   ``edgecolor='face'``, both the faces and the edges are left uncolored.
   Previously the edges would be color-mapped.
3. When a mappable array is set, with ``facecolor='none'`` and
   ``edgecolor='red'``, the edges are red. This addresses Issue #1302.
   Previously the edges would be color-mapped.

Transparency (alpha) can be set as an array in collections
----------------------------------------------------------

Previously, the alpha value controlling transparency in collections could be
specified only as a scalar applied to all elements in the collection. For
example, all the markers in a `~.Axes.scatter` plot, or all the quadrilaterals
in a `~.Axes.pcolormesh` plot, would have the same alpha value.

Now it is possible to supply alpha as an array with one value for each element
(marker, quadrilateral, etc.) in a collection.

.. plot::

    x = np.arange(5, dtype=float)
    y = np.arange(5, dtype=float)
    # z and zalpha for demo pcolormesh
    z = x[1:, np.newaxis] + y[np.newaxis, 1:]
    zalpha = np.ones_like(z)
    zalpha[::2, ::2] = 0.3  # alternate patches are partly transparent
    # s and salpha for demo scatter
    s = x
    salpha = np.linspace(0.1, 0.9, len(x))  # just a ramp

    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    axs[0, 0].pcolormesh(x, y, z, alpha=zalpha)
    axs[0, 0].set_title("pcolormesh")
    axs[0, 1].scatter(x, y, c=s, alpha=salpha)
    axs[0, 1].set_title("color-mapped")
    axs[1, 0].scatter(x, y, c='k', alpha=salpha)
    axs[1, 0].set_title("c='k'")
    axs[1, 1].scatter(x, y, c=['r', 'g', 'b', 'c', 'm'], alpha=salpha)
    axs[1, 1].set_title("c=['r', 'g', 'b', 'c', 'm']")

pcolormesh has improved transparency handling by enabling snapping
------------------------------------------------------------------

Due to how the snapping keyword argument was getting passed to the Agg backend,
previous versions of Matplotlib would appear to show lines between the grid
edges of a mesh with transparency. This version now applies snapping by
default. To restore the old behavior (e.g., for test images), you may set
:rc:`pcolormesh.snap` to `False`.

.. plot::

    # Use old pcolormesh snapping values
    plt.rcParams['pcolormesh.snap'] = False
    fig, ax = plt.subplots()
    xx, yy = np.meshgrid(np.arange(10), np.arange(10))
    z = (xx + 1) * (yy + 1)
    mesh = ax.pcolormesh(xx, yy, z, shading='auto', alpha=0.5)
    fig.colorbar(mesh, orientation='vertical')
    ax.set_title('Before (pcolormesh.snap = False)')

Note that there are lines between the grid boundaries of the main plot which
are not the same transparency. The colorbar also shows these lines when a
transparency is added to the colormap because internally it uses pcolormesh to
draw the colorbar. With snapping on by default (below), the lines at the grid
boundaries disappear.

.. plot::

    fig, ax = plt.subplots()
    xx, yy = np.meshgrid(np.arange(10), np.arange(10))
    z = (xx + 1) * (yy + 1)
    mesh = ax.pcolormesh(xx, yy, z, shading='auto', alpha=0.5)
    fig.colorbar(mesh, orientation='vertical')
    ax.set_title('After (default: pcolormesh.snap = True)')

IPython representations for Colormap objects
--------------------------------------------

The `matplotlib.colors.Colormap` object now has image representations for
IPython / Jupyter backends. Cells returning a colormap on the last line will
display an image of the colormap.

.. only:: html

    .. code-block::

        In[1]: cmap = plt.get_cmap('viridis').with_extremes(bad='r', under='g', over='b')

        In[2]: cmap
        Out[2]:

.. raw:: html

    <div style="vertical-align: middle;">
        <strong>viridis</strong>
    </div>
    <div class="cmap">
        <img alt="viridis colormap" title="viridis" style="border: 1px solid #555;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAABACAYAAABsv8+/AAAAFnRFWHRUaXRsZQB2aXJpZGlzIGNvbG9ybWFwrE0mCwAAABx0RVh0RGVzY3JpcHRpb24AdmlyaWRpcyBjb2xvcm1hcAtjl3IAAABKdEVYdEF1dGhvcgBNYXRwbG90bGliIHYzLjQuMHJjMy5wb3N0OS5kZXYwK2czZTQzMThmMjgwLCBodHRwczovL21hdHBsb3RsaWIub3JndvlliwAAAEx0RVh0U29mdHdhcmUATWF0cGxvdGxpYiB2My40LjByYzMucG9zdDkuZGV2MCtnM2U0MzE4ZjI4MCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZ9pNs1oAAAIiSURBVHic7dZBkpswFEXRL9halpD9LyX0IDIUAhnHldk7Z+KS9BFUD7pu+9V+b1VV1Vr9/V36z3ldfd1ec0vfH9bH+f3z43su987uv9x7/7s9nM+e3/bz+vK8Tvfv863u54b7xvnrerx/dm8Nzw33LA/nl+ffv+d5/en99+tv3/O/73+cq/dzn+9v3z1fT/PbV98xnh9zk/P9O2bPv99vk7l2WQ/P1Tg3/Fubrh/2+73LZX7r+zWsx/P7e2Zz+289nA9zS/vz4dx5fv3n8/N71rp/77i/vp6rh/XrvcP7ruv77zjuPX//MX++7zo/vG+2P3zH7HvXGv8u57/netmvvl/n9b7fhv2+7vv7uk8c80v/7XNtOd0DAAQRAAAQSAAAQCABAACBBAAABBIAABBIAABAIAEAAIEEAAAEEgAAEEgAAEAgAQAAgQQAAAQSAAAQSAAAQCABAACBBAAABBIAABBIAABAIAEAAIEEAAAEEgAAEEgAAEAgAQAAgQQAAAQSAAAQSAAAQCABAACBBAAABBIAABBIAABAIAEAAIEEAAAEEgAAEEgAAEAgAQAAgQQAAAQSAAAQSAAAQCABAACBBAAABBIAABBIAABAIAEAAIEEAAAEEgAAEEgAAEAgAQAAgQQAAAQSAAAQSAAAQCABAACBBAAABBIAABBIAABAIAEAAIEEAAAEEgAAEEgAAEAgAQAAgQQAAAQSAAAQSAAAQKAfbnCJh8XCmbQAAAAASUVORK5CYII=">
    </div>
    <div style="vertical-align: middle; max-width: 514px; display: flex; justify-content: space-between;">
        <div style="float: left;">
            <div title="#008000ff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #008000ff;"></div>
            under
        </div>
        <div style="margin: 0 auto; display: inline-block;">
            bad
            <div title="#ff0000ff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #ff0000ff;"></div>
        </div>
        <div style="float: right;">
            over
            <div title="#0000ffff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #0000ffff;"></div>
    </div>

``Colormap.set_extremes`` and ``Colormap.with_extremes``
--------------------------------------------------------

Because the `.Colormap.set_bad`, `.Colormap.set_under` and `.Colormap.set_over`
methods modify the colormap in place, the user must be careful to first make a
copy of the colormap if setting the extreme colors e.g. for a builtin colormap.

The new ``Colormap.with_extremes(bad=..., under=..., over=...)`` can be used to
first copy the colormap and set the extreme colors on that copy.

The new `.Colormap.set_extremes` method is provided for API symmetry with
`.Colormap.with_extremes`, but note that it suffers from the same issue as the
earlier individual setters.

Get under/over/bad colors of Colormap objects
---------------------------------------------

`matplotlib.colors.Colormap` now has methods `~.colors.Colormap.get_under`,
`~.colors.Colormap.get_over`, `~.colors.Colormap.get_bad` for the colors used
for out-of-range and masked values.

New ``cm.unregister_cmap`` function
-----------------------------------

`.cm.unregister_cmap` allows users to remove a colormap that they have
previously registered.

New ``CenteredNorm`` for symmetrical data around a center
---------------------------------------------------------

In cases where data is symmetrical around a center, for example, positive and
negative anomalies around a center zero, `~.matplotlib.colors.CenteredNorm` is
a new norm that automatically creates a symmetrical mapping around the center.
This norm is well suited to be combined with a divergent colormap which uses an
unsaturated color in its center.

.. plot::

    from matplotlib.colors import CenteredNorm

    np.random.seed(20201004)
    data = np.random.normal(size=(3, 4), loc=1)

    fig, ax = plt.subplots()
    pc = ax.pcolormesh(data, cmap=plt.get_cmap('RdGy'), norm=CenteredNorm())
    fig.colorbar(pc)
    ax.set_title('data centered around zero')

    # add text annotation
    for irow, data_row in enumerate(data):
        for icol, val in enumerate(data_row):
            ax.text(icol + 0.5, irow + 0.5, f'{val:.2f}', color='C0',
                    size=16, va='center', ha='center')
    plt.show()

If the center of symmetry is different from 0, it can be set with the *vcenter*
argument. To manually set the range of `~.matplotlib.colors.CenteredNorm`, use
the *halfrange* argument.

See :ref:`colormapnorms` for an example and more details
about data normalization.

New ``FuncNorm`` for arbitrary normalizations
---------------------------------------------

The `.FuncNorm` allows for arbitrary normalization using functions for the
forward and inverse.

.. plot::

    from matplotlib.colors import FuncNorm

    def forward(x):
        return x**2
    def inverse(x):
        return np.sqrt(x)

    norm = FuncNorm((forward, inverse), vmin=0, vmax=3)

    np.random.seed(20201004)
    data = np.random.normal(size=(3, 4), loc=1)

    fig, ax = plt.subplots()
    pc = ax.pcolormesh(data, norm=norm)
    fig.colorbar(pc)
    ax.set_title('squared normalization')

    # add text annotation
    for irow, data_row in enumerate(data):
        for icol, val in enumerate(data_row):
            ax.text(icol + 0.5, irow + 0.5, f'{val:.2f}', color='C0',
                    size=16, va='center', ha='center')
    plt.show()

See :ref:`colormapnorms` for an example and more details about data
normalization.

GridSpec-based colorbars can now be positioned above or to the left of the main axes
------------------------------------------------------------------------------------

... by passing ``location="top"`` or ``location="left"`` to the ``colorbar()``
call.


Titles, ticks, and labels
=========================

supxlabel and supylabel
-----------------------

It is possible to add x- and y-labels to a whole figure, analogous to
`.FigureBase.suptitle` using the new `.FigureBase.supxlabel` and
`.FigureBase.supylabel` methods.

.. plot::

    np.random.seed(19680801)
    fig, axs = plt.subplots(3, 2, figsize=(5, 5), constrained_layout=True,
                            sharex=True, sharey=True)

    for nn, ax in enumerate(axs.flat):
        ax.set_title(f'Channel {nn}')
        ax.plot(np.cumsum(np.random.randn(50)))

    fig.supxlabel('Time [s]')
    fig.supylabel('Data [V]')

Shared-axes ``subplots`` tick label visibility is now correct for top or left labels
------------------------------------------------------------------------------------

When calling ``subplots(..., sharex=True, sharey=True)``, Matplotlib
automatically hides x tick labels for Axes not in the first column and y tick
labels for Axes not in the last row. This behavior is incorrect if rcParams
specify that Axes should be labeled on the top (``rcParams["xtick.labeltop"] =
True``) or on the right (``rcParams["ytick.labelright"] = True``).

Cases such as the following are now handled correctly (adjusting visibility as
needed on the first row and last column of Axes):

.. plot::
    :include-source:

    plt.rcParams["xtick.labelbottom"] = False
    plt.rcParams["xtick.labeltop"] = True
    plt.rcParams["ytick.labelleft"] = False
    plt.rcParams["ytick.labelright"] = True

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)

An iterable object with labels can be passed to `.Axes.plot`
------------------------------------------------------------

When plotting multiple datasets by passing 2D data as *y* value to
`~.Axes.plot`, labels for the datasets can be passed as a list, the length
matching the number of columns in *y*.

.. plot::
    :include-source:

    x = [1, 2, 3]

    y = [[1, 2],
         [2, 5],
         [4, 9]]

    plt.plot(x, y, label=['low', 'high'])
    plt.legend()


Fonts and Text
==============

Text transform can rotate text direction
----------------------------------------

The new `.Text` parameter ``transform_rotates_text`` now sets whether rotations
of the transform affect the text direction.

.. figure:: /gallery/text_labels_and_annotations/images/sphx_glr_text_rotation_relative_to_line_001.png
   :target: ../../gallery/text_labels_and_annotations/text_rotation_relative_to_line.html

   Example of the new *transform_rotates_text* parameter

``matplotlib.mathtext`` now supports *overset* and *underset* LaTeX symbols
---------------------------------------------------------------------------

`.mathtext` now supports *overset* and *underset*, called as
``\overset{annotation}{body}`` or ``\underset{annotation}{body}``, where
*annotation* is the text "above" or "below" the *body*.

.. plot::

    math_expr = r"$ x \overset{f}{\rightarrow} y \underset{f}{\leftarrow} z $"
    plt.text(0.4, 0.5, math_expr, usetex=False)

*math_fontfamily* parameter to change ``Text`` font family
----------------------------------------------------------

The new *math_fontfamily* parameter may be used to change the family of fonts
for each individual text element in a plot. If no parameter is set, the global
value :rc:`mathtext.fontset` will be used.

.. figure:: /gallery/text_labels_and_annotations/images/sphx_glr_mathtext_fontfamily_example_001.png
   :target: ../../gallery/text_labels_and_annotations/mathtext_fontfamily_example.html

``TextArea``/``AnchoredText`` support *horizontalalignment*
-----------------------------------------------------------

The horizontal alignment of text in a `.TextArea` or `.AnchoredText` may now be
specified, which is mostly effective for multiline text:

.. plot::

    from matplotlib.offsetbox import AnchoredText

    fig, ax = plt.subplots()

    text0 = AnchoredText("test\ntest long text", loc="center left",
                         pad=0.2, prop={"ha": "left"})
    ax.add_artist(text0)

    text1 = AnchoredText("test\ntest long text", loc="center",
                         pad=0.2, prop={"ha": "center"})
    ax.add_artist(text1)

    text2 = AnchoredText("test\ntest long text", loc="center right",
                         pad=0.2, prop={"ha": "right"})
    ax.add_artist(text2)

PDF supports URLs on ``Text`` artists
-------------------------------------

URLs on `.text.Text` artists (i.e., from `.Artist.set_url`) will now be saved
in PDF files.


rcParams improvements
=====================

New rcParams for dates: set converter and whether to use interval_multiples
---------------------------------------------------------------------------

The new :rc:`date.converter` allows toggling between
`matplotlib.dates.DateConverter` and `matplotlib.dates.ConciseDateConverter`
using the strings 'auto' and 'concise' respectively.

The new :rc:`date.interval_multiples` allows toggling between the dates locator
trying to pick ticks at set intervals (i.e., day 1 and 15 of the month), versus
evenly spaced ticks that start wherever the timeseries starts:

.. plot::
    :include-source:

    dates = np.arange('2001-01-10', '2001-05-23', dtype='datetime64[D]')
    y = np.sin(dates.astype(float) / 10)
    fig, axs = plt.subplots(nrows=2, constrained_layout=True)

    plt.rcParams['date.converter'] = 'concise'
    plt.rcParams['date.interval_multiples'] = True
    axs[0].plot(dates, y)

    plt.rcParams['date.converter'] = 'auto'
    plt.rcParams['date.interval_multiples'] = False
    axs[1].plot(dates, y)

Date formatters now respect *usetex* rcParam
--------------------------------------------

The `.AutoDateFormatter` and `.ConciseDateFormatter` now respect
:rc:`text.usetex`, and will thus use fonts consistent with TeX rendering of the
default (non-date) formatter. TeX rendering may also be enabled/disabled by
passing the *usetex* parameter when creating the formatter instance.

In the following plot, both the x-axis (dates) and y-axis (numbers) now use the
same (TeX) font:

.. plot::

    from datetime import datetime, timedelta
    from matplotlib.dates import ConciseDateFormatter

    plt.rc('text', usetex=True)

    t0 = datetime(1968, 8, 1)
    ts = [t0 + i * timedelta(days=1) for i in range(10)]

    fig, ax = plt.subplots()
    ax.plot(ts, range(10))
    ax.xaxis.set_major_formatter(ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')

Setting *image.cmap* to a ``Colormap``
--------------------------------------

It is now possible to set :rc:`image.cmap` to a `.Colormap` instance, such as a
colormap created with the new `~.Colormap.set_extremes` above. (This can only
be done from Python code, not from the :file:`matplotlibrc` file.)

Tick and tick label colors can be set independently using rcParams
------------------------------------------------------------------

Previously, :rc:`xtick.color` defined both the tick color and the label color.
The label color can now be set independently using :rc:`xtick.labelcolor`. It
defaults to ``'inherit'`` which will take the value from :rc:`xtick.color`. The
same holds for ``ytick.[label]color``. For instance, to set the ticks to light
grey and the tick labels to black, one can use the following code in a script::

    import matplotlib as mpl

    mpl.rcParams['xtick.labelcolor'] = 'lightgrey'
    mpl.rcParams['xtick.color'] = 'black'
    mpl.rcParams['ytick.labelcolor'] = 'lightgrey'
    mpl.rcParams['ytick.color'] = 'black'

Or by adding the following lines to the :ref:`matplotlibrc
<customizing-with-matplotlibrc-files>` file, or a Matplotlib style file:

.. code-block:: none

   xtick.labelcolor : lightgrey
   xtick.color      : black
   ytick.labelcolor : lightgrey
   ytick.color      : black


3D Axes improvements
====================

Errorbar method in 3D Axes
--------------------------

The errorbar function `.Axes.errorbar` is ported into the 3D Axes framework in
its entirety, supporting features such as custom styling for error lines and
cap marks, control over errorbar spacing, upper and lower limit marks.

.. figure:: /gallery/mplot3d/images/sphx_glr_errorbar3d_001.png
   :target: ../../gallery/mplot3d/errorbar3d.html

Stem plots in 3D Axes
---------------------

Stem plots are now supported on 3D Axes. Much like 2D stems,
`~.axes3d.Axes3D.stem` supports plotting the stems in various orientations:

.. plot::

    theta = np.linspace(0, 2*np.pi)
    x = np.cos(theta - np.pi/2)
    y = np.sin(theta - np.pi/2)
    z = theta
    directions = ['z', 'x', 'y']
    names = [r'$\theta$', r'$\cos\theta$', r'$\sin\theta$']

    fig, axs = plt.subplots(1, 3, figsize=(8, 4),
                            constrained_layout=True,
                            subplot_kw={'projection': '3d'})
    for ax, zdir, name in zip(axs, directions, names):
        ax.stem(x, y, z, orientation=zdir)
        ax.set_title(name)
    fig.suptitle(r'A parametric circle: $(x, y) = (\cos\theta, \sin\theta)$')

See also the :doc:`/gallery/mplot3d/stem3d_demo` demo.

3D Collection properties are now modifiable
-------------------------------------------

Previously, properties of a 3D Collection that were used for 3D effects (e.g.,
colors were modified to produce depth shading) could not be changed after it
was created.

Now it is possible to modify all properties of 3D Collections at any time.

Panning in 3D Axes
------------------

Click and drag with the middle mouse button to pan 3D Axes.


Interactive tool improvements
=============================

New ``RangeSlider`` widget
--------------------------

`.widgets.RangeSlider` allows for creating a slider that defines
a range rather than a single value.

.. plot::

    fig, ax = plt.subplots(2, 1, figsize=(5, 1))
    fig.subplots_adjust(left=0.2, right=0.8)

    from matplotlib.widgets import Slider, RangeSlider
    Slider(ax[0], 'Slider', 0, 1)
    RangeSlider(ax[1], 'RangeSlider', 0, 1)

Sliders can now snap to arbitrary values
----------------------------------------

The `~matplotlib.widgets.Slider` UI widget now accepts arrays for *valstep*.
This generalizes the previous behavior by allowing the slider to snap to
arbitrary values.

Pausing and Resuming Animations
-------------------------------

The `.animation.Animation.pause` and `.animation.Animation.resume` methods
allow you to pause and resume animations. These methods can be used as
callbacks for event listeners on UI elements so that your plots can have some
playback control UI.


Sphinx extensions
=================

``plot_directive`` *caption* option
-----------------------------------

Captions were previously supported when using the ``plot_directive`` directive
with an external source file by specifying content::

    .. plot:: path/to/plot.py

        This is the caption for the plot.

The ``:caption:`` option allows specifying the caption for both external::

    .. plot:: path/to/plot.py
        :caption: This is the caption for the plot.

and inline plots::

    .. plot::
        :caption: This is a caption for the plot.

        plt.plot([1, 2, 3])


Backend-specific improvements
=============================

Consecutive rasterized draws now merged
---------------------------------------

Elements of a vector output can be individually set to rasterized, using the
*rasterized* keyword argument, or `~.artist.Artist.set_rasterized()`. This can
be useful to reduce file sizes. For figures with multiple raster elements they
are now automatically merged into a smaller number of bitmaps where this will
not effect the visual output. For cases with many elements this can result in
significantly smaller file sizes.

To ensure this happens do not place vector elements between raster ones.

To inhibit this merging set ``Figure.suppressComposite`` to True.

Support raw/rgba frame format in ``FFMpegFileWriter``
-----------------------------------------------------

When using `.FFMpegFileWriter`, the  *frame_format* may now be set to ``"raw"``
or ``"rgba"``, which may be slightly faster than an image format, as no
encoding/decoding need take place between Matplotlib and FFmpeg.

nbAgg/WebAgg support middle-click and double-click
--------------------------------------------------

Double click events are now supported by the nbAgg and WebAgg backends.
Formerly, WebAgg would report middle-click events as right clicks, but now
reports the correct button type.

nbAgg support binary communication
----------------------------------

If the web browser and notebook support binary websockets, nbAgg will now use
them for slightly improved transfer of figure display.

Indexed color for PNG images in PDF files when possible
-------------------------------------------------------

When PNG images have 256 colors or fewer, they are converted to indexed color
before saving them in a PDF. This can result in a significant reduction in file
size in some cases. This is particularly true for raster data that uses a
colormap but no interpolation, such as Healpy mollview plots. Currently, this
is only done for RGB images.

Improved font subsettings in PDF/PS
-----------------------------------

Font subsetting in PDF and PostScript has been re-written from the embedded
``ttconv`` C code to Python. Some composite characters and outlines may have
changed slightly. This fixes ttc subsetting in PDF, and adds support for
subsetting of type 3 OTF fonts, resulting in smaller files (much smaller when
using CJK fonts), and avoids running into issues with type 42 embedding and
certain PDF readers such as Acrobat Reader.

Kerning added to strings in PDFs
--------------------------------

As with text produced in the Agg backend (see :ref:`the previous what's new
entry <whats-new-3-2-0-kerning>` for examples), PDFs now include kerning in
text strings.

Fully-fractional HiDPI in QtAgg
-------------------------------

Fully-fractional HiDPI (that is, HiDPI ratios that are not whole integers) was
added in Qt 5.14, and is now supported by the QtAgg backend when using this
version of Qt or newer.

wxAgg supports fullscreen toggle
--------------------------------

The wxAgg backend supports toggling fullscreen using the :kbd:`f` shortcut, or
the manager function `.FigureManagerBase.full_screen_toggle`.

# ===== SOURCE: https://raw.githubusercontent.com/matplotlib/matplotlib/v3.8.0/doc/users/prev_whats_new/whats_new_3.5.0.rst =====

=============================================
What's new in Matplotlib 3.5.0 (Nov 15, 2021)
=============================================

For a list of all of the issues and pull requests since the last revision, see
the :ref:`github-stats`.

.. contents:: Table of Contents
   :depth: 4

.. toctree::
   :maxdepth: 4

Figure and Axes creation / management
=====================================

``subplot_mosaic`` supports simple Axes sharing
-----------------------------------------------

`.Figure.subplot_mosaic`, `.pyplot.subplot_mosaic` support *simple* Axes
sharing (i.e., only `True`/`False` may be passed to *sharex*/*sharey*). When
`True`, tick label visibility and Axis units will be shared.

.. plot::
    :include-source:

    mosaic = [
        ['A', [['B', 'C'],
               ['D', 'E']]],
        ['F', 'G'],
    ]
    fig = plt.figure(constrained_layout=True)
    ax_dict = fig.subplot_mosaic(mosaic, sharex=True, sharey=True)
    # All Axes use these scales after this call.
    ax_dict['A'].set(xscale='log', yscale='logit')

Figure now has ``draw_without_rendering`` method
------------------------------------------------

Some aspects of a figure are only determined at draw-time, such as the exact
position of text artists or deferred computation like automatic data limits.
If you need these values, you can use ``figure.canvas.draw()`` to force a full
draw. However, this has side effects, sometimes requires an open file, and is
doing more work than is needed.

The new `.Figure.draw_without_rendering` method runs all the updates that
``draw()`` does, but skips rendering the figure. It's thus more efficient if
you need the updated values to configure further aspects of the figure.

Figure ``__init__`` passes keyword arguments through to set
-----------------------------------------------------------

Similar to many other sub-classes of `~.Artist`, the `~.FigureBase`,
`~.SubFigure`, and `~.Figure` classes will now pass any additional keyword
arguments to `~.Artist.set` to allow properties of the newly created object to
be set at initialization time. For example::

    from matplotlib.figure import Figure
    fig = Figure(label='my figure')

Plotting methods
================

Add ``Annulus`` patch
---------------------

`.Annulus` is a new class for drawing elliptical annuli.

.. plot::

    import matplotlib.pyplot as plt
    from matplotlib.patches import Annulus

    fig, ax = plt.subplots()
    cir = Annulus((0.5, 0.5), 0.2, 0.05, fc='g')        # circular annulus
    ell = Annulus((0.5, 0.5), (0.5, 0.3), 0.1, 45,      # elliptical
                  fc='m', ec='b', alpha=0.5, hatch='xxx')
    ax.add_patch(cir)
    ax.add_patch(ell)
    ax.set_aspect('equal')

``set_data`` method for ``FancyArrow`` patch
--------------------------------------------

`.FancyArrow`, the patch returned by ``ax.arrow``, now has a ``set_data``
method that allows modifying the arrow after creation, e.g., for animation.

New arrow styles in ``ArrowStyle`` and ``ConnectionPatch``
----------------------------------------------------------

The new *arrow* parameter to `.ArrowStyle` substitutes the use of the
*beginarrow* and *endarrow* parameters in the creation of arrows. It receives
arrows strings like ``'<-'``, ``']-[``' and ``']->``' instead of individual
booleans.

Two new styles ``']->'`` and ``'<-['`` are also added via this mechanism.
`.ConnectionPatch`, which accepts arrow styles though its *arrowstyle*
parameter, also accepts these new styles.

.. plot::

    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(figsize=(4, 4))

    ax.plot([0.75, 0.75], [0.25, 0.75], 'ok')
    ax.set(xlim=(0, 1), ylim=(0, 1), title='New ArrowStyle options')

    ax.annotate(']->', (0.75, 0.25), (0.25, 0.25),
                arrowprops=dict(
                    arrowstyle=']->', connectionstyle="arc3,rad=-0.05",
                    shrinkA=5, shrinkB=5,
                ),
                bbox=dict(boxstyle='square', fc='w'), size='large')

    ax.annotate('<-[', (0.75, 0.75), (0.25, 0.75),
                arrowprops=dict(
                    arrowstyle='<-[', connectionstyle="arc3,rad=-0.05",
                    shrinkA=5, shrinkB=5,
                ),
                bbox=dict(boxstyle='square', fc='w'), size='large')

Setting collection offset transform after initialization
--------------------------------------------------------

The added `.collections.Collection.set_offset_transform` may be used to set the
offset transform after initialization. This can be helpful when creating a
`.collections.Collection` outside an Axes object, and later adding it with
`.Axes.add_collection()` and setting the offset transform to ``Axes.transData``.

Colors and colormaps
====================

Colormap registry (experimental)
--------------------------------

Colormaps are now managed via `matplotlib.colormaps` (or `.pyplot.colormaps`),
which is a `.ColormapRegistry`. While we are confident that the API is final,
we formally mark it as experimental for 3.5 because we want to keep the option
to still modify the API for 3.6 should the need arise.

Colormaps can be obtained using item access::

    import matplotlib.pyplot as plt
    cmap = plt.colormaps['viridis']

To register new colormaps use::

    plt.colormaps.register(my_colormap)

We recommend to use the new API instead of the `~.cm.get_cmap` and
`~.cm.register_cmap` functions for new code. `matplotlib.cm.get_cmap` and
`matplotlib.cm.register_cmap` will eventually be deprecated and removed.
Within `.pyplot`, ``plt.get_cmap()`` and ``plt.register_cmap()`` will continue
to be supported for backward compatibility.

Image interpolation now possible at RGBA stage
----------------------------------------------

Images in Matplotlib created via `~.axes.Axes.imshow` are resampled to match
the resolution of the current canvas. It is useful to apply an auto-aliasing
filter when downsampling to reduce Moiré effects. By default, interpolation is
done on the data, a norm applied, and then the colormapping performed.

However, it is often desirable for the anti-aliasing interpolation to happen
in RGBA space, where the colors are interpolated rather than the data. This
usually leads to colors outside the colormap, but visually blends adjacent
colors, and is what browsers and other image processing software do.

A new keyword argument *interpolation_stage* is provided for
`~.axes.Axes.imshow` to set the stage at which the anti-aliasing interpolation
happens. The default is the current behaviour of "data", with the alternative
being "rgba" for the newly-available behavior.

.. figure:: /gallery/images_contours_and_fields/images/sphx_glr_image_antialiasing_001.png
   :target: ../../gallery/images_contours_and_fields/image_antialiasing.html

   Example of the interpolation stage options.

For more details see the discussion of the new keyword argument in
:doc:`/gallery/images_contours_and_fields/image_antialiasing`.

``imshow`` supports half-float arrays
-------------------------------------

The `~.axes.Axes.imshow` method now supports half-float arrays, i.e., NumPy
arrays with dtype ``np.float16``.

A callback registry has been added to Normalize objects
-------------------------------------------------------

`.colors.Normalize` objects now have a callback registry, ``callbacks``, that
can be connected to by other objects to be notified when the norm is updated.
The callback emits the key ``changed`` when the norm is modified.
`.cm.ScalarMappable` is now a listener and will register a change when the
norm's vmin, vmax or other attributes are changed.

Titles, ticks, and labels
=========================

Settings tick positions and labels simultaneously in ``set_ticks``
------------------------------------------------------------------

`.Axis.set_ticks` (and the corresponding `.Axes.set_xticks` /
`.Axes.set_yticks`) has a new parameter *labels* allowing to set tick positions
and labels simultaneously.

Previously, setting tick labels was done using `.Axis.set_ticklabels` (or
the corresponding `.Axes.set_xticklabels` / `.Axes.set_yticklabels`); this
usually only makes sense if tick positions were previously fixed with
`~.Axis.set_ticks`::

    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['a', 'b', 'c'])

The combined functionality is now available in `~.Axis.set_ticks`::

    ax.set_xticks([1, 2, 3], ['a', 'b', 'c'])

The use of `.Axis.set_ticklabels` is discouraged, but it will stay available
for backward compatibility.

Note: This addition makes the API of `~.Axis.set_ticks` also more similar to
`.pyplot.xticks` / `.pyplot.yticks`, which already had the additional *labels*
parameter.

Fonts and Text
==============

Triple and quadruple dot mathtext accents
-----------------------------------------

In addition to single and double dot accents, mathtext now supports triple and
quadruple dot accents.

.. plot::
    :include-source:

    fig = plt.figure(figsize=(3, 1))
    fig.text(0.5, 0.5, r'$\dot{a} \ddot{b} \dddot{c} \ddddot{d}$', fontsize=40,
             horizontalalignment='center', verticalalignment='center')

Font properties of legend title are configurable
------------------------------------------------

Title's font properties can be set via the *title_fontproperties* keyword
argument, for example:

.. plot::

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(range(10), label='point')
    ax.legend(title='Points',
              title_fontproperties={'family': 'serif', 'size': 20})

``Text`` and ``TextBox`` added *parse_math* option
--------------------------------------------------

`.Text` and `.TextBox` objects now allow a *parse_math* keyword-only argument
which controls whether math should be parsed from the displayed string. If
*True*, the string will be parsed as a math text object. If *False*, the string
will be considered a literal and no parsing will occur.

Text can be positioned inside TextBox widget
--------------------------------------------

A new parameter called *textalignment* can be used to control for the position
of the text inside the Axes of the `.TextBox` widget.

.. plot::

    from matplotlib import pyplot as plt
    from matplotlib.widgets import TextBox

    fig = plt.figure(figsize=(4, 3))
    for i, alignment in enumerate(['left', 'center', 'right']):
            box_input = fig.add_axes([0.1, 0.7 - i*0.3, 0.8, 0.2])
            text_box = TextBox(ax=box_input, initial=f'{alignment} alignment',
                               label='', textalignment=alignment)

Simplifying the font setting for usetex mode
--------------------------------------------

Now the :rc:`font.family` accepts some font names as value for a more
user-friendly setup.

.. code-block::

    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "Helvetica"
    })

Type 42 subsetting is now enabled for PDF/PS backends
-----------------------------------------------------

`~matplotlib.backends.backend_pdf` and `~matplotlib.backends.backend_ps` now
use a unified Type 42 font subsetting interface, with the help of `fontTools
<https://fonttools.readthedocs.io/en/latest/>`_

Set :rc:`pdf.fonttype` or :rc:`ps.fonttype` to ``42`` to trigger this
workflow::

    # for PDF backend
    plt.rcParams['pdf.fonttype'] = 42

    # for PS backend
    plt.rcParams['ps.fonttype'] = 42

    fig, ax = plt.subplots()
    ax.text(0.4, 0.5, 'subsetted document is smaller in size!')

    fig.savefig("document.pdf")
    fig.savefig("document.ps")

rcParams improvements
=====================

Allow setting default legend labelcolor globally
------------------------------------------------

A new :rc:`legend.labelcolor` sets the default *labelcolor* argument for
`.Figure.legend`.  The special values  'linecolor', 'markerfacecolor' (or
'mfc'), or 'markeredgecolor' (or 'mec') will cause the legend text to match the
corresponding color of marker.

.. plot::

    plt.rcParams['legend.labelcolor'] = 'linecolor'

    # Make some fake data.
    a = np.arange(0, 3, .02)
    c = np.exp(a)
    d = c[::-1]

    fig, ax = plt.subplots()
    ax.plot(a, c, 'g--', label='Model length')
    ax.plot(a, d, 'r:', label='Data length')

    ax.legend()

    plt.show()

3D Axes improvements
====================

Axes3D now allows manual control of draw order
----------------------------------------------

The `~mpl_toolkits.mplot3d.axes3d.Axes3D` class now has *computed_zorder*
parameter. When set to False, Artists are drawn using their ``zorder``
attribute.

.. plot::

    import matplotlib.patches as mpatches
    from mpl_toolkits.mplot3d import art3d

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.4, 3),
                                   subplot_kw=dict(projection='3d'))

    ax1.set_title('computed_zorder = True (default)')
    ax2.set_title('computed_zorder = False')
    ax2.computed_zorder = False

    corners = ((0, 0, 0), (0, 5, 0), (5, 5, 0), (5, 0, 0))
    for ax in (ax1, ax2):
        tri = art3d.Poly3DCollection([corners],
                                     facecolors='white',
                                     edgecolors='black',
                                     zorder=1)
        ax.add_collection3d(tri)
        line, = ax.plot((2, 2), (2, 2), (0, 4), c='red', zorder=2,
                        label='zorder=2')
        points = ax.scatter((3, 3), (1, 3), (1, 3), c='red', zorder=10,
                            label='zorder=10')

        ax.set_xlim((0, 5))
        ax.set_ylim((0, 5))
        ax.set_zlim((0, 2.5))

    plane = mpatches.Patch(facecolor='white', edgecolor='black',
                           label='zorder=1')
    fig.legend(handles=[plane, line, points], loc='lower center')

Allow changing the vertical axis in 3d plots
----------------------------------------------

`~mpl_toolkits.mplot3d.axes3d.Axes3D.view_init` now has the parameter
*vertical_axis* which allows switching which axis is aligned vertically.

.. plot::

    Nphi, Nr = 18, 8
    phi = np.linspace(0, np.pi, Nphi)
    r = np.arange(Nr)
    phi = np.tile(phi, Nr).flatten()
    r = np.repeat(r, Nphi).flatten()

    x = r * np.sin(phi)
    y = r * np.cos(phi)
    z = Nr - r

    fig, axs = plt.subplots(1, 3, figsize=(7, 3),
                            subplot_kw=dict(projection='3d'),
                            gridspec_kw=dict(wspace=0.4, left=0.08, right=0.98,
                                             bottom=0, top=1))
    for vert_a, ax in zip(['z', 'y', 'x'], axs):
        pc = ax.scatter(x, y, z, c=z)
        ax.view_init(azim=30, elev=30, vertical_axis=vert_a)
        ax.set(xlabel='x', ylabel='y', zlabel='z',
               title=f'vertical_axis={vert_a!r}')

``plot_surface`` supports masked arrays and NaNs
------------------------------------------------

`.axes3d.Axes3D.plot_surface` supports masked arrays and NaNs, and will now
hide quads that contain masked or NaN points. The behaviour is similar to
`.Axes.contour` with ``corner_mask=True``.

.. plot::

    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': '3d'},
                           constrained_layout=True)

    x, y = np.mgrid[1:10:1, 1:10:1]
    z = x ** 3 + y ** 3 - 500
    z = np.ma.masked_array(z, z < 0)

    ax.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0, cmap='inferno')
    ax.view_init(35, -90)

3D plotting methods support *data* keyword argument
---------------------------------------------------

To match all 2D plotting methods, the 3D Axes now support the *data* keyword
argument. This allows passing arguments indirectly from a DataFrame-like
structure. ::

    data = {  # A labelled data set, or e.g., Pandas DataFrame.
        'x': ...,
        'y': ...,
        'z': ...,
        'width': ...,
        'depth': ...,
        'top': ...,
    }

    fig, ax = plt.subplots(subplot_kw={'projection': '3d')
    ax.bar3d('x', 'y', 'z', 'width', 'depth', 'top', data=data)

Interactive tool improvements
=============================

Colorbars now have pan and zoom functionality
---------------------------------------------

Interactive plots with colorbars can now be zoomed and panned on the colorbar
axis. This adjusts the *vmin* and *vmax* of the ``ScalarMappable`` associated
with the colorbar. This is currently only enabled for continuous norms. Norms
used with contourf and categoricals, such as ``BoundaryNorm`` and ``NoNorm``,
have the interactive capability disabled by default. ``cb.ax.set_navigate()``
can be used to set whether a colorbar axes is interactive or not.

Updated the appearance of Slider widgets
----------------------------------------

The appearance of `~.Slider` and `~.RangeSlider` widgets were updated and given
new styling parameters for the added handles.

.. plot::

    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider

    plt.figure(figsize=(4, 2))
    ax_old = plt.axes([0.2, 0.65, 0.65, 0.1])
    ax_new = plt.axes([0.2, 0.25, 0.65, 0.1])
    Slider(ax_new, "New", 0, 1)

    ax = ax_old
    valmin = 0
    valinit = 0.5
    ax.set_xlim([0, 1])
    ax_old.axvspan(valmin, valinit, 0, 1)
    ax.axvline(valinit, 0, 1, color="r", lw=1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(
        -0.02,
        0.5,
        "Old",
        transform=ax.transAxes,
        verticalalignment="center",
        horizontalalignment="right",
    )

    ax.text(
        1.02,
        0.5,
        "0.5",
        transform=ax.transAxes,
        verticalalignment="center",
        horizontalalignment="left",
    )

Removing points on a PolygonSelector
------------------------------------

After completing a `~matplotlib.widgets.PolygonSelector`, individual points can
now be removed by right-clicking on them.

Dragging selectors
------------------

The `~matplotlib.widgets.SpanSelector`, `~matplotlib.widgets.RectangleSelector`
and `~matplotlib.widgets.EllipseSelector` have a new keyword argument,
*drag_from_anywhere*, which when set to `True` allows you to click and drag
from anywhere inside the selector to move it. Previously it was only possible
to move it by either activating the move modifier button, or clicking on the
central handle.

The size of the `~matplotlib.widgets.SpanSelector` can now be changed using the
edge handles.

Clearing selectors
------------------

The selectors (`~.widgets.EllipseSelector`, `~.widgets.LassoSelector`,
`~.widgets.PolygonSelector`, `~.widgets.RectangleSelector`, and
`~.widgets.SpanSelector`) have a new method *clear*, which will clear the
current selection and get the selector ready to make a new selection. This is
equivalent to pressing the *escape* key.

Setting artist properties of selectors
--------------------------------------

The artist properties of the `~.widgets.EllipseSelector`,
`~.widgets.LassoSelector`, `~.widgets.PolygonSelector`,
`~.widgets.RectangleSelector` and `~.widgets.SpanSelector` selectors can be
changed using the ``set_props`` and ``set_handle_props`` methods.

Ignore events outside selection
-------------------------------

The `~.widgets.EllipseSelector`, `~.widgets.RectangleSelector` and
`~.widgets.SpanSelector` selectors have a new keyword argument,
*ignore_event_outside*, which when set to `True` will ignore events outside of
the current selection. The handles or the new dragging functionality can instead
be used to change the selection.

``CallbackRegistry`` objects gain a method to temporarily block signals
-----------------------------------------------------------------------

The context manager `~matplotlib.cbook.CallbackRegistry.blocked` can be used
to block callback signals from being processed by the ``CallbackRegistry``.
The optional keyword, *signal*, can be used to block a specific signal
from being processed and let all other signals pass.

.. code-block::

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.imshow([[0, 1], [2, 3]])

    # Block all interactivity through the canvas callbacks
    with fig.canvas.callbacks.blocked():
        plt.show()

    fig, ax = plt.subplots()
    ax.imshow([[0, 1], [2, 3]])

    # Only block key press events
    with fig.canvas.callbacks.blocked(signal="key_press_event"):
        plt.show()

Directional sizing cursors
--------------------------

Canvases now support setting directional sizing cursors, i.e., horizontal and
vertical double arrows. These are used in e.g., selector widgets. Try the
:doc:`/gallery/widgets/mouse_cursor` example to see the cursor in your desired
backend.

Sphinx extensions
=================

More configuration of ``mathmpl`` sphinx extension
--------------------------------------------------

The `matplotlib.sphinxext.mathmpl` sphinx extension supports two new
configuration options that may be specified in your ``conf.py``:

- ``mathmpl_fontsize`` (float), which sets the font size of the math text in
  points;
- ``mathmpl_srcset`` (list of str), which provides a list of sizes to support
  `responsive resolution images
  <https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images>`__
  The list should contain additional x-descriptors (``'1.5x'``, ``'2x'``, etc.)
  to generate (1x is the default and always included.)

Backend-specific improvements
=============================

GTK backend
-----------

A backend supporting GTK4_ has been added. Both Agg and Cairo renderers are
supported. The GTK4 backends may be selected as GTK4Agg or GTK4Cairo.

.. _GTK4: https://www.gtk.org/

Qt backends
-----------

Support for Qt6 (using either PyQt6_ or PySide6_) has been added, with either
the Agg or Cairo renderers. Simultaneously, support for Qt4 has been dropped.
Both Qt6 and Qt5 are supported by a combined backend (QtAgg or QtCairo), and
the loaded version is determined by modules already imported, the
:envvar:`QT_API` environment variable, and available packages. See
:ref:`QT_bindings` for details. The versioned Qt5 backend names (Qt5Agg or
Qt5Cairo) remain supported for backwards compatibility.

.. _PyQt6: https://www.riverbankcomputing.com/static/Docs/PyQt6/
.. _PySide6: https://doc.qt.io/qtforpython/

HiDPI support in Cairo-based, GTK, and Tk backends
--------------------------------------------------

The GTK3 backends now support HiDPI fully, including mixed monitor cases (on
Wayland only). The newly added GTK4 backends also support HiDPI.

The TkAgg backend now supports HiDPI **on Windows only**, including mixed
monitor cases.

All Cairo-based backends correctly support HiDPI as well as their Agg
counterparts did (i.e., if the toolkit supports HiDPI, then the \*Cairo backend
will now support it, but not otherwise.)

Qt figure options editor improvements
-------------------------------------

The figure options editor in the Qt backend now also supports editing the left
and right titles (plus the existing centre title). Editing Axis limits is
better supported when using a date converter. The ``symlog`` option is now
available in Axis scaling options. All entries with the same label are now
shown in the Curves tab.

WX backends support mouse navigation buttons
--------------------------------------------

The WX backends now support navigating through view states using the mouse
forward/backward buttons, as in other backends.

WebAgg uses asyncio instead of Tornado
--------------------------------------

The WebAgg backend defaults to using `asyncio` over Tornado for timer support.
This allows using the WebAgg backend in JupyterLite.

Version information
===================

We switched to the `release-branch-semver`_ version scheme of setuptools-scm.
This only affects the version information for development builds. Their version
number now describes the targeted release, i.e. 3.5.0.dev820+g6768ef8c4c is 820
commits after the previous release and is scheduled to be officially released
as 3.5.0 later.

In addition to the string ``__version__``, there is now a namedtuple
``__version_info__`` as well, which is modelled after `sys.version_info`_. Its
primary use is safely comparing version information, e.g.  ``if
__version_info__ >= (3, 4, 2)``.

.. _release-branch-semver: https://github.com/pypa/setuptools_scm#version-number-construction
.. _sys.version_info: https://docs.python.org/3/library/sys.html#sys.version_info

# ===== SOURCE: https://raw.githubusercontent.com/matplotlib/matplotlib/v3.8.0/doc/users/prev_whats_new/whats_new_3.8.0.rst =====

==============================================
What's new in Matplotlib 3.8.0 (Sept 13, 2023)
==============================================

For a list of all of the issues and pull requests since the last revision, see
the :ref:`github-stats`.

.. contents:: Table of Contents
   :depth: 4

.. toctree::
   :maxdepth: 4

Type Hints
==========

Matplotlib now provides first-party PEP484 style type hints files for most public APIs.

While still considered provisional and subject to change (and sometimes we are not
quite able to fully specify what we would like to), they should provide a reasonable
basis to type check many common usage patterns, as well as integrating with many
editors/IDEs.

Plotting and Annotation improvements
====================================

Support customizing antialiasing for text and annotation
--------------------------------------------------------
``matplotlib.pyplot.annotate()`` and ``matplotlib.pyplot.text()`` now support parameter *antialiased*.
When *antialiased* is set to ``True``, antialiasing will be applied to the text.
When *antialiased* is set to ``False``, antialiasing will not be applied to the text.
When *antialiased* is not specified, antialiasing will be set by :rc:`text.antialiased` at the creation time of ``Text`` and ``Annotation`` object.
Examples:

.. code-block::

    mpl.text.Text(.5, .5, "foo\nbar", antialiased=True)
    plt.text(0.5, 0.5, '6 inches x 2 inches', antialiased=True)
    ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5), antialiased=False)

If the text contains math expression, *antialiased* applies to the whole text.
Examples:

.. code-block::

    # no part will be antialiased for the text below
    plt.text(0.5, 0.25, r"$I'm \sqrt{x}$", antialiased=False)

Also note that antialiasing for tick labels will be set with :rc:`text.antialiased` when they are created (usually when a ``Figure`` is created) and cannot be changed afterwards.

Furthermore, with this new feature, you may want to make sure that you are creating and saving/showing the figure under the same context::

    # previously this was a no-op, now it is what works
    with rccontext(text.antialiased=False):
        fig, ax = plt.subplots()
        ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5))
        fig.savefig('/tmp/test.png')


    # previously this had an effect, now this is a no-op
    fig, ax = plt.subplots()
    ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5))
    with rccontext(text.antialiased=False):
        fig.savefig('/tmp/test.png')

rcParams for ``AutoMinorLocator`` divisions
-------------------------------------------
The rcParams :rc:`xtick.minor.ndivs` and :rc:`ytick.minor.ndivs` have been
added to enable setting the default number of divisions; if set to ``auto``,
the number of divisions will be chosen by the distance between major ticks.

Axline setters and getters
--------------------------

The returned object from `.axes.Axes.axline` now supports getter and setter
methods for its *xy1*, *xy2* and *slope* attributes:

.. code-block:: python

    line1.get_xy1()
    line1.get_slope()
    line2.get_xy2()

.. code-block:: python

    line1.set_xy1(.2, .3)
    line1.set_slope(2.4)
    line2.set_xy2(.1, .6)

Clipping for contour plots
--------------------------

`-.Axes.contour` and `-.Axes.contourf` now accept the *clip_path* parameter.

.. plot::
    :include-source: true

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    x = y = np.arange(-3.0, 3.01, 0.025)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
    Z = (Z1 - Z2) * 2

    fig, ax = plt.subplots()
    patch = mpatches.RegularPolygon((0, 0), 5, radius=2,
                                    transform=ax.transData)
    ax.contourf(X, Y, Z, clip_path=patch)

    plt.show()

``Axes.ecdf``
-------------
A new Axes method, `-.Axes.ecdf`, allows plotting empirical cumulative
distribution functions without any binning.

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   import numpy as np

   fig, ax = plt.subplots()
   ax.ecdf(np.random.randn(100))

``Figure.get_suptitle()``, ``Figure.get_supxlabel()``, ``Figure.get_supylabel()``
---------------------------------------------------------------------------------
These methods return the strings set by ``Figure.suptitle()``, ``Figure.supxlabel()``
and ``Figure.supylabel()`` respectively.

``Ellipse.get_vertices()``, ``Ellipse.get_co_vertices()``
---------------------------------------------------------------------------------
These methods return the coordinates of ellipse vertices of
major and minor axis. Additionally, an example gallery demo is added which
shows how to add an arrow to an ellipse showing a clockwise or counter-clockwise
rotation of the ellipse. To place the arrow exactly on the ellipse,
the coordinates of the vertices are used.

Remove inner ticks in ``label_outer()``
---------------------------------------
Up to now, ``label_outer()`` has only removed the ticklabels. The ticks lines
were left visible. This is now configurable through a new parameter
``label_outer(remove_inner_ticks=True)``.


.. plot::
   :include-source: true

    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(0, 2 * np.pi, 100)

    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True,
                            gridspec_kw=dict(hspace=0, wspace=0))

    axs[0, 0].plot(x, np.sin(x))
    axs[0, 1].plot(x, np.cos(x))
    axs[1, 0].plot(x, -np.cos(x))
    axs[1, 1].plot(x, -np.sin(x))

    for ax in axs.flat:
        ax.grid(color='0.9')
        ax.label_outer(remove_inner_ticks=True)

Configurable legend shadows
---------------------------
The *shadow* parameter of legends now accepts dicts in addition to booleans.
Dictionaries can contain any keywords for `.patches.Patch`.
For example, this allows one to set the color and/or the transparency of a legend shadow:

.. code-block:: python

   ax.legend(loc='center left', shadow={'color': 'red', 'alpha': 0.5})

and to control the shadow location:

.. code-block:: python

   ax.legend(loc='center left', shadow={"ox":20, "oy":-20})

Configuration is currently not supported via :rc:`legend.shadow`.


``offset`` parameter for MultipleLocator
----------------------------------------

An *offset* may now be specified to shift all the ticks by the given value.

.. plot::
    :include-source: true

    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker

    _, ax = plt.subplots()
    ax.plot(range(10))
    locator = mticker.MultipleLocator(base=3, offset=0.3)
    ax.xaxis.set_major_locator(locator)

    plt.show()

Add a new valid color format ``(matplotlib_color, alpha)``
----------------------------------------------------------


.. plot::
    :include-source: true

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots()

    rectangle = Rectangle((.2, .2), .6, .6,
                          facecolor=('blue', 0.2),
                          edgecolor=('green', 0.5))
    ax.add_patch(rectangle)


Users can define a color using the new color specification, *(matplotlib_color, alpha)*.
Note that an explicit alpha keyword argument will override an alpha value from
*(matplotlib_color, alpha)*.

The pie chart shadow can be controlled
--------------------------------------

The *shadow* argument to `-.Axes.pie` can now be a dict, allowing more control
of the `.Shadow`-patch used.


``PolyQuadMesh`` is a new class for drawing quadrilateral meshes
----------------------------------------------------------------

`-.Axes.pcolor` previously returned a flattened `.PolyCollection` with only
the valid polygons (unmasked) contained within it. Now, we return a `.PolyQuadMesh`,
which is a mixin incorporating the usefulness of 2D array and mesh coordinates
handling, but still inheriting the draw methods of `.PolyCollection`, which enables
more control over the rendering properties than a normal `.QuadMesh` that is
returned from `-.Axes.pcolormesh`. The new class subclasses `.PolyCollection` and thus
should still behave the same as before. This new class keeps track of the mask for
the user and updates the Polygons that are sent to the renderer appropriately.

.. plot::

    arr = np.arange(12).reshape((3, 4))

    fig, ax = plt.subplots()
    pc = ax.pcolor(arr)

    # Mask one element and show that the hatch is also not drawn
    # over that region
    pc.set_array(np.ma.masked_equal(arr, 5))
    pc.set_hatch('//')

    plt.show()

Shadow shade can be controlled
------------------------------

The `.Shadow` patch now has a *shade* argument to control the shadow darkness.
If 1, the shadow is black, if 0, the shadow has the same color as the patch that
is shadowed. The default value, which earlier was fixed, is 0.7.

``SpinesProxy`` now supports calling the ``set()`` method
---------------------------------------------------------
One can now call e.g. ``ax.spines[:].set(visible=False)``.

Allow setting the tick label fonts with a keyword argument
----------------------------------------------------------
``Axes.tick_params`` now accepts a *labelfontfamily* keyword that changes the tick
label font separately from the rest of the text objects:

.. code-block:: python

    Axis.tick_params(labelfontfamily='monospace')


Figure, Axes, and Legend Layout
===============================

pad_inches="layout" for savefig
-------------------------------

When using constrained or compressed layout,

.. code-block:: python

    savefig(filename, bbox_inches="tight", pad_inches="layout")

will now use the padding sizes defined on the layout engine.

Add a public method to modify the location of ``Legend``
--------------------------------------------------------

`-matplotlib.legend.Legend` locations now can be tweaked after they've been defined.

.. plot::
    :include-source: true

    from matplotlib import pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    x = list(range(-100, 101))
    y = [i**2 for i in x]

    ax.plot(x, y, label="f(x)")
    ax.legend()
    ax.get_legend().set_loc("right")
    # Or
    # ax.get_legend().set(loc="right")

    plt.show()


``rcParams['legend.loc']`` now accepts float-tuple inputs
---------------------------------------------------------

The :rc:`legend.loc` rcParams now accepts float-tuple inputs, same as the *loc* keyword argument to `.Legend`.
This allows users to set the location of the legend in a more flexible and consistent way.

Mathtext improvements
=====================

Boldsymbol mathtext command ``\boldsymbol``
-------------------------------------------

Supports using the ``\boldsymbol{}`` command in mathtext:

To change symbols to bold enclose the text in a font command as
shown:

.. code-block::

    r'$\boldsymbol{a+2+\alpha}$'

.. math::
   \boldsymbol{a+2+\alpha}

``mathtext`` has more sizable delimiters
----------------------------------------

The ``\lgroup`` and ``\rgroup`` sizable delimiters have been added.

The following delimiter names have been supported earlier, but can now be sized with
``\left`` and ``\right``:

* ``\lbrace``, ``\rbrace``, ``\leftbrace``, and ``\rightbrace``
* ``\lbrack`` and ``\rbrack``
* ``\leftparen`` and ``\rightparen``

There are really no obvious advantages in using these.
Instead, they are are added for completeness.

``mathtext`` documentation improvements
---------------------------------------

The documentation is updated to take information directly from the parser. This
means that (almost) all supported symbols, operators etc are shown at :ref:`mathtext`.

``mathtext`` now supports ``\substack``
---------------------------------------

``\substack`` can be used to create multi-line subscripts or superscripts within an equation.

To use it to enclose the math in a substack command as shown:

.. code-block::

    r'$\sum_{\substack{1\leq i\leq 3\\ 1\leq j\leq 5}}$'

.. mathmpl::

    \sum_{\substack{1\leq i\leq 3\\ 1\leq j\leq 5}}



``mathtext`` now supports ``\middle`` delimiter
-----------------------------------------------

The ``\middle`` delimiter has been added, and can now be used with the
``\left`` and ``\right`` delimiters:

To use the middle command enclose it in between the ``\left`` and
``\right`` delimiter command as shown:

.. code-block::

    r'$\left( \frac{a}{b} \middle| q \right)$'

.. mathmpl::

    \left( \frac{a}{b} \middle| q \right)

``mathtext`` operators
----------------------

There has been a number of operators added and corrected when a Unicode font is used.
In addition, correct spacing has been added to a number of the previous operators.
Especially, the characters used for ``\gnapprox``, ``\lnapprox``, ``\leftangle``, and
``\rightangle`` have been corrected.

``mathtext`` spacing corrections
--------------------------------

As consequence of the updated documentation, the spacing on a number of relational and
operator symbols were classified like that and therefore will be spaced properly.

``mathtext`` now supports ``\text``
-----------------------------------

``\text`` can be used to obtain upright text within an equation and to get a plain dash
(-).

.. plot::
    :include-source: true
    :alt: Illustration of the newly added \text command, showing that it renders as normal text, including spaces, despite being part of an equation. Also show that a dash is not rendered as a minus when part of a \text command.

    import matplotlib.pyplot as plt
    plt.text(0.1, 0.5, r"$a = \sin(\phi) \text{ such that } \phi = \frac{x}{y}$")
    plt.text(0.1, 0.3, r"$\text{dashes (-) are retained}$")


Bold-italic mathtext command ``\mathbfit``
------------------------------------------

Supports use of bold-italic font style in mathtext using the ``\mathbfit{}`` command:

To change font to bold and italic enclose the text in a font command as
shown:

.. code-block::

    r'$\mathbfit{\eta \leq C(\delta(\eta))}$

.. math::
   \mathbfit{\eta \leq C(\delta(\eta))}


3D plotting improvements
========================

Specify ticks and axis label positions for 3D plots
---------------------------------------------------

You can now specify the positions of ticks and axis labels for 3D plots.

.. plot::
   :include-source:

   import matplotlib.pyplot as plt

   positions = ['lower', 'upper', 'default', 'both', 'none']
   fig, axs = plt.subplots(2, 3, figsize=(12, 8),
                           subplot_kw={'projection': '3d'})
   for ax, pos in zip(axs.flatten(), positions):
       for axis in ax.xaxis, ax.yaxis, ax.zaxis:
           axis.set_label_position(pos)
           axis.set_ticks_position(pos)
       title = f'position="{pos}"'
       ax.set(xlabel='x', ylabel='y', zlabel='z', title=title)
   axs[1, 2].axis('off')

3D hover coordinates
--------------------

The x, y, z coordinates displayed in 3D plots were previously showing
nonsensical values. This has been fixed to report the coordinate on the view
pane directly beneath the mouse cursor. This is likely to be most useful when
viewing 3D plots along a primary axis direction when using an orthographic
projection, or when a 2D plot has been projected onto one of the 3D axis panes.
Note that there is still no way to directly display the coordinates of plotted
data points.

3D plots can share view angles
------------------------------

3D plots can now share the same view angles, so that when you rotate one plot
the other plots also rotate. This can be done with the *shareview* keyword
argument when adding an axes, or by using the *ax1.shareview(ax2)* method of
existing 3D axes.


Other improvements
==================

macosx: New figures can be opened in either windows or tabs
-----------------------------------------------------------

There is a new :rc:`macosx.window_mode`` rcParam to control how
new figures are opened with the macosx backend. The default is
**system** which uses the system settings, or one can specify either
**tab** or **window** to explicitly choose the mode used to open new figures.

``matplotlib.mpl_toolkits`` is now an implicit namespace package
----------------------------------------------------------------

Following the deprecation of ``pkg_resources.declare_namespace`` in ``setuptools`` 67.3.0,
``matplotlib.mpl_toolkits`` is now implemented as an implicit namespace, following
`PEP 420 <https://peps.python.org/pep-0420/>`_.

Plot Directive now can make responsive images with "srcset"
-----------------------------------------------------------

The plot sphinx directive (``matplotlib.sphinxext.plot_directive``, invoked in
rst as ``.. plot::``) can be configured to automatically make higher res
figures and add these to the the built html docs.  In ``conf.py``::

    extensions = [
    ...
        'matplotlib.sphinxext.plot_directive',
        'matplotlib.sphinxext.figmpl_directive',
    ...]

    plot_srcset = ['2x']

will make png files with double the resolution for hiDPI displays.  Resulting
html files will have image entries like::

    <img src="../_images/nestedpage-index-2.png" style="" srcset="../_images/nestedpage-index-2.png, ../_images/nestedpage-index-2.2x.png 2.00x" alt="" class="plot-directive "/>
