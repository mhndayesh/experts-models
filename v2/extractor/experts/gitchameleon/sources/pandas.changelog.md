
# ===== SOURCE: https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/source/whatsnew/v1.4.0.rst =====

.. _whatsnew_140:

What's new in 1.4.0 (January 22, 2022)
--------------------------------------

These are the changes in pandas 1.4.0. See :ref:`release` for a full changelog
including other versions of pandas.

{{ header }}

.. ---------------------------------------------------------------------------

.. _whatsnew_140.enhancements:

Enhancements
~~~~~~~~~~~~

.. _whatsnew_140.enhancements.warning_lineno:

Improved warning messages
^^^^^^^^^^^^^^^^^^^^^^^^^

Previously, warning messages may have pointed to lines within the pandas
library. Running the script ``setting_with_copy_warning.py``

.. code-block:: python

    import pandas as pd

    df = pd.DataFrame({'a': [1, 2, 3]})
    df[:2].loc[:, 'a'] = 5

with pandas 1.3 resulted in::

    .../site-packages/pandas/core/indexing.py:1951: SettingWithCopyWarning:
    A value is trying to be set on a copy of a slice from a DataFrame.

This made it difficult to determine where the warning was being generated from.
Now pandas will inspect the call stack, reporting the first line outside of the
pandas library that gave rise to the warning. The output of the above script is
now::

    setting_with_copy_warning.py:4: SettingWithCopyWarning:
    A value is trying to be set on a copy of a slice from a DataFrame.




.. _whatsnew_140.enhancements.ExtensionIndex:

Index can hold arbitrary ExtensionArrays
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Until now, passing a custom :class:`ExtensionArray` to ``pd.Index`` would cast
the array to ``object`` dtype. Now :class:`Index` can directly hold arbitrary
ExtensionArrays (:issue:`43930`).

*Previous behavior*:

.. ipython:: python

   arr = pd.array([1, 2, pd.NA])
   idx = pd.Index(arr)

In the old behavior, ``idx`` would be object-dtype:

*Previous behavior*:

.. code-block:: ipython

   In [1]: idx
   Out[1]: Index([1, 2, <NA>], dtype='object')

With the new behavior, we keep the original dtype:

*New behavior*:

.. ipython:: python

   idx

One exception to this is ``SparseArray``, which will continue to cast to numpy
dtype until pandas 2.0. At that point it will retain its dtype like other
ExtensionArrays.

.. _whatsnew_140.enhancements.styler:

Styler
^^^^^^

:class:`.Styler` has been further developed in 1.4.0. The following general enhancements have been made:

  - Styling and formatting of indexes has been added, with :meth:`.Styler.apply_index`, :meth:`.Styler.applymap_index` and :meth:`.Styler.format_index`. These mirror the signature of the methods already used to style and format data values, and work with both HTML, LaTeX and Excel format (:issue:`41893`, :issue:`43101`, :issue:`41993`, :issue:`41995`)
  - The new method :meth:`.Styler.hide` deprecates :meth:`.Styler.hide_index` and :meth:`.Styler.hide_columns` (:issue:`43758`)
  - The keyword arguments ``level`` and ``names`` have been added to :meth:`.Styler.hide` (and implicitly to the deprecated methods :meth:`.Styler.hide_index` and :meth:`.Styler.hide_columns`) for additional control of visibility of MultiIndexes and of Index names (:issue:`25475`, :issue:`43404`, :issue:`43346`)
  - The :meth:`.Styler.export` and :meth:`.Styler.use` have been updated to address all of the added functionality from v1.2.0 and v1.3.0 (:issue:`40675`)
  - Global options under the category ``pd.options.styler`` have been extended to configure default ``Styler`` properties which address formatting, encoding, and HTML and LaTeX rendering. Note that formerly ``Styler`` relied on ``display.html.use_mathjax``, which has now been replaced by ``styler.html.mathjax`` (:issue:`41395`)
  - Validation of certain keyword arguments, e.g. ``caption`` (:issue:`43368`)
  - Various bug fixes as recorded below

Additionally there are specific enhancements to the HTML specific rendering:

  - :meth:`.Styler.bar` introduces additional arguments to control alignment and display (:issue:`26070`, :issue:`36419`), and it also validates the input arguments ``width`` and ``height`` (:issue:`42511`)
  - :meth:`.Styler.to_html` introduces keyword arguments ``sparse_index``, ``sparse_columns``, ``bold_headers``, ``caption``, ``max_rows`` and ``max_columns`` (:issue:`41946`, :issue:`43149`, :issue:`42972`)
  - :meth:`.Styler.to_html` omits CSSStyle rules for hidden table elements as a performance enhancement (:issue:`43619`)
  - Custom CSS classes can now be directly specified without string replacement (:issue:`43686`)
  - Ability to render hyperlinks automatically via a new ``hyperlinks`` formatting keyword argument (:issue:`45058`)

There are also some LaTeX specific enhancements:

  - :meth:`.Styler.to_latex` introduces keyword argument ``environment``, which also allows a specific "longtable" entry through a separate jinja2 template (:issue:`41866`)
  - Naive sparsification is now possible for LaTeX without the necessity of including the multirow package (:issue:`43369`)
  - *cline* support has been added for :class:`MultiIndex` row sparsification through a keyword argument (:issue:`45138`)

.. _whatsnew_140.enhancements.pyarrow_csv_engine:

Multi-threaded CSV reading with a new CSV Engine based on pyarrow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:func:`pandas.read_csv` now accepts ``engine="pyarrow"`` (requires at least
``pyarrow`` 1.0.1) as an argument, allowing for faster csv parsing on multicore
machines with pyarrow installed. See the :doc:`I/O docs </user_guide/io>` for
more info. (:issue:`23697`, :issue:`43706`)

.. _whatsnew_140.enhancements.window_rank:

Rank function for rolling and expanding windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Added ``rank`` function to :class:`Rolling` and :class:`Expanding`. The new
function supports the ``method``, ``ascending``, and ``pct`` flags of
:meth:`DataFrame.rank`. The ``method`` argument supports ``min``, ``max``, and
``average`` ranking methods.
Example:

.. ipython:: python

    s = pd.Series([1, 4, 2, 3, 5, 3])
    s.rolling(3).rank()

    s.rolling(3).rank(method="max")

.. _whatsnew_140.enhancements.groupby_indexing:

Groupby positional indexing
^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is now possible to specify positional ranges relative to the ends of each
group.

Negative arguments for :meth:`.DataFrameGroupBy.head`, :meth:`.SeriesGroupBy.head`, :meth:`.DataFrameGroupBy.tail`, and :meth:`.SeriesGroupBy.tail` now work
correctly and result in ranges relative to the end and start of each group,
respectively. Previously, negative arguments returned empty frames.

.. ipython:: python

    df = pd.DataFrame([["g", "g0"], ["g", "g1"], ["g", "g2"], ["g", "g3"],
                       ["h", "h0"], ["h", "h1"]], columns=["A", "B"])
    df.groupby("A").head(-1)


:meth:`.DataFrameGroupBy.nth` and :meth:`.SeriesGroupBy.nth` now accept a slice or list of integers and slices.

.. ipython:: python

    df.groupby("A").nth(slice(1, -1))
    df.groupby("A").nth([slice(None, 1), slice(-1, None)])

:meth:`.DataFrameGroupBy.nth` and :meth:`.SeriesGroupBy.nth` now accept index notation.

.. ipython:: python

    df.groupby("A").nth[1, -1]
    df.groupby("A").nth[1:-1]
    df.groupby("A").nth[:1, -1:]

.. _whatsnew_140.dict_tight:

DataFrame.from_dict and DataFrame.to_dict have new ``'tight'`` option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A new ``'tight'`` dictionary format that preserves :class:`MultiIndex` entries
and names is now available with the :meth:`DataFrame.from_dict` and
:meth:`DataFrame.to_dict` methods and can be used with the standard ``json``
library to produce a tight representation of :class:`DataFrame` objects
(:issue:`4889`).

.. ipython:: python

    df = pd.DataFrame.from_records(
        [[1, 3], [2, 4]],
        index=pd.MultiIndex.from_tuples([("a", "b"), ("a", "c")],
                                        names=["n1", "n2"]),
        columns=pd.MultiIndex.from_tuples([("x", 1), ("y", 2)],
                                          names=["z1", "z2"]),
    )
    df
    df.to_dict(orient='tight')

.. _whatsnew_140.enhancements.other:

Other enhancements
^^^^^^^^^^^^^^^^^^
- :meth:`concat` will preserve the ``attrs`` when it is the same for all objects and discard the ``attrs`` when they are different (:issue:`41828`)
- :class:`DataFrameGroupBy` operations with ``as_index=False`` now correctly retain ``ExtensionDtype`` dtypes for columns being grouped on (:issue:`41373`)
- Add support for assigning values to ``by`` argument in :meth:`DataFrame.plot.hist` and :meth:`DataFrame.plot.box` (:issue:`15079`)
- :meth:`Series.sample`, :meth:`DataFrame.sample`, :meth:`.DataFrameGroupBy.sample`, and :meth:`.SeriesGroupBy.sample` now accept a ``np.random.Generator`` as input to ``random_state``. A generator will be more performant, especially with ``replace=False`` (:issue:`38100`)
- :meth:`Series.ewm` and :meth:`DataFrame.ewm` now support a ``method`` argument with a ``'table'`` option that performs the windowing operation over an entire :class:`DataFrame`. See :ref:`Window Overview <window.overview>` for performance and functional benefits (:issue:`42273`)
- :meth:`.DataFrameGroupBy.cummin`, :meth:`.SeriesGroupBy.cummin`, :meth:`.DataFrameGroupBy.cummax`, and :meth:`.SeriesGroupBy.cummax` now support the argument ``skipna`` (:issue:`34047`)
- :meth:`read_table` now supports the argument ``storage_options`` (:issue:`39167`)
- :meth:`DataFrame.to_stata` and :meth:`StataWriter` now accept the keyword only argument ``value_labels`` to save labels for non-categorical columns (:issue:`38454`)
- Methods that relied on hashmap based algos such as :meth:`DataFrameGroupBy.value_counts`, :meth:`DataFrameGroupBy.count` and :func:`factorize` ignored imaginary component for complex numbers (:issue:`17927`)
- Add :meth:`Series.str.removeprefix` and :meth:`Series.str.removesuffix` introduced in Python 3.9 to remove pre-/suffixes from string-type :class:`Series` (:issue:`36944`)
- Attempting to write into a file in missing parent directory with :meth:`DataFrame.to_csv`, :meth:`DataFrame.to_html`, :meth:`DataFrame.to_excel`, :meth:`DataFrame.to_feather`, :meth:`DataFrame.to_parquet`, :meth:`DataFrame.to_stata`, :meth:`DataFrame.to_json`, :meth:`DataFrame.to_pickle`, and :meth:`DataFrame.to_xml` now explicitly mentions missing parent directory, the same is true for :class:`Series` counterparts (:issue:`24306`)
- Indexing with ``.loc`` and ``.iloc`` now supports ``Ellipsis`` (:issue:`37750`)
- :meth:`IntegerArray.all` , :meth:`IntegerArray.any`, :meth:`FloatingArray.any`, and :meth:`FloatingArray.all` use Kleene logic (:issue:`41967`)
- Added support for nullable boolean and integer types in :meth:`DataFrame.to_stata`, :class:`~pandas.io.stata.StataWriter`, :class:`~pandas.io.stata.StataWriter117`, and :class:`~pandas.io.stata.StataWriterUTF8` (:issue:`40855`)
- :meth:`DataFrame.__pos__` and :meth:`DataFrame.__neg__` now retain ``ExtensionDtype`` dtypes (:issue:`43883`)
- The error raised when an optional dependency can't be imported now includes the original exception, for easier investigation (:issue:`43882`)
- Added :meth:`.ExponentialMovingWindow.sum` (:issue:`13297`)
- :meth:`Series.str.split` now supports a ``regex`` argument that explicitly specifies whether the pattern is a regular expression. Default is ``None`` (:issue:`43563`, :issue:`32835`, :issue:`25549`)
- :meth:`DataFrame.dropna` now accepts a single label as ``subset`` along with array-like (:issue:`41021`)
- Added :meth:`DataFrameGroupBy.value_counts` (:issue:`43564`)
- :func:`read_csv` now accepts a ``callable`` function in ``on_bad_lines`` when ``engine="python"`` for custom handling of bad lines (:issue:`5686`)
- :class:`ExcelWriter` argument ``if_sheet_exists="overlay"`` option added (:issue:`40231`)
- :meth:`read_excel` now accepts a ``decimal`` argument that allow the user to specify the decimal point when parsing string columns to numeric (:issue:`14403`)
- :meth:`.DataFrameGroupBy.mean`, :meth:`.SeriesGroupBy.mean`, :meth:`.DataFrameGroupBy.std`, :meth:`.SeriesGroupBy.std`, :meth:`.DataFrameGroupBy.var`, :meth:`.SeriesGroupBy.var`, :meth:`.DataFrameGroupBy.sum`, and :meth:`.SeriesGroupBy.sum` now support `Numba <http://numba.pydata.org/>`_ execution with the ``engine`` keyword (:issue:`43731`, :issue:`44862`, :issue:`44939`)
- :meth:`Timestamp.isoformat` now handles the ``timespec`` argument from the base ``datetime`` class (:issue:`26131`)
- :meth:`NaT.to_numpy` ``dtype`` argument is now respected, so ``np.timedelta64`` can be returned (:issue:`44460`)
- New option ``display.max_dir_items`` customizes the number of columns added to :meth:`Dataframe.__dir__` and suggested for tab completion (:issue:`37996`)
- Added "Juneteenth National Independence Day" to ``USFederalHolidayCalendar`` (:issue:`44574`)
- :meth:`.Rolling.var`, :meth:`.Expanding.var`, :meth:`.Rolling.std`, and :meth:`.Expanding.std` now support `Numba <http://numba.pydata.org/>`_ execution with the ``engine`` keyword (:issue:`44461`)
- :meth:`Series.info` has been added, for compatibility with :meth:`DataFrame.info` (:issue:`5167`)
- Implemented :meth:`IntervalArray.min` and :meth:`IntervalArray.max`, as a result of which ``min`` and ``max`` now work for :class:`IntervalIndex`, :class:`Series` and :class:`DataFrame` with ``IntervalDtype`` (:issue:`44746`)
- :meth:`UInt64Index.map` now retains ``dtype`` where possible (:issue:`44609`)
- :meth:`read_json` can now parse unsigned long long integers (:issue:`26068`)
- :meth:`DataFrame.take` now raises a ``TypeError`` when passed a scalar for the indexer (:issue:`42875`)
- :meth:`is_list_like` now identifies duck-arrays as list-like unless ``.ndim == 0`` (:issue:`35131`)
- :class:`ExtensionDtype` and :class:`ExtensionArray` are now (de)serialized when exporting a :class:`DataFrame` with :meth:`DataFrame.to_json` using ``orient='table'`` (:issue:`20612`, :issue:`44705`)
- Add support for `Zstandard <http://facebook.github.io/zstd/>`_ compression to :meth:`DataFrame.to_pickle`/:meth:`read_pickle` and friends (:issue:`43925`)
- :meth:`DataFrame.to_sql` now returns an ``int`` of the number of written rows (:issue:`23998`)

.. ---------------------------------------------------------------------------

.. _whatsnew_140.notable_bug_fixes:

Notable bug fixes
~~~~~~~~~~~~~~~~~

These are bug fixes that might have notable behavior changes.

.. _whatsnew_140.notable_bug_fixes.inconsistent_date_string_parsing:

Inconsistent date string parsing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``dayfirst`` option of :func:`to_datetime` isn't strict, and this can lead
to surprising behavior:

.. ipython:: python
    :okwarning:

    pd.to_datetime(["31-12-2021"], dayfirst=False)

Now, a warning will be raised if a date string cannot be parsed accordance to
the given ``dayfirst`` value when the value is a delimited date string (e.g.
``31-12-2012``).

.. _whatsnew_140.notable_bug_fixes.concat_with_empty_or_all_na:

Ignoring dtypes in concat with empty or all-NA columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This behaviour change has been reverted in pandas 1.4.3.

When using :func:`concat` to concatenate two or more :class:`DataFrame` objects,
if one of the DataFrames was empty or had all-NA values, its dtype was
*sometimes* ignored when finding the concatenated dtype.  These are now
consistently *not* ignored (:issue:`43507`).

.. code-block:: ipython

    In [3]: df1 = pd.DataFrame({"bar": [pd.Timestamp("2013-01-01")]}, index=range(1))
    In [4]: df2 = pd.DataFrame({"bar": np.nan}, index=range(1, 2))
    In [5]: res = pd.concat([df1, df2])

Previously, the float-dtype in ``df2`` would be ignored so the result dtype
would be ``datetime64[ns]``. As a result, the ``np.nan`` would be cast to
``NaT``.

*Previous behavior*:

.. code-block:: ipython

    In [6]: res
    Out[6]:
             bar
    0 2013-01-01
    1        NaT

Now the float-dtype is respected. Since the common dtype for these DataFrames is
object, the ``np.nan`` is retained.

*New behavior*:

.. code-block:: ipython

    In [6]: res
    Out[6]:
                       bar
    0  2013-01-01 00:00:00
    1                  NaN



.. _whatsnew_140.notable_bug_fixes.value_counts_and_mode_do_not_coerce_to_nan:

Null-values are no longer coerced to NaN-value in value_counts and mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:meth:`Series.value_counts` and :meth:`Series.mode` no longer coerce ``None``,
``NaT`` and other null-values to a NaN-value for ``np.object_``-dtype. This
behavior is now consistent with ``unique``, ``isin`` and others
(:issue:`42688`).

.. ipython:: python

    s = pd.Series([True, None, pd.NaT, None, pd.NaT, None])
    res = s.value_counts(dropna=False)

Previously, all null-values were replaced by a NaN-value.

*Previous behavior*:

.. code-block:: ipython

    In [3]: res
    Out[3]:
    NaN     5
    True    1
    dtype: int64

Now null-values are no longer mangled.

*New behavior*:

.. ipython:: python

    res

.. _whatsnew_140.notable_bug_fixes.read_csv_mangle_dup_cols:

mangle_dupe_cols in read_csv no longer renames unique columns conflicting with target names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:func:`read_csv` no longer renames unique column labels which conflict with the target
names of duplicated columns. Already existing columns are skipped, i.e. the next
available index is used for the target column name (:issue:`14704`).

.. ipython:: python

    import io

    data = "a,a,a.1\n1,2,3"
    res = pd.read_csv(io.StringIO(data))

Previously, the second column was called ``a.1``, while the third column was
also renamed to ``a.1.1``.

*Previous behavior*:

.. code-block:: ipython

    In [3]: res
    Out[3]:
        a  a.1  a.1.1
    0   1    2      3

Now the renaming checks if ``a.1`` already exists when changing the name of the
second column and jumps this index. The second column is instead renamed to
``a.2``.

*New behavior*:

.. ipython:: python

    res

.. _whatsnew_140.notable_bug_fixes.unstack_pivot_int32_limit:

unstack and pivot_table no longer raises ValueError for result that would exceed int32 limit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Previously :meth:`DataFrame.pivot_table` and :meth:`DataFrame.unstack` would
raise a ``ValueError`` if the operation could produce a result with more than
``2**31 - 1`` elements. This operation now raises a
:class:`errors.PerformanceWarning` instead (:issue:`26314`).

*Previous behavior*:

.. code-block:: ipython

    In [3]: df = DataFrame({"ind1": np.arange(2 ** 16), "ind2": np.arange(2 ** 16), "count": 0})
    In [4]: df.pivot_table(index="ind1", columns="ind2", values="count", aggfunc="count")
    ValueError: Unstacked DataFrame is too big, causing int32 overflow

*New behavior*:

.. code-block:: python

    In [4]: df.pivot_table(index="ind1", columns="ind2", values="count", aggfunc="count")
    PerformanceWarning: The following operation may generate 4294967296 cells in the resulting pandas object.

.. ---------------------------------------------------------------------------

.. _whatsnew_140.notable_bug_fixes.groupby_apply_mutation:

groupby.apply consistent transform detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:meth:`.DataFrameGroupBy.apply` and :meth:`.SeriesGroupBy.apply` are designed to be flexible, allowing users to perform
aggregations, transformations, filters, and use it with user-defined functions
that might not fall into any of these categories. As part of this, apply will
attempt to detect when an operation is a transform, and in such a case, the
result will have the same index as the input. In order to determine if the
operation is a transform, pandas compares the input's index to the result's and
determines if it has been mutated. Previously in pandas 1.3, different code
paths used different definitions of "mutated": some would use Python's ``is``
whereas others would test only up to equality.

This inconsistency has been removed, pandas now tests up to equality.

.. ipython:: python

    def func(x):
        return x.copy()

    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4], 'c': [5, 6]})
    df

*Previous behavior*:

.. code-block:: ipython

    In [3]: df.groupby(['a']).apply(func)
    Out[3]:
         a  b  c
    a
    1 0  1  3  5
    2 1  2  4  6

    In [4]: df.set_index(['a', 'b']).groupby(['a']).apply(func)
    Out[4]:
         c
    a b
    1 3  5
    2 4  6

In the examples above, the first uses a code path where pandas uses ``is`` and
determines that ``func`` is not a transform whereas the second tests up to
equality and determines that ``func`` is a transform. In the first case, the
result's index is not the same as the input's.

*New behavior*:

.. code-block:: ipython

    In [5]: df.groupby(['a']).apply(func)
    Out[5]:
       a  b  c
    0  1  3  5
    1  2  4  6

    In [6]: df.set_index(['a', 'b']).groupby(['a']).apply(func)
    Out[6]:
         c
    a b
    1 3  5
    2 4  6

Now in both cases it is determined that ``func`` is a transform. In each case,
the result has the same index as the input.

.. _whatsnew_140.api_breaking:

Backwards incompatible API changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _whatsnew_140.api_breaking.python:

Increased minimum version for Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

pandas 1.4.0 supports Python 3.8 and higher.

.. _whatsnew_140.api_breaking.deps:

Increased minimum versions for dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Some minimum supported versions of dependencies were updated.
If installed, we now require:

+-----------------+-----------------+----------+---------+
| Package         | Minimum Version | Required | Changed |
+=================+=================+==========+=========+
| numpy           | 1.18.5          |    X     |    X    |
+-----------------+-----------------+----------+---------+
| pytz            | 2020.1          |    X     |    X    |
+-----------------+-----------------+----------+---------+
| python-dateutil | 2.8.1           |    X     |    X    |
+-----------------+-----------------+----------+---------+
| bottleneck      | 1.3.1           |          |    X    |
+-----------------+-----------------+----------+---------+
| numexpr         | 2.7.1           |          |    X    |
+-----------------+-----------------+----------+---------+
| pytest (dev)    | 6.0             |          |         |
+-----------------+-----------------+----------+---------+
| mypy (dev)      | 0.930           |          |    X    |
+-----------------+-----------------+----------+---------+

For `optional libraries
<https://pandas.pydata.org/docs/getting_started/install.html>`_ the general
recommendation is to use the latest version. The following table lists the
lowest version per library that is currently being tested throughout the
development of pandas. Optional libraries below the lowest tested version may
still work, but are not considered supported.

+-----------------+-----------------+---------+
| Package         | Minimum Version | Changed |
+=================+=================+=========+
| beautifulsoup4  | 4.8.2           |    X    |
+-----------------+-----------------+---------+
| fastparquet     | 0.4.0           |         |
+-----------------+-----------------+---------+
| fsspec          | 0.7.4           |         |
+-----------------+-----------------+---------+
| gcsfs           | 0.6.0           |         |
+-----------------+-----------------+---------+
| lxml            | 4.5.0           |    X    |
+-----------------+-----------------+---------+
| matplotlib      | 3.3.2           |    X    |
+-----------------+-----------------+---------+
| numba           | 0.50.1          |    X    |
+-----------------+-----------------+---------+
| openpyxl        | 3.0.3           |    X    |
+-----------------+-----------------+---------+
| pandas-gbq      | 0.14.0          |    X    |
+-----------------+-----------------+---------+
| pyarrow         | 1.0.1           |    X    |
+-----------------+-----------------+---------+
| pymysql         | 0.10.1          |    X    |
+-----------------+-----------------+---------+
| pytables        | 3.6.1           |    X    |
+-----------------+-----------------+---------+
| s3fs            | 0.4.0           |         |
+-----------------+-----------------+---------+
| scipy           | 1.4.1           |    X    |
+-----------------+-----------------+---------+
| sqlalchemy      | 1.4.0           |    X    |
+-----------------+-----------------+---------+
| tabulate        | 0.8.7           |         |
+-----------------+-----------------+---------+
| xarray          | 0.15.1          |    X    |
+-----------------+-----------------+---------+
| xlrd            | 2.0.1           |    X    |
+-----------------+-----------------+---------+
| xlsxwriter      | 1.2.2           |    X    |
+-----------------+-----------------+---------+
| xlwt            | 1.3.0           |         |
+-----------------+-----------------+---------+

See :ref:`install.dependencies` and :ref:`install.optional_dependencies` for more.

.. _whatsnew_140.api_breaking.other:

Other API changes
^^^^^^^^^^^^^^^^^
- :meth:`Index.get_indexer_for` no longer accepts keyword arguments (other than ``target``); in the past these would be silently ignored if the index was not unique (:issue:`42310`)
- Change in the position of the ``min_rows`` argument in :meth:`DataFrame.to_string` due to change in the docstring (:issue:`44304`)
- Reduction operations for :class:`DataFrame` or :class:`Series` now raising a ``ValueError`` when ``None`` is passed for ``skipna`` (:issue:`44178`)
- :func:`read_csv` and :func:`read_html` no longer raising an error when one of the header rows consists only of ``Unnamed:`` columns (:issue:`13054`)
- Changed the ``name`` attribute of several holidays in
  ``USFederalHolidayCalendar`` to match `official federal holiday
  names <https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/>`_
  specifically:

   - "New Year's Day" gains the possessive apostrophe
   - "Presidents Day" becomes "Washington's Birthday"
   - "Martin Luther King Jr. Day" is now "Birthday of Martin Luther King, Jr."
   - "July 4th" is now "Independence Day"
   - "Thanksgiving" is now "Thanksgiving Day"
   - "Christmas" is now "Christmas Day"
   - Added "Juneteenth National Independence Day"

.. ---------------------------------------------------------------------------

.. _whatsnew_140.deprecations:

Deprecations
~~~~~~~~~~~~

.. _whatsnew_140.deprecations.int64_uint64_float64index:

Deprecated Int64Index, UInt64Index & Float64Index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`Int64Index`, :class:`UInt64Index` and :class:`Float64Index` have been
deprecated in favor of the base :class:`Index` class and will be removed in
pandas 2.0 (:issue:`43028`).

For constructing a numeric index, you can use the base :class:`Index` class
instead specifying the data type (which will also work on older pandas
releases):

.. code-block:: python

    # replace
    pd.Int64Index([1, 2, 3])
    # with
    pd.Index([1, 2, 3], dtype="int64")

For checking the data type of an index object, you can replace ``isinstance``
checks with checking the ``dtype``:

.. code-block:: python

    # replace
    isinstance(idx, pd.Int64Index)
    # with
    idx.dtype == "int64"

Currently, in order to maintain backward compatibility, calls to :class:`Index`
will continue to return :class:`Int64Index`, :class:`UInt64Index` and
:class:`Float64Index` when given numeric data, but in the future, an
:class:`Index` will be returned.

*Current behavior*:

.. code-block:: ipython

    In [1]: pd.Index([1, 2, 3], dtype="int32")
    Out [1]: Int64Index([1, 2, 3], dtype='int64')
    In [1]: pd.Index([1, 2, 3], dtype="uint64")
    Out [1]: UInt64Index([1, 2, 3], dtype='uint64')

*Future behavior*:

.. code-block:: ipython

    In [3]: pd.Index([1, 2, 3], dtype="int32")
    Out [3]: Index([1, 2, 3], dtype='int32')
    In [4]: pd.Index([1, 2, 3], dtype="uint64")
    Out [4]: Index([1, 2, 3], dtype='uint64')


.. _whatsnew_140.deprecations.frame_series_append:

Deprecated DataFrame.append and Series.append
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:meth:`DataFrame.append` and :meth:`Series.append` have been deprecated and will
be removed in a future version. Use :func:`pandas.concat` instead (:issue:`35407`).

*Deprecated syntax*

.. code-block:: ipython

    In [1]: pd.Series([1, 2]).append(pd.Series([3, 4]))
    Out [1]:
    <stdin>:1: FutureWarning: The series.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
    0    1
    1    2
    0    3
    1    4
    dtype: int64

    In [2]: df1 = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
    In [3]: df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
    In [4]: df1.append(df2)
    Out [4]:
    <stdin>:1: FutureWarning: The series.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
       A  B
    0  1  2
    1  3  4
    0  5  6
    1  7  8

*Recommended syntax*

.. ipython:: python

    pd.concat([pd.Series([1, 2]), pd.Series([3, 4])])

    df1 = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
    df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
    pd.concat([df1, df2])


.. _whatsnew_140.deprecations.other:

Other Deprecations
^^^^^^^^^^^^^^^^^^
- Deprecated :meth:`Index.is_type_compatible` (:issue:`42113`)
- Deprecated ``method`` argument in :meth:`Index.get_loc`, use ``index.get_indexer([label], method=...)`` instead (:issue:`42269`)
- Deprecated treating integer keys in :meth:`Series.__setitem__` as positional when the index is a :class:`Float64Index` not containing the key, a :class:`IntervalIndex` with no entries containing the key, or a :class:`MultiIndex` with leading :class:`Float64Index` level not containing the key (:issue:`33469`)
- Deprecated treating ``numpy.datetime64`` objects as UTC times when passed to the :class:`Timestamp` constructor along with a timezone. In a future version, these will be treated as wall-times. To retain the old behavior, use ``Timestamp(dt64).tz_localize("UTC").tz_convert(tz)`` (:issue:`24559`)
- Deprecated ignoring missing labels when indexing with a sequence of labels on a level of a :class:`MultiIndex` (:issue:`42351`)
- Creating an empty :class:`Series` without a ``dtype`` will now raise a more visible ``FutureWarning`` instead of a ``DeprecationWarning`` (:issue:`30017`)
- Deprecated the ``kind`` argument in :meth:`Index.get_slice_bound`, :meth:`Index.slice_indexer`, and :meth:`Index.slice_locs`; in a future version passing ``kind`` will raise (:issue:`42857`)
- Deprecated dropping of nuisance columns in :class:`Rolling`, :class:`Expanding`, and :class:`EWM` aggregations (:issue:`42738`)
- Deprecated :meth:`Index.reindex` with a non-unique :class:`Index` (:issue:`42568`)
- Deprecated :meth:`.Styler.render` in favor of :meth:`.Styler.to_html` (:issue:`42140`)
- Deprecated :meth:`.Styler.hide_index` and :meth:`.Styler.hide_columns` in favor of :meth:`.Styler.hide` (:issue:`43758`)
- Deprecated passing in a string column label into ``times`` in :meth:`DataFrame.ewm` (:issue:`43265`)
- Deprecated the ``include_start`` and ``include_end`` arguments in :meth:`DataFrame.between_time`; in a future version passing ``include_start`` or ``include_end`` will raise (:issue:`40245`)
- Deprecated the ``squeeze`` argument to :meth:`read_csv`, :meth:`read_table`, and :meth:`read_excel`. Users should squeeze the :class:`DataFrame` afterwards with ``.squeeze("columns")`` instead (:issue:`43242`)
- Deprecated the ``index`` argument to :class:`SparseArray` construction (:issue:`23089`)
- Deprecated the ``closed`` argument in :meth:`date_range` and :meth:`bdate_range` in favor of ``inclusive`` argument; In a future version passing ``closed`` will raise (:issue:`40245`)
- Deprecated :meth:`.Rolling.validate`, :meth:`.Expanding.validate`, and :meth:`.ExponentialMovingWindow.validate` (:issue:`43665`)
- Deprecated silent dropping of columns that raised a ``TypeError`` in :class:`Series.transform` and :class:`DataFrame.transform` when used with a dictionary (:issue:`43740`)
- Deprecated silent dropping of columns that raised a ``TypeError``, ``DataError``, and some cases of ``ValueError`` in :meth:`Series.aggregate`, :meth:`DataFrame.aggregate`, :meth:`Series.groupby.aggregate`, and :meth:`DataFrame.groupby.aggregate` when used with a list (:issue:`43740`)
- Deprecated casting behavior when setting timezone-aware value(s) into a timezone-aware :class:`Series` or :class:`DataFrame` column when the timezones do not match. Previously this cast to object dtype. In a future version, the values being inserted will be converted to the series or column's existing timezone (:issue:`37605`)
- Deprecated casting behavior when passing an item with mismatched-timezone to :meth:`DatetimeIndex.insert`, :meth:`DatetimeIndex.putmask`, :meth:`DatetimeIndex.where` :meth:`DatetimeIndex.fillna`, :meth:`Series.mask`, :meth:`Series.where`, :meth:`Series.fillna`, :meth:`Series.shift`, :meth:`Series.replace`, :meth:`Series.reindex` (and :class:`DataFrame` column analogues). In the past this has cast to object ``dtype``. In a future version, these will cast the passed item to the index or series's timezone (:issue:`37605`, :issue:`44940`)
- Deprecated the ``prefix`` keyword argument in :func:`read_csv` and :func:`read_table`, in a future version the argument will be removed (:issue:`43396`)
- Deprecated passing non boolean argument to ``sort`` in :func:`concat` (:issue:`41518`)
- Deprecated passing arguments as positional for :func:`read_fwf` other than ``filepath_or_buffer`` (:issue:`41485`)
- Deprecated passing arguments as positional for :func:`read_xml` other than ``path_or_buffer`` (:issue:`45133`)
- Deprecated passing ``skipna=None`` for :meth:`DataFrame.mad` and :meth:`Series.mad`, pass ``skipna=True`` instead (:issue:`44580`)
- Deprecated the behavior of :func:`to_datetime` with the string "now" with ``utc=False``; in a future version this will match ``Timestamp("now")``, which in turn matches :meth:`Timestamp.now` returning the local time (:issue:`18705`)
- Deprecated :meth:`DateOffset.apply`, use ``offset + other`` instead (:issue:`44522`)
- Deprecated parameter ``names`` in :meth:`Index.copy` (:issue:`44916`)
- A deprecation warning is now shown for :meth:`DataFrame.to_latex` indicating the arguments signature may change and emulate more the arguments to :meth:`.Styler.to_latex` in future versions (:issue:`44411`)
- Deprecated behavior of :func:`concat` between objects with bool-dtype and numeric-dtypes; in a future version these will cast to object dtype instead of coercing bools to numeric values (:issue:`39817`)
- Deprecated :meth:`Categorical.replace`, use :meth:`Series.replace` instead (:issue:`44929`)
- Deprecated passing ``set`` or ``dict`` as indexer for :meth:`DataFrame.loc.__setitem__`, :meth:`DataFrame.loc.__getitem__`, :meth:`Series.loc.__setitem__`, :meth:`Series.loc.__getitem__`, :meth:`DataFrame.__getitem__`, :meth:`Series.__getitem__` and :meth:`Series.__setitem__` (:issue:`42825`)
- Deprecated :meth:`Index.__getitem__` with a bool key; use ``index.values[key]`` to get the old behavior (:issue:`44051`)
- Deprecated downcasting column-by-column in :meth:`DataFrame.where` with integer-dtypes (:issue:`44597`)
- Deprecated :meth:`DatetimeIndex.union_many`, use :meth:`DatetimeIndex.union` instead (:issue:`44091`)
- Deprecated :meth:`.Groupby.pad` in favor of :meth:`.Groupby.ffill` (:issue:`33396`)
- Deprecated :meth:`.Groupby.backfill` in favor of :meth:`.Groupby.bfill` (:issue:`33396`)
- Deprecated :meth:`.Resample.pad` in favor of :meth:`.Resample.ffill` (:issue:`33396`)
- Deprecated :meth:`.Resample.backfill` in favor of :meth:`.Resample.bfill` (:issue:`33396`)
- Deprecated ``numeric_only=None`` in :meth:`DataFrame.rank`; in a future version ``numeric_only`` must be either ``True`` or ``False`` (the default) (:issue:`45036`)
- Deprecated the behavior of :meth:`Timestamp.utcfromtimestamp`, in the future it will return a timezone-aware UTC :class:`Timestamp` (:issue:`22451`)
- Deprecated :meth:`NaT.freq` (:issue:`45071`)
- Deprecated behavior of :class:`Series` and :class:`DataFrame` construction when passed float-dtype data containing ``NaN`` and an integer dtype ignoring the dtype argument; in a future version this will raise (:issue:`40110`)
- Deprecated the behaviour of :meth:`Series.to_frame` and :meth:`Index.to_frame` to ignore the ``name`` argument when ``name=None``. Currently, this means to preserve the existing name, but in the future explicitly passing ``name=None`` will set ``None`` as the name of the column in the resulting DataFrame (:issue:`44212`)

.. ---------------------------------------------------------------------------

.. _whatsnew_140.performance:

Performance improvements
~~~~~~~~~~~~~~~~~~~~~~~~
- Performance improvement in :meth:`.DataFrameGroupBy.sample` and :meth:`.SeriesGroupBy.sample`, especially when ``weights`` argument provided (:issue:`34483`)
- Performance improvement when converting non-string arrays to string arrays (:issue:`34483`)
- Performance improvement in :meth:`.DataFrameGroupBy.transform` and :meth:`.SeriesGroupBy.transform` for user-defined functions (:issue:`41598`)
- Performance improvement in constructing :class:`DataFrame` objects (:issue:`42631`, :issue:`43142`, :issue:`43147`, :issue:`43307`, :issue:`43144`, :issue:`44826`)
- Performance improvement in :meth:`.DataFrameGroupBy.shift` and :meth:`.SeriesGroupBy.shift` when ``fill_value`` argument is provided (:issue:`26615`)
- Performance improvement in :meth:`DataFrame.corr` for ``method=pearson`` on data without missing values (:issue:`40956`)
- Performance improvement in some :meth:`.DataFrameGroupBy.apply` and :meth:`.SeriesGroupBy.apply` operations (:issue:`42992`, :issue:`43578`)
- Performance improvement in :func:`read_stata` (:issue:`43059`, :issue:`43227`)
- Performance improvement in :func:`read_sas` (:issue:`43333`)
- Performance improvement in :meth:`to_datetime` with ``uint`` dtypes (:issue:`42606`)
- Performance improvement in :meth:`to_datetime` with ``infer_datetime_format`` set to ``True`` (:issue:`43901`)
- Performance improvement in :meth:`Series.sparse.to_coo` (:issue:`42880`)
- Performance improvement in indexing with a :class:`UInt64Index` (:issue:`43862`)
- Performance improvement in indexing with a :class:`Float64Index` (:issue:`43705`)
- Performance improvement in indexing with a non-unique :class:`Index` (:issue:`43792`)
- Performance improvement in indexing with a listlike indexer on a :class:`MultiIndex` (:issue:`43370`)
- Performance improvement in indexing with a :class:`MultiIndex` indexer on another :class:`MultiIndex` (:issue:`43370`)
- Performance improvement in :meth:`.DataFrameGroupBy.quantile` and :meth:`.SeriesGroupBy.quantile` (:issue:`43469`, :issue:`43725`)
- Performance improvement in :meth:`.DataFrameGroupBy.count` and :meth:`.SeriesGroupBy.count` (:issue:`43730`, :issue:`43694`)
- Performance improvement in :meth:`.DataFrameGroupBy.any`, :meth:`.SeriesGroupBy.any`, :meth:`.DataFrameGroupBy.all`, and :meth:`.SeriesGroupBy.all` (:issue:`43675`, :issue:`42841`)
- Performance improvement in :meth:`.DataFrameGroupBy.std` and :meth:`.SeriesGroupBy.std` (:issue:`43115`, :issue:`43576`)
- Performance improvement in :meth:`.DataFrameGroupBy.cumsum` and :meth:`.SeriesGroupBy.cumsum` (:issue:`43309`)
- :meth:`SparseArray.min` and :meth:`SparseArray.max` no longer require converting to a dense array (:issue:`43526`)
- Indexing into a :class:`SparseArray` with a ``slice`` with ``step=1`` no longer requires converting to a dense array (:issue:`43777`)
- Performance improvement in :meth:`SparseArray.take` with ``allow_fill=False`` (:issue:`43654`)
- Performance improvement in :meth:`.Rolling.mean`, :meth:`.Expanding.mean`, :meth:`.Rolling.sum`, :meth:`.Expanding.sum`, :meth:`.Rolling.max`, :meth:`.Expanding.max`, :meth:`.Rolling.min` and :meth:`.Expanding.min` with ``engine="numba"`` (:issue:`43612`, :issue:`44176`, :issue:`45170`)
- Improved performance of :meth:`pandas.read_csv` with ``memory_map=True`` when file encoding is UTF-8 (:issue:`43787`)
- Performance improvement in :meth:`RangeIndex.sort_values` overriding :meth:`Index.sort_values` (:issue:`43666`)
- Performance improvement in :meth:`RangeIndex.insert` (:issue:`43988`)
- Performance improvement in :meth:`Index.insert` (:issue:`43953`)
- Performance improvement in :meth:`DatetimeIndex.tolist` (:issue:`43823`)
- Performance improvement in :meth:`DatetimeIndex.union` (:issue:`42353`)
- Performance improvement in :meth:`Series.nsmallest` (:issue:`43696`)
- Performance improvement in :meth:`DataFrame.insert` (:issue:`42998`)
- Performance improvement in :meth:`DataFrame.dropna` (:issue:`43683`)
- Performance improvement in :meth:`DataFrame.fillna` (:issue:`43316`)
- Performance improvement in :meth:`DataFrame.values` (:issue:`43160`)
- Performance improvement in :meth:`DataFrame.select_dtypes` (:issue:`42611`)
- Performance improvement in :class:`DataFrame` reductions (:issue:`43185`, :issue:`43243`, :issue:`43311`, :issue:`43609`)
- Performance improvement in :meth:`Series.unstack` and :meth:`DataFrame.unstack` (:issue:`43335`, :issue:`43352`, :issue:`42704`, :issue:`43025`)
- Performance improvement in :meth:`Series.to_frame` (:issue:`43558`)
- Performance improvement in :meth:`Series.mad` (:issue:`43010`)
- Performance improvement in :func:`merge` (:issue:`43332`)
- Performance improvement in :func:`to_csv` when index column is a datetime and is formatted (:issue:`39413`)
- Performance improvement in :func:`to_csv` when :class:`MultiIndex` contains a lot of unused levels (:issue:`37484`)
- Performance improvement in :func:`read_csv` when ``index_col`` was set with a numeric column (:issue:`44158`)
- Performance improvement in :func:`concat` (:issue:`43354`)
- Performance improvement in :meth:`SparseArray.__getitem__` (:issue:`23122`)
- Performance improvement in constructing a :class:`DataFrame` from array-like objects like a ``Pytorch`` tensor (:issue:`44616`)

.. ---------------------------------------------------------------------------

.. _whatsnew_140.bug_fixes:

Bug fixes
~~~~~~~~~

Categorical
^^^^^^^^^^^
- Bug in setting dtype-incompatible values into a :class:`Categorical` (or ``Series`` or ``DataFrame`` backed by ``Categorical``) raising ``ValueError`` instead of ``TypeError`` (:issue:`41919`)
- Bug in :meth:`Categorical.searchsorted` when passing a dtype-incompatible value raising ``KeyError`` instead of ``TypeError`` (:issue:`41919`)
- Bug in :meth:`Categorical.astype` casting datetimes and :class:`Timestamp` to int for dtype ``object`` (:issue:`44930`)
- Bug in :meth:`Series.where` with ``CategoricalDtype`` when passing a dtype-incompatible value raising ``ValueError`` instead of ``TypeError`` (:issue:`41919`)
- Bug in :meth:`Categorical.fillna` when passing a dtype-incompatible value raising ``ValueError`` instead of ``TypeError`` (:issue:`41919`)
- Bug in :meth:`Categorical.fillna` with a tuple-like category raising ``ValueError`` instead of ``TypeError`` when filling with a non-category tuple (:issue:`41919`)

Datetimelike
^^^^^^^^^^^^
- Bug in :class:`DataFrame` constructor unnecessarily copying non-datetimelike 2D object arrays (:issue:`39272`)
- Bug in :func:`to_datetime` with ``format`` and ``pandas.NA`` was raising ``ValueError`` (:issue:`42957`)
- :func:`to_datetime` would silently swap ``MM/DD/YYYY`` and ``DD/MM/YYYY`` formats if the given ``dayfirst`` option could not be respected - now, a warning is raised in the case of delimited date strings (e.g. ``31-12-2012``) (:issue:`12585`)
- Bug in :meth:`date_range` and :meth:`bdate_range` do not return right bound when ``start`` = ``end`` and set is closed on one side (:issue:`43394`)
- Bug in inplace addition and subtraction of :class:`DatetimeIndex` or :class:`TimedeltaIndex` with :class:`DatetimeArray` or :class:`TimedeltaArray` (:issue:`43904`)
- Bug in calling ``np.isnan``, ``np.isfinite``, or ``np.isinf`` on a timezone-aware :class:`DatetimeIndex` incorrectly raising ``TypeError`` (:issue:`43917`)
- Bug in constructing a :class:`Series` from datetime-like strings with mixed timezones incorrectly partially-inferring datetime values (:issue:`40111`)
- Bug in addition of a :class:`Tick` object and a ``np.timedelta64`` object incorrectly raising instead of returning :class:`Timedelta` (:issue:`44474`)
- ``np.maximum.reduce`` and ``np.minimum.reduce`` now correctly return :class:`Timestamp` and :class:`Timedelta` objects when operating on :class:`Series`, :class:`DataFrame`, or :class:`Index` with ``datetime64[ns]`` or ``timedelta64[ns]`` dtype (:issue:`43923`)
- Bug in adding a ``np.timedelta64`` object to a :class:`BusinessDay` or :class:`CustomBusinessDay` object incorrectly raising (:issue:`44532`)
- Bug in :meth:`Index.insert` for inserting ``np.datetime64``, ``np.timedelta64`` or ``tuple`` into :class:`Index` with ``dtype='object'`` with negative loc adding ``None`` and replacing existing value (:issue:`44509`)
- Bug in :meth:`Timestamp.to_pydatetime` failing to retain the ``fold`` attribute (:issue:`45087`)
- Bug in :meth:`Series.mode` with ``DatetimeTZDtype`` incorrectly returning timezone-naive and ``PeriodDtype`` incorrectly raising (:issue:`41927`)
- Fixed regression in :meth:`~Series.reindex` raising an error when using an incompatible fill value with a datetime-like dtype (or not raising a deprecation warning for using a ``datetime.date`` as fill value) (:issue:`42921`)
- Bug in :class:`DateOffset` addition with :class:`Timestamp` where ``offset.nanoseconds`` would not be included in the result (:issue:`43968`, :issue:`36589`)
- Bug in :meth:`Timestamp.fromtimestamp` not supporting the ``tz`` argument (:issue:`45083`)
- Bug in :class:`DataFrame` construction from dict of :class:`Series` with mismatched index dtypes sometimes raising depending on the ordering of the passed dict (:issue:`44091`)
- Bug in :class:`Timestamp` hashing during some DST transitions caused a segmentation fault (:issue:`33931` and :issue:`40817`)

Timedelta
^^^^^^^^^
- Bug in division of all-``NaT`` :class:`TimeDeltaIndex`, :class:`Series` or :class:`DataFrame` column with object-dtype array like of numbers failing to infer the result as timedelta64-dtype (:issue:`39750`)
- Bug in floor division of ``timedelta64[ns]`` data with a scalar returning garbage values (:issue:`44466`)
- Bug in :class:`Timedelta` now properly taking into account any nanoseconds contribution of any kwarg (:issue:`43764`, :issue:`45227`)

Time Zones
^^^^^^^^^^
- Bug in :func:`to_datetime` with ``infer_datetime_format=True`` failing to parse zero UTC offset (``Z``) correctly (:issue:`41047`)
- Bug in :meth:`Series.dt.tz_convert` resetting index in a :class:`Series` with :class:`CategoricalIndex` (:issue:`43080`)
- Bug in ``Timestamp`` and ``DatetimeIndex`` incorrectly raising a ``TypeError`` when subtracting two timezone-aware objects with mismatched timezones (:issue:`31793`)

Numeric
^^^^^^^
- Bug in floor-dividing a list or tuple of integers by a :class:`Series` incorrectly raising (:issue:`44674`)
- Bug in :meth:`DataFrame.rank` raising ``ValueError`` with ``object`` columns and ``method="first"`` (:issue:`41931`)
- Bug in :meth:`DataFrame.rank` treating missing values and extreme values as equal (for example ``np.nan`` and ``np.inf``), causing incorrect results when ``na_option="bottom"`` or ``na_option="top`` used (:issue:`41931`)
- Bug in ``numexpr`` engine still being used when the option ``compute.use_numexpr`` is set to ``False`` (:issue:`32556`)
- Bug in :class:`DataFrame` arithmetic ops with a subclass whose :meth:`_constructor` attribute is a callable other than the subclass itself (:issue:`43201`)
- Bug in arithmetic operations involving :class:`RangeIndex` where the result would have the incorrect ``name`` (:issue:`43962`)
- Bug in arithmetic operations involving :class:`Series` where the result could have the incorrect ``name`` when the operands having matching NA or matching tuple names (:issue:`44459`)
- Bug in division with ``IntegerDtype`` or ``BooleanDtype`` array and NA scalar incorrectly raising (:issue:`44685`)
- Bug in multiplying a :class:`Series` with ``FloatingDtype`` with a timedelta-like scalar incorrectly raising (:issue:`44772`)

Conversion
^^^^^^^^^^
- Bug in :class:`UInt64Index` constructor when passing a list containing both positive integers small enough to cast to int64 and integers too large to hold in int64 (:issue:`42201`)
- Bug in :class:`Series` constructor returning 0 for missing values with dtype ``int64`` and ``False`` for dtype ``bool`` (:issue:`43017`, :issue:`43018`)
- Bug in constructing a :class:`DataFrame` from a :class:`PandasArray` containing :class:`Series` objects behaving differently than an equivalent ``np.ndarray`` (:issue:`43986`)
- Bug in :class:`IntegerDtype` not allowing coercion from string dtype (:issue:`25472`)
- Bug in :func:`to_datetime` with ``arg:xr.DataArray`` and ``unit="ns"`` specified raises ``TypeError`` (:issue:`44053`)
- Bug in :meth:`DataFrame.convert_dtypes` not returning the correct type when a subclass does not overload :meth:`_constructor_sliced` (:issue:`43201`)
- Bug in :meth:`DataFrame.astype` not propagating ``attrs`` from the original :class:`DataFrame` (:issue:`44414`)
- Bug in :meth:`DataFrame.convert_dtypes` result losing ``columns.names`` (:issue:`41435`)
- Bug in constructing a ``IntegerArray`` from pyarrow data failing to validate dtypes (:issue:`44891`)
- Bug in :meth:`Series.astype` not allowing converting from a ``PeriodDtype`` to ``datetime64`` dtype, inconsistent with the :class:`PeriodIndex` behavior (:issue:`45038`)

Strings
^^^^^^^
- Bug in checking for ``string[pyarrow]`` dtype incorrectly raising an ``ImportError`` when pyarrow is not installed (:issue:`44276`)

Interval
^^^^^^^^
- Bug in :meth:`Series.where` with ``IntervalDtype`` incorrectly raising when the ``where`` call should not replace anything (:issue:`44181`)

Indexing
^^^^^^^^
- Bug in :meth:`Series.rename` with :class:`MultiIndex` and ``level`` is provided (:issue:`43659`)
- Bug in :meth:`DataFrame.truncate` and :meth:`Series.truncate` when the object's :class:`Index` has a length greater than one but only one unique value (:issue:`42365`)
- Bug in :meth:`Series.loc` and :meth:`DataFrame.loc` with a :class:`MultiIndex` when indexing with a tuple in which one of the levels is also a tuple (:issue:`27591`)
- Bug in :meth:`Series.loc` with a :class:`MultiIndex` whose first level contains only ``np.nan`` values (:issue:`42055`)
- Bug in indexing on a :class:`Series` or :class:`DataFrame` with a :class:`DatetimeIndex` when passing a string, the return type depended on whether the index was monotonic (:issue:`24892`)
- Bug in indexing on a :class:`MultiIndex` failing to drop scalar levels when the indexer is a tuple containing a datetime-like string (:issue:`42476`)
- Bug in :meth:`DataFrame.sort_values` and :meth:`Series.sort_values` when passing an ascending value, failed to raise or incorrectly raising ``ValueError`` (:issue:`41634`)
- Bug in updating values of :class:`pandas.Series` using boolean index, created by using :meth:`pandas.DataFrame.pop` (:issue:`42530`)
- Bug in :meth:`Index.get_indexer_non_unique` when index contains multiple ``np.nan`` (:issue:`35392`)
- Bug in :meth:`DataFrame.query` did not handle the degree sign in a backticked column name, such as \`Temp(°C)\`, used in an expression to query a :class:`DataFrame` (:issue:`42826`)
- Bug in :meth:`DataFrame.drop` where the error message did not show missing labels with commas when raising ``KeyError`` (:issue:`42881`)
- Bug in :meth:`DataFrame.query` where method calls in query strings led to errors when the ``numexpr`` package was installed (:issue:`22435`)
- Bug in :meth:`DataFrame.nlargest` and :meth:`Series.nlargest` where sorted result did not count indexes containing ``np.nan`` (:issue:`28984`)
- Bug in indexing on a non-unique object-dtype :class:`Index` with an NA scalar (e.g. ``np.nan``) (:issue:`43711`)
- Bug in :meth:`DataFrame.__setitem__` incorrectly writing into an existing column's array rather than setting a new array when the new dtype and the old dtype match (:issue:`43406`)
- Bug in setting floating-dtype values into a :class:`Series` with integer dtype failing to set inplace when those values can be losslessly converted to integers (:issue:`44316`)
- Bug in :meth:`Series.__setitem__` with object dtype when setting an array with matching size and dtype='datetime64[ns]' or dtype='timedelta64[ns]' incorrectly converting the datetime/timedeltas to integers (:issue:`43868`)
- Bug in :meth:`DataFrame.sort_index` where ``ignore_index=True`` was not being respected when the index was already sorted (:issue:`43591`)
- Bug in :meth:`Index.get_indexer_non_unique` when index contains multiple ``np.datetime64("NaT")`` and ``np.timedelta64("NaT")`` (:issue:`43869`)
- Bug in setting a scalar :class:`Interval` value into a :class:`Series` with ``IntervalDtype`` when the scalar's sides are floats and the values' sides are integers (:issue:`44201`)
- Bug when setting string-backed :class:`Categorical` values that can be parsed to datetimes into a :class:`DatetimeArray` or :class:`Series` or :class:`DataFrame` column backed by :class:`DatetimeArray` failing to parse these strings (:issue:`44236`)
- Bug in :meth:`Series.__setitem__` with an integer dtype other than ``int64`` setting with a ``range`` object unnecessarily upcasting to ``int64`` (:issue:`44261`)
- Bug in :meth:`Series.__setitem__` with a boolean mask indexer setting a listlike value of length 1 incorrectly broadcasting that value (:issue:`44265`)
- Bug in :meth:`Series.reset_index` not ignoring ``name`` argument when ``drop`` and ``inplace`` are set to ``True`` (:issue:`44575`)
- Bug in :meth:`DataFrame.loc.__setitem__` and :meth:`DataFrame.iloc.__setitem__` with mixed dtypes sometimes failing to operate in-place (:issue:`44345`)
- Bug in :meth:`DataFrame.loc.__getitem__` incorrectly raising ``KeyError`` when selecting a single column with a boolean key (:issue:`44322`).
- Bug in setting :meth:`DataFrame.iloc` with a single ``ExtensionDtype`` column and setting 2D values e.g. ``df.iloc[:] = df.values`` incorrectly raising (:issue:`44514`)
- Bug in setting values with :meth:`DataFrame.iloc` with a single ``ExtensionDtype`` column and a tuple of arrays as the indexer (:issue:`44703`)
- Bug in indexing on columns with ``loc`` or ``iloc`` using a slice with a negative step with ``ExtensionDtype`` columns incorrectly raising (:issue:`44551`)
- Bug in :meth:`DataFrame.loc.__setitem__` changing dtype when indexer was completely ``False`` (:issue:`37550`)
- Bug in :meth:`IntervalIndex.get_indexer_non_unique` returning boolean mask instead of array of integers for a non unique and non monotonic index (:issue:`44084`)
- Bug in :meth:`IntervalIndex.get_indexer_non_unique` not handling targets of ``dtype`` 'object' with NaNs correctly (:issue:`44482`)
- Fixed regression where a single column ``np.matrix`` was no longer coerced to a 1d ``np.ndarray`` when added to a :class:`DataFrame` (:issue:`42376`)
- Bug in :meth:`Series.__getitem__` with a :class:`CategoricalIndex` of integers treating lists of integers as positional indexers, inconsistent with the behavior with a single scalar integer (:issue:`15470`, :issue:`14865`)
- Bug in :meth:`Series.__setitem__` when setting floats or integers into integer-dtype :class:`Series` failing to upcast when necessary to retain precision (:issue:`45121`)
- Bug in :meth:`DataFrame.iloc.__setitem__` ignores axis argument (:issue:`45032`)

Missing
^^^^^^^
- Bug in :meth:`DataFrame.fillna` with ``limit`` and no ``method`` ignores ``axis='columns'`` or ``axis = 1`` (:issue:`40989`, :issue:`17399`)
- Bug in :meth:`DataFrame.fillna` not replacing missing values when using a dict-like ``value`` and duplicate column names (:issue:`43476`)
- Bug in constructing a :class:`DataFrame` with a dictionary ``np.datetime64`` as a value and ``dtype='timedelta64[ns]'``, or vice-versa, incorrectly casting instead of raising (:issue:`44428`)
- Bug in :meth:`Series.interpolate` and :meth:`DataFrame.interpolate` with ``inplace=True`` not writing to the underlying array(s) in-place (:issue:`44749`)
- Bug in :meth:`Index.fillna` incorrectly returning an unfilled :class:`Index` when NA values are present and ``downcast`` argument is specified. This now raises ``NotImplementedError`` instead; do not pass ``downcast`` argument (:issue:`44873`)
- Bug in :meth:`DataFrame.dropna` changing :class:`Index` even if no entries were dropped (:issue:`41965`)
- Bug in :meth:`Series.fillna` with an object-dtype incorrectly ignoring ``downcast="infer"`` (:issue:`44241`)

MultiIndex
^^^^^^^^^^
- Bug in :meth:`MultiIndex.get_loc` where the first level is a :class:`DatetimeIndex` and a string key is passed (:issue:`42465`)
- Bug in :meth:`MultiIndex.reindex` when passing a ``level`` that corresponds to an ``ExtensionDtype`` level (:issue:`42043`)
- Bug in :meth:`MultiIndex.get_loc` raising ``TypeError`` instead of ``KeyError`` on nested tuple (:issue:`42440`)
- Bug in :meth:`MultiIndex.union` setting wrong ``sortorder`` causing errors in subsequent indexing operations with slices (:issue:`44752`)
- Bug in :meth:`MultiIndex.putmask` where the other value was also a :class:`MultiIndex` (:issue:`43212`)
- Bug in :meth:`MultiIndex.dtypes` duplicate level names returned only one dtype per name (:issue:`45174`)

I/O
^^^
- Bug in :func:`read_excel` attempting to read chart sheets from .xlsx files (:issue:`41448`)
- Bug in :func:`json_normalize` where ``errors=ignore`` could fail to ignore missing values of ``meta`` when ``record_path`` has a length greater than one (:issue:`41876`)
- Bug in :func:`read_csv` with multi-header input and arguments referencing column names as tuples (:issue:`42446`)
- Bug in :func:`read_fwf`, where difference in lengths of ``colspecs`` and ``names`` was not raising ``ValueError`` (:issue:`40830`)
- Bug in :func:`Series.to_json` and :func:`DataFrame.to_json` where some attributes were skipped when serializing plain Python objects to JSON (:issue:`42768`, :issue:`33043`)
- Column headers are dropped when constructing a :class:`DataFrame` from a sqlalchemy's ``Row`` object (:issue:`40682`)
- Bug in unpickling an :class:`Index` with object dtype incorrectly inferring numeric dtypes (:issue:`43188`)
- Bug in :func:`read_csv` where reading multi-header input with unequal lengths incorrectly raised ``IndexError`` (:issue:`43102`)
- Bug in :func:`read_csv` raising ``ParserError`` when reading file in chunks and some chunk blocks have fewer columns than header for ``engine="c"`` (:issue:`21211`)
- Bug in :func:`read_csv`, changed exception class when expecting a file path name or file-like object from ``OSError`` to ``TypeError`` (:issue:`43366`)
- Bug in :func:`read_csv` and :func:`read_fwf` ignoring all ``skiprows`` except first when ``nrows`` is specified for ``engine='python'`` (:issue:`44021`, :issue:`10261`)
- Bug in :func:`read_csv` keeping the original column in object format when ``keep_date_col=True`` is set (:issue:`13378`)
- Bug in :func:`read_json` not handling non-numpy dtypes correctly (especially ``category``) (:issue:`21892`, :issue:`33205`)
- Bug in :func:`json_normalize` where multi-character ``sep`` parameter is incorrectly prefixed to every key (:issue:`43831`)
- Bug in :func:`json_normalize` where reading data with missing multi-level metadata would not respect ``errors="ignore"`` (:issue:`44312`)
- Bug in :func:`read_csv` used second row to guess implicit index if ``header`` was set to ``None`` for ``engine="python"`` (:issue:`22144`)
- Bug in :func:`read_csv` not recognizing bad lines when ``names`` were given for ``engine="c"`` (:issue:`22144`)
- Bug in :func:`read_csv` with :code:`float_precision="round_trip"` which did not skip initial/trailing whitespace (:issue:`43713`)
- Bug when Python is built without the lzma module: a warning was raised at the pandas import time, even if the lzma capability isn't used (:issue:`43495`)
- Bug in :func:`read_csv` not applying dtype for ``index_col`` (:issue:`9435`)
- Bug in dumping/loading a :class:`DataFrame` with ``yaml.dump(frame)`` (:issue:`42748`)
- Bug in :func:`read_csv` raising ``ValueError`` when ``names`` was longer than ``header`` but equal to data rows for ``engine="python"`` (:issue:`38453`)
- Bug in :class:`ExcelWriter`, where ``engine_kwargs`` were not passed through to all engines (:issue:`43442`)
- Bug in :func:`read_csv` raising ``ValueError`` when ``parse_dates`` was used with :class:`MultiIndex` columns (:issue:`8991`)
- Bug in :func:`read_csv` not raising an ``ValueError`` when ``\n`` was specified as ``delimiter`` or ``sep`` which conflicts with ``lineterminator`` (:issue:`43528`)
- Bug in :func:`to_csv` converting datetimes in categorical :class:`Series` to integers (:issue:`40754`)
- Bug in :func:`read_csv` converting columns to numeric after date parsing failed (:issue:`11019`)
- Bug in :func:`read_csv` not replacing ``NaN`` values with ``np.nan`` before attempting date conversion (:issue:`26203`)
- Bug in :func:`read_csv` raising ``AttributeError`` when attempting to read a .csv file and infer index column dtype from an nullable integer type (:issue:`44079`)
- Bug in :func:`to_csv` always coercing datetime columns with different formats to the same format (:issue:`21734`)
- :meth:`DataFrame.to_csv` and :meth:`Series.to_csv` with ``compression`` set to ``'zip'`` no longer create a zip file containing a file ending with ".zip". Instead, they try to infer the inner file name more smartly (:issue:`39465`)
- Bug in :func:`read_csv` where reading a mixed column of booleans and missing values to a float type results in the missing values becoming 1.0 rather than NaN (:issue:`42808`, :issue:`34120`)
- Bug in :func:`to_xml` raising error for ``pd.NA`` with extension array dtype (:issue:`43903`)
- Bug in :func:`read_csv` when passing simultaneously a parser in ``date_parser`` and ``parse_dates=False``, the parsing was still called (:issue:`44366`)
- Bug in :func:`read_csv` not setting name of :class:`MultiIndex` columns correctly when ``index_col`` is not the first column (:issue:`38549`)
- Bug in :func:`read_csv` silently ignoring errors when failing to create a memory-mapped file (:issue:`44766`)
- Bug in :func:`read_csv` when passing a ``tempfile.SpooledTemporaryFile`` opened in binary mode (:issue:`44748`)
- Bug in :func:`read_json` raising ``ValueError`` when attempting to parse json strings containing "://" (:issue:`36271`)
- Bug in :func:`read_csv` when ``engine="c"`` and ``encoding_errors=None`` which caused a segfault (:issue:`45180`)
- Bug in :func:`read_csv` an invalid value of ``usecols`` leading to an unclosed file handle (:issue:`45384`)
- Bug in :meth:`DataFrame.to_json` fix memory leak (:issue:`43877`)

Period
^^^^^^
- Bug in adding a :class:`Period` object to a ``np.timedelta64`` object incorrectly raising ``TypeError`` (:issue:`44182`)
- Bug in :meth:`PeriodIndex.to_timestamp` when the index has ``freq="B"`` inferring ``freq="D"`` for its result instead of ``freq="B"`` (:issue:`44105`)
- Bug in :class:`Period` constructor incorrectly allowing ``np.timedelta64("NaT")`` (:issue:`44507`)
- Bug in :meth:`PeriodIndex.to_timestamp` giving incorrect values for indexes with non-contiguous data (:issue:`44100`)
- Bug in :meth:`Series.where` with ``PeriodDtype`` incorrectly raising when the ``where`` call should not replace anything (:issue:`45135`)

Plotting
^^^^^^^^
- When given non-numeric data, :meth:`DataFrame.boxplot` now raises a ``ValueError`` rather than a cryptic ``KeyError`` or ``ZeroDivisionError``, in line with other plotting functions like :meth:`DataFrame.hist` (:issue:`43480`)

Groupby/resample/rolling
^^^^^^^^^^^^^^^^^^^^^^^^
- Bug in :meth:`SeriesGroupBy.apply` where passing an unrecognized string argument failed to raise ``TypeError`` when the underlying ``Series`` is empty (:issue:`42021`)
- Bug in :meth:`Series.rolling.apply`, :meth:`DataFrame.rolling.apply`, :meth:`Series.expanding.apply` and :meth:`DataFrame.expanding.apply` with ``engine="numba"`` where ``*args`` were being cached with the user passed function (:issue:`42287`)
- Bug in :meth:`.DataFrameGroupBy.max`, :meth:`.SeriesGroupBy.max`, :meth:`.DataFrameGroupBy.min`, and :meth:`.SeriesGroupBy.min` with nullable integer dtypes losing precision (:issue:`41743`)
- Bug in :meth:`DataFrame.groupby.rolling.var` would calculate the rolling variance only on the first group (:issue:`42442`)
- Bug in :meth:`.DataFrameGroupBy.shift` and :meth:`.SeriesGroupBy.shift` that would return the grouping columns if ``fill_value`` was not ``None`` (:issue:`41556`)
- Bug in :meth:`SeriesGroupBy.nlargest` and :meth:`SeriesGroupBy.nsmallest` would have an inconsistent index when the input :class:`Series` was sorted and ``n`` was greater than or equal to all group sizes (:issue:`15272`, :issue:`16345`, :issue:`29129`)
- Bug in :meth:`pandas.DataFrame.ewm`, where non-float64 dtypes were silently failing (:issue:`42452`)
- Bug in :meth:`pandas.DataFrame.rolling` operation along rows (``axis=1``) incorrectly omits columns containing ``float16`` and ``float32`` (:issue:`41779`)
- Bug in :meth:`Resampler.aggregate` did not allow the use of Named Aggregation (:issue:`32803`)
- Bug in :meth:`Series.rolling` when the :class:`Series` ``dtype`` was ``Int64`` (:issue:`43016`)
- Bug in :meth:`DataFrame.rolling.corr` when the :class:`DataFrame` columns was a :class:`MultiIndex` (:issue:`21157`)
- Bug in :meth:`DataFrame.groupby.rolling` when specifying ``on`` and calling ``__getitem__`` would subsequently return incorrect results (:issue:`43355`)
- Bug in :meth:`.DataFrameGroupBy.apply` and :meth:`.SeriesGroupBy.apply` with time-based :class:`Grouper` objects incorrectly raising ``ValueError`` in corner cases where the grouping vector contains a ``NaT`` (:issue:`43500`, :issue:`43515`)
- Bug in :meth:`.DataFrameGroupBy.mean` and :meth:`.SeriesGroupBy.mean` failing with ``complex`` dtype (:issue:`43701`)
- Bug in :meth:`Series.rolling` and :meth:`DataFrame.rolling` not calculating window bounds correctly for the first row when ``center=True`` and index is decreasing (:issue:`43927`)
- Bug in :meth:`Series.rolling` and :meth:`DataFrame.rolling` for centered datetimelike windows with uneven nanosecond (:issue:`43997`)
- Bug in :meth:`.DataFrameGroupBy.mean` and :meth:`.SeriesGroupBy.mean` raising ``KeyError`` when column was selected at least twice (:issue:`44924`)
- Bug in :meth:`.DataFrameGroupBy.nth` and :meth:`.SeriesGroupBy.nth` failing on ``axis=1`` (:issue:`43926`)
- Bug in :meth:`Series.rolling` and :meth:`DataFrame.rolling` not respecting right bound on centered datetime-like windows, if the index contain duplicates (:issue:`3944`)
- Bug in :meth:`Series.rolling` and :meth:`DataFrame.rolling` when using a :class:`pandas.api.indexers.BaseIndexer` subclass that returned unequal start and end arrays would segfault instead of raising a ``ValueError`` (:issue:`44470`)
- Bug in :meth:`Groupby.nunique` not respecting ``observed=True`` for ``categorical`` grouping columns (:issue:`45128`)
- Bug in :meth:`.DataFrameGroupBy.head`, :meth:`.SeriesGroupBy.head`, :meth:`.DataFrameGroupBy.tail`, and :meth:`.SeriesGroupBy.tail` not dropping groups with ``NaN`` when ``dropna=True`` (:issue:`45089`)
- Bug in :meth:`GroupBy.__iter__` after selecting a subset of columns in a :class:`GroupBy` object, which returned all columns instead of the chosen subset (:issue:`44821`)
- Bug in :meth:`Groupby.rolling` when non-monotonic data passed, fails to correctly raise ``ValueError`` (:issue:`43909`)
- Bug where grouping by a :class:`Series` that has a ``categorical`` data type and length unequal to the axis of grouping raised ``ValueError`` (:issue:`44179`)

Reshaping
^^^^^^^^^
- Improved error message when creating a :class:`DataFrame` column from a multi-dimensional :class:`numpy.ndarray` (:issue:`42463`)
- Bug in :func:`concat` creating :class:`MultiIndex` with duplicate level entries when concatenating a :class:`DataFrame` with duplicates in :class:`Index` and multiple keys (:issue:`42651`)
- Bug in :meth:`pandas.cut` on :class:`Series` with duplicate indices and non-exact :meth:`pandas.CategoricalIndex` (:issue:`42185`, :issue:`42425`)
- Bug in :meth:`DataFrame.append` failing to retain dtypes when appended columns do not match (:issue:`43392`)
- Bug in :func:`concat` of ``bool`` and ``boolean`` dtypes resulting in ``object`` dtype instead of ``boolean`` dtype (:issue:`42800`)
- Bug in :func:`crosstab` when inputs are categorical :class:`Series`, there are categories that are not present in one or both of the :class:`Series`, and ``margins=True``. Previously the margin value for missing categories was ``NaN``. It is now correctly reported as 0 (:issue:`43505`)
- Bug in :func:`concat` would fail when the ``objs`` argument all had the same index and the ``keys`` argument contained duplicates (:issue:`43595`)
- Bug in :func:`concat` which ignored the ``sort`` parameter (:issue:`43375`)
- Bug in :func:`merge` with :class:`MultiIndex` as column index for the ``on`` argument returning an error when assigning a column internally (:issue:`43734`)
- Bug in :func:`crosstab` would fail when inputs are lists or tuples (:issue:`44076`)
- Bug in :meth:`DataFrame.append` failing to retain ``index.name`` when appending a list of :class:`Series` objects (:issue:`44109`)
- Fixed metadata propagation in :meth:`Dataframe.apply` method, consequently fixing the same issue for :meth:`Dataframe.transform`, :meth:`Dataframe.nunique` and :meth:`Dataframe.mode` (:issue:`28283`)
- Bug in :func:`concat` casting levels of :class:`MultiIndex` to float if all levels only consist of missing values (:issue:`44900`)
- Bug in :meth:`DataFrame.stack` with ``ExtensionDtype`` columns incorrectly raising (:issue:`43561`)
- Bug in :func:`merge` raising ``KeyError`` when joining over differently named indexes with on keywords (:issue:`45094`)
- Bug in :meth:`Series.unstack` with object doing unwanted type inference on resulting columns (:issue:`44595`)
- Bug in :meth:`MultiIndex.join` with overlapping ``IntervalIndex`` levels (:issue:`44096`)
- Bug in :meth:`DataFrame.replace` and :meth:`Series.replace` results is different ``dtype`` based on ``regex`` parameter (:issue:`44864`)
- Bug in :meth:`DataFrame.pivot` with ``index=None`` when the :class:`DataFrame` index was a :class:`MultiIndex` (:issue:`23955`)

Sparse
^^^^^^
- Bug in :meth:`DataFrame.sparse.to_coo` raising ``AttributeError`` when column names are not unique (:issue:`29564`)
- Bug in :meth:`SparseArray.max` and :meth:`SparseArray.min` raising ``ValueError`` for arrays with 0 non-null elements (:issue:`43527`)
- Bug in :meth:`DataFrame.sparse.to_coo` silently converting non-zero fill values to zero (:issue:`24817`)
- Bug in :class:`SparseArray` comparison methods with an array-like operand of mismatched length raising ``AssertionError`` or unclear ``ValueError`` depending on the input (:issue:`43863`)
- Bug in :class:`SparseArray` arithmetic methods ``floordiv`` and ``mod`` behaviors when dividing by zero not matching the non-sparse :class:`Series` behavior (:issue:`38172`)
- Bug in :class:`SparseArray` unary methods as well as :meth:`SparseArray.isna` doesn't recalculate indexes (:issue:`44955`)

ExtensionArray
^^^^^^^^^^^^^^
- Bug in :func:`array` failing to preserve :class:`PandasArray` (:issue:`43887`)
- NumPy ufuncs ``np.abs``, ``np.positive``, ``np.negative`` now correctly preserve dtype when called on ExtensionArrays that implement ``__abs__, __pos__, __neg__``, respectively. In particular this is fixed for :class:`TimedeltaArray` (:issue:`43899`, :issue:`23316`)
- NumPy ufuncs ``np.minimum.reduce`` ``np.maximum.reduce``, ``np.add.reduce``, and ``np.prod.reduce`` now work correctly instead of raising ``NotImplementedError`` on :class:`Series` with ``IntegerDtype`` or ``FloatDtype`` (:issue:`43923`, :issue:`44793`)
- NumPy ufuncs with ``out`` keyword are now supported by arrays with ``IntegerDtype`` and ``FloatingDtype`` (:issue:`45122`)
- Avoid raising ``PerformanceWarning`` about fragmented :class:`DataFrame` when using many columns with an extension dtype (:issue:`44098`)
- Bug in :class:`IntegerArray` and :class:`FloatingArray` construction incorrectly coercing mismatched NA values (e.g. ``np.timedelta64("NaT")``) to numeric NA (:issue:`44514`)
- Bug in :meth:`BooleanArray.__eq__` and :meth:`BooleanArray.__ne__` raising ``TypeError`` on comparison with an incompatible type (like a string). This caused :meth:`DataFrame.replace` to sometimes raise a ``TypeError`` if a nullable boolean column was included (:issue:`44499`)
- Bug in :func:`array` incorrectly raising when passed a ``ndarray`` with ``float16`` dtype (:issue:`44715`)
- Bug in calling ``np.sqrt`` on :class:`BooleanArray` returning a malformed :class:`FloatingArray` (:issue:`44715`)
- Bug in :meth:`Series.where` with ``ExtensionDtype`` when ``other`` is a NA scalar incompatible with the :class:`Series` dtype (e.g. ``NaT`` with a numeric dtype) incorrectly casting to a compatible NA value (:issue:`44697`)
- Bug in :meth:`Series.replace` where explicitly passing ``value=None`` is treated as if no ``value`` was passed, and ``None`` not being in the result (:issue:`36984`, :issue:`19998`)
- Bug in :meth:`Series.replace` with unwanted downcasting being done in no-op replacements (:issue:`44498`)
- Bug in :meth:`Series.replace` with ``FloatDtype``, ``string[python]``, or ``string[pyarrow]`` dtype not being preserved when possible (:issue:`33484`, :issue:`40732`, :issue:`31644`, :issue:`41215`, :issue:`25438`)

Styler
^^^^^^
- Bug in :class:`.Styler` where the ``uuid`` at initialization maintained a floating underscore (:issue:`43037`)
- Bug in :meth:`.Styler.to_html` where the ``Styler`` object was updated if the ``to_html`` method was called with some args (:issue:`43034`)
- Bug in :meth:`.Styler.copy` where ``uuid`` was not previously copied (:issue:`40675`)
- Bug in :meth:`Styler.apply` where functions which returned :class:`Series` objects were not correctly handled in terms of aligning their index labels (:issue:`13657`, :issue:`42014`)
- Bug when rendering an empty :class:`DataFrame` with a named :class:`Index` (:issue:`43305`)
- Bug when rendering a single level :class:`MultiIndex` (:issue:`43383`)
- Bug when combining non-sparse rendering and :meth:`.Styler.hide_columns` or :meth:`.Styler.hide_index` (:issue:`43464`)
- Bug setting a table style when using multiple selectors in :class:`.Styler` (:issue:`44011`)
- Bugs where row trimming and column trimming failed to reflect hidden rows (:issue:`43703`, :issue:`44247`)

Other
^^^^^
- Bug in :meth:`DataFrame.astype` with non-unique columns and a :class:`Series` ``dtype`` argument (:issue:`44417`)
- Bug in :meth:`CustomBusinessMonthBegin.__add__` (:meth:`CustomBusinessMonthEnd.__add__`) not applying the extra ``offset`` parameter when beginning (end) of the target month is already a business day (:issue:`41356`)
- Bug in :meth:`RangeIndex.union` with another ``RangeIndex`` with matching (even) ``step`` and starts differing by strictly less than ``step / 2`` (:issue:`44019`)
- Bug in :meth:`RangeIndex.difference` with ``sort=None`` and ``step<0`` failing to sort (:issue:`44085`)
- Bug in :meth:`Series.replace` and :meth:`DataFrame.replace` with ``value=None`` and ExtensionDtypes (:issue:`44270`, :issue:`37899`)
- Bug in :meth:`FloatingArray.equals` failing to consider two arrays equal if they contain ``np.nan`` values (:issue:`44382`)
- Bug in :meth:`DataFrame.shift` with ``axis=1`` and ``ExtensionDtype`` columns incorrectly raising when an incompatible ``fill_value`` is passed (:issue:`44564`)
- Bug in :meth:`DataFrame.shift` with ``axis=1`` and ``periods`` larger than ``len(frame.columns)`` producing an invalid :class:`DataFrame` (:issue:`44978`)
- Bug in :meth:`DataFrame.diff` when passing a NumPy integer object instead of an ``int`` object (:issue:`44572`)
- Bug in :meth:`Series.replace` raising ``ValueError`` when using ``regex=True`` with a :class:`Series` containing ``np.nan`` values (:issue:`43344`)
- Bug in :meth:`DataFrame.to_records` where an incorrect ``n`` was used when missing names were replaced by ``level_n`` (:issue:`44818`)
- Bug in :meth:`DataFrame.eval` where ``resolvers`` argument was overriding the default resolvers (:issue:`34966`)
- :meth:`Series.__repr__` and :meth:`DataFrame.__repr__` no longer replace all null-values in indexes with "NaN" but use their real string-representations. "NaN" is used only for ``float("nan")`` (:issue:`45263`)

.. ---------------------------------------------------------------------------

.. _whatsnew_140.contributors:

Contributors
~~~~~~~~~~~~

.. contributors:: v1.3.5..v1.4.0

# ===== SOURCE: https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/source/whatsnew/v1.5.0.rst =====

.. _whatsnew_150:

What's new in 1.5.0 (September 19, 2022)
----------------------------------------

These are the changes in pandas 1.5.0. See :ref:`release` for a full changelog
including other versions of pandas.

{{ header }}

.. ---------------------------------------------------------------------------
.. _whatsnew_150.enhancements:

Enhancements
~~~~~~~~~~~~

.. _whatsnew_150.enhancements.pandas-stubs:

``pandas-stubs``
^^^^^^^^^^^^^^^^

The ``pandas-stubs`` library is now supported by the pandas development team, providing type stubs for the pandas API. Please visit
https://github.com/pandas-dev/pandas-stubs for more information.

We thank VirtusLab and Microsoft for their initial, significant contributions to ``pandas-stubs``

.. _whatsnew_150.enhancements.arrow:

Native PyArrow-backed ExtensionArray
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With `Pyarrow <https://arrow.apache.org/docs/python/index.html>`__ installed, users can now create pandas objects
that are backed by a ``pyarrow.ChunkedArray`` and ``pyarrow.DataType``.

The ``dtype`` argument can accept a string of a `pyarrow data type <https://arrow.apache.org/docs/python/api/datatypes.html>`__
with ``pyarrow`` in brackets e.g. ``"int64[pyarrow]"`` or, for pyarrow data types that take parameters, a :class:`ArrowDtype`
initialized with a ``pyarrow.DataType``.

.. ipython:: python

    import pyarrow as pa
    ser_float = pd.Series([1.0, 2.0, None], dtype="float32[pyarrow]")
    ser_float

    list_of_int_type = pd.ArrowDtype(pa.list_(pa.int64()))
    ser_list = pd.Series([[1, 2], [3, None]], dtype=list_of_int_type)
    ser_list

    ser_list.take([1, 0])
    ser_float * 5
    ser_float.mean()
    ser_float.dropna()

Most operations are supported and have been implemented using `pyarrow compute <https://arrow.apache.org/docs/python/api/compute.html>`__ functions.
We recommend installing the latest version of PyArrow to access the most recently implemented compute functions.

.. warning::

    This feature is experimental, and the API can change in a future release without warning.

.. _whatsnew_150.enhancements.dataframe_interchange:

DataFrame interchange protocol implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

pandas now implement the DataFrame interchange API spec.
See the full details on the API at https://data-apis.org/dataframe-protocol/latest/index.html

The protocol consists of two parts:

- New method :meth:`DataFrame.__dataframe__` which produces the interchange object.
  It effectively "exports" the pandas dataframe as an interchange object so
  any other library which has the protocol implemented can "import" that dataframe
  without knowing anything about the producer except that it makes an interchange object.
- New function :func:`pandas.api.interchange.from_dataframe` which can take
  an arbitrary interchange object from any conformant library and construct a
  pandas DataFrame out of it.

.. _whatsnew_150.enhancements.styler:

Styler
^^^^^^

The most notable development is the new method :meth:`.Styler.concat` which
allows adding customised footer rows to visualise additional calculations on the data,
e.g. totals and counts etc. (:issue:`43875`, :issue:`46186`)

Additionally there is an alternative output method :meth:`.Styler.to_string`,
which allows using the Styler's formatting methods to create, for example, CSVs (:issue:`44502`).

A new feature :meth:`.Styler.relabel_index` is also made available to provide full customisation of the display of
index or column headers (:issue:`47864`)

Minor feature improvements are:

  - Adding the ability to render ``border`` and ``border-{side}`` CSS properties in Excel (:issue:`42276`)
  - Making keyword arguments consist: :meth:`.Styler.highlight_null` now accepts ``color`` and deprecates ``null_color`` although this remains backwards compatible (:issue:`45907`)

.. _whatsnew_150.enhancements.resample_group_keys:

Control of index with ``group_keys`` in :meth:`DataFrame.resample`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The argument ``group_keys`` has been added to the method :meth:`DataFrame.resample`.
As with :meth:`DataFrame.groupby`, this argument controls the whether each group is added
to the index in the resample when :meth:`.Resampler.apply` is used.

.. warning::
   Not specifying the ``group_keys`` argument will retain the
   previous behavior and emit a warning if the result will change
   by specifying ``group_keys=False``. In a future version
   of pandas, not specifying ``group_keys`` will default to
   the same behavior as ``group_keys=False``.

.. code-block:: ipython

    In [11]: df = pd.DataFrame(
       ....:     {'a': range(6)},
       ....:     index=pd.date_range("2021-01-01", periods=6, freq="8H")
       ....: )
       ....:

    In [12]: df.resample("D", group_keys=True).apply(lambda x: x)
    Out[12]:
                                    a
    2021-01-01 2021-01-01 00:00:00  0
               2021-01-01 08:00:00  1
               2021-01-01 16:00:00  2
    2021-01-02 2021-01-02 00:00:00  3
               2021-01-02 08:00:00  4
               2021-01-02 16:00:00  5

    In [13]: df.resample("D", group_keys=False).apply(lambda x: x)
    Out[13]:
                         a
    2021-01-01 00:00:00  0
    2021-01-01 08:00:00  1
    2021-01-01 16:00:00  2
    2021-01-02 00:00:00  3
    2021-01-02 08:00:00  4
    2021-01-02 16:00:00  5

Previously, the resulting index would depend upon the values returned by ``apply``,
as seen in the following example.

.. code-block:: ipython

    In [1]: # pandas 1.3
    In [2]: df.resample("D").apply(lambda x: x)
    Out[2]:
                         a
    2021-01-01 00:00:00  0
    2021-01-01 08:00:00  1
    2021-01-01 16:00:00  2
    2021-01-02 00:00:00  3
    2021-01-02 08:00:00  4
    2021-01-02 16:00:00  5

    In [3]: df.resample("D").apply(lambda x: x.reset_index())
    Out[3]:
                               index  a
    2021-01-01 0 2021-01-01 00:00:00  0
               1 2021-01-01 08:00:00  1
               2 2021-01-01 16:00:00  2
    2021-01-02 0 2021-01-02 00:00:00  3
               1 2021-01-02 08:00:00  4
               2 2021-01-02 16:00:00  5

.. _whatsnew_150.enhancements.from_dummies:

from_dummies
^^^^^^^^^^^^

Added new function :func:`~pandas.from_dummies` to convert a dummy coded :class:`DataFrame` into a categorical :class:`DataFrame`.

.. ipython:: python

    import pandas as pd

    df = pd.DataFrame({"col1_a": [1, 0, 1], "col1_b": [0, 1, 0],
                       "col2_a": [0, 1, 0], "col2_b": [1, 0, 0],
                       "col2_c": [0, 0, 1]})

    pd.from_dummies(df, sep="_")

.. _whatsnew_150.enhancements.orc:

Writing to ORC files
^^^^^^^^^^^^^^^^^^^^

The new method :meth:`DataFrame.to_orc` allows writing to ORC files (:issue:`43864`).

This functionality depends the `pyarrow <http://arrow.apache.org/docs/python/>`__ library. For more details, see :ref:`the IO docs on ORC <io.orc>`.

.. warning::

   * It is *highly recommended* to install pyarrow using conda due to some issues occurred by pyarrow.
   * :func:`~pandas.DataFrame.to_orc` requires pyarrow>=7.0.0.
   * :func:`~pandas.DataFrame.to_orc` is not supported on Windows yet, you can find valid environments on :ref:`install optional dependencies <install.warn_orc>`.
   * For supported dtypes please refer to `supported ORC features in Arrow <https://arrow.apache.org/docs/cpp/orc.html#data-types>`__.
   * Currently timezones in datetime columns are not preserved when a dataframe is converted into ORC files.

.. code-block:: python

    df = pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]})
    df.to_orc("./out.orc")

.. _whatsnew_150.enhancements.tar:

Reading directly from TAR archives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I/O methods like :func:`read_csv` or :meth:`DataFrame.to_json` now allow reading and writing
directly on TAR archives (:issue:`44787`).

.. code-block:: python

   df = pd.read_csv("./movement.tar.gz")
   # ...
   df.to_csv("./out.tar.gz")

This supports ``.tar``, ``.tar.gz``, ``.tar.bz`` and ``.tar.xz2`` archives.
The used compression method is inferred from the filename.
If the compression method cannot be inferred, use the ``compression`` argument:

.. code-block:: python

   df = pd.read_csv(some_file_obj, compression={"method": "tar", "mode": "r:gz"}) # noqa F821

(``mode`` being one of ``tarfile.open``'s modes: https://docs.python.org/3/library/tarfile.html#tarfile.open)


.. _whatsnew_150.enhancements.read_xml_dtypes:

read_xml now supports ``dtype``, ``converters``, and ``parse_dates``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similar to other IO methods, :func:`pandas.read_xml` now supports assigning specific dtypes to columns,
apply converter methods, and parse dates (:issue:`43567`).

.. ipython:: python

    from io import StringIO
    xml_dates = """<?xml version='1.0' encoding='utf-8'?>
    <data>
      <row>
        <shape>square</shape>
        <degrees>00360</degrees>
        <sides>4.0</sides>
        <date>2020-01-01</date>
       </row>
      <row>
        <shape>circle</shape>
        <degrees>00360</degrees>
        <sides/>
        <date>2021-01-01</date>
      </row>
      <row>
        <shape>triangle</shape>
        <degrees>00180</degrees>
        <sides>3.0</sides>
        <date>2022-01-01</date>
      </row>
    </data>"""

    df = pd.read_xml(
        StringIO(xml_dates),
        dtype={'sides': 'Int64'},
        converters={'degrees': str},
        parse_dates=['date']
    )
    df
    df.dtypes


.. _whatsnew_150.enhancements.read_xml_iterparse:

read_xml now supports large XML using ``iterparse``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For very large XML files that can range in hundreds of megabytes to gigabytes, :func:`pandas.read_xml`
now supports parsing such sizeable files using `lxml's iterparse`_ and `etree's iterparse`_
which are memory-efficient methods to iterate through XML trees and extract specific elements
and attributes without holding entire tree in memory (:issue:`45442`).

.. code-block:: ipython

    In [1]: df = pd.read_xml(
    ...      "/path/to/downloaded/enwikisource-latest-pages-articles.xml",
    ...      iterparse = {"page": ["title", "ns", "id"]}
    ...  )
    df
    Out[2]:
                                                         title   ns        id
    0                                       Gettysburg Address    0     21450
    1                                                Main Page    0     42950
    2                            Declaration by United Nations    0      8435
    3             Constitution of the United States of America    0      8435
    4                     Declaration of Independence (Israel)    0     17858
    ...                                                    ...  ...       ...
    3578760               Page:Black cat 1897 07 v2 n10.pdf/17  104    219649
    3578761               Page:Black cat 1897 07 v2 n10.pdf/43  104    219649
    3578762               Page:Black cat 1897 07 v2 n10.pdf/44  104    219649
    3578763      The History of Tom Jones, a Foundling/Book IX    0  12084291
    3578764  Page:Shakespeare of Stratford (1926) Yale.djvu/91  104     21450

    [3578765 rows x 3 columns]


.. _`lxml's iterparse`: https://lxml.de/3.2/parsing.html#iterparse-and-iterwalk
.. _`etree's iterparse`: https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.iterparse

.. _whatsnew_150.enhancements.copy_on_write:

Copy on Write
^^^^^^^^^^^^^

A new feature ``copy_on_write`` was added (:issue:`46958`). Copy on write ensures that
any DataFrame or Series derived from another in any way always behaves as a copy.
Copy on write disallows updating any other object than the object the method
was applied to.

Copy on write can be enabled through:

.. code-block:: python

    pd.set_option("mode.copy_on_write", True)
    pd.options.mode.copy_on_write = True

Alternatively, copy on write can be enabled locally through:

.. code-block:: python

    with pd.option_context("mode.copy_on_write", True):
        ...

Without copy on write, the parent :class:`DataFrame` is updated when updating a child
:class:`DataFrame` that was derived from this :class:`DataFrame`.

.. ipython:: python

    df = pd.DataFrame({"foo": [1, 2, 3], "bar": 1})
    view = df["foo"]
    view.iloc[0]
    df

With copy on write enabled, df won't be updated anymore:

.. ipython:: python

    with pd.option_context("mode.copy_on_write", True):
        df = pd.DataFrame({"foo": [1, 2, 3], "bar": 1})
        view = df["foo"]
        view.iloc[0]
        df

A more detailed explanation can be found `here <https://phofl.github.io/cow-introduction.html>`_.

.. _whatsnew_150.enhancements.other:

Other enhancements
^^^^^^^^^^^^^^^^^^
- :meth:`Series.map` now raises when ``arg`` is dict but ``na_action`` is not either ``None`` or ``'ignore'`` (:issue:`46588`)
- :meth:`MultiIndex.to_frame` now supports the argument ``allow_duplicates`` and raises on duplicate labels if it is missing or False (:issue:`45245`)
- :class:`.StringArray` now accepts array-likes containing nan-likes (``None``, ``np.nan``) for the ``values`` parameter in its constructor in addition to strings and :attr:`pandas.NA`. (:issue:`40839`)
- Improved the rendering of ``categories`` in :class:`CategoricalIndex` (:issue:`45218`)
- :meth:`DataFrame.plot` will now allow the ``subplots`` parameter to be a list of iterables specifying column groups, so that columns may be grouped together in the same subplot (:issue:`29688`).
- :meth:`to_numeric` now preserves float64 arrays when downcasting would generate values not representable in float32 (:issue:`43693`)
- :meth:`Series.reset_index` and :meth:`DataFrame.reset_index` now support the argument ``allow_duplicates`` (:issue:`44410`)
- :meth:`.DataFrameGroupBy.min`, :meth:`.SeriesGroupBy.min`, :meth:`.DataFrameGroupBy.max`, and :meth:`.SeriesGroupBy.max` now supports `Numba <https://numba.pydata.org/>`_ execution with the ``engine`` keyword (:issue:`45428`)
- :func:`read_csv` now supports ``defaultdict`` as a ``dtype`` parameter (:issue:`41574`)
- :meth:`DataFrame.rolling` and :meth:`Series.rolling` now support a ``step`` parameter with fixed-length windows (:issue:`15354`)
- Implemented a ``bool``-dtype :class:`Index`, passing a bool-dtype array-like to ``pd.Index`` will now retain ``bool`` dtype instead of casting to ``object`` (:issue:`45061`)
- Implemented a complex-dtype :class:`Index`, passing a complex-dtype array-like to ``pd.Index`` will now retain complex dtype instead of casting to ``object`` (:issue:`45845`)
- :class:`Series` and :class:`DataFrame` with :class:`IntegerDtype` now supports bitwise operations (:issue:`34463`)
- Add ``milliseconds`` field support for :class:`.DateOffset` (:issue:`43371`)
- :meth:`DataFrame.where` tries to maintain dtype of :class:`DataFrame` if fill value can be cast without loss of precision (:issue:`45582`)
- :meth:`DataFrame.reset_index` now accepts a ``names`` argument which renames the index names (:issue:`6878`)
- :func:`concat` now raises when ``levels`` is given but ``keys`` is None (:issue:`46653`)
- :func:`concat` now raises when ``levels`` contains duplicate values (:issue:`46653`)
- Added ``numeric_only`` argument to :meth:`DataFrame.corr`, :meth:`DataFrame.corrwith`, :meth:`DataFrame.cov`, :meth:`DataFrame.idxmin`, :meth:`DataFrame.idxmax`, :meth:`.DataFrameGroupBy.idxmin`, :meth:`.DataFrameGroupBy.idxmax`, :meth:`.DataFrameGroupBy.var`, :meth:`.SeriesGroupBy.var`, :meth:`.DataFrameGroupBy.std`, :meth:`.SeriesGroupBy.std`, :meth:`.DataFrameGroupBy.sem`, :meth:`.SeriesGroupBy.sem`, and :meth:`.DataFrameGroupBy.quantile` (:issue:`46560`)
- A :class:`errors.PerformanceWarning` is now thrown when using ``string[pyarrow]`` dtype with methods that don't dispatch to ``pyarrow.compute`` methods (:issue:`42613`, :issue:`46725`)
- Added ``validate`` argument to :meth:`DataFrame.join` (:issue:`46622`)
- Added ``numeric_only`` argument to :meth:`.Resampler.sum`, :meth:`.Resampler.prod`, :meth:`.Resampler.min`, :meth:`.Resampler.max`, :meth:`.Resampler.first`, and :meth:`.Resampler.last` (:issue:`46442`)
- ``times`` argument in :class:`.ExponentialMovingWindow` now accepts ``np.timedelta64`` (:issue:`47003`)
- :class:`.DataError`, :class:`.SpecificationError`, ``SettingWithCopyError``, ``SettingWithCopyWarning``, :class:`.NumExprClobberingError`, :class:`.UndefinedVariableError`, :class:`.IndexingError`, :class:`.PyperclipException`, :class:`.PyperclipWindowsException`, :class:`.CSSWarning`, :class:`.PossibleDataLossError`, :class:`.ClosedFileError`, :class:`.IncompatibilityWarning`, :class:`.AttributeConflictWarning`, :class:`.DatabaseError`, :class:`.PossiblePrecisionLoss`, :class:`.ValueLabelTypeMismatch`, :class:`.InvalidColumnName`, and :class:`.CategoricalConversionWarning` are now exposed in ``pandas.errors`` (:issue:`27656`)
- Added ``check_like`` argument to :func:`testing.assert_series_equal` (:issue:`47247`)
- Add support for :meth:`.DataFrameGroupBy.ohlc` and :meth:`.SeriesGroupBy.ohlc` for extension array dtypes (:issue:`37493`)
- Allow reading compressed SAS files with :func:`read_sas` (e.g., ``.sas7bdat.gz`` files)
- :func:`pandas.read_html` now supports extracting links from table cells (:issue:`13141`)
- :meth:`DatetimeIndex.astype` now supports casting timezone-naive indexes to ``datetime64[s]``, ``datetime64[ms]``, and ``datetime64[us]``, and timezone-aware indexes to the corresponding ``datetime64[unit, tzname]`` dtypes (:issue:`47579`)
- :class:`Series` reducers (e.g. ``min``, ``max``, ``sum``, ``mean``) will now successfully operate when the dtype is numeric and ``numeric_only=True`` is provided; previously this would raise a ``NotImplementedError`` (:issue:`47500`)
- :meth:`RangeIndex.union` now can return a :class:`RangeIndex` instead of a :class:`Int64Index` if the resulting values are equally spaced (:issue:`47557`, :issue:`43885`)
- :meth:`DataFrame.compare` now accepts an argument ``result_names`` to allow the user to specify the result's names of both left and right DataFrame which are being compared. This is by default ``'self'`` and ``'other'`` (:issue:`44354`)
- :meth:`DataFrame.quantile` gained a ``method`` argument that can accept ``table`` to evaluate multi-column quantiles (:issue:`43881`)
- :class:`Interval` now supports checking whether one interval is contained by another interval (:issue:`46613`)
- Added ``copy`` keyword to :meth:`Series.set_axis` and :meth:`DataFrame.set_axis` to allow user to set axis on a new object without necessarily copying the underlying data (:issue:`47932`)
- The method :meth:`.ExtensionArray.factorize` accepts ``use_na_sentinel=False`` for determining how null values are to be treated (:issue:`46601`)
- The ``Dockerfile`` now installs a dedicated ``pandas-dev`` virtual environment for pandas development instead of using the ``base`` environment (:issue:`48427`)

.. ---------------------------------------------------------------------------
.. _whatsnew_150.notable_bug_fixes:

Notable bug fixes
~~~~~~~~~~~~~~~~~

These are bug fixes that might have notable behavior changes.

.. _whatsnew_150.notable_bug_fixes.groupby_transform_dropna:

Using ``dropna=True`` with ``groupby`` transforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A transform is an operation whose result has the same size as its input. When the
result is a :class:`DataFrame` or :class:`Series`, it is also required that the
index of the result matches that of the input. In pandas 1.4, using
:meth:`.DataFrameGroupBy.transform` or :meth:`.SeriesGroupBy.transform` with null
values in the groups and ``dropna=True`` gave incorrect results. Demonstrated by the
examples below, the incorrect results either contained incorrect values, or the result
did not have the same index as the input.

.. ipython:: python

    df = pd.DataFrame({'a': [1, 1, np.nan], 'b': [2, 3, 4]})

*Old behavior*:

.. code-block:: ipython

    In [3]: # Value in the last row should be np.nan
            df.groupby('a', dropna=True).transform('sum')
    Out[3]:
       b
    0  5
    1  5
    2  5

    In [3]: # Should have one additional row with the value np.nan
            df.groupby('a', dropna=True).transform(lambda x: x.sum())
    Out[3]:
       b
    0  5
    1  5

    In [3]: # The value in the last row is np.nan interpreted as an integer
            df.groupby('a', dropna=True).transform('ffill')
    Out[3]:
                         b
    0                    2
    1                    3
    2 -9223372036854775808

    In [3]: # Should have one additional row with the value np.nan
            df.groupby('a', dropna=True).transform(lambda x: x)
    Out[3]:
       b
    0  2
    1  3

*New behavior*:

.. ipython:: python

    df.groupby('a', dropna=True).transform('sum')
    df.groupby('a', dropna=True).transform(lambda x: x.sum())
    df.groupby('a', dropna=True).transform('ffill')
    df.groupby('a', dropna=True).transform(lambda x: x)

.. _whatsnew_150.notable_bug_fixes.to_json_incorrectly_localizing_naive_timestamps:

Serializing tz-naive Timestamps with to_json() with ``iso_dates=True``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:meth:`DataFrame.to_json`, :meth:`Series.to_json`, and :meth:`Index.to_json`
would incorrectly localize DatetimeArrays/DatetimeIndexes with tz-naive Timestamps
to UTC. (:issue:`38760`)

Note that this patch does not fix the localization of tz-aware Timestamps to UTC
upon serialization. (Related issue :issue:`12997`)

*Old Behavior*

.. code-block:: ipython

    In [32]: index = pd.date_range(
       ....:     start='2020-12-28 00:00:00',
       ....:     end='2020-12-28 02:00:00',
       ....:     freq='1H',
       ....: )
       ....:

    In [33]: a = pd.Series(
       ....:     data=range(3),
       ....:     index=index,
       ....: )
       ....:

    In [4]: from io import StringIO

    In [5]: a.to_json(date_format='iso')
    Out[5]: '{"2020-12-28T00:00:00.000Z":0,"2020-12-28T01:00:00.000Z":1,"2020-12-28T02:00:00.000Z":2}'

    In [6]: pd.read_json(StringIO(a.to_json(date_format='iso')), typ="series").index == a.index
    Out[6]: array([False, False, False])

*New Behavior*

.. code-block:: ipython

    In [34]: from io import StringIO

    In [35]: a.to_json(date_format='iso')
    Out[35]: '{"2020-12-28T00:00:00.000Z":0,"2020-12-28T01:00:00.000Z":1,"2020-12-28T02:00:00.000Z":2}'

    # Roundtripping now works
    In [36]: pd.read_json(StringIO(a.to_json(date_format='iso')), typ="series").index == a.index
    Out[36]: array([ True,  True,  True])

.. _whatsnew_150.notable_bug_fixes.groupby_value_counts_categorical:

DataFrameGroupBy.value_counts with non-grouping categorical columns and ``observed=True``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Calling :meth:`.DataFrameGroupBy.value_counts` with ``observed=True`` would incorrectly drop non-observed categories of non-grouping columns (:issue:`46357`).

.. code-block:: ipython

    In [6]: df = pd.DataFrame(["a", "b", "c"], dtype="category").iloc[0:2]
    In [7]: df
    Out[7]:
       0
    0  a
    1  b

*Old Behavior*

.. code-block:: ipython

    In [8]: df.groupby(level=0, observed=True).value_counts()
    Out[8]:
    0  a    1
    1  b    1
    dtype: int64


*New Behavior*

.. code-block:: ipython

    In [9]: df.groupby(level=0, observed=True).value_counts()
    Out[9]:
    0  a    1
    1  a    0
       b    1
    0  b    0
       c    0
    1  c    0
    dtype: int64

.. ---------------------------------------------------------------------------
.. _whatsnew_150.api_breaking:

Backwards incompatible API changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _whatsnew_150.api_breaking.deps:

Increased minimum versions for dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Some minimum supported versions of dependencies were updated.
If installed, we now require:

+-----------------+-----------------+----------+---------+
| Package         | Minimum Version | Required | Changed |
+=================+=================+==========+=========+
| numpy           | 1.20.3          |    X     |    X    |
+-----------------+-----------------+----------+---------+
| mypy (dev)      | 0.971           |          |    X    |
+-----------------+-----------------+----------+---------+
| beautifulsoup4  | 4.9.3           |          |    X    |
+-----------------+-----------------+----------+---------+
| blosc           | 1.21.0          |          |    X    |
+-----------------+-----------------+----------+---------+
| bottleneck      | 1.3.2           |          |    X    |
+-----------------+-----------------+----------+---------+
| fsspec          | 2021.07.0       |          |    X    |
+-----------------+-----------------+----------+---------+
| hypothesis      | 6.13.0          |          |    X    |
+-----------------+-----------------+----------+---------+
| gcsfs           | 2021.07.0       |          |    X    |
+-----------------+-----------------+----------+---------+
| jinja2          | 3.0.0           |          |    X    |
+-----------------+-----------------+----------+---------+
| lxml            | 4.6.3           |          |    X    |
+-----------------+-----------------+----------+---------+
| numba           | 0.53.1          |          |    X    |
+-----------------+-----------------+----------+---------+
| numexpr         | 2.7.3           |          |    X    |
+-----------------+-----------------+----------+---------+
| openpyxl        | 3.0.7           |          |    X    |
+-----------------+-----------------+----------+---------+
| pandas-gbq      | 0.15.0          |          |    X    |
+-----------------+-----------------+----------+---------+
| psycopg2        | 2.8.6           |          |    X    |
+-----------------+-----------------+----------+---------+
| pymysql         | 1.0.2           |          |    X    |
+-----------------+-----------------+----------+---------+
| pyreadstat      | 1.1.2           |          |    X    |
+-----------------+-----------------+----------+---------+
| pyxlsb          | 1.0.8           |          |    X    |
+-----------------+-----------------+----------+---------+
| s3fs            | 2021.08.0       |          |    X    |
+-----------------+-----------------+----------+---------+
| scipy           | 1.7.1           |          |    X    |
+-----------------+-----------------+----------+---------+
| sqlalchemy      | 1.4.16          |          |    X    |
+-----------------+-----------------+----------+---------+
| tabulate        | 0.8.9           |          |    X    |
+-----------------+-----------------+----------+---------+
| xarray          | 0.19.0          |          |    X    |
+-----------------+-----------------+----------+---------+
| xlsxwriter      | 1.4.3           |          |    X    |
+-----------------+-----------------+----------+---------+

For `optional libraries <https://pandas.pydata.org/docs/getting_started/install.html>`_ the general recommendation is to use the latest version.
The following table lists the lowest version per library that is currently being tested throughout the development of pandas.
Optional libraries below the lowest tested version may still work, but are not considered supported.

+-----------------+-----------------+---------+
| Package         | Minimum Version | Changed |
+=================+=================+=========+
| beautifulsoup4  |4.9.3            |    X    |
+-----------------+-----------------+---------+
| blosc           |1.21.0           |    X    |
+-----------------+-----------------+---------+
| bottleneck      |1.3.2            |    X    |
+-----------------+-----------------+---------+
| brotlipy        |0.7.0            |         |
+-----------------+-----------------+---------+
| fastparquet     |0.4.0            |         |
+-----------------+-----------------+---------+
| fsspec          |2021.08.0        |    X    |
+-----------------+-----------------+---------+
| html5lib        |1.1              |         |
+-----------------+-----------------+---------+
| hypothesis      |6.13.0           |    X    |
+-----------------+-----------------+---------+
| gcsfs           |2021.08.0        |    X    |
+-----------------+-----------------+---------+
| jinja2          |3.0.0            |    X    |
+-----------------+-----------------+---------+
| lxml            |4.6.3            |    X    |
+-----------------+-----------------+---------+
| matplotlib      |3.3.2            |         |
+-----------------+-----------------+---------+
| numba           |0.53.1           |    X    |
+-----------------+-----------------+---------+
| numexpr         |2.7.3            |    X    |
+-----------------+-----------------+---------+
| odfpy           |1.4.1            |         |
+-----------------+-----------------+---------+
| openpyxl        |3.0.7            |    X    |
+-----------------+-----------------+---------+
| pandas-gbq      |0.15.0           |    X    |
+-----------------+-----------------+---------+
| psycopg2        |2.8.6            |    X    |
+-----------------+-----------------+---------+
| pyarrow         |1.0.1            |         |
+-----------------+-----------------+---------+
| pymysql         |1.0.2            |    X    |
+-----------------+-----------------+---------+
| pyreadstat      |1.1.2            |    X    |
+-----------------+-----------------+---------+
| pytables        |3.6.1            |         |
+-----------------+-----------------+---------+
| python-snappy   |0.6.0            |         |
+-----------------+-----------------+---------+
| pyxlsb          |1.0.8            |    X    |
+-----------------+-----------------+---------+
| s3fs            |2021.08.0        |    X    |
+-----------------+-----------------+---------+
| scipy           |1.7.1            |    X    |
+-----------------+-----------------+---------+
| sqlalchemy      |1.4.16           |    X    |
+-----------------+-----------------+---------+
| tabulate        |0.8.9            |    X    |
+-----------------+-----------------+---------+
| tzdata          |2022a            |         |
+-----------------+-----------------+---------+
| xarray          |0.19.0           |    X    |
+-----------------+-----------------+---------+
| xlrd            |2.0.1            |         |
+-----------------+-----------------+---------+
| xlsxwriter      |1.4.3            |    X    |
+-----------------+-----------------+---------+
| xlwt            |1.3.0            |         |
+-----------------+-----------------+---------+
| zstandard       |0.15.2           |         |
+-----------------+-----------------+---------+

See :ref:`install.dependencies` and :ref:`install.optional_dependencies` for more.

.. _whatsnew_150.api_breaking.other:

Other API changes
^^^^^^^^^^^^^^^^^

- BigQuery I/O methods :func:`read_gbq` and :meth:`DataFrame.to_gbq` default to
  ``auth_local_webserver = True``. Google has deprecated the
  ``auth_local_webserver = False`` `"out of band" (copy-paste) flow
  <https://developers.googleblog.com/2022/02/making-oauth-flows-safer.html?m=1#disallowed-oob>`_.
  The ``auth_local_webserver = False`` option is planned to stop working in
  October 2022. (:issue:`46312`)
- :func:`read_json` now raises ``FileNotFoundError`` (previously ``ValueError``) when input is a string ending in ``.json``, ``.json.gz``, ``.json.bz2``, etc. but no such file exists. (:issue:`29102`)
- Operations with :class:`Timestamp` or :class:`Timedelta` that would previously raise ``OverflowError`` instead raise ``OutOfBoundsDatetime`` or ``OutOfBoundsTimedelta`` where appropriate (:issue:`47268`)
- When :func:`read_sas` previously returned ``None``, it now returns an empty :class:`DataFrame` (:issue:`47410`)
- :class:`DataFrame` constructor raises if ``index`` or ``columns`` arguments are sets (:issue:`47215`)

.. ---------------------------------------------------------------------------
.. _whatsnew_150.deprecations:

Deprecations
~~~~~~~~~~~~

.. warning::

    In the next major version release, 2.0, several larger API changes are being considered without a formal deprecation such as
    making the standard library `zoneinfo <https://docs.python.org/3/library/zoneinfo.html>`_ the default timezone implementation instead of ``pytz``,
    having the :class:`Index` support all data types instead of having multiple subclasses (:class:`CategoricalIndex`, :class:`Int64Index`, etc.), and more.
    The changes under consideration are logged in `this GitHub issue <https://github.com/pandas-dev/pandas/issues/44823>`_, and any
    feedback or concerns are welcome.

.. _whatsnew_150.deprecations.int_slicing_series:

Label-based integer slicing on a Series with an Int64Index or RangeIndex
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In a future version, integer slicing on a :class:`Series` with a :class:`Int64Index` or :class:`RangeIndex` will be treated as *label-based*, not positional. This will make the behavior consistent with other :meth:`Series.__getitem__` and :meth:`Series.__setitem__` behaviors (:issue:`45162`).

For example:

.. ipython:: python

   ser = pd.Series([1, 2, 3, 4, 5], index=[2, 3, 5, 7, 11])

In the old behavior, ``ser[2:4]`` treats the slice as positional:

*Old behavior*:

.. code-block:: ipython

    In [3]: ser[2:4]
    Out[3]:
    5    3
    7    4
    dtype: int64

In a future version, this will be treated as label-based:

*Future behavior*:

.. code-block:: ipython

    In [4]: ser.loc[2:4]
    Out[4]:
    2    1
    3    2
    dtype: int64

To retain the old behavior, use ``series.iloc[i:j]``. To get the future behavior,
use ``series.loc[i:j]``.

Slicing on a :class:`DataFrame` will not be affected.

.. _whatsnew_150.deprecations.excel_writer_attributes:

:class:`ExcelWriter` attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All attributes of :class:`ExcelWriter` were previously documented as not
public. However some third party Excel engines documented accessing
``ExcelWriter.book`` or ``ExcelWriter.sheets``, and users were utilizing these
and possibly other attributes. Previously these attributes were not safe to use;
e.g. modifications to ``ExcelWriter.book`` would not update ``ExcelWriter.sheets``
and conversely. In order to support this, pandas has made some attributes public
and improved their implementations so that they may now be safely used. (:issue:`45572`)

The following attributes are now public and considered safe to access.

 - ``book``
 - ``check_extension``
 - ``close``
 - ``date_format``
 - ``datetime_format``
 - ``engine``
 - ``if_sheet_exists``
 - ``sheets``
 - ``supported_extensions``

The following attributes have been deprecated. They now raise a ``FutureWarning``
when accessed and will be removed in a future version. Users should be aware
that their usage is considered unsafe, and can lead to unexpected results.

 - ``cur_sheet``
 - ``handles``
 - ``path``
 - ``save``
 - ``write_cells``

See the documentation of :class:`ExcelWriter` for further details.

.. _whatsnew_150.deprecations.group_keys_in_apply:

Using ``group_keys`` with transformers in :meth:`.DataFrameGroupBy.apply` and :meth:`.SeriesGroupBy.apply`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In previous versions of pandas, if it was inferred that the function passed to
:meth:`.DataFrameGroupBy.apply` or :meth:`.SeriesGroupBy.apply` was a transformer (i.e. the resulting index was equal to
the input index), the ``group_keys`` argument of :meth:`DataFrame.groupby` and
:meth:`Series.groupby` was ignored and the group keys would never be added to
the index of the result. In the future, the group keys will be added to the index
when the user specifies ``group_keys=True``.

As ``group_keys=True`` is the default value of :meth:`DataFrame.groupby` and
:meth:`Series.groupby`, not specifying ``group_keys`` with a transformer will
raise a ``FutureWarning``. This can be silenced and the previous behavior
retained by specifying ``group_keys=False``.

.. _whatsnew_150.deprecations.setitem_column_try_inplace:
   _ see also _whatsnew_130.notable_bug_fixes.setitem_column_try_inplace

Inplace operation when setting values with ``loc`` and ``iloc``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Most of the time setting values with :meth:`DataFrame.iloc` attempts to set values
inplace, only falling back to inserting a new array if necessary. There are
some cases where this rule is not followed, for example when setting an entire
column from an array with different dtype:

.. ipython:: python

   df = pd.DataFrame({'price': [11.1, 12.2]}, index=['book1', 'book2'])
   original_prices = df['price']
   new_prices = np.array([98, 99])

*Old behavior*:

.. code-block:: ipython

    In [3]: df.iloc[:, 0] = new_prices
    In [4]: df.iloc[:, 0]
    Out[4]:
    book1    98
    book2    99
    Name: price, dtype: int64
    In [5]: original_prices
    Out[5]:
    book1    11.1
    book2    12.2
    Name: price, float: 64

This behavior is deprecated. In a future version, setting an entire column with
iloc will attempt to operate inplace.

*Future behavior*:

.. code-block:: ipython

    In [3]: df.iloc[:, 0] = new_prices
    In [4]: df.iloc[:, 0]
    Out[4]:
    book1    98.0
    book2    99.0
    Name: price, dtype: float64
    In [5]: original_prices
    Out[5]:
    book1    98.0
    book2    99.0
    Name: price, dtype: float64

To get the old behavior, use :meth:`DataFrame.__setitem__` directly:

.. code-block:: ipython

    In [3]: df[df.columns[0]] = new_prices
    In [4]: df.iloc[:, 0]
    Out[4]
    book1    98
    book2    99
    Name: price, dtype: int64
    In [5]: original_prices
    Out[5]:
    book1    11.1
    book2    12.2
    Name: price, dtype: float64

To get the old behaviour when ``df.columns`` is not unique and you want to
change a single column by index, you can use :meth:`DataFrame.isetitem`, which
has been added in pandas 1.5:

.. code-block:: ipython

    In [3]: df_with_duplicated_cols = pd.concat([df, df], axis='columns')
    In [3]: df_with_duplicated_cols.isetitem(0, new_prices)
    In [4]: df_with_duplicated_cols.iloc[:, 0]
    Out[4]:
    book1    98
    book2    99
    Name: price, dtype: int64
    In [5]: original_prices
    Out[5]:
    book1    11.1
    book2    12.2
    Name: 0, dtype: float64

.. _whatsnew_150.deprecations.numeric_only_default:

``numeric_only`` default value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Across the :class:`DataFrame`, :class:`.DataFrameGroupBy`, and :class:`.Resampler` operations such as
``min``, ``sum``, and ``idxmax``, the default
value of the ``numeric_only`` argument, if it exists at all, was inconsistent.
Furthermore, operations with the default value ``None`` can lead to surprising
results. (:issue:`46560`)

.. code-block:: ipython

    In [1]: df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})

    In [2]: # Reading the next line without knowing the contents of df, one would
            # expect the result to contain the products for both columns a and b.
            df[["a", "b"]].prod()
    Out[2]:
    a    2
    dtype: int64

To avoid this behavior, the specifying the value ``numeric_only=None`` has been
deprecated, and will be removed in a future version of pandas. In the future,
all operations with a ``numeric_only`` argument will default to ``False``. Users
should either call the operation only with columns that can be operated on, or
specify ``numeric_only=True`` to operate only on Boolean, integer, and float columns.

In order to support the transition to the new behavior, the following methods have
gained the ``numeric_only`` argument.

- :meth:`DataFrame.corr`
- :meth:`DataFrame.corrwith`
- :meth:`DataFrame.cov`
- :meth:`DataFrame.idxmin`
- :meth:`DataFrame.idxmax`
- :meth:`.DataFrameGroupBy.cummin`
- :meth:`.DataFrameGroupBy.cummax`
- :meth:`.DataFrameGroupBy.idxmin`
- :meth:`.DataFrameGroupBy.idxmax`
- :meth:`.DataFrameGroupBy.var`
- :meth:`.DataFrameGroupBy.std`
- :meth:`.DataFrameGroupBy.sem`
- :meth:`.DataFrameGroupBy.quantile`
- :meth:`.Resampler.mean`
- :meth:`.Resampler.median`
- :meth:`.Resampler.sem`
- :meth:`.Resampler.std`
- :meth:`.Resampler.var`
- :meth:`DataFrame.rolling` operations
- :meth:`DataFrame.expanding` operations
- :meth:`DataFrame.ewm` operations

.. _whatsnew_150.deprecations.other:

Other Deprecations
^^^^^^^^^^^^^^^^^^
- Deprecated the keyword ``line_terminator`` in :meth:`DataFrame.to_csv` and :meth:`Series.to_csv`, use ``lineterminator`` instead; this is for consistency with :func:`read_csv` and the standard library 'csv' module (:issue:`9568`)
- Deprecated behavior of :meth:`SparseArray.astype`, :meth:`Series.astype`, and :meth:`DataFrame.astype` with :class:`SparseDtype` when passing a non-sparse ``dtype``. In a future version, this will cast to that non-sparse dtype instead of wrapping it in a :class:`SparseDtype` (:issue:`34457`)
- Deprecated behavior of :meth:`DatetimeIndex.intersection` and :meth:`DatetimeIndex.symmetric_difference` (``union`` behavior was already deprecated in version 1.3.0) with mixed time zones; in a future version both will be cast to UTC instead of object dtype (:issue:`39328`, :issue:`45357`)
- Deprecated :meth:`DataFrame.iteritems`, :meth:`Series.iteritems`, :meth:`HDFStore.iteritems` in favor of :meth:`DataFrame.items`, :meth:`Series.items`, :meth:`HDFStore.items`  (:issue:`45321`)
- Deprecated :meth:`Series.is_monotonic` and :meth:`Index.is_monotonic` in favor of :meth:`Series.is_monotonic_increasing` and :meth:`Index.is_monotonic_increasing` (:issue:`45422`, :issue:`21335`)
- Deprecated behavior of :meth:`DatetimeIndex.astype`, :meth:`TimedeltaIndex.astype`, :meth:`PeriodIndex.astype` when converting to an integer dtype other than ``int64``. In a future version, these will convert to exactly the specified dtype (instead of always ``int64``) and will raise if the conversion overflows (:issue:`45034`)
- Deprecated the ``__array_wrap__`` method of DataFrame and Series, rely on standard numpy ufuncs instead (:issue:`45451`)
- Deprecated treating float-dtype data as wall-times when passed with a timezone to :class:`Series` or :class:`DatetimeIndex` (:issue:`45573`)
- Deprecated the behavior of :meth:`Series.fillna` and :meth:`DataFrame.fillna` with ``timedelta64[ns]`` dtype and incompatible fill value; in a future version this will cast to a common dtype (usually object) instead of raising, matching the behavior of other dtypes (:issue:`45746`)
- Deprecated the ``warn`` parameter in :func:`infer_freq` (:issue:`45947`)
- Deprecated allowing non-keyword arguments in :meth:`.ExtensionArray.argsort` (:issue:`46134`)
- Deprecated treating all-bool ``object``-dtype columns as bool-like in :meth:`DataFrame.any` and :meth:`DataFrame.all` with ``bool_only=True``, explicitly cast to bool instead (:issue:`46188`)
- Deprecated behavior of method :meth:`DataFrame.quantile`, attribute ``numeric_only`` will default False. Including datetime/timedelta columns in the result (:issue:`7308`).
- Deprecated :attr:`Timedelta.freq` and :attr:`Timedelta.is_populated` (:issue:`46430`)
- Deprecated :attr:`Timedelta.delta` (:issue:`46476`)
- Deprecated passing arguments as positional in :meth:`DataFrame.any` and :meth:`Series.any` (:issue:`44802`)
- Deprecated passing positional arguments to :meth:`DataFrame.pivot` and :func:`pivot` except ``data`` (:issue:`30228`)
- Deprecated the methods :meth:`DataFrame.mad`, :meth:`Series.mad`, and the corresponding groupby methods (:issue:`11787`)
- Deprecated positional arguments to :meth:`Index.join` except for ``other``, use keyword-only arguments instead of positional arguments (:issue:`46518`)
- Deprecated positional arguments to :meth:`StringMethods.rsplit` and :meth:`StringMethods.split` except for ``pat``, use keyword-only arguments instead of positional arguments (:issue:`47423`)
- Deprecated indexing on a timezone-naive :class:`DatetimeIndex` using a string representing a timezone-aware datetime (:issue:`46903`, :issue:`36148`)
- Deprecated allowing ``unit="M"`` or ``unit="Y"`` in :class:`Timestamp` constructor with a non-round float value (:issue:`47267`)
- Deprecated the ``display.column_space`` global configuration option (:issue:`7576`)
- Deprecated the argument ``na_sentinel`` in :func:`factorize`, :meth:`Index.factorize`, and :meth:`.ExtensionArray.factorize`; pass ``use_na_sentinel=True`` instead to use the sentinel ``-1`` for NaN values and ``use_na_sentinel=False`` instead of ``na_sentinel=None`` to encode NaN values (:issue:`46910`)
- Deprecated :meth:`.DataFrameGroupBy.transform` not aligning the result when the UDF returned DataFrame (:issue:`45648`)
- Clarified warning from :func:`to_datetime` when delimited dates can't be parsed in accordance to specified ``dayfirst`` argument (:issue:`46210`)
- Emit warning from :func:`to_datetime` when delimited dates can't be parsed in accordance to specified ``dayfirst`` argument even for dates where leading zero is omitted (e.g. ``31/1/2001``) (:issue:`47880`)
- Deprecated :class:`Series` and :class:`Resampler` reducers (e.g. ``min``, ``max``, ``sum``, ``mean``) raising a ``NotImplementedError`` when the dtype is non-numric and ``numeric_only=True`` is provided; this will raise a ``TypeError`` in a future version (:issue:`47500`)
- Deprecated :meth:`Series.rank` returning an empty result when the dtype is non-numeric and ``numeric_only=True`` is provided; this will raise a ``TypeError`` in a future version (:issue:`47500`)
- Deprecated argument ``errors`` for :meth:`Series.mask`, :meth:`Series.where`, :meth:`DataFrame.mask`, and :meth:`DataFrame.where` as ``errors`` had no effect on this methods (:issue:`47728`)
- Deprecated arguments ``*args`` and ``**kwargs`` in :class:`Rolling`, :class:`Expanding`, and :class:`ExponentialMovingWindow` ops. (:issue:`47836`)
- Deprecated the ``inplace`` keyword in :meth:`Categorical.set_ordered`, :meth:`Categorical.as_ordered`, and :meth:`Categorical.as_unordered` (:issue:`37643`)
- Deprecated setting a categorical's categories with ``cat.categories = ['a', 'b', 'c']``, use :meth:`Categorical.rename_categories` instead (:issue:`37643`)
- Deprecated unused arguments ``encoding`` and ``verbose`` in :meth:`Series.to_excel` and :meth:`DataFrame.to_excel` (:issue:`47912`)
- Deprecated the ``inplace`` keyword in :meth:`DataFrame.set_axis` and :meth:`Series.set_axis`, use ``obj = obj.set_axis(..., copy=False)`` instead (:issue:`48130`)
- Deprecated producing a single element when iterating over a :class:`DataFrameGroupBy` or a :class:`SeriesGroupBy` that has been grouped by a list of length 1; A tuple of length one will be returned instead (:issue:`42795`)
- Fixed up warning message of deprecation of :meth:`MultiIndex.lesort_depth` as public method, as the message previously referred to :meth:`MultiIndex.is_lexsorted` instead (:issue:`38701`)
- Deprecated the ``sort_columns`` argument in :meth:`DataFrame.plot` and :meth:`Series.plot` (:issue:`47563`).
- Deprecated positional arguments for all but the first argument of :meth:`DataFrame.to_stata` and :func:`read_stata`, use keyword arguments instead (:issue:`48128`).
- Deprecated the ``mangle_dupe_cols`` argument in :func:`read_csv`, :func:`read_fwf`, :func:`read_table` and :func:`read_excel`. The argument was never implemented, and a new argument where the renaming pattern can be specified will be added instead (:issue:`47718`)
- Deprecated allowing ``dtype='datetime64'`` or ``dtype=np.datetime64`` in :meth:`Series.astype`, use "datetime64[ns]" instead (:issue:`47844`)

.. ---------------------------------------------------------------------------
.. _whatsnew_150.performance:

Performance improvements
~~~~~~~~~~~~~~~~~~~~~~~~
- Performance improvement in :meth:`DataFrame.corrwith` for column-wise (axis=0) Pearson and Spearman correlation when other is a :class:`Series` (:issue:`46174`)
- Performance improvement in :meth:`.DataFrameGroupBy.transform` and :meth:`.SeriesGroupBy.transform` for some user-defined DataFrame -> Series functions (:issue:`45387`)
- Performance improvement in :meth:`DataFrame.duplicated` when subset consists of only one column (:issue:`45236`)
- Performance improvement in :meth:`.DataFrameGroupBy.diff` and :meth:`.SeriesGroupBy.diff` (:issue:`16706`)
- Performance improvement in :meth:`.DataFrameGroupBy.transform` and :meth:`.SeriesGroupBy.transform` when broadcasting values for user-defined functions (:issue:`45708`)
- Performance improvement in :meth:`.DataFrameGroupBy.transform` and :meth:`.SeriesGroupBy.transform` for user-defined functions when only a single group exists (:issue:`44977`)
- Performance improvement in :meth:`.DataFrameGroupBy.apply` and :meth:`.SeriesGroupBy.apply` when grouping on a non-unique unsorted index (:issue:`46527`)
- Performance improvement in :meth:`DataFrame.loc` and :meth:`Series.loc` for tuple-based indexing of a :class:`MultiIndex` (:issue:`45681`, :issue:`46040`, :issue:`46330`)
- Performance improvement in :meth:`.DataFrameGroupBy.var` and :meth:`.SeriesGroupBy.var` with ``ddof`` other than one (:issue:`48152`)
- Performance improvement in :meth:`DataFrame.to_records` when the index is a :class:`MultiIndex` (:issue:`47263`)
- Performance improvement in :attr:`MultiIndex.values` when the MultiIndex contains levels of type DatetimeIndex, TimedeltaIndex or ExtensionDtypes (:issue:`46288`)
- Performance improvement in :func:`merge` when left and/or right are empty (:issue:`45838`)
- Performance improvement in :meth:`DataFrame.join` when left and/or right are empty (:issue:`46015`)
- Performance improvement in :meth:`DataFrame.reindex` and :meth:`Series.reindex` when target is a :class:`MultiIndex` (:issue:`46235`)
- Performance improvement when setting values in a pyarrow backed string array (:issue:`46400`)
- Performance improvement in :func:`factorize` (:issue:`46109`)
- Performance improvement in :class:`DataFrame` and :class:`Series` constructors for extension dtype scalars (:issue:`45854`)
- Performance improvement in :func:`read_excel` when ``nrows`` argument provided (:issue:`32727`)
- Performance improvement in :meth:`.Styler.to_excel` when applying repeated CSS formats (:issue:`47371`)
- Performance improvement in :meth:`MultiIndex.is_monotonic_increasing`  (:issue:`47458`)
- Performance improvement in :class:`BusinessHour` ``str`` and ``repr`` (:issue:`44764`)
- Performance improvement in datetime arrays string formatting when one of the default strftime formats ``"%Y-%m-%d %H:%M:%S"`` or ``"%Y-%m-%d %H:%M:%S.%f"`` is used. (:issue:`44764`)
- Performance improvement in :meth:`Series.to_sql` and :meth:`DataFrame.to_sql` (:class:`SQLiteTable`) when processing time arrays. (:issue:`44764`)
- Performance improvement to :func:`read_sas` (:issue:`47404`)
- Performance improvement in ``argmax`` and ``argmin`` for :class:`arrays.SparseArray` (:issue:`34197`)

.. ---------------------------------------------------------------------------
.. _whatsnew_150.bug_fixes:

Bug fixes
~~~~~~~~~

Categorical
^^^^^^^^^^^
- Bug in :meth:`.Categorical.view` not accepting integer dtypes (:issue:`25464`)
- Bug in :meth:`.CategoricalIndex.union` when the index's categories are integer-dtype and the index contains ``NaN`` values incorrectly raising instead of casting to ``float64`` (:issue:`45362`)
- Bug in :meth:`concat` when concatenating two (or more) unordered :class:`CategoricalIndex` variables, whose categories are permutations, yields incorrect index values (:issue:`24845`)

Datetimelike
^^^^^^^^^^^^
- Bug in :meth:`DataFrame.quantile` with datetime-like dtypes and no rows incorrectly returning ``float64`` dtype instead of retaining datetime-like dtype (:issue:`41544`)
- Bug in :func:`to_datetime` with sequences of ``np.str_`` objects incorrectly raising (:issue:`32264`)
- Bug in :class:`Timestamp` construction when passing datetime components as positional arguments and ``tzinfo`` as a keyword argument incorrectly raising (:issue:`31929`)
- Bug in :meth:`Index.astype` when casting from object dtype to ``timedelta64[ns]`` dtype incorrectly casting ``np.datetime64("NaT")`` values to ``np.timedelta64("NaT")`` instead of raising (:issue:`45722`)
- Bug in :meth:`.SeriesGroupBy.value_counts` index when passing categorical column (:issue:`44324`)
- Bug in :meth:`DatetimeIndex.tz_localize` localizing to UTC failing to make a copy of the underlying data (:issue:`46460`)
- Bug in :meth:`DatetimeIndex.resolution` incorrectly returning "day" instead of "nanosecond" for nanosecond-resolution indexes (:issue:`46903`)
- Bug in :class:`Timestamp` with an integer or float value and ``unit="Y"`` or ``unit="M"`` giving slightly-wrong results (:issue:`47266`)
- Bug in :class:`.DatetimeArray` construction when passed another :class:`.DatetimeArray` and ``freq=None`` incorrectly inferring the freq from the given array (:issue:`47296`)
- Bug in :func:`to_datetime` where ``OutOfBoundsDatetime`` would be thrown even if ``errors=coerce`` if there were more than 50 rows (:issue:`45319`)
- Bug when adding a :class:`DateOffset` to a :class:`Series` would not add the ``nanoseconds`` field (:issue:`47856`)

Timedelta
^^^^^^^^^
- Bug in :func:`astype_nansafe` astype("timedelta64[ns]") fails when np.nan is included (:issue:`45798`)
- Bug in constructing a :class:`Timedelta` with a ``np.timedelta64`` object and a ``unit`` sometimes silently overflowing and returning incorrect results instead of raising ``OutOfBoundsTimedelta`` (:issue:`46827`)
- Bug in constructing a :class:`Timedelta` from a large integer or float with ``unit="W"`` silently overflowing and returning incorrect results instead of raising ``OutOfBoundsTimedelta`` (:issue:`47268`)

Time Zones
^^^^^^^^^^
- Bug in :class:`Timestamp` constructor raising when passed a ``ZoneInfo`` tzinfo object (:issue:`46425`)

Numeric
^^^^^^^
- Bug in operations with array-likes with ``dtype="boolean"`` and :attr:`NA` incorrectly altering the array in-place (:issue:`45421`)
- Bug in arithmetic operations with nullable types without :attr:`NA` values not matching the same operation with non-nullable types (:issue:`48223`)
- Bug in ``floordiv`` when dividing by ``IntegerDtype`` ``0`` would return ``0`` instead of ``inf`` (:issue:`48223`)
- Bug in division, ``pow`` and ``mod`` operations on array-likes with ``dtype="boolean"`` not being like their ``np.bool_`` counterparts (:issue:`46063`)
- Bug in multiplying a :class:`Series` with ``IntegerDtype`` or ``FloatingDtype`` by an array-like with ``timedelta64[ns]`` dtype incorrectly raising (:issue:`45622`)
- Bug in :meth:`mean` where the optional dependency ``bottleneck`` causes precision loss linear in the length of the array. ``bottleneck`` has been disabled for :meth:`mean` improving the loss to log-linear but may result in a performance decrease. (:issue:`42878`)

Conversion
^^^^^^^^^^
- Bug in :meth:`DataFrame.astype` not preserving subclasses (:issue:`40810`)
- Bug in constructing a :class:`Series` from a float-containing list or a floating-dtype ndarray-like (e.g. ``dask.Array``) and an integer dtype raising instead of casting like we would with an ``np.ndarray`` (:issue:`40110`)
- Bug in :meth:`Float64Index.astype` to unsigned integer dtype incorrectly casting to ``np.int64`` dtype (:issue:`45309`)
- Bug in :meth:`Series.astype` and :meth:`DataFrame.astype` from floating dtype to unsigned integer dtype failing to raise in the presence of negative values (:issue:`45151`)
- Bug in :func:`array` with ``FloatingDtype`` and values containing float-castable strings incorrectly raising (:issue:`45424`)
- Bug when comparing string and datetime64ns objects causing ``OverflowError`` exception. (:issue:`45506`)
- Bug in metaclass of generic abstract dtypes causing :meth:`DataFrame.apply` and :meth:`Series.apply` to raise for the built-in function ``type`` (:issue:`46684`)
- Bug in :meth:`DataFrame.to_records` returning inconsistent numpy types if the index was a :class:`MultiIndex` (:issue:`47263`)
- Bug in :meth:`DataFrame.to_dict` for ``orient="list"`` or ``orient="index"`` was not returning native types (:issue:`46751`)
- Bug in :meth:`DataFrame.apply` that returns a :class:`DataFrame` instead of a :class:`Series` when applied to an empty :class:`DataFrame` and ``axis=1`` (:issue:`39111`)
- Bug when inferring the dtype from an iterable that is *not* a NumPy ``ndarray`` consisting of all NumPy unsigned integer scalars did not result in an unsigned integer dtype (:issue:`47294`)
- Bug in :meth:`DataFrame.eval` when pandas objects (e.g. ``'Timestamp'``) were column names (:issue:`44603`)

Strings
^^^^^^^
- Bug in :meth:`str.startswith` and :meth:`str.endswith` when using other series as parameter _pat_. Now raises ``TypeError`` (:issue:`3485`)
- Bug in :meth:`Series.str.zfill` when strings contain leading signs, padding '0' before the sign character rather than after as ``str.zfill`` from standard library (:issue:`20868`)

Interval
^^^^^^^^
- Bug in :meth:`IntervalArray.__setitem__` when setting ``np.nan`` into an integer-backed array raising ``ValueError`` instead of ``TypeError`` (:issue:`45484`)
- Bug in :class:`IntervalDtype` when using datetime64[ns, tz] as a dtype string (:issue:`46999`)

Indexing
^^^^^^^^
- Bug in :meth:`DataFrame.iloc` where indexing a single row on a :class:`DataFrame` with a single ExtensionDtype column gave a copy instead of a view on the underlying data (:issue:`45241`)
- Bug in :meth:`DataFrame.__getitem__` returning copy when :class:`DataFrame` has duplicated columns even if a unique column is selected (:issue:`45316`, :issue:`41062`)
- Bug in :meth:`Series.align` does not create :class:`MultiIndex` with union of levels when both MultiIndexes intersections are identical (:issue:`45224`)
- Bug in setting a NA value (``None`` or ``np.nan``) into a :class:`Series` with int-based :class:`IntervalDtype` incorrectly casting to object dtype instead of a float-based :class:`IntervalDtype` (:issue:`45568`)
- Bug in indexing setting values into an ``ExtensionDtype`` column with ``df.iloc[:, i] = values`` with ``values`` having the same dtype as ``df.iloc[:, i]`` incorrectly inserting a new array instead of setting in-place (:issue:`33457`)
- Bug in :meth:`Series.__setitem__` with a non-integer :class:`Index` when using an integer key to set a value that cannot be set inplace where a ``ValueError`` was raised instead of casting to a common dtype (:issue:`45070`)
- Bug in :meth:`DataFrame.loc` not casting ``None`` to ``NA`` when setting value as a list into :class:`DataFrame` (:issue:`47987`)
- Bug in :meth:`Series.__setitem__` when setting incompatible values into a ``PeriodDtype`` or ``IntervalDtype`` :class:`Series` raising when indexing with a boolean mask but coercing when indexing with otherwise-equivalent indexers; these now consistently coerce, along with :meth:`Series.mask` and :meth:`Series.where` (:issue:`45768`)
- Bug in :meth:`DataFrame.where` with multiple columns with datetime-like dtypes failing to downcast results consistent with other dtypes (:issue:`45837`)
- Bug in :func:`isin` upcasting to ``float64`` with unsigned integer dtype and list-like argument without a dtype (:issue:`46485`)
- Bug in :meth:`Series.loc.__setitem__` and :meth:`Series.loc.__getitem__` not raising when using multiple keys without using a :class:`MultiIndex` (:issue:`13831`)
- Bug in :meth:`Index.reindex` raising ``AssertionError`` when ``level`` was specified but no :class:`MultiIndex` was given; level is ignored now (:issue:`35132`)
- Bug when setting a value too large for a :class:`Series` dtype failing to coerce to a common type (:issue:`26049`, :issue:`32878`)
- Bug in :meth:`loc.__setitem__` treating ``range`` keys as positional instead of label-based (:issue:`45479`)
- Bug in :meth:`DataFrame.__setitem__` casting extension array dtypes to object when setting with a scalar key and :class:`DataFrame` as value (:issue:`46896`)
- Bug in :meth:`Series.__setitem__` when setting a scalar to a nullable pandas dtype would not raise a ``TypeError`` if the scalar could not be cast (losslessly) to the nullable type (:issue:`45404`)
- Bug in :meth:`Series.__setitem__` when setting ``boolean`` dtype values containing ``NA`` incorrectly raising instead of casting to ``boolean`` dtype (:issue:`45462`)
- Bug in :meth:`Series.loc` raising with boolean indexer containing ``NA`` when :class:`Index` did not match (:issue:`46551`)
- Bug in :meth:`Series.__setitem__` where setting :attr:`NA` into a numeric-dtype :class:`Series` would incorrectly upcast to object-dtype rather than treating the value as ``np.nan`` (:issue:`44199`)
- Bug in :meth:`DataFrame.loc` when setting values to a column and right hand side is a dictionary (:issue:`47216`)
- Bug in :meth:`Series.__setitem__` with ``datetime64[ns]`` dtype, an all-``False`` boolean mask, and an incompatible value incorrectly casting to ``object`` instead of retaining ``datetime64[ns]`` dtype (:issue:`45967`)
- Bug in :meth:`Index.__getitem__`  raising ``ValueError`` when indexer is from boolean dtype with ``NA`` (:issue:`45806`)
- Bug in :meth:`Series.__setitem__` losing precision when enlarging :class:`Series` with scalar (:issue:`32346`)
- Bug in :meth:`Series.mask` with ``inplace=True`` or setting values with a boolean mask with small integer dtypes incorrectly raising (:issue:`45750`)
- Bug in :meth:`DataFrame.mask` with ``inplace=True`` and ``ExtensionDtype`` columns incorrectly raising (:issue:`45577`)
- Bug in getting a column from a DataFrame with an object-dtype row index with datetime-like values: the resulting Series now preserves the exact object-dtype Index from the parent DataFrame (:issue:`42950`)
- Bug in :meth:`DataFrame.__getattribute__` raising ``AttributeError`` if columns have ``"string"`` dtype (:issue:`46185`)
- Bug in :meth:`DataFrame.compare` returning all ``NaN`` column when comparing extension array dtype and numpy dtype (:issue:`44014`)
- Bug in :meth:`DataFrame.where` setting wrong values with ``"boolean"`` mask for numpy dtype (:issue:`44014`)
- Bug in indexing on a :class:`DatetimeIndex` with a ``np.str_`` key incorrectly raising (:issue:`45580`)
- Bug in :meth:`CategoricalIndex.get_indexer` when index contains ``NaN`` values, resulting in elements that are in target but not present in the index to be mapped to the index of the NaN element, instead of -1 (:issue:`45361`)
- Bug in setting large integer values into :class:`Series` with ``float32`` or ``float16`` dtype incorrectly altering these values instead of coercing to ``float64`` dtype (:issue:`45844`)
- Bug in :meth:`Series.asof` and :meth:`DataFrame.asof` incorrectly casting bool-dtype results to ``float64`` dtype (:issue:`16063`)
- Bug in :meth:`NDFrame.xs`, :meth:`DataFrame.iterrows`, :meth:`DataFrame.loc` and :meth:`DataFrame.iloc` not always propagating metadata (:issue:`28283`)
- Bug in :meth:`DataFrame.sum` min_count changes dtype if input contains NaNs (:issue:`46947`)
- Bug in :class:`IntervalTree` that lead to an infinite recursion. (:issue:`46658`)
- Bug in :class:`PeriodIndex` raising ``AttributeError`` when indexing on ``NA``, rather than putting ``NaT`` in its place. (:issue:`46673`)
- Bug in :meth:`DataFrame.at` would allow the modification of multiple columns (:issue:`48296`)

Missing
^^^^^^^
- Bug in :meth:`Series.fillna` and :meth:`DataFrame.fillna` with ``downcast`` keyword not being respected in some cases where there are no NA values present (:issue:`45423`)
- Bug in :meth:`Series.fillna` and :meth:`DataFrame.fillna` with :class:`IntervalDtype` and incompatible value raising instead of casting to a common (usually object) dtype (:issue:`45796`)
- Bug in :meth:`Series.map` not respecting ``na_action`` argument if mapper is a ``dict`` or :class:`Series` (:issue:`47527`)
- Bug in :meth:`DataFrame.interpolate` with object-dtype column not returning a copy with ``inplace=False`` (:issue:`45791`)
- Bug in :meth:`DataFrame.dropna` allows to set both ``how`` and ``thresh`` incompatible arguments (:issue:`46575`)
- Bug in :meth:`DataFrame.fillna` ignored ``axis`` when :class:`DataFrame` is single block (:issue:`47713`)

MultiIndex
^^^^^^^^^^
- Bug in :meth:`DataFrame.loc` returning empty result when slicing a :class:`MultiIndex` with a negative step size and non-null start/stop values (:issue:`46156`)
- Bug in :meth:`DataFrame.loc` raising when slicing a :class:`MultiIndex` with a negative step size other than -1 (:issue:`46156`)
- Bug in :meth:`DataFrame.loc` raising when slicing a :class:`MultiIndex` with a negative step size and slicing a non-int labeled index level (:issue:`46156`)
- Bug in :meth:`Series.to_numpy` where multiindexed Series could not be converted to numpy arrays when an ``na_value`` was supplied (:issue:`45774`)
- Bug in :class:`MultiIndex.equals` not commutative when only one side has extension array dtype (:issue:`46026`)
- Bug in :meth:`MultiIndex.from_tuples` cannot construct Index of empty tuples (:issue:`45608`)

I/O
^^^
- Bug in :meth:`DataFrame.to_stata` where no error is raised if the :class:`DataFrame` contains ``-np.inf`` (:issue:`45350`)
- Bug in :func:`read_excel` results in an infinite loop with certain ``skiprows`` callables (:issue:`45585`)
- Bug in :meth:`DataFrame.info` where a new line at the end of the output is omitted when called on an empty :class:`DataFrame` (:issue:`45494`)
- Bug in :func:`read_csv` not recognizing line break for ``on_bad_lines="warn"`` for ``engine="c"`` (:issue:`41710`)
- Bug in :meth:`DataFrame.to_csv` not respecting ``float_format`` for ``Float64`` dtype (:issue:`45991`)
- Bug in :func:`read_csv` not respecting a specified converter to index columns in all cases (:issue:`40589`)
- Bug in :func:`read_csv` interpreting second row as :class:`Index` names even when ``index_col=False`` (:issue:`46569`)
- Bug in :func:`read_parquet` when ``engine="pyarrow"`` which caused partial write to disk when column of unsupported datatype was passed (:issue:`44914`)
- Bug in :func:`DataFrame.to_excel` and :class:`ExcelWriter` would raise when writing an empty DataFrame to a ``.ods`` file (:issue:`45793`)
- Bug in :func:`read_csv` ignoring non-existing header row for ``engine="python"`` (:issue:`47400`)
- Bug in :func:`read_excel` raising uncontrolled ``IndexError`` when ``header`` references non-existing rows (:issue:`43143`)
- Bug in :func:`read_html` where elements surrounding ``<br>`` were joined without a space between them (:issue:`29528`)
- Bug in :func:`read_csv` when data is longer than header leading to issues with callables in ``usecols`` expecting strings (:issue:`46997`)
- Bug in Parquet roundtrip for Interval dtype with ``datetime64[ns]`` subtype (:issue:`45881`)
- Bug in :func:`read_excel` when reading a ``.ods`` file with newlines between xml elements (:issue:`45598`)
- Bug in :func:`read_parquet` when ``engine="fastparquet"`` where the file was not closed on error (:issue:`46555`)
- :meth:`DataFrame.to_html` now excludes the ``border`` attribute from ``<table>`` elements when ``border`` keyword is set to ``False``.
- Bug in :func:`read_sas` with certain types of compressed SAS7BDAT files (:issue:`35545`)
- Bug in :func:`read_excel` not forward filling :class:`MultiIndex` when no names were given (:issue:`47487`)
- Bug in :func:`read_sas` returned ``None`` rather than an empty DataFrame for SAS7BDAT files with zero rows (:issue:`18198`)
- Bug in :meth:`DataFrame.to_string` using wrong missing value with extension arrays in :class:`MultiIndex` (:issue:`47986`)
- Bug in :class:`StataWriter` where value labels were always written with default encoding (:issue:`46750`)
- Bug in :class:`StataWriterUTF8` where some valid characters were removed from variable names (:issue:`47276`)
- Bug in :meth:`DataFrame.to_excel` when writing an empty dataframe with :class:`MultiIndex` (:issue:`19543`)
- Bug in :func:`read_sas` with RLE-compressed SAS7BDAT files that contain 0x40 control bytes (:issue:`31243`)
- Bug in :func:`read_sas` that scrambled column names (:issue:`31243`)
- Bug in :func:`read_sas` with RLE-compressed SAS7BDAT files that contain 0x00 control bytes (:issue:`47099`)
- Bug in :func:`read_parquet` with ``use_nullable_dtypes=True`` where ``float64`` dtype was returned instead of nullable ``Float64`` dtype (:issue:`45694`)
- Bug in :meth:`DataFrame.to_json` where ``PeriodDtype`` would not make the serialization roundtrip when read back with :meth:`read_json` (:issue:`44720`)
- Bug in :func:`read_xml` when reading XML files with Chinese character tags and would raise ``XMLSyntaxError`` (:issue:`47902`)

Period
^^^^^^
- Bug in subtraction of :class:`Period` from :class:`.PeriodArray` returning wrong results (:issue:`45999`)
- Bug in :meth:`Period.strftime` and :meth:`PeriodIndex.strftime`, directives ``%l`` and ``%u`` were giving wrong results (:issue:`46252`)
- Bug in inferring an incorrect ``freq`` when passing a string to :class:`Period` microseconds that are a multiple of 1000 (:issue:`46811`)
- Bug in constructing a :class:`Period` from a :class:`Timestamp` or ``np.datetime64`` object with non-zero nanoseconds and ``freq="ns"`` incorrectly truncating the nanoseconds (:issue:`46811`)
- Bug in adding ``np.timedelta64("NaT", "ns")`` to a :class:`Period` with a timedelta-like freq incorrectly raising ``IncompatibleFrequency`` instead of returning ``NaT`` (:issue:`47196`)
- Bug in adding an array of integers to an array with :class:`PeriodDtype` giving incorrect results when ``dtype.freq.n > 1`` (:issue:`47209`)
- Bug in subtracting a :class:`Period` from an array with :class:`PeriodDtype` returning incorrect results instead of raising ``OverflowError`` when the operation overflows (:issue:`47538`)

Plotting
^^^^^^^^
- Bug in :meth:`DataFrame.plot.barh` that prevented labeling the x-axis and ``xlabel`` updating the y-axis label (:issue:`45144`)
- Bug in :meth:`DataFrame.plot.box` that prevented labeling the x-axis (:issue:`45463`)
- Bug in :meth:`DataFrame.boxplot` that prevented passing in ``xlabel`` and ``ylabel`` (:issue:`45463`)
- Bug in :meth:`DataFrame.boxplot` that prevented specifying ``vert=False`` (:issue:`36918`)
- Bug in :meth:`DataFrame.plot.scatter` that prevented specifying ``norm`` (:issue:`45809`)
- Fix showing "None" as ylabel in :meth:`Series.plot` when not setting ylabel (:issue:`46129`)
- Bug in :meth:`DataFrame.plot` that led to xticks and vertical grids being improperly placed when plotting a quarterly series (:issue:`47602`)
- Bug in :meth:`DataFrame.plot` that prevented setting y-axis label, limits and ticks for a secondary y-axis (:issue:`47753`)

Groupby/resample/rolling
^^^^^^^^^^^^^^^^^^^^^^^^
- Bug in :meth:`DataFrame.resample` ignoring ``closed="right"`` on :class:`TimedeltaIndex` (:issue:`45414`)
- Bug in :meth:`.DataFrameGroupBy.transform` fails when ``func="size"`` and the input DataFrame has multiple columns (:issue:`27469`)
- Bug in :meth:`.DataFrameGroupBy.size` and :meth:`.DataFrameGroupBy.transform` with ``func="size"`` produced incorrect results when ``axis=1`` (:issue:`45715`)
- Bug in :meth:`.ExponentialMovingWindow.mean` with ``axis=1`` and ``engine='numba'`` when the :class:`DataFrame` has more columns than rows (:issue:`46086`)
- Bug when using ``engine="numba"`` would return the same jitted function when modifying ``engine_kwargs`` (:issue:`46086`)
- Bug in :meth:`.DataFrameGroupBy.transform` fails when ``axis=1`` and ``func`` is ``"first"`` or ``"last"`` (:issue:`45986`)
- Bug in :meth:`.DataFrameGroupBy.cumsum` with ``skipna=False`` giving incorrect results (:issue:`46216`)
- Bug in :meth:`.DataFrameGroupBy.sum`, :meth:`.SeriesGroupBy.sum`, :meth:`.DataFrameGroupBy.prod`, :meth:`.SeriesGroupBy.prod, :meth:`.DataFrameGroupBy.cumsum`, and :meth:`.SeriesGroupBy.cumsum` with integer dtypes losing precision (:issue:`37493`)
- Bug in :meth:`.DataFrameGroupBy.cumsum` and :meth:`.SeriesGroupBy.cumsum` with ``timedelta64[ns]`` dtype failing to recognize ``NaT`` as a null value (:issue:`46216`)
- Bug in :meth:`.DataFrameGroupBy.cumsum` and :meth:`.SeriesGroupBy.cumsum` with integer dtypes causing overflows when sum was bigger than maximum of dtype (:issue:`37493`)
- Bug in :meth:`.DataFrameGroupBy.cummin`, :meth:`.SeriesGroupBy.cummin`, :meth:`.DataFrameGroupBy.cummax` and :meth:`.SeriesGroupBy.cummax` with nullable dtypes incorrectly altering the original data in place (:issue:`46220`)
- Bug in :meth:`DataFrame.groupby` raising error when ``None`` is in first level of :class:`MultiIndex` (:issue:`47348`)
- Bug in :meth:`.DataFrameGroupBy.cummax` and :meth:`.SeriesGroupBy.cummax` with ``int64`` dtype with leading value being the smallest possible int64 (:issue:`46382`)
- Bug in :meth:`.DataFrameGroupBy.cumprod` and :meth:`.SeriesGroupBy.cumprod` ``NaN`` influences calculation in different columns with ``skipna=False`` (:issue:`48064`)
- Bug in :meth:`.DataFrameGroupBy.max` and :meth:`.SeriesGroupBy.max` with empty groups and ``uint64`` dtype incorrectly raising ``RuntimeError`` (:issue:`46408`)
- Bug in :meth:`.DataFrameGroupBy.apply` and :meth:`.SeriesGroupBy.apply` would fail when ``func`` was a string and args or kwargs were supplied (:issue:`46479`)
- Bug in :meth:`SeriesGroupBy.apply` would incorrectly name its result when there was a unique group (:issue:`46369`)
- Bug in :meth:`.Rolling.sum` and :meth:`.Rolling.mean` would give incorrect result with window of same values (:issue:`42064`, :issue:`46431`)
- Bug in :meth:`.Rolling.var` and :meth:`.Rolling.std` would give non-zero result with window of same values (:issue:`42064`)
- Bug in :meth:`.Rolling.skew` and :meth:`.Rolling.kurt` would give NaN with window of same values (:issue:`30993`)
- Bug in :meth:`.Rolling.var` would segfault calculating weighted variance when window size was larger than data size (:issue:`46760`)
- Bug in :meth:`Grouper.__repr__` where ``dropna`` was not included. Now it is (:issue:`46754`)
- Bug in :meth:`DataFrame.rolling` gives ValueError when center=True, axis=1 and win_type is specified (:issue:`46135`)
- Bug in :meth:`.DataFrameGroupBy.describe` and :meth:`.SeriesGroupBy.describe` produces inconsistent results for empty datasets (:issue:`41575`)
- Bug in :meth:`DataFrame.resample` reduction methods when used with ``on`` would attempt to aggregate the provided column (:issue:`47079`)
- Bug in :meth:`DataFrame.groupby` and :meth:`Series.groupby` would not respect ``dropna=False`` when the input DataFrame/Series had a NaN values in a :class:`MultiIndex` (:issue:`46783`)
- Bug in :meth:`DataFrameGroupBy.resample` raises ``KeyError`` when getting the result from a key list which misses the resample key (:issue:`47362`)
- Bug in :meth:`DataFrame.groupby` would lose index columns when the DataFrame is empty for transforms, like fillna (:issue:`47787`)
- Bug in :meth:`DataFrame.groupby` and :meth:`Series.groupby` with ``dropna=False`` and ``sort=False`` would put any null groups at the end instead the order that they are encountered (:issue:`46584`)

Reshaping
^^^^^^^^^
- Bug in :func:`concat` between a :class:`Series` with integer dtype and another with :class:`CategoricalDtype` with integer categories and containing ``NaN`` values casting to object dtype instead of ``float64`` (:issue:`45359`)
- Bug in :func:`get_dummies` that selected object and categorical dtypes but not string (:issue:`44965`)
- Bug in :meth:`DataFrame.align` when aligning a :class:`MultiIndex` to a :class:`Series` with another :class:`MultiIndex` (:issue:`46001`)
- Bug in concatenation with ``IntegerDtype``, or ``FloatingDtype`` arrays where the resulting dtype did not mirror the behavior of the non-nullable dtypes (:issue:`46379`)
- Bug in :func:`concat` losing dtype of columns when ``join="outer"`` and ``sort=True`` (:issue:`47329`)
- Bug in :func:`concat` not sorting the column names when ``None`` is included (:issue:`47331`)
- Bug in :func:`concat` with identical key leads to error when indexing :class:`MultiIndex` (:issue:`46519`)
- Bug in :func:`pivot_table` raising ``TypeError`` when ``dropna=True`` and aggregation column has extension array dtype (:issue:`47477`)
- Bug in :func:`merge` raising error for ``how="cross"`` when using ``FIPS`` mode in ssl library (:issue:`48024`)
- Bug in :meth:`DataFrame.join` with a list when using suffixes to join DataFrames with duplicate column names (:issue:`46396`)
- Bug in :meth:`DataFrame.pivot_table` with ``sort=False`` results in sorted index (:issue:`17041`)
- Bug in :meth:`concat` when ``axis=1`` and ``sort=False`` where the resulting Index was a :class:`Int64Index` instead of a :class:`RangeIndex` (:issue:`46675`)
- Bug in :meth:`wide_to_long` raises when ``stubnames`` is missing in columns and ``i`` contains string dtype column (:issue:`46044`)
- Bug in :meth:`DataFrame.join` with categorical index results in unexpected reordering (:issue:`47812`)

Sparse
^^^^^^
- Bug in :meth:`Series.where` and :meth:`DataFrame.where` with ``SparseDtype`` failing to retain the array's ``fill_value`` (:issue:`45691`)
- Bug in :meth:`SparseArray.unique` fails to keep original elements order (:issue:`47809`)

ExtensionArray
^^^^^^^^^^^^^^
- Bug in :meth:`IntegerArray.searchsorted` and :meth:`FloatingArray.searchsorted` returning inconsistent results when acting on ``np.nan`` (:issue:`45255`)

Styler
^^^^^^
- Bug when attempting to apply styling functions to an empty DataFrame subset (:issue:`45313`)
- Bug in :class:`CSSToExcelConverter` leading to ``TypeError`` when border color provided without border style for ``xlsxwriter`` engine (:issue:`42276`)
- Bug in :meth:`Styler.set_sticky` leading to white text on white background in dark mode (:issue:`46984`)
- Bug in :meth:`Styler.to_latex` causing ``UnboundLocalError`` when ``clines="all;data"`` and the ``DataFrame`` has no rows. (:issue:`47203`)
- Bug in :meth:`Styler.to_excel` when using ``vertical-align: middle;`` with ``xlsxwriter`` engine (:issue:`30107`)
- Bug when applying styles to a DataFrame with boolean column labels (:issue:`47838`)

Metadata
^^^^^^^^
- Fixed metadata propagation in :meth:`DataFrame.melt` (:issue:`28283`)
- Fixed metadata propagation in :meth:`DataFrame.explode` (:issue:`28283`)

Other
^^^^^

.. ***DO NOT USE THIS SECTION***

- Bug in :func:`.assert_index_equal` with ``names=True`` and ``check_order=False`` not checking names (:issue:`47328`)

.. ---------------------------------------------------------------------------
.. _whatsnew_150.contributors:

Contributors
~~~~~~~~~~~~

.. contributors:: v1.4.4..v1.5.0

# ===== SOURCE: https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/source/whatsnew/v2.0.0.rst =====

.. _whatsnew_200:

What's new in 2.0.0 (April 3, 2023)
-----------------------------------

These are the changes in pandas 2.0.0. See :ref:`release` for a full changelog
including other versions of pandas.

{{ header }}

.. ---------------------------------------------------------------------------
.. _whatsnew_200.enhancements:

Enhancements
~~~~~~~~~~~~

.. _whatsnew_200.enhancements.optional_dependency_management_pip:

Installing optional dependencies with pip extras
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When installing pandas using pip, sets of optional dependencies can also be installed by specifying extras.

.. code-block:: bash

  pip install "pandas[performance, aws]>=2.0.0"

The available extras, found in the :ref:`installation guide<install.dependencies>`, are
``[all, performance, computation, fss, aws, gcp, excel, parquet, feather, hdf5, spss, postgresql, mysql,
sql-other, html, xml, plot, output_formatting, clipboard, compression, test]`` (:issue:`39164`).

.. _whatsnew_200.enhancements.index_can_hold_numpy_numeric_dtypes:

:class:`Index` can now hold numpy numeric dtypes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is now possible to use any numpy numeric dtype in a :class:`Index` (:issue:`42717`).

Previously it was only possible to use ``int64``, ``uint64`` & ``float64`` dtypes:

.. code-block:: ipython

    In [1]: pd.Index([1, 2, 3], dtype=np.int8)
    Out[1]: Int64Index([1, 2, 3], dtype="int64")
    In [2]: pd.Index([1, 2, 3], dtype=np.uint16)
    Out[2]: UInt64Index([1, 2, 3], dtype="uint64")
    In [3]: pd.Index([1, 2, 3], dtype=np.float32)
    Out[3]: Float64Index([1.0, 2.0, 3.0], dtype="float64")

:class:`Int64Index`, :class:`UInt64Index` & :class:`Float64Index` were deprecated in pandas
version 1.4 and have now been removed. Instead :class:`Index` should be used directly, and
can it now take all numpy numeric dtypes, i.e.
``int8``/ ``int16``/``int32``/``int64``/``uint8``/``uint16``/``uint32``/``uint64``/``float32``/``float64`` dtypes:

.. ipython:: python

    pd.Index([1, 2, 3], dtype=np.int8)
    pd.Index([1, 2, 3], dtype=np.uint16)
    pd.Index([1, 2, 3], dtype=np.float32)

The ability for :class:`Index` to hold the numpy numeric dtypes has meant some changes in pandas
functionality. In particular, operations that previously were forced to create 64-bit indexes,
can now create indexes with lower bit sizes, e.g. 32-bit indexes.

Below is a possibly non-exhaustive list of changes:

1. Instantiating using a numpy numeric array now follows the dtype of the numpy array.
   Previously, all indexes created from numpy numeric arrays were forced to 64-bit. Now,
   for example, ``Index(np.array([1, 2, 3]))`` will be ``int32`` on 32-bit systems, where
   it previously would have been ``int64`` even on 32-bit systems.
   Instantiating :class:`Index` using a list of numbers will still return 64bit dtypes,
   e.g. ``Index([1, 2, 3])`` will have a ``int64`` dtype, which is the same as previously.
2. The various numeric datetime attributes of :class:`DatetimeIndex` (:attr:`~DatetimeIndex.day`,
   :attr:`~DatetimeIndex.month`, :attr:`~DatetimeIndex.year` etc.) were previously in of
   dtype ``int64``, while they were ``int32`` for :class:`arrays.DatetimeArray`. They are now
   ``int32`` on :class:`DatetimeIndex` also:

   .. ipython:: python

       idx = pd.date_range(start='1/1/2018', periods=3, freq='ME')
       idx.array.year
       idx.year

3. Level dtypes on Indexes from :meth:`Series.sparse.from_coo` are now of dtype ``int32``,
   the same as they are on the ``rows``/``cols`` on a scipy sparse matrix. Previously they
   were of dtype ``int64``.

   .. ipython:: python

       from scipy import sparse
       A = sparse.coo_matrix(
           ([3.0, 1.0, 2.0], ([1, 0, 0], [0, 2, 3])), shape=(3, 4)
       )
       ser = pd.Series.sparse.from_coo(A)
       ser.index.dtypes

4. :class:`Index` cannot be instantiated using a float16 dtype. Previously instantiating
   an :class:`Index` using dtype ``float16`` resulted in a :class:`Float64Index` with a
   ``float64`` dtype. It now raises a ``NotImplementedError``:

   .. ipython:: python
       :okexcept:

       pd.Index([1, 2, 3], dtype=np.float16)


.. _whatsnew_200.enhancements.io_dtype_backend:

Argument ``dtype_backend``, to return pyarrow-backed or numpy-backed nullable dtypes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following functions gained a new keyword ``dtype_backend`` (:issue:`36712`)

* :func:`read_csv`
* :func:`read_clipboard`
* :func:`read_fwf`
* :func:`read_excel`
* :func:`read_html`
* :func:`read_xml`
* :func:`read_json`
* :func:`read_sql`
* :func:`read_sql_query`
* :func:`read_sql_table`
* :func:`read_parquet`
* :func:`read_orc`
* :func:`read_feather`
* :func:`read_spss`
* :func:`to_numeric`
* :meth:`DataFrame.convert_dtypes`
* :meth:`Series.convert_dtypes`

When this option is set to ``"numpy_nullable"`` it will return a :class:`DataFrame` that is
backed by nullable dtypes.

When this keyword is set to ``"pyarrow"``, then these functions will return pyarrow-backed nullable :class:`ArrowDtype` DataFrames (:issue:`48957`, :issue:`49997`):

* :func:`read_csv`
* :func:`read_clipboard`
* :func:`read_fwf`
* :func:`read_excel`
* :func:`read_html`
* :func:`read_xml`
* :func:`read_json`
* :func:`read_sql`
* :func:`read_sql_query`
* :func:`read_sql_table`
* :func:`read_parquet`
* :func:`read_orc`
* :func:`read_feather`
* :func:`read_spss`
* :func:`to_numeric`
* :meth:`DataFrame.convert_dtypes`
* :meth:`Series.convert_dtypes`

.. ipython:: python

    import io
    data = io.StringIO("""a,b,c,d,e,f,g,h,i
        1,2.5,True,a,,,,,
        3,4.5,False,b,6,7.5,True,a,
    """)
    df = pd.read_csv(data, dtype_backend="pyarrow")
    df.dtypes

    data.seek(0)
    df_pyarrow = pd.read_csv(data, dtype_backend="pyarrow", engine="pyarrow")
    df_pyarrow.dtypes

Copy-on-Write improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^

- A new lazy copy mechanism that defers the copy until the object in question is modified
  was added to the methods listed in
  :ref:`Copy-on-Write optimizations <copy_on_write.optimizations>`.
  These methods return views when Copy-on-Write is enabled, which provides a significant
  performance improvement compared to the regular execution (:issue:`49473`).

- Accessing a single column of a DataFrame as a Series (e.g. ``df["col"]``) now always
  returns a new object every time it is constructed when Copy-on-Write is enabled (not
  returning multiple times an identical, cached Series object). This ensures that those
  Series objects correctly follow the Copy-on-Write rules (:issue:`49450`)

- The :class:`Series` constructor will now create a lazy copy (deferring the copy until
  a modification to the data happens) when constructing a Series from an existing
  Series with the default of ``copy=False`` (:issue:`50471`)

- The :class:`DataFrame` constructor will now create a lazy copy (deferring the copy until
  a modification to the data happens) when constructing from an existing
  :class:`DataFrame` with the default of ``copy=False`` (:issue:`51239`)

- The :class:`DataFrame` constructor, when constructing a DataFrame from a dictionary
  of Series objects and specifying ``copy=False``, will now use a lazy copy
  of those Series objects for the columns of the DataFrame (:issue:`50777`)

- The :class:`DataFrame` constructor, when constructing a DataFrame from a
  :class:`Series` or :class:`Index` and specifying ``copy=False``, will
  now respect Copy-on-Write.

- The :class:`DataFrame` and :class:`Series` constructors, when constructing from
  a NumPy array, will now copy the array by default to avoid mutating
  the :class:`DataFrame` / :class:`Series`
  when mutating the array. Specify ``copy=False`` to get the old behavior.
  When setting ``copy=False`` pandas does not guarantee correct Copy-on-Write
  behavior when the NumPy array is modified after creation of the
  :class:`DataFrame` / :class:`Series`.

- The :meth:`DataFrame.from_records` will now respect Copy-on-Write when called
  with a :class:`DataFrame`.

- Trying to set values using chained assignment (for example, ``df["a"][1:3] = 0``)
  will now always raise a warning when Copy-on-Write is enabled. In this mode,
  chained assignment can never work because we are always setting into a temporary
  object that is the result of an indexing operation (getitem), which under
  Copy-on-Write always behaves as a copy. Thus, assigning through a chain
  can never update the original Series or DataFrame. Therefore, an informative
  warning is raised to the user to avoid silently doing nothing (:issue:`49467`)

- :meth:`DataFrame.replace` will now respect the Copy-on-Write mechanism
  when ``inplace=True``.

- :meth:`DataFrame.transpose` will now respect the Copy-on-Write mechanism.

- Arithmetic operations that can be inplace, e.g. ``ser *= 2`` will now respect the
  Copy-on-Write mechanism.

- :meth:`DataFrame.__getitem__` will now respect the Copy-on-Write mechanism when the
  :class:`DataFrame` has :class:`MultiIndex` columns.

- :meth:`Series.__getitem__` will now respect the Copy-on-Write mechanism when the
   :class:`Series` has a :class:`MultiIndex`.

- :meth:`Series.view` will now respect the Copy-on-Write mechanism.

Copy-on-Write can be enabled through one of

.. code-block:: python

    pd.set_option("mode.copy_on_write", True)


.. code-block:: python

    pd.options.mode.copy_on_write = True

Alternatively, copy on write can be enabled locally through:

.. code-block:: python

    with pd.option_context("mode.copy_on_write", True):
        ...

.. _whatsnew_200.enhancements.other:

Other enhancements
^^^^^^^^^^^^^^^^^^
- Added support for ``str`` accessor methods when using :class:`ArrowDtype`  with a ``pyarrow.string`` type (:issue:`50325`)
- Added support for ``dt`` accessor methods when using :class:`ArrowDtype` with a ``pyarrow.timestamp`` type (:issue:`50954`)
- :func:`read_sas` now supports using ``encoding='infer'`` to correctly read and use the encoding specified by the sas file. (:issue:`48048`)
- :meth:`.DataFrameGroupBy.quantile`, :meth:`.SeriesGroupBy.quantile` and :meth:`.DataFrameGroupBy.std` now preserve nullable dtypes instead of casting to numpy dtypes (:issue:`37493`)
- :meth:`.DataFrameGroupBy.std`, :meth:`.SeriesGroupBy.std` now support datetime64, timedelta64, and :class:`DatetimeTZDtype` dtypes (:issue:`48481`)
- :meth:`Series.add_suffix`, :meth:`DataFrame.add_suffix`, :meth:`Series.add_prefix` and :meth:`DataFrame.add_prefix` support an ``axis`` argument. If ``axis`` is set, the default behaviour of which axis to consider can be overwritten (:issue:`47819`)
- :func:`.testing.assert_frame_equal` now shows the first element where the DataFrames differ, analogously to ``pytest``'s output (:issue:`47910`)
- Added ``index`` parameter to :meth:`DataFrame.to_dict` (:issue:`46398`)
- Added support for extension array dtypes in :func:`merge` (:issue:`44240`)
- Added metadata propagation for binary operators on :class:`DataFrame` (:issue:`28283`)
- Added ``cumsum``, ``cumprod``, ``cummin`` and ``cummax`` to the ``ExtensionArray`` interface via ``_accumulate`` (:issue:`28385`)
- :class:`.CategoricalConversionWarning`, :class:`.InvalidComparison`, :class:`.InvalidVersion`, :class:`.LossySetitemError`, and :class:`.NoBufferPresent` are now exposed in ``pandas.errors`` (:issue:`27656`)
- Fix ``test`` optional_extra by adding missing test package ``pytest-asyncio`` (:issue:`48361`)
- :func:`DataFrame.astype` exception message thrown improved to include column name when type conversion is not possible. (:issue:`47571`)
- :func:`date_range` now supports a ``unit`` keyword ("s", "ms", "us", or "ns") to specify the desired resolution of the output index (:issue:`49106`)
- :func:`timedelta_range` now supports a ``unit`` keyword ("s", "ms", "us", or "ns") to specify the desired resolution of the output index (:issue:`49824`)
- :meth:`DataFrame.to_json` now supports a ``mode`` keyword with supported inputs 'w' and 'a'. Defaulting to 'w', 'a' can be used when lines=True and orient='records' to append record oriented json lines to an existing json file. (:issue:`35849`)
- Added ``name`` parameter to :meth:`IntervalIndex.from_breaks`, :meth:`IntervalIndex.from_arrays` and :meth:`IntervalIndex.from_tuples` (:issue:`48911`)
- Improve exception message when using :func:`.testing.assert_frame_equal` on a :class:`DataFrame` to include the column that is compared (:issue:`50323`)
- Improved error message for :func:`merge_asof` when join-columns were duplicated (:issue:`50102`)
- Added support for extension array dtypes to :func:`get_dummies` (:issue:`32430`)
- Added :meth:`Index.infer_objects` analogous to :meth:`Series.infer_objects` (:issue:`50034`)
- Added ``copy`` parameter to :meth:`Series.infer_objects` and :meth:`DataFrame.infer_objects`, passing ``False`` will avoid making copies for series or columns that are already non-object or where no better dtype can be inferred (:issue:`50096`)
- :meth:`DataFrame.plot.hist` now recognizes ``xlabel`` and ``ylabel`` arguments (:issue:`49793`)
- :meth:`Series.drop_duplicates` has gained ``ignore_index`` keyword to reset index (:issue:`48304`)
- :meth:`Series.dropna` and :meth:`DataFrame.dropna` has gained ``ignore_index`` keyword to reset index (:issue:`31725`)
- Improved error message in :func:`to_datetime` for non-ISO8601 formats, informing users about the position of the first error (:issue:`50361`)
- Improved error message when trying to align :class:`DataFrame` objects (for example, in :func:`DataFrame.compare`) to clarify that "identically labelled" refers to both index and columns (:issue:`50083`)
- Added support for :meth:`Index.min` and :meth:`Index.max` for pyarrow string dtypes (:issue:`51397`)
- Added :meth:`DatetimeIndex.as_unit` and :meth:`TimedeltaIndex.as_unit` to convert to different resolutions; supported resolutions are "s", "ms", "us", and "ns" (:issue:`50616`)
- Added :meth:`Series.dt.unit` and :meth:`Series.dt.as_unit` to convert to different resolutions; supported resolutions are "s", "ms", "us", and "ns" (:issue:`51223`)
- Added new argument ``dtype`` to :func:`read_sql` to be consistent with :func:`read_sql_query` (:issue:`50797`)
- :func:`read_csv`, :func:`read_table`, :func:`read_fwf` and :func:`read_excel` now accept ``date_format`` (:issue:`50601`)
- :func:`to_datetime` now accepts ``"ISO8601"`` as an argument to ``format``, which will match any ISO8601 string (but possibly not identically-formatted) (:issue:`50411`)
- :func:`to_datetime` now accepts ``"mixed"`` as an argument to ``format``, which will infer the format for each element individually (:issue:`50972`)
- Added new argument ``engine`` to :func:`read_json` to support parsing JSON with pyarrow by specifying ``engine="pyarrow"`` (:issue:`48893`)
- Added support for SQLAlchemy 2.0 (:issue:`40686`)
- Added support for ``decimal`` parameter when ``engine="pyarrow"`` in :func:`read_csv` (:issue:`51302`)
- :class:`Index` set operations :meth:`Index.union`, :meth:`Index.intersection`, :meth:`Index.difference`, and :meth:`Index.symmetric_difference` now support ``sort=True``, which will always return a sorted result, unlike the default ``sort=None`` which does not sort in some cases (:issue:`25151`)
- Added new escape mode "latex-math" to avoid escaping "$" in formatter (:issue:`50040`)

.. ---------------------------------------------------------------------------
.. _whatsnew_200.notable_bug_fixes:

Notable bug fixes
~~~~~~~~~~~~~~~~~

These are bug fixes that might have notable behavior changes.

.. _whatsnew_200.notable_bug_fixes.cumsum_cumprod_overflow:

:meth:`.DataFrameGroupBy.cumsum` and :meth:`.DataFrameGroupBy.cumprod` overflow instead of lossy casting to float
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In previous versions we cast to float when applying ``cumsum`` and ``cumprod`` which
lead to incorrect results even if the result could be hold by ``int64`` dtype.
Additionally, the aggregation overflows consistent with numpy and the regular
:meth:`DataFrame.cumprod` and :meth:`DataFrame.cumsum` methods when the limit of
``int64`` is reached (:issue:`37493`).

*Old Behavior*

.. code-block:: ipython

    In [1]: df = pd.DataFrame({"key": ["b"] * 7, "value": 625})
    In [2]: df.groupby("key")["value"].cumprod()[5]
    Out[2]: 5.960464477539062e+16

We return incorrect results with the 6th value.

*New Behavior*

.. ipython:: python

    df = pd.DataFrame({"key": ["b"] * 7, "value": 625})
    df.groupby("key")["value"].cumprod()

We overflow with the 7th value, but the 6th value is still correct.

.. _whatsnew_200.notable_bug_fixes.groupby_nth_filter:

:meth:`.DataFrameGroupBy.nth` and :meth:`.SeriesGroupBy.nth` now behave as filtrations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In previous versions of pandas, :meth:`.DataFrameGroupBy.nth` and
:meth:`.SeriesGroupBy.nth` acted as if they were aggregations. However, for most
inputs ``n``, they may return either zero or multiple rows per group. This means
that they are filtrations, similar to e.g. :meth:`.DataFrameGroupBy.head`. pandas
now treats them as filtrations (:issue:`13666`).

.. ipython:: python

    df = pd.DataFrame({"a": [1, 1, 2, 1, 2], "b": [np.nan, 2.0, 3.0, 4.0, 5.0]})
    gb = df.groupby("a")

*Old Behavior*

.. code-block:: ipython

    In [5]: gb.nth(n=1)
    Out[5]:
       A    B
    1  1  2.0
    4  2  5.0

*New Behavior*

.. ipython:: python

    gb.nth(n=1)

In particular, the index of the result is derived from the input by selecting
the appropriate rows. Also, when ``n`` is larger than the group, no rows instead of
``NaN`` is returned.

*Old Behavior*

.. code-block:: ipython

    In [5]: gb.nth(n=3, dropna="any")
    Out[5]:
        B
    A
    1 NaN
    2 NaN

*New Behavior*

.. ipython:: python

    gb.nth(n=3, dropna="any")

.. ---------------------------------------------------------------------------
.. _whatsnew_200.api_breaking:

Backwards incompatible API changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _whatsnew_200.api_breaking.unsupported_datetimelike_dtype_arg:

Construction with datetime64 or timedelta64 dtype with unsupported resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In past versions, when constructing a :class:`Series` or :class:`DataFrame` and
passing a "datetime64" or "timedelta64" dtype with unsupported resolution
(i.e. anything other than "ns"), pandas would silently replace the given dtype
with its nanosecond analogue:

*Previous behavior*:

.. code-block:: ipython

   In [5]: pd.Series(["2016-01-01"], dtype="datetime64[s]")
   Out[5]:
   0   2016-01-01
   dtype: datetime64[ns]

   In [6] pd.Series(["2016-01-01"], dtype="datetime64[D]")
   Out[6]:
   0   2016-01-01
   dtype: datetime64[ns]

In pandas 2.0 we support resolutions "s", "ms", "us", and "ns". When passing
a supported dtype (e.g. "datetime64[s]"), the result now has exactly
the requested dtype:

*New behavior*:

.. ipython:: python

   pd.Series(["2016-01-01"], dtype="datetime64[s]")

With an un-supported dtype, pandas now raises instead of silently swapping in
a supported dtype:

*New behavior*:

.. ipython:: python
   :okexcept:

   pd.Series(["2016-01-01"], dtype="datetime64[D]")

.. _whatsnew_200.api_breaking.value_counts:

Value counts sets the resulting name to ``count``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In past versions, when running :meth:`Series.value_counts`, the result would inherit
the original object's name, and the result index would be nameless. This would cause
confusion when resetting the index, and the column names would not correspond with the
column values.
Now, the result name will be ``'count'`` (or ``'proportion'`` if ``normalize=True`` was passed),
and the index will be named after the original object (:issue:`49497`).

*Previous behavior*:

.. code-block:: ipython

    In [8]: pd.Series(['quetzal', 'quetzal', 'elk'], name='animal').value_counts()

    Out[2]:
    quetzal    2
    elk        1
    Name: animal, dtype: int64

*New behavior*:

.. ipython:: python

    pd.Series(['quetzal', 'quetzal', 'elk'], name='animal').value_counts()

Likewise for other ``value_counts`` methods (for example, :meth:`DataFrame.value_counts`).

.. _whatsnew_200.api_breaking.astype_to_unsupported_datetimelike:

Disallow astype conversion to non-supported datetime64/timedelta64 dtypes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In previous versions, converting a :class:`Series` or :class:`DataFrame`
from ``datetime64[ns]`` to a different ``datetime64[X]`` dtype would return
with ``datetime64[ns]`` dtype instead of the requested dtype. In pandas 2.0,
support is added for "datetime64[s]", "datetime64[ms]", and "datetime64[us]" dtypes,
so converting to those dtypes gives exactly the requested dtype:

*Previous behavior*:

.. ipython:: python

   idx = pd.date_range("2016-01-01", periods=3)
   ser = pd.Series(idx)

*Previous behavior*:

.. code-block:: ipython

   In [4]: ser.astype("datetime64[s]")
   Out[4]:
   0   2016-01-01
   1   2016-01-02
   2   2016-01-03
   dtype: datetime64[ns]

With the new behavior, we get exactly the requested dtype:

*New behavior*:

.. ipython:: python

   ser.astype("datetime64[s]")

For non-supported resolutions e.g. "datetime64[D]", we raise instead of silently
ignoring the requested dtype:

*New behavior*:

.. ipython:: python
   :okexcept:

   ser.astype("datetime64[D]")

For conversion from ``timedelta64[ns]`` dtypes, the old behavior converted
to a floating point format.

*Previous behavior*:

.. ipython:: python

   idx = pd.timedelta_range("1 Day", periods=3)
   ser = pd.Series(idx)

*Previous behavior*:

.. code-block:: ipython

   In [7]: ser.astype("timedelta64[s]")
   Out[7]:
   0     86400.0
   1    172800.0
   2    259200.0
   dtype: float64

   In [8]: ser.astype("timedelta64[D]")
   Out[8]:
   0    1.0
   1    2.0
   2    3.0
   dtype: float64

The new behavior, as for datetime64, either gives exactly the requested dtype or raises:

*New behavior*:

.. ipython:: python
   :okexcept:

   ser.astype("timedelta64[s]")
   ser.astype("timedelta64[D]")

.. _whatsnew_200.api_breaking.default_to_stdlib_tzinfos:

UTC and fixed-offset timezones default to standard-library tzinfo objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In previous versions, the default ``tzinfo`` object used to represent UTC
was ``pytz.UTC``. In pandas 2.0, we default to ``datetime.timezone.utc`` instead.
Similarly, for timezones represent fixed UTC offsets, we use ``datetime.timezone``
objects instead of ``pytz.FixedOffset`` objects. See (:issue:`34916`)

*Previous behavior*:

.. code-block:: ipython

   In [2]: ts = pd.Timestamp("2016-01-01", tz="UTC")
   In [3]: type(ts.tzinfo)
   Out[3]: pytz.UTC

   In [4]: ts2 = pd.Timestamp("2016-01-01 04:05:06-07:00")
   In [3]: type(ts2.tzinfo)
   Out[5]: pytz._FixedOffset

*New behavior*:

.. ipython:: python

   ts = pd.Timestamp("2016-01-01", tz="UTC")
   type(ts.tzinfo)

   ts2 = pd.Timestamp("2016-01-01 04:05:06-07:00")
   type(ts2.tzinfo)

For timezones that are neither UTC nor fixed offsets, e.g. "US/Pacific", we
continue to default to ``pytz`` objects.

.. _whatsnew_200.api_breaking.zero_len_indexes:

Empty DataFrames/Series will now default to have a ``RangeIndex``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before, constructing an empty (where ``data`` is ``None`` or an empty list-like argument) :class:`Series` or :class:`DataFrame` without
specifying the axes (``index=None``, ``columns=None``) would return the axes as empty :class:`Index` with object dtype.

Now, the axes return an empty :class:`RangeIndex` (:issue:`49572`).

*Previous behavior*:

.. code-block:: ipython

   In [8]: pd.Series().index
   Out[8]:
   Index([], dtype='object')

   In [9] pd.DataFrame().axes
   Out[9]:
   [Index([], dtype='object'), Index([], dtype='object')]

*New behavior*:

.. ipython:: python

   pd.Series().index
   pd.DataFrame().axes

.. _whatsnew_200.api_breaking.to_latex:

DataFrame to LaTeX has a new render engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The existing :meth:`DataFrame.to_latex` has been restructured to utilise the
extended implementation previously available under :meth:`.Styler.to_latex`.
The arguments signature is similar, albeit ``col_space`` has been removed since
it is ignored by LaTeX engines. This render engine also requires ``jinja2`` as a
dependency which needs to be installed, since rendering is based upon jinja2 templates.

The pandas latex options below are no longer used and have been removed. The generic
max rows and columns arguments remain but for this functionality should be replaced
by the Styler equivalents.
The alternative options giving similar functionality are indicated below:

- ``display.latex.escape``: replaced with ``styler.format.escape``,
- ``display.latex.longtable``: replaced with ``styler.latex.environment``,
- ``display.latex.multicolumn``, ``display.latex.multicolumn_format`` and
  ``display.latex.multirow``: replaced with ``styler.sparse.rows``,
  ``styler.sparse.columns``, ``styler.latex.multirow_align`` and
  ``styler.latex.multicol_align``,
- ``display.latex.repr``: replaced with ``styler.render.repr``,
- ``display.max_rows`` and ``display.max_columns``: replace with
  ``styler.render.max_rows``, ``styler.render.max_columns`` and
  ``styler.render.max_elements``.

Note that due to this change some defaults have also changed:

- ``multirow`` now defaults to *True*.
- ``multirow_align`` defaults to *"r"* instead of *"l"*.
- ``multicol_align`` defaults to *"r"* instead of *"l"*.
- ``escape`` now defaults to *False*.

Note that the behaviour of ``_repr_latex_`` is also changed. Previously
setting ``display.latex.repr`` would generate LaTeX only when using nbconvert for a
JupyterNotebook, and not when the user is running the notebook. Now the
``styler.render.repr`` option allows control of the specific output
within JupyterNotebooks for operations (not just on nbconvert). See :issue:`39911`.

.. _whatsnew_200.api_breaking.deps:

Increased minimum versions for dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Some minimum supported versions of dependencies were updated.
If installed, we now require:

+-------------------+-----------------+----------+---------+
| Package           | Minimum Version | Required | Changed |
+===================+=================+==========+=========+
| mypy (dev)        | 1.0             |          |    X    |
+-------------------+-----------------+----------+---------+
| pytest (dev)      | 7.0.0           |          |    X    |
+-------------------+-----------------+----------+---------+
| pytest-xdist (dev)| 2.2.0           |          |    X    |
+-------------------+-----------------+----------+---------+
| hypothesis (dev)  | 6.34.2          |          |    X    |
+-------------------+-----------------+----------+---------+
| python-dateutil   | 2.8.2           |    X     |    X    |
+-------------------+-----------------+----------+---------+
| tzdata            | 2022.1          |    X     |    X    |
+-------------------+-----------------+----------+---------+

For `optional libraries <https://pandas.pydata.org/docs/getting_started/install.html>`_ the general recommendation is to use the latest version.
The following table lists the lowest version per library that is currently being tested throughout the development of pandas.
Optional libraries below the lowest tested version may still work, but are not considered supported.

+-----------------+-----------------+---------+
| Package         | Minimum Version | Changed |
+=================+=================+=========+
| pyarrow         | 7.0.0           |    X    |
+-----------------+-----------------+---------+
| matplotlib      | 3.6.1           |    X    |
+-----------------+-----------------+---------+
| fastparquet     | 0.6.3           |    X    |
+-----------------+-----------------+---------+
| xarray          | 0.21.0          |    X    |
+-----------------+-----------------+---------+

See :ref:`install.dependencies` and :ref:`install.optional_dependencies` for more.

Datetimes are now parsed with a consistent format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the past, :func:`to_datetime` guessed the format for each element independently. This was appropriate for some cases where elements had mixed date formats - however, it would regularly cause problems when users expected a consistent format but the function would switch formats between elements. As of version 2.0.0, parsing will use a consistent format, determined by the first non-NA value (unless the user specifies a format, in which case that is used).

*Old behavior*:

.. code-block:: ipython

   In [1]: ser = pd.Series(['13-01-2000', '12-01-2000'])
   In [2]: pd.to_datetime(ser)
   Out[2]:
   0   2000-01-13
   1   2000-12-01
   dtype: datetime64[ns]

*New behavior*:

.. ipython:: python
    :okwarning:

     ser = pd.Series(['13-01-2000', '12-01-2000'])
     pd.to_datetime(ser)

Note that this affects :func:`read_csv` as well.

If you still need to parse dates with inconsistent formats, you can use
``format='mixed'`` (possibly alongside ``dayfirst``) ::

     ser = pd.Series(['13-01-2000', '12 January 2000'])
     pd.to_datetime(ser, format='mixed', dayfirst=True)

or, if your formats are all ISO8601 (but possibly not identically-formatted) ::

     ser = pd.Series(['2020-01-01', '2020-01-01 03:00'])
     pd.to_datetime(ser, format='ISO8601')

.. _whatsnew_200.api_breaking.other:

Other API changes
^^^^^^^^^^^^^^^^^
- The ``tz``, ``nanosecond``, and ``unit`` keywords in the :class:`Timestamp` constructor are now keyword-only (:issue:`45307`, :issue:`32526`)
- Passing ``nanoseconds`` greater than 999 or less than 0 in :class:`Timestamp` now raises a ``ValueError`` (:issue:`48538`, :issue:`48255`)
- :func:`read_csv`: specifying an incorrect number of columns with ``index_col`` of now raises ``ParserError`` instead of ``IndexError`` when using the c parser.
- Default value of ``dtype`` in :func:`get_dummies` is changed to ``bool`` from ``uint8`` (:issue:`45848`)
- :meth:`DataFrame.astype`, :meth:`Series.astype`, and :meth:`DatetimeIndex.astype` casting datetime64 data to any of "datetime64[s]", "datetime64[ms]", "datetime64[us]" will return an object with the given resolution instead of coercing back to "datetime64[ns]" (:issue:`48928`)
- :meth:`DataFrame.astype`, :meth:`Series.astype`, and :meth:`DatetimeIndex.astype` casting timedelta64 data to any of "timedelta64[s]", "timedelta64[ms]", "timedelta64[us]" will return an object with the given resolution instead of coercing to "float64" dtype (:issue:`48963`)
- :meth:`DatetimeIndex.astype`, :meth:`TimedeltaIndex.astype`, :meth:`PeriodIndex.astype` :meth:`Series.astype`, :meth:`DataFrame.astype` with ``datetime64``, ``timedelta64`` or :class:`PeriodDtype` dtypes no longer allow converting to integer dtypes other than "int64", do ``obj.astype('int64', copy=False).astype(dtype)`` instead (:issue:`49715`)
- :meth:`Index.astype` now allows casting from ``float64`` dtype to datetime-like dtypes, matching :class:`Series` behavior (:issue:`49660`)
- Passing data with dtype of "timedelta64[s]", "timedelta64[ms]", or "timedelta64[us]" to :class:`TimedeltaIndex`, :class:`Series`, or :class:`DataFrame` constructors will now retain that dtype instead of casting to "timedelta64[ns]"; timedelta64 data with lower resolution will be cast to the lowest supported resolution "timedelta64[s]" (:issue:`49014`)
- Passing ``dtype`` of "timedelta64[s]", "timedelta64[ms]", or "timedelta64[us]" to :class:`TimedeltaIndex`, :class:`Series`, or :class:`DataFrame` constructors will now retain that dtype instead of casting to "timedelta64[ns]"; passing a dtype with lower resolution for :class:`Series` or :class:`DataFrame` will be cast to the lowest supported resolution "timedelta64[s]" (:issue:`49014`)
- Passing a ``np.datetime64`` object with non-nanosecond resolution to :class:`Timestamp` will retain the input resolution if it is "s", "ms", "us", or "ns"; otherwise it will be cast to the closest supported resolution (:issue:`49008`)
- Passing ``datetime64`` values with resolution other than nanosecond to :func:`to_datetime` will retain the input resolution if it is "s", "ms", "us", or "ns"; otherwise it will be cast to the closest supported resolution (:issue:`50369`)
- Passing integer values and a non-nanosecond datetime64 dtype (e.g. "datetime64[s]") :class:`DataFrame`, :class:`Series`, or :class:`Index` will treat the values as multiples of the dtype's unit, matching the behavior of e.g. ``Series(np.array(values, dtype="M8[s]"))`` (:issue:`51092`)
- Passing a string in ISO-8601 format to :class:`Timestamp` will retain the resolution of the parsed input if it is "s", "ms", "us", or "ns"; otherwise it will be cast to the closest supported resolution (:issue:`49737`)
- The ``other`` argument in :meth:`DataFrame.mask` and :meth:`Series.mask` now defaults to ``no_default`` instead of ``np.nan`` consistent with :meth:`DataFrame.where` and :meth:`Series.where`. Entries will be filled with the corresponding NULL value (``np.nan`` for numpy dtypes, ``pd.NA`` for extension dtypes). (:issue:`49111`)
- Changed behavior of :meth:`Series.quantile` and :meth:`DataFrame.quantile` with :class:`SparseDtype` to retain sparse dtype (:issue:`49583`)
- When creating a :class:`Series` with a object-dtype :class:`Index` of datetime objects, pandas no longer silently converts the index to a :class:`DatetimeIndex` (:issue:`39307`, :issue:`23598`)
- :func:`pandas.testing.assert_index_equal` with parameter ``exact="equiv"`` now considers two indexes equal when both are either a :class:`RangeIndex` or :class:`Index` with an ``int64`` dtype. Previously it meant either a :class:`RangeIndex` or a :class:`Int64Index` (:issue:`51098`)
- :meth:`Series.unique` with dtype "timedelta64[ns]" or "datetime64[ns]" now returns :class:`TimedeltaArray` or :class:`DatetimeArray` instead of ``numpy.ndarray`` (:issue:`49176`)
- :func:`to_datetime` and :class:`DatetimeIndex` now allow sequences containing both ``datetime`` objects and numeric entries, matching :class:`Series` behavior (:issue:`49037`, :issue:`50453`)
- :func:`pandas.api.types.is_string_dtype` now only returns ``True`` for array-likes with ``dtype=object`` when the elements are inferred to be strings (:issue:`15585`)
- Passing a sequence containing ``datetime`` objects and ``date`` objects to :class:`Series` constructor will return with ``object`` dtype instead of ``datetime64[ns]`` dtype, consistent with :class:`Index` behavior (:issue:`49341`)
- Passing strings that cannot be parsed as datetimes to :class:`Series` or :class:`DataFrame` with ``dtype="datetime64[ns]"`` will raise instead of silently ignoring the keyword and returning ``object`` dtype (:issue:`24435`)
- Passing a sequence containing a type that cannot be converted to :class:`Timedelta` to :func:`to_timedelta` or to the :class:`Series` or :class:`DataFrame` constructor with ``dtype="timedelta64[ns]"`` or to :class:`TimedeltaIndex` now raises ``TypeError`` instead of ``ValueError`` (:issue:`49525`)
- Changed behavior of :class:`Index` constructor with sequence containing at least one ``NaT`` and everything else either ``None`` or ``NaN`` to infer ``datetime64[ns]`` dtype instead of ``object``, matching :class:`Series` behavior (:issue:`49340`)
- :func:`read_stata` with parameter ``index_col`` set to ``None`` (the default) will now set the index on the returned :class:`DataFrame` to a :class:`RangeIndex` instead of a :class:`Int64Index` (:issue:`49745`)
- Changed behavior of :class:`Index`, :class:`Series`, and :class:`DataFrame` arithmetic methods when working with object-dtypes, the results no longer do type inference on the result of the array operations, use ``result.infer_objects(copy=False)`` to do type inference on the result (:issue:`49999`, :issue:`49714`)
- Changed behavior of :class:`Index` constructor with an object-dtype ``numpy.ndarray`` containing all-``bool`` values or all-complex values, this will now retain object dtype, consistent with the :class:`Series` behavior (:issue:`49594`)
- Changed behavior of :meth:`Series.astype` from object-dtype containing ``bytes`` objects to string dtypes; this now does ``val.decode()`` on bytes objects instead of ``str(val)``, matching :meth:`Index.astype` behavior (:issue:`45326`)
- Added ``"None"`` to default ``na_values`` in :func:`read_csv` (:issue:`50286`)
- Changed behavior of :class:`Series` and :class:`DataFrame` constructors when given an integer dtype and floating-point data that is not round numbers, this now raises ``ValueError`` instead of silently retaining the float dtype; do ``Series(data)`` or ``DataFrame(data)`` to get the old behavior, and ``Series(data).astype(dtype)`` or ``DataFrame(data).astype(dtype)`` to get the specified dtype (:issue:`49599`)
- Changed behavior of :meth:`DataFrame.shift` with ``axis=1``, an integer ``fill_value``, and homogeneous datetime-like dtype, this now fills new columns with integer dtypes instead of casting to datetimelike (:issue:`49842`)
- Files are now closed when encountering an exception in :func:`read_json` (:issue:`49921`)
- Changed behavior of :func:`read_csv`, :func:`read_json` & :func:`read_fwf`, where the index will now always be a :class:`RangeIndex`, when no index is specified. Previously the index would be a :class:`Index` with dtype ``object`` if the new DataFrame/Series has length 0 (:issue:`49572`)
- :meth:`DataFrame.values`, :meth:`DataFrame.to_numpy`, :meth:`DataFrame.xs`, :meth:`DataFrame.reindex`, :meth:`DataFrame.fillna`, and :meth:`DataFrame.replace` no longer silently consolidate the underlying arrays; do ``df = df.copy()`` to ensure consolidation (:issue:`49356`)
- Creating a new DataFrame using a full slice on both axes with :attr:`~DataFrame.loc`
  or :attr:`~DataFrame.iloc` (thus, ``df.loc[:, :]`` or ``df.iloc[:, :]``) now returns a
  new DataFrame (shallow copy) instead of the original DataFrame, consistent with other
  methods to get a full slice (for example ``df.loc[:]`` or ``df[:]``) (:issue:`49469`)
- The :class:`Series` and :class:`DataFrame` constructors will now return a shallow copy
  (i.e. share data, but not attributes) when passed a Series and DataFrame,
  respectively, and with the default of ``copy=False`` (and if no other keyword triggers
  a copy). Previously, the new Series or DataFrame would share the index attribute (e.g.
  ``df.index = ...`` would also update the index of the parent or child) (:issue:`49523`)
- Disallow computing ``cumprod`` for :class:`Timedelta` object; previously this returned incorrect values (:issue:`50246`)
- :class:`DataFrame` objects read from a :class:`HDFStore` file without an index now have a :class:`RangeIndex` instead of an ``int64`` index (:issue:`51076`)
- Instantiating an :class:`Index` with an numeric numpy dtype with data containing :class:`NA` and/or :class:`NaT` now raises a ``ValueError``. Previously a ``TypeError`` was raised (:issue:`51050`)
- Loading a JSON file with duplicate columns using ``read_json(orient='split')`` renames columns to avoid duplicates, as :func:`read_csv` and the other readers do (:issue:`50370`)
- The levels of the index of the :class:`Series` returned from ``Series.sparse.from_coo`` now always have dtype ``int32``. Previously they had dtype ``int64`` (:issue:`50926`)
- :func:`to_datetime` with ``unit`` of either "Y" or "M" will now raise if a sequence contains a non-round ``float`` value, matching the ``Timestamp`` behavior (:issue:`50301`)
- The methods :meth:`Series.round`, :meth:`DataFrame.__invert__`, :meth:`Series.__invert__`, :meth:`DataFrame.swapaxes`, :meth:`DataFrame.first`, :meth:`DataFrame.last`, :meth:`Series.first`, :meth:`Series.last` and :meth:`DataFrame.align` will now always return new objects (:issue:`51032`)
- :class:`DataFrame` and :class:`DataFrameGroupBy` aggregations (e.g. "sum") with object-dtype columns no longer infer non-object dtypes for their results, explicitly call ``result.infer_objects(copy=False)`` on the result to obtain the old behavior (:issue:`51205`, :issue:`49603`)
- Division by zero with :class:`ArrowDtype` dtypes returns ``-inf``, ``nan``, or ``inf`` depending on the numerator, instead of raising (:issue:`51541`)
- Added :func:`pandas.api.types.is_any_real_numeric_dtype` to check for real numeric dtypes (:issue:`51152`)
- :meth:`~arrays.ArrowExtensionArray.value_counts` now returns data with :class:`ArrowDtype` with ``pyarrow.int64`` type instead of ``"Int64"`` type (:issue:`51462`)
- :func:`factorize` and :func:`unique` preserve the original dtype when passed numpy timedelta64 or datetime64 with non-nanosecond resolution (:issue:`48670`)

.. note::

    A current PDEP proposes the deprecation and removal of the keywords ``inplace`` and ``copy``
    for all but a small subset of methods from the pandas API. The current discussion takes place
    at `here <https://github.com/pandas-dev/pandas/pull/51466>`_. The keywords won't be necessary
    anymore in the context of Copy-on-Write. If this proposal is accepted, both
    keywords would be deprecated in the next release of pandas and removed in pandas 3.0.

.. ---------------------------------------------------------------------------
.. _whatsnew_200.deprecations:

Deprecations
~~~~~~~~~~~~
- Deprecated parsing datetime strings with system-local timezone to ``tzlocal``, pass a ``tz`` keyword or explicitly call ``tz_localize`` instead (:issue:`50791`)
- Deprecated argument ``infer_datetime_format`` in :func:`to_datetime` and :func:`read_csv`, as a strict version of it is now the default (:issue:`48621`)
- Deprecated behavior of :func:`to_datetime` with ``unit`` when parsing strings, in a future version these will be parsed as datetimes (matching unit-less behavior) instead of cast to floats. To retain the old behavior, cast strings to numeric types before calling :func:`to_datetime` (:issue:`50735`)
- Deprecated :func:`pandas.io.sql.execute` (:issue:`50185`)
- :meth:`Index.is_boolean` has been deprecated. Use :func:`pandas.api.types.is_bool_dtype` instead (:issue:`50042`)
- :meth:`Index.is_integer` has been deprecated. Use :func:`pandas.api.types.is_integer_dtype` instead (:issue:`50042`)
- :meth:`Index.is_floating` has been deprecated. Use :func:`pandas.api.types.is_float_dtype` instead (:issue:`50042`)
- :meth:`Index.holds_integer` has been deprecated. Use :func:`pandas.api.types.infer_dtype` instead (:issue:`50243`)
- :meth:`Index.is_numeric` has been deprecated. Use :func:`pandas.api.types.is_any_real_numeric_dtype` instead (:issue:`50042`,:issue:`51152`)
- :meth:`Index.is_categorical` has been deprecated. Use :func:`pandas.api.types.is_categorical_dtype` instead (:issue:`50042`)
- :meth:`Index.is_object` has been deprecated. Use :func:`pandas.api.types.is_object_dtype` instead (:issue:`50042`)
- :meth:`Index.is_interval` has been deprecated. Use :func:`pandas.api.types.is_interval_dtype` instead (:issue:`50042`)
- Deprecated argument ``date_parser`` in :func:`read_csv`, :func:`read_table`, :func:`read_fwf`, and :func:`read_excel` in favour of ``date_format`` (:issue:`50601`)
- Deprecated ``all`` and ``any`` reductions with ``datetime64`` and :class:`DatetimeTZDtype` dtypes, use e.g. ``(obj != pd.Timestamp(0), tz=obj.tz).all()`` instead (:issue:`34479`)
- Deprecated unused arguments ``*args`` and ``**kwargs`` in :class:`Resampler` (:issue:`50977`)
- Deprecated calling ``float`` or ``int`` on a single element :class:`Series` to return a ``float`` or ``int`` respectively. Extract the element before calling ``float`` or ``int`` instead (:issue:`51101`)
- Deprecated :meth:`Grouper.groups`, use :meth:`Groupby.groups` instead (:issue:`51182`)
- Deprecated :meth:`Grouper.grouper`, use :meth:`Groupby.grouper` instead (:issue:`51182`)
- Deprecated :meth:`Grouper.obj`, use :meth:`Groupby.obj` instead (:issue:`51206`)
- Deprecated :meth:`Grouper.indexer`, use :meth:`Resampler.indexer` instead (:issue:`51206`)
- Deprecated :meth:`Grouper.ax`, use :meth:`Resampler.ax` instead (:issue:`51206`)
- Deprecated keyword ``use_nullable_dtypes`` in :func:`read_parquet`, use ``dtype_backend`` instead (:issue:`51853`)
- Deprecated :meth:`Series.pad` in favor of :meth:`Series.ffill` (:issue:`33396`)
- Deprecated :meth:`Series.backfill` in favor of :meth:`Series.bfill` (:issue:`33396`)
- Deprecated :meth:`DataFrame.pad` in favor of :meth:`DataFrame.ffill` (:issue:`33396`)
- Deprecated :meth:`DataFrame.backfill` in favor of :meth:`DataFrame.bfill` (:issue:`33396`)
- Deprecated :meth:`~pandas.io.stata.StataReader.close`. Use :class:`~pandas.io.stata.StataReader` as a context manager instead (:issue:`49228`)
- Deprecated producing a scalar when iterating over a :class:`.DataFrameGroupBy` or a :class:`.SeriesGroupBy` that has been grouped by a ``level`` parameter that is a list of length 1; a tuple of length one will be returned instead (:issue:`51583`)

.. ---------------------------------------------------------------------------
.. _whatsnew_200.prior_deprecations:

Removal of prior version deprecations/changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Removed :class:`Int64Index`, :class:`UInt64Index` and :class:`Float64Index`. See also :ref:`here <whatsnew_200.enhancements.index_can_hold_numpy_numeric_dtypes>` for more information (:issue:`42717`)
- Removed deprecated :attr:`Timestamp.freq`, :attr:`Timestamp.freqstr` and argument ``freq`` from the :class:`Timestamp` constructor and :meth:`Timestamp.fromordinal` (:issue:`14146`)
- Removed deprecated :class:`CategoricalBlock`, :meth:`Block.is_categorical`, require datetime64 and timedelta64 values to be wrapped in :class:`DatetimeArray` or :class:`TimedeltaArray` before passing to :meth:`Block.make_block_same_class`, require ``DatetimeTZBlock.values`` to have the correct ndim when passing to the :class:`BlockManager` constructor, and removed the "fastpath" keyword from the :class:`SingleBlockManager` constructor (:issue:`40226`, :issue:`40571`)
- Removed deprecated global option ``use_inf_as_null`` in favor of ``use_inf_as_na`` (:issue:`17126`)
- Removed deprecated module ``pandas.core.index`` (:issue:`30193`)
- Removed deprecated alias ``pandas.core.tools.datetimes.to_time``, import the function directly from ``pandas.core.tools.times`` instead (:issue:`34145`)
- Removed deprecated alias ``pandas.io.json.json_normalize``, import the function directly from ``pandas.json_normalize`` instead (:issue:`27615`)
- Removed deprecated :meth:`Categorical.to_dense`, use ``np.asarray(cat)`` instead (:issue:`32639`)
- Removed deprecated :meth:`Categorical.take_nd` (:issue:`27745`)
- Removed deprecated :meth:`Categorical.mode`, use ``Series(cat).mode()`` instead (:issue:`45033`)
- Removed deprecated :meth:`Categorical.is_dtype_equal` and :meth:`CategoricalIndex.is_dtype_equal` (:issue:`37545`)
- Removed deprecated :meth:`CategoricalIndex.take_nd` (:issue:`30702`)
- Removed deprecated :meth:`Index.is_type_compatible` (:issue:`42113`)
- Removed deprecated :meth:`Index.is_mixed`, check ``index.inferred_type`` directly instead (:issue:`32922`)
- Removed deprecated :func:`pandas.api.types.is_categorical`; use :func:`pandas.api.types.is_categorical_dtype` instead  (:issue:`33385`)
- Removed deprecated :meth:`Index.asi8` (:issue:`37877`)
- Enforced deprecation changing behavior when passing ``datetime64[ns]`` dtype data and timezone-aware dtype to :class:`Series`, interpreting the values as wall-times instead of UTC times, matching :class:`DatetimeIndex` behavior (:issue:`41662`)
- Enforced deprecation changing behavior when applying a numpy ufunc on multiple non-aligned (on the index or columns) :class:`DataFrame` that will now align the inputs first (:issue:`39239`)
- Removed deprecated :meth:`DataFrame._AXIS_NUMBERS`, :meth:`DataFrame._AXIS_NAMES`, :meth:`Series._AXIS_NUMBERS`, :meth:`Series._AXIS_NAMES` (:issue:`33637`)
- Removed deprecated :meth:`Index.to_native_types`, use ``obj.astype(str)`` instead (:issue:`36418`)
- Removed deprecated :meth:`Series.iteritems`, :meth:`DataFrame.iteritems`, use ``obj.items`` instead (:issue:`45321`)
- Removed deprecated :meth:`DataFrame.lookup` (:issue:`35224`)
- Removed deprecated :meth:`Series.append`, :meth:`DataFrame.append`, use :func:`concat` instead (:issue:`35407`)
- Removed deprecated :meth:`Series.iteritems`, :meth:`DataFrame.iteritems` and :meth:`HDFStore.iteritems` use ``obj.items`` instead (:issue:`45321`)
- Removed deprecated :meth:`DatetimeIndex.union_many` (:issue:`45018`)
- Removed deprecated ``weekofyear`` and ``week`` attributes of :class:`DatetimeArray`, :class:`DatetimeIndex` and ``dt`` accessor in favor of ``isocalendar().week`` (:issue:`33595`)
- Removed deprecated :meth:`RangeIndex._start`, :meth:`RangeIndex._stop`, :meth:`RangeIndex._step`, use ``start``, ``stop``, ``step`` instead (:issue:`30482`)
- Removed deprecated :meth:`DatetimeIndex.to_perioddelta`, Use ``dtindex - dtindex.to_period(freq).to_timestamp()`` instead (:issue:`34853`)
- Removed deprecated :meth:`.Styler.hide_index` and :meth:`.Styler.hide_columns` (:issue:`49397`)
- Removed deprecated :meth:`.Styler.set_na_rep` and :meth:`.Styler.set_precision` (:issue:`49397`)
- Removed deprecated :meth:`.Styler.where` (:issue:`49397`)
- Removed deprecated :meth:`.Styler.render` (:issue:`49397`)
- Removed deprecated argument ``col_space`` in :meth:`DataFrame.to_latex` (:issue:`47970`)
- Removed deprecated argument ``null_color`` in :meth:`.Styler.highlight_null` (:issue:`49397`)
- Removed deprecated argument ``check_less_precise`` in :meth:`.testing.assert_frame_equal`, :meth:`.testing.assert_extension_array_equal`, :meth:`.testing.assert_series_equal`,  :meth:`.testing.assert_index_equal` (:issue:`30562`)
- Removed deprecated ``null_counts`` argument in :meth:`DataFrame.info`. Use ``show_counts`` instead (:issue:`37999`)
- Removed deprecated :meth:`Index.is_monotonic`, and :meth:`Series.is_monotonic`; use ``obj.is_monotonic_increasing`` instead (:issue:`45422`)
- Removed deprecated :meth:`Index.is_all_dates` (:issue:`36697`)
- Enforced deprecation disallowing passing a timezone-aware :class:`Timestamp` and ``dtype="datetime64[ns]"`` to :class:`Series` or :class:`DataFrame` constructors (:issue:`41555`)
- Enforced deprecation disallowing passing a sequence of timezone-aware values and ``dtype="datetime64[ns]"`` to :class:`Series` or :class:`DataFrame` constructors (:issue:`41555`)
- Enforced deprecation disallowing ``numpy.ma.mrecords.MaskedRecords`` in the :class:`DataFrame` constructor; pass ``"{name: data[name] for name in data.dtype.names}`` instead (:issue:`40363`)
- Enforced deprecation disallowing unit-less "datetime64" dtype in :meth:`Series.astype` and :meth:`DataFrame.astype` (:issue:`47844`)
- Enforced deprecation disallowing using ``.astype`` to convert a ``datetime64[ns]`` :class:`Series`, :class:`DataFrame`, or :class:`DatetimeIndex` to timezone-aware dtype, use ``obj.tz_localize`` or ``ser.dt.tz_localize`` instead (:issue:`39258`)
- Enforced deprecation disallowing using ``.astype`` to convert a timezone-aware :class:`Series`, :class:`DataFrame`, or :class:`DatetimeIndex` to timezone-naive ``datetime64[ns]`` dtype, use ``obj.tz_localize(None)`` or ``obj.tz_convert("UTC").tz_localize(None)`` instead (:issue:`39258`)
- Enforced deprecation disallowing passing non boolean argument to sort in :func:`concat` (:issue:`44629`)
- Removed Date parser functions :func:`~pandas.io.date_converters.parse_date_time`,
  :func:`~pandas.io.date_converters.parse_date_fields`, :func:`~pandas.io.date_converters.parse_all_fields`
  and :func:`~pandas.io.date_converters.generic_parser` (:issue:`24518`)
- Removed argument ``index`` from the :class:`core.arrays.SparseArray` constructor (:issue:`43523`)
- Remove argument ``squeeze`` from :meth:`DataFrame.groupby` and :meth:`Series.groupby` (:issue:`32380`)
- Removed deprecated ``apply``, ``apply_index``, ``__call__``, ``onOffset``, and ``isAnchored`` attributes from :class:`DateOffset` (:issue:`34171`)
- Removed ``keep_tz`` argument in :meth:`DatetimeIndex.to_series` (:issue:`29731`)
- Remove arguments ``names`` and ``dtype`` from :meth:`Index.copy` and ``levels`` and ``codes`` from :meth:`MultiIndex.copy` (:issue:`35853`, :issue:`36685`)
- Remove argument ``inplace`` from :meth:`MultiIndex.set_levels` and :meth:`MultiIndex.set_codes` (:issue:`35626`)
- Removed arguments ``verbose`` and ``encoding`` from :meth:`DataFrame.to_excel` and :meth:`Series.to_excel` (:issue:`47912`)
- Removed argument ``line_terminator`` from :meth:`DataFrame.to_csv` and :meth:`Series.to_csv`, use ``lineterminator`` instead (:issue:`45302`)
- Removed argument ``inplace`` from :meth:`DataFrame.set_axis` and :meth:`Series.set_axis`, use ``obj = obj.set_axis(..., copy=False)`` instead (:issue:`48130`)
- Disallow passing positional arguments to :meth:`MultiIndex.set_levels` and :meth:`MultiIndex.set_codes` (:issue:`41485`)
- Disallow parsing to Timedelta strings with components with units "Y", "y", or "M", as these do not represent unambiguous durations (:issue:`36838`)
- Removed :meth:`MultiIndex.is_lexsorted` and :meth:`MultiIndex.lexsort_depth` (:issue:`38701`)
- Removed argument ``how`` from :meth:`PeriodIndex.astype`, use :meth:`PeriodIndex.to_timestamp` instead (:issue:`37982`)
- Removed argument ``try_cast`` from :meth:`DataFrame.mask`, :meth:`DataFrame.where`, :meth:`Series.mask` and :meth:`Series.where` (:issue:`38836`)
- Removed argument ``tz`` from :meth:`Period.to_timestamp`, use ``obj.to_timestamp(...).tz_localize(tz)`` instead (:issue:`34522`)
- Removed argument ``sort_columns`` in :meth:`DataFrame.plot` and :meth:`Series.plot` (:issue:`47563`)
- Removed argument ``is_copy`` from :meth:`DataFrame.take` and :meth:`Series.take` (:issue:`30615`)
- Removed argument ``kind`` from :meth:`Index.get_slice_bound`, :meth:`Index.slice_indexer` and :meth:`Index.slice_locs` (:issue:`41378`)
- Removed arguments ``prefix``, ``squeeze``, ``error_bad_lines`` and ``warn_bad_lines`` from :func:`read_csv` (:issue:`40413`, :issue:`43427`)
- Removed arguments ``squeeze`` from :func:`read_excel` (:issue:`43427`)
- Removed argument ``datetime_is_numeric`` from :meth:`DataFrame.describe` and :meth:`Series.describe` as datetime data will always be summarized as numeric data (:issue:`34798`)
- Disallow passing list ``key`` to :meth:`Series.xs` and :meth:`DataFrame.xs`, pass a tuple instead (:issue:`41789`)
- Disallow subclass-specific keywords (e.g. "freq", "tz", "names", "closed") in the :class:`Index` constructor (:issue:`38597`)
- Removed argument ``inplace`` from :meth:`Categorical.remove_unused_categories` (:issue:`37918`)
- Disallow passing non-round floats to :class:`Timestamp` with ``unit="M"`` or ``unit="Y"`` (:issue:`47266`)
- Remove keywords ``convert_float`` and ``mangle_dupe_cols`` from :func:`read_excel` (:issue:`41176`)
- Remove keyword ``mangle_dupe_cols`` from :func:`read_csv` and :func:`read_table` (:issue:`48137`)
- Removed ``errors`` keyword from :meth:`DataFrame.where`, :meth:`Series.where`, :meth:`DataFrame.mask` and :meth:`Series.mask` (:issue:`47728`)
- Disallow passing non-keyword arguments to :func:`read_excel` except ``io`` and ``sheet_name`` (:issue:`34418`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.drop` and :meth:`Series.drop` except ``labels`` (:issue:`41486`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.fillna` and :meth:`Series.fillna` except ``value`` (:issue:`41485`)
- Disallow passing non-keyword arguments to :meth:`StringMethods.split` and :meth:`StringMethods.rsplit` except for ``pat`` (:issue:`47448`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.set_index` except ``keys`` (:issue:`41495`)
- Disallow passing non-keyword arguments to :meth:`Resampler.interpolate` except ``method`` (:issue:`41699`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.reset_index` and :meth:`Series.reset_index` except ``level`` (:issue:`41496`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.dropna` and :meth:`Series.dropna` (:issue:`41504`)
- Disallow passing non-keyword arguments to :meth:`ExtensionArray.argsort` (:issue:`46134`)
- Disallow passing non-keyword arguments to :meth:`Categorical.sort_values` (:issue:`47618`)
- Disallow passing non-keyword arguments to :meth:`Index.drop_duplicates` and :meth:`Series.drop_duplicates` (:issue:`41485`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.drop_duplicates` except for ``subset`` (:issue:`41485`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.sort_index` and :meth:`Series.sort_index` (:issue:`41506`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.interpolate` and :meth:`Series.interpolate` except for ``method`` (:issue:`41510`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.any` and :meth:`Series.any` (:issue:`44896`)
- Disallow passing non-keyword arguments to :meth:`Index.set_names` except for ``names`` (:issue:`41551`)
- Disallow passing non-keyword arguments to :meth:`Index.join` except for ``other`` (:issue:`46518`)
- Disallow passing non-keyword arguments to :func:`concat` except for ``objs`` (:issue:`41485`)
- Disallow passing non-keyword arguments to :func:`pivot` except for ``data`` (:issue:`48301`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.pivot` (:issue:`48301`)
- Disallow passing non-keyword arguments to :func:`read_html` except for ``io`` (:issue:`27573`)
- Disallow passing non-keyword arguments to :func:`read_json` except for ``path_or_buf`` (:issue:`27573`)
- Disallow passing non-keyword arguments to :func:`read_sas` except for ``filepath_or_buffer`` (:issue:`47154`)
- Disallow passing non-keyword arguments to :func:`read_stata` except for ``filepath_or_buffer`` (:issue:`48128`)
- Disallow passing non-keyword arguments to :func:`read_csv` except ``filepath_or_buffer`` (:issue:`41485`)
- Disallow passing non-keyword arguments to :func:`read_table` except ``filepath_or_buffer`` (:issue:`41485`)
- Disallow passing non-keyword arguments to :func:`read_fwf` except ``filepath_or_buffer`` (:issue:`44710`)
- Disallow passing non-keyword arguments to :func:`read_xml` except for ``path_or_buffer`` (:issue:`45133`)
- Disallow passing non-keyword arguments to :meth:`Series.mask` and :meth:`DataFrame.mask` except ``cond`` and ``other`` (:issue:`41580`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.to_stata` except for ``path`` (:issue:`48128`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.where` and :meth:`Series.where` except for ``cond`` and ``other`` (:issue:`41523`)
- Disallow passing non-keyword arguments to :meth:`Series.set_axis` and :meth:`DataFrame.set_axis` except for ``labels`` (:issue:`41491`)
- Disallow passing non-keyword arguments to :meth:`Series.rename_axis` and :meth:`DataFrame.rename_axis` except for ``mapper`` (:issue:`47587`)
- Disallow passing non-keyword arguments to :meth:`Series.clip` and :meth:`DataFrame.clip` except ``lower`` and ``upper`` (:issue:`41511`)
- Disallow passing non-keyword arguments to :meth:`Series.bfill`, :meth:`Series.ffill`, :meth:`DataFrame.bfill` and :meth:`DataFrame.ffill` (:issue:`41508`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.replace`, :meth:`Series.replace` except for ``to_replace`` and ``value`` (:issue:`47587`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.sort_values` except for ``by`` (:issue:`41505`)
- Disallow passing non-keyword arguments to :meth:`Series.sort_values` (:issue:`41505`)
- Disallow passing non-keyword arguments to :meth:`DataFrame.reindex` except for ``labels`` (:issue:`17966`)
- Disallow :meth:`Index.reindex` with non-unique :class:`Index` objects (:issue:`42568`)
- Disallowed constructing :class:`Categorical` with scalar ``data`` (:issue:`38433`)
- Disallowed constructing :class:`CategoricalIndex` without passing ``data`` (:issue:`38944`)
- Removed :meth:`.Rolling.validate`, :meth:`.Expanding.validate`, and :meth:`.ExponentialMovingWindow.validate` (:issue:`43665`)
- Removed :attr:`Rolling.win_type` returning ``"freq"`` (:issue:`38963`)
- Removed :attr:`Rolling.is_datetimelike` (:issue:`38963`)
- Removed the ``level`` keyword in :class:`DataFrame` and :class:`Series` aggregations; use ``groupby`` instead (:issue:`39983`)
- Removed deprecated :meth:`Timedelta.delta`, :meth:`Timedelta.is_populated`, and :attr:`Timedelta.freq` (:issue:`46430`, :issue:`46476`)
- Removed deprecated :attr:`NaT.freq` (:issue:`45071`)
- Removed deprecated :meth:`Categorical.replace`, use :meth:`Series.replace` instead (:issue:`44929`)
- Removed the ``numeric_only`` keyword from :meth:`Categorical.min` and :meth:`Categorical.max` in favor of ``skipna`` (:issue:`48821`)
- Changed behavior of :meth:`DataFrame.median` and :meth:`DataFrame.mean` with ``numeric_only=None`` to not exclude datetime-like columns THIS NOTE WILL BE IRRELEVANT ONCE ``numeric_only=None`` DEPRECATION IS ENFORCED (:issue:`29941`)
- Removed :func:`is_extension_type` in favor of :func:`is_extension_array_dtype` (:issue:`29457`)
- Removed ``.ExponentialMovingWindow.vol`` (:issue:`39220`)
- Removed :meth:`Index.get_value` and :meth:`Index.set_value` (:issue:`33907`, :issue:`28621`)
- Removed :meth:`Series.slice_shift` and :meth:`DataFrame.slice_shift` (:issue:`37601`)
- Remove :meth:`DataFrameGroupBy.pad` and :meth:`DataFrameGroupBy.backfill` (:issue:`45076`)
- Remove ``numpy`` argument from :func:`read_json` (:issue:`30636`)
- Disallow passing abbreviations for ``orient`` in :meth:`DataFrame.to_dict` (:issue:`32516`)
- Disallow partial slicing on an non-monotonic :class:`DatetimeIndex` with keys which are not in Index. This now raises a ``KeyError`` (:issue:`18531`)
- Removed ``get_offset`` in favor of :func:`to_offset` (:issue:`30340`)
- Removed the ``warn`` keyword in :func:`infer_freq` (:issue:`45947`)
- Removed the ``include_start`` and ``include_end`` arguments in :meth:`DataFrame.between_time` in favor of ``inclusive`` (:issue:`43248`)
- Removed the ``closed`` argument in :meth:`date_range` and :meth:`bdate_range` in favor of ``inclusive`` argument (:issue:`40245`)
- Removed the ``center`` keyword in :meth:`DataFrame.expanding` (:issue:`20647`)
- Removed the ``truediv`` keyword from :func:`eval` (:issue:`29812`)
- Removed the ``method`` and ``tolerance`` arguments in :meth:`Index.get_loc`. Use ``index.get_indexer([label], method=..., tolerance=...)`` instead (:issue:`42269`)
- Removed the ``pandas.datetime`` submodule (:issue:`30489`)
- Removed the ``pandas.np`` submodule (:issue:`30296`)
- Removed ``pandas.util.testing`` in favor of ``pandas.testing`` (:issue:`30745`)
- Removed :meth:`Series.str.__iter__` (:issue:`28277`)
- Removed ``pandas.SparseArray`` in favor of :class:`arrays.SparseArray` (:issue:`30642`)
- Removed ``pandas.SparseSeries`` and ``pandas.SparseDataFrame``, including pickle support. (:issue:`30642`)
- Enforced disallowing passing an integer ``fill_value`` to :meth:`DataFrame.shift` and :meth:`Series.shift` with datetime64, timedelta64, or period dtypes (:issue:`32591`)
- Enforced disallowing a string column label into ``times`` in :meth:`DataFrame.ewm` (:issue:`43265`)
- Enforced disallowing passing ``True`` and ``False`` into ``inclusive`` in :meth:`Series.between` in favor of ``"both"`` and ``"neither"`` respectively (:issue:`40628`)
- Enforced disallowing using ``usecols`` with out of bounds indices for ``read_csv`` with ``engine="c"`` (:issue:`25623`)
- Enforced disallowing the use of ``**kwargs`` in :class:`.ExcelWriter`; use the keyword argument ``engine_kwargs`` instead (:issue:`40430`)
- Enforced disallowing a tuple of column labels into :meth:`.DataFrameGroupBy.__getitem__` (:issue:`30546`)
- Enforced disallowing missing labels when indexing with a sequence of labels on a level of a :class:`MultiIndex`. This now raises a ``KeyError`` (:issue:`42351`)
- Enforced disallowing setting values with ``.loc`` using a positional slice. Use ``.loc`` with labels or ``.iloc`` with positions instead (:issue:`31840`)
- Enforced disallowing positional indexing with a ``float`` key even if that key is a round number, manually cast to integer instead (:issue:`34193`)
- Enforced disallowing using a :class:`DataFrame` indexer with ``.iloc``, use ``.loc`` instead for automatic alignment (:issue:`39022`)
- Enforced disallowing ``set`` or ``dict`` indexers in ``__getitem__`` and ``__setitem__`` methods (:issue:`42825`)
- Enforced disallowing indexing on a :class:`Index` or positional indexing on a :class:`Series` producing multi-dimensional objects e.g. ``obj[:, None]``, convert to numpy before indexing instead (:issue:`35141`)
- Enforced disallowing ``dict`` or ``set`` objects in ``suffixes`` in :func:`merge` (:issue:`34810`)
- Enforced disallowing :func:`merge` to produce duplicated columns through the ``suffixes`` keyword and already existing columns (:issue:`22818`)
- Enforced disallowing using :func:`merge` or :func:`join` on a different number of levels (:issue:`34862`)
- Enforced disallowing ``value_name`` argument in :func:`DataFrame.melt` to match an element in the :class:`DataFrame` columns (:issue:`35003`)
- Enforced disallowing passing ``showindex`` into ``**kwargs`` in :func:`DataFrame.to_markdown` and :func:`Series.to_markdown` in favor of ``index`` (:issue:`33091`)
- Removed setting Categorical._codes directly (:issue:`41429`)
- Removed setting Categorical.categories directly (:issue:`47834`)
- Removed argument ``inplace`` from :meth:`Categorical.add_categories`, :meth:`Categorical.remove_categories`, :meth:`Categorical.set_categories`, :meth:`Categorical.rename_categories`, :meth:`Categorical.reorder_categories`, :meth:`Categorical.set_ordered`, :meth:`Categorical.as_ordered`, :meth:`Categorical.as_unordered` (:issue:`37981`, :issue:`41118`, :issue:`41133`, :issue:`47834`)
- Enforced :meth:`Rolling.count` with ``min_periods=None`` to default to the size of the window (:issue:`31302`)
- Renamed ``fname`` to ``path`` in :meth:`DataFrame.to_parquet`, :meth:`DataFrame.to_stata` and :meth:`DataFrame.to_feather` (:issue:`30338`)
- Enforced disallowing indexing a :class:`Series` with a single item list with a slice (e.g. ``ser[[slice(0, 2)]]``). Either convert the list to tuple, or pass the slice directly instead (:issue:`31333`)
- Changed behavior indexing on a :class:`DataFrame` with a :class:`DatetimeIndex` index using a string indexer, previously this operated as a slice on rows, now it operates like any other column key; use ``frame.loc[key]`` for the old behavior (:issue:`36179`)
- Enforced the ``display.max_colwidth`` option to not accept negative integers (:issue:`31569`)
- Removed the ``display.column_space`` option in favor of ``df.to_string(col_space=...)`` (:issue:`47280`)
- Removed the deprecated method ``mad`` from pandas classes (:issue:`11787`)
- Removed the deprecated method ``tshift`` from pandas classes (:issue:`11631`)
- Changed behavior of empty data passed into :class:`Series`; the default dtype will be ``object`` instead of ``float64`` (:issue:`29405`)
- Changed the behavior of :meth:`DatetimeIndex.union`, :meth:`DatetimeIndex.intersection`, and :meth:`DatetimeIndex.symmetric_difference` with mismatched timezones to convert to UTC instead of casting to object dtype (:issue:`39328`)
- Changed the behavior of :func:`to_datetime` with argument "now" with ``utc=False`` to match ``Timestamp("now")`` (:issue:`18705`)
- Changed the behavior of indexing on a timezone-aware :class:`DatetimeIndex` with a timezone-naive ``datetime`` object or vice-versa; these now behave like any other non-comparable type by raising ``KeyError`` (:issue:`36148`)
- Changed the behavior of :meth:`Index.reindex`, :meth:`Series.reindex`, and :meth:`DataFrame.reindex` with a ``datetime64`` dtype and a ``datetime.date`` object for ``fill_value``; these are no longer considered equivalent to ``datetime.datetime`` objects so the reindex casts to object dtype (:issue:`39767`)
- Changed behavior of :meth:`SparseArray.astype` when given a dtype that is not explicitly ``SparseDtype``, cast to the exact requested dtype rather than silently using a ``SparseDtype`` instead (:issue:`34457`)
- Changed behavior of :meth:`Index.ravel` to return a view on the original :class:`Index` instead of a ``np.ndarray`` (:issue:`36900`)
- Changed behavior of :meth:`Series.to_frame` and :meth:`Index.to_frame` with explicit ``name=None`` to use ``None`` for the column name instead of the index's name or default ``0`` (:issue:`45523`)
- Changed behavior of :func:`concat` with one array of ``bool``-dtype and another of integer dtype, this now returns ``object`` dtype instead of integer dtype; explicitly cast the bool object to integer before concatenating to get the old behavior (:issue:`45101`)
- Changed behavior of :class:`DataFrame` constructor given floating-point ``data`` and an integer ``dtype``, when the data cannot be cast losslessly, the floating point dtype is retained, matching :class:`Series` behavior (:issue:`41170`)
- Changed behavior of :class:`Index` constructor when given a ``np.ndarray`` with object-dtype containing numeric entries; this now retains object dtype rather than inferring a numeric dtype, consistent with :class:`Series` behavior (:issue:`42870`)
- Changed behavior of :meth:`Index.__and__`, :meth:`Index.__or__` and :meth:`Index.__xor__` to behave as logical operations (matching :class:`Series` behavior) instead of aliases for set operations (:issue:`37374`)
- Changed behavior of :class:`DataFrame` constructor when passed a list whose first element is a :class:`Categorical`, this now treats the elements as rows casting to ``object`` dtype, consistent with behavior for other types (:issue:`38845`)
- Changed behavior of :class:`DataFrame` constructor when passed a ``dtype`` (other than int) that the data cannot be cast to; it now raises instead of silently ignoring the dtype (:issue:`41733`)
- Changed the behavior of :class:`Series` constructor, it will no longer infer a datetime64 or timedelta64 dtype from string entries (:issue:`41731`)
- Changed behavior of :class:`Timestamp` constructor with a ``np.datetime64`` object and a ``tz`` passed to interpret the input as a wall-time as opposed to a UTC time (:issue:`42288`)
- Changed behavior of :meth:`Timestamp.utcfromtimestamp` to return a timezone-aware object satisfying ``Timestamp.utcfromtimestamp(val).timestamp() == val`` (:issue:`45083`)
- Changed behavior of :class:`Index` constructor when passed a ``SparseArray`` or ``SparseDtype`` to retain that dtype instead of casting to ``numpy.ndarray`` (:issue:`43930`)
- Changed behavior of setitem-like operations (``__setitem__``, ``fillna``, ``where``, ``mask``, ``replace``, ``insert``, fill_value for ``shift``) on an object with :class:`DatetimeTZDtype` when using a value with a non-matching timezone, the value will be cast to the object's timezone instead of casting both to object-dtype (:issue:`44243`)
- Changed behavior of :class:`Index`, :class:`Series`, :class:`DataFrame` constructors with floating-dtype data and a :class:`DatetimeTZDtype`, the data are now interpreted as UTC-times instead of wall-times, consistent with how integer-dtype data are treated (:issue:`45573`)
- Changed behavior of :class:`Series` and :class:`DataFrame` constructors with integer dtype and floating-point data containing ``NaN``, this now raises ``IntCastingNaNError`` (:issue:`40110`)
- Changed behavior of :class:`Series` and :class:`DataFrame` constructors with an integer ``dtype`` and values that are too large to losslessly cast to this dtype, this now raises ``ValueError`` (:issue:`41734`)
- Changed behavior of :class:`Series` and :class:`DataFrame` constructors with an integer ``dtype`` and values having either ``datetime64`` or ``timedelta64`` dtypes, this now raises ``TypeError``, use ``values.view("int64")`` instead (:issue:`41770`)
- Removed the deprecated ``base`` and ``loffset`` arguments from :meth:`pandas.DataFrame.resample`, :meth:`pandas.Series.resample` and :class:`pandas.Grouper`. Use ``offset`` or ``origin`` instead (:issue:`31809`)
- Changed behavior of :meth:`Series.fillna` and :meth:`DataFrame.fillna` with ``timedelta64[ns]`` dtype and an incompatible ``fill_value``; this now casts to ``object`` dtype instead of raising, consistent with the behavior with other dtypes (:issue:`45746`)
- Change the default argument of ``regex`` for :meth:`Series.str.replace` from ``True`` to ``False``. Additionally, a single character ``pat`` with ``regex=True`` is now treated as a regular expression instead of a string literal. (:issue:`36695`, :issue:`24804`)
- Changed behavior of :meth:`DataFrame.any` and :meth:`DataFrame.all` with ``bool_only=True``; object-dtype columns with all-bool values will no longer be included, manually cast to ``bool`` dtype first (:issue:`46188`)
- Changed behavior of :meth:`DataFrame.max`, :class:`DataFrame.min`, :class:`DataFrame.mean`, :class:`DataFrame.median`, :class:`DataFrame.skew`, :class:`DataFrame.kurt` with ``axis=None`` to return a scalar applying the aggregation across both axes (:issue:`45072`)
- Changed behavior of comparison of a :class:`Timestamp` with a ``datetime.date`` object; these now compare as un-equal and raise on inequality comparisons, matching the ``datetime.datetime`` behavior (:issue:`36131`)
- Changed behavior of comparison of ``NaT`` with a ``datetime.date`` object; these now raise on inequality comparisons (:issue:`39196`)
- Enforced deprecation of silently dropping columns that raised a ``TypeError`` in :class:`Series.transform` and :class:`DataFrame.transform` when used with a list or dictionary (:issue:`43740`)
- Changed behavior of :meth:`DataFrame.apply` with list-like so that any partial failure will raise an error (:issue:`43740`)
- Changed behaviour of :meth:`DataFrame.to_latex` to now use the Styler implementation via :meth:`.Styler.to_latex` (:issue:`47970`)
- Changed behavior of :meth:`Series.__setitem__` with an integer key and a :class:`Float64Index` when the key is not present in the index; previously we treated the key as positional (behaving like ``series.iloc[key] = val``), now we treat it is a label (behaving like ``series.loc[key] = val``), consistent with :meth:`Series.__getitem__` behavior (:issue:`33469`)
- Removed ``na_sentinel`` argument from :func:`factorize`, :meth:`.Index.factorize`, and :meth:`.ExtensionArray.factorize` (:issue:`47157`)
- Changed behavior of :meth:`Series.diff` and :meth:`DataFrame.diff` with :class:`ExtensionDtype` dtypes whose arrays do not implement ``diff``, these now raise ``TypeError`` rather than casting to numpy (:issue:`31025`)
- Enforced deprecation of calling numpy "ufunc"s on :class:`DataFrame` with ``method="outer"``; this now raises ``NotImplementedError`` (:issue:`36955`)
- Enforced deprecation disallowing passing ``numeric_only=True`` to :class:`Series` reductions (``rank``, ``any``, ``all``, ...) with non-numeric dtype (:issue:`47500`)
- Changed behavior of :meth:`.DataFrameGroupBy.apply` and :meth:`.SeriesGroupBy.apply` so that ``group_keys`` is respected even if a transformer is detected (:issue:`34998`)
- Comparisons between a :class:`DataFrame` and a :class:`Series` where the frame's columns do not match the series's index raise ``ValueError`` instead of automatically aligning, do ``left, right = left.align(right, axis=1, copy=False)`` before comparing (:issue:`36795`)
- Enforced deprecation ``numeric_only=None`` (the default) in DataFrame reductions that would silently drop columns that raised; ``numeric_only`` now defaults to ``False`` (:issue:`41480`)
- Changed default of ``numeric_only`` to ``False`` in all DataFrame methods with that argument (:issue:`46096`, :issue:`46906`)
- Changed default of ``numeric_only`` to ``False`` in :meth:`Series.rank` (:issue:`47561`)
- Enforced deprecation of silently dropping nuisance columns in groupby and resample operations when ``numeric_only=False`` (:issue:`41475`)
- Enforced deprecation of silently dropping nuisance columns in :class:`Rolling`, :class:`Expanding`, and :class:`ExponentialMovingWindow` ops. This will now raise a :class:`.errors.DataError` (:issue:`42834`)
- Changed behavior in setting values with ``df.loc[:, foo] = bar`` or ``df.iloc[:, foo] = bar``, these now always attempt to set values inplace before falling back to casting (:issue:`45333`)
- Changed default of ``numeric_only`` in various :class:`.DataFrameGroupBy` methods; all methods now default to ``numeric_only=False`` (:issue:`46072`)
- Changed default of ``numeric_only`` to ``False`` in :class:`.Resampler` methods (:issue:`47177`)
- Using the method :meth:`.DataFrameGroupBy.transform` with a callable that returns DataFrames will align to the input's index (:issue:`47244`)
- When providing a list of columns of length one to :meth:`DataFrame.groupby`, the keys that are returned by iterating over the resulting :class:`DataFrameGroupBy` object will now be tuples of length one (:issue:`47761`)
- Removed deprecated methods :meth:`ExcelWriter.write_cells`, :meth:`ExcelWriter.save`, :meth:`ExcelWriter.cur_sheet`, :meth:`ExcelWriter.handles`, :meth:`ExcelWriter.path` (:issue:`45795`)
- The :class:`ExcelWriter` attribute ``book`` can no longer be set; it is still available to be accessed and mutated (:issue:`48943`)
- Removed unused ``*args`` and ``**kwargs`` in :class:`Rolling`, :class:`Expanding`, and :class:`ExponentialMovingWindow` ops (:issue:`47851`)
- Removed the deprecated argument ``line_terminator`` from :meth:`DataFrame.to_csv` (:issue:`45302`)
- Removed the deprecated argument ``label`` from :func:`lreshape` (:issue:`30219`)
- Arguments after ``expr`` in :meth:`DataFrame.eval` and :meth:`DataFrame.query` are keyword-only (:issue:`47587`)
- Removed :meth:`Index._get_attributes_dict` (:issue:`50648`)
- Removed :meth:`Series.__array_wrap__` (:issue:`50648`)
- Changed behavior of :meth:`.DataFrame.value_counts` to return a :class:`Series` with :class:`MultiIndex` for any list-like(one element or not) but an :class:`Index` for a single label (:issue:`50829`)

.. ---------------------------------------------------------------------------
.. _whatsnew_200.performance:

Performance improvements
~~~~~~~~~~~~~~~~~~~~~~~~
- Performance improvement in :meth:`.DataFrameGroupBy.median` and :meth:`.SeriesGroupBy.median` and :meth:`.DataFrameGroupBy.cumprod` for nullable dtypes (:issue:`37493`)
- Performance improvement in :meth:`.DataFrameGroupBy.all`, :meth:`.DataFrameGroupBy.any`, :meth:`.SeriesGroupBy.all`, and :meth:`.SeriesGroupBy.any` for object dtype (:issue:`50623`)
- Performance improvement in :meth:`MultiIndex.argsort` and :meth:`MultiIndex.sort_values` (:issue:`48406`)
- Performance improvement in :meth:`MultiIndex.size` (:issue:`48723`)
- Performance improvement in :meth:`MultiIndex.union` without missing values and without duplicates (:issue:`48505`, :issue:`48752`)
- Performance improvement in :meth:`MultiIndex.difference` (:issue:`48606`)
- Performance improvement in :class:`MultiIndex` set operations with sort=None (:issue:`49010`)
- Performance improvement in :meth:`.DataFrameGroupBy.mean`, :meth:`.SeriesGroupBy.mean`, :meth:`.DataFrameGroupBy.var`, and :meth:`.SeriesGroupBy.var` for extension array dtypes (:issue:`37493`)
- Performance improvement in :meth:`MultiIndex.isin` when ``level=None`` (:issue:`48622`, :issue:`49577`)
- Performance improvement in :meth:`MultiIndex.putmask` (:issue:`49830`)
- Performance improvement in :meth:`Index.union` and :meth:`MultiIndex.union` when index contains duplicates (:issue:`48900`)
- Performance improvement in :meth:`Series.rank` for pyarrow-backed dtypes (:issue:`50264`)
- Performance improvement in :meth:`Series.searchsorted` for pyarrow-backed dtypes (:issue:`50447`)
- Performance improvement in :meth:`Series.fillna` for extension array dtypes (:issue:`49722`, :issue:`50078`)
- Performance improvement in :meth:`Index.join`, :meth:`Index.intersection` and :meth:`Index.union` for masked and arrow dtypes when :class:`Index` is monotonic (:issue:`50310`, :issue:`51365`)
- Performance improvement for :meth:`Series.value_counts` with nullable dtype (:issue:`48338`)
- Performance improvement for :class:`Series` constructor passing integer numpy array with nullable dtype (:issue:`48338`)
- Performance improvement for :class:`DatetimeIndex` constructor passing a list (:issue:`48609`)
- Performance improvement in :func:`merge` and :meth:`DataFrame.join` when joining on a sorted :class:`MultiIndex` (:issue:`48504`)
- Performance improvement in :func:`to_datetime` when parsing strings with timezone offsets (:issue:`50107`)
- Performance improvement in :meth:`DataFrame.loc` and :meth:`Series.loc` for tuple-based indexing of a :class:`MultiIndex` (:issue:`48384`)
- Performance improvement for :meth:`Series.replace` with categorical dtype (:issue:`49404`)
- Performance improvement for :meth:`MultiIndex.unique` (:issue:`48335`)
- Performance improvement for indexing operations with nullable and arrow dtypes (:issue:`49420`, :issue:`51316`)
- Performance improvement for :func:`concat` with extension array backed indexes (:issue:`49128`, :issue:`49178`)
- Performance improvement for :func:`api.types.infer_dtype` (:issue:`51054`)
- Reduce memory usage of :meth:`DataFrame.to_pickle`/:meth:`Series.to_pickle` when using BZ2 or LZMA (:issue:`49068`)
- Performance improvement for :class:`~arrays.StringArray` constructor passing a numpy array with type ``np.str_`` (:issue:`49109`)
- Performance improvement in :meth:`~arrays.IntervalArray.from_tuples` (:issue:`50620`)
- Performance improvement in :meth:`~arrays.ArrowExtensionArray.factorize` (:issue:`49177`)
- Performance improvement in :meth:`~arrays.ArrowExtensionArray.__setitem__` (:issue:`50248`, :issue:`50632`)
- Performance improvement in :class:`~arrays.ArrowExtensionArray` comparison methods when array contains NA (:issue:`50524`)
- Performance improvement in :meth:`~arrays.ArrowExtensionArray.to_numpy` (:issue:`49973`, :issue:`51227`)
- Performance improvement when parsing strings to :class:`BooleanDtype` (:issue:`50613`)
- Performance improvement in :meth:`DataFrame.join` when joining on a subset of a :class:`MultiIndex` (:issue:`48611`)
- Performance improvement for :meth:`MultiIndex.intersection` (:issue:`48604`)
- Performance improvement in :meth:`DataFrame.__setitem__` (:issue:`46267`)
- Performance improvement in ``var`` and ``std`` for nullable dtypes (:issue:`48379`).
- Performance improvement when iterating over pyarrow and nullable dtypes (:issue:`49825`, :issue:`49851`)
- Performance improvements to :func:`read_sas` (:issue:`47403`, :issue:`47405`, :issue:`47656`, :issue:`48502`)
- Memory improvement in :meth:`RangeIndex.sort_values` (:issue:`48801`)
- Performance improvement in :meth:`Series.to_numpy` if ``copy=True`` by avoiding copying twice (:issue:`24345`)
- Performance improvement in :meth:`Series.rename` with :class:`MultiIndex` (:issue:`21055`)
- Performance improvement in :class:`DataFrameGroupBy` and :class:`SeriesGroupBy` when ``by`` is a categorical type and ``sort=False`` (:issue:`48976`)
- Performance improvement in :class:`DataFrameGroupBy` and :class:`SeriesGroupBy` when ``by`` is a categorical type and ``observed=False`` (:issue:`49596`)
- Performance improvement in :func:`read_stata` with parameter ``index_col`` set to ``None`` (the default). Now the index will be a :class:`RangeIndex` instead of :class:`Int64Index` (:issue:`49745`)
- Performance improvement in :func:`merge` when not merging on the index - the new index will now be :class:`RangeIndex` instead of :class:`Int64Index` (:issue:`49478`)
- Performance improvement in :meth:`DataFrame.to_dict` and :meth:`Series.to_dict` when using any non-object dtypes (:issue:`46470`)
- Performance improvement in :func:`read_html` when there are multiple tables (:issue:`49929`)
- Performance improvement in :class:`Period` constructor when constructing from a string or integer (:issue:`38312`)
- Performance improvement in :func:`to_datetime` when using ``'%Y%m%d'`` format (:issue:`17410`)
- Performance improvement in :func:`to_datetime` when format is given or can be inferred (:issue:`50465`)
- Performance improvement in :meth:`Series.median` for nullable dtypes (:issue:`50838`)
- Performance improvement in :func:`read_csv` when passing :func:`to_datetime` lambda-function to ``date_parser`` and inputs have mixed timezone offsets (:issue:`35296`)
- Performance improvement in :func:`isna` and :func:`isnull` (:issue:`50658`)
- Performance improvement in :meth:`.SeriesGroupBy.value_counts` with categorical dtype (:issue:`46202`)
- Fixed a reference leak in :func:`read_hdf` (:issue:`37441`)
- Fixed a memory leak in :meth:`DataFrame.to_json` and :meth:`Series.to_json` when serializing datetimes and timedeltas (:issue:`40443`)
- Decreased memory usage in many :class:`DataFrameGroupBy` methods (:issue:`51090`)
- Performance improvement in :meth:`DataFrame.round` for an integer ``decimal`` parameter (:issue:`17254`)
- Performance improvement in :meth:`DataFrame.replace` and :meth:`Series.replace` when using a large dict for ``to_replace`` (:issue:`6697`)
- Memory improvement in :class:`StataReader` when reading seekable files (:issue:`48922`)

.. ---------------------------------------------------------------------------
.. _whatsnew_200.bug_fixes:

Bug fixes
~~~~~~~~~

Categorical
^^^^^^^^^^^
- Bug in :meth:`Categorical.set_categories` losing dtype information (:issue:`48812`)
- Bug in :meth:`Series.replace` with categorical dtype when ``to_replace`` values overlap with new values (:issue:`49404`)
- Bug in :meth:`Series.replace` with categorical dtype losing nullable dtypes of underlying categories (:issue:`49404`)
- Bug in :meth:`DataFrame.groupby` and :meth:`Series.groupby` would reorder categories when used as a grouper (:issue:`48749`)
- Bug in :class:`Categorical` constructor when constructing from a :class:`Categorical` object and ``dtype="category"`` losing ordered-ness (:issue:`49309`)
- Bug in :meth:`.SeriesGroupBy.min`, :meth:`.SeriesGroupBy.max`, :meth:`.DataFrameGroupBy.min`, and :meth:`.DataFrameGroupBy.max` with unordered :class:`CategoricalDtype` with no groups failing to raise ``TypeError`` (:issue:`51034`)

Datetimelike
^^^^^^^^^^^^
- Bug in :func:`pandas.infer_freq`, raising ``TypeError`` when inferred on :class:`RangeIndex` (:issue:`47084`)
- Bug in :func:`to_datetime` incorrectly raising ``OverflowError`` with string arguments corresponding to large integers (:issue:`50533`)
- Bug in :func:`to_datetime` was raising on invalid offsets with ``errors='coerce'`` and ``infer_datetime_format=True`` (:issue:`48633`)
- Bug in :class:`DatetimeIndex` constructor failing to raise when ``tz=None`` is explicitly specified in conjunction with timezone-aware ``dtype`` or data (:issue:`48659`)
- Bug in subtracting a ``datetime`` scalar from :class:`DatetimeIndex` failing to retain the original ``freq`` attribute (:issue:`48818`)
- Bug in ``pandas.tseries.holiday.Holiday`` where a half-open date interval causes inconsistent return types from :meth:`USFederalHolidayCalendar.holidays` (:issue:`49075`)
- Bug in rendering :class:`DatetimeIndex` and :class:`Series` and :class:`DataFrame` with timezone-aware dtypes with ``dateutil`` or ``zoneinfo`` timezones near daylight-savings transitions (:issue:`49684`)
- Bug in :func:`to_datetime` was raising ``ValueError`` when parsing :class:`Timestamp`, ``datetime.datetime``, ``datetime.date``, or ``np.datetime64`` objects when non-ISO8601 ``format`` was passed (:issue:`49298`, :issue:`50036`)
- Bug in :func:`to_datetime` was raising ``ValueError`` when parsing empty string and non-ISO8601 format was passed. Now, empty strings will be parsed as :class:`NaT`, for compatibility with how is done for ISO8601 formats (:issue:`50251`)
- Bug in :class:`Timestamp` was showing ``UserWarning``, which was not actionable by users, when parsing non-ISO8601 delimited date strings (:issue:`50232`)
- Bug in :func:`to_datetime` was showing misleading ``ValueError`` when parsing dates with format containing ISO week directive and ISO weekday directive (:issue:`50308`)
- Bug in :meth:`Timestamp.round` when the ``freq`` argument has zero-duration (e.g. "0ns") returning incorrect results instead of raising (:issue:`49737`)
- Bug in :func:`to_datetime` was not raising ``ValueError`` when invalid format was passed and ``errors`` was ``'ignore'`` or ``'coerce'`` (:issue:`50266`)
- Bug in :class:`DateOffset` was throwing ``TypeError`` when constructing with milliseconds and another super-daily argument (:issue:`49897`)
- Bug in :func:`to_datetime` was not raising ``ValueError`` when parsing string with decimal date with format ``'%Y%m%d'`` (:issue:`50051`)
- Bug in :func:`to_datetime` was not converting ``None`` to ``NaT`` when parsing mixed-offset date strings with ISO8601 format (:issue:`50071`)
- Bug in :func:`to_datetime` was not returning input when parsing out-of-bounds date string with ``errors='ignore'`` and ``format='%Y%m%d'`` (:issue:`14487`)
- Bug in :func:`to_datetime` was converting timezone-naive ``datetime.datetime`` to timezone-aware when parsing with timezone-aware strings, ISO8601 format, and ``utc=False`` (:issue:`50254`)
- Bug in :func:`to_datetime` was throwing ``ValueError`` when parsing dates with ISO8601 format where some values were not zero-padded (:issue:`21422`)
- Bug in :func:`to_datetime` was giving incorrect results when using ``format='%Y%m%d'`` and ``errors='ignore'`` (:issue:`26493`)
- Bug in :func:`to_datetime` was failing to parse date strings ``'today'`` and ``'now'`` if ``format`` was not ISO8601 (:issue:`50359`)
- Bug in :func:`Timestamp.utctimetuple` raising a ``TypeError`` (:issue:`32174`)
- Bug in :func:`to_datetime` was raising ``ValueError`` when parsing mixed-offset :class:`Timestamp` with ``errors='ignore'`` (:issue:`50585`)
- Bug in :func:`to_datetime` was incorrectly handling floating-point inputs within 1 ``unit`` of the overflow boundaries (:issue:`50183`)
- Bug in :func:`to_datetime` with unit of "Y" or "M" giving incorrect results, not matching pointwise :class:`Timestamp` results (:issue:`50870`)
- Bug in :meth:`Series.interpolate` and :meth:`DataFrame.interpolate` with datetime or timedelta dtypes incorrectly raising ``ValueError`` (:issue:`11312`)
- Bug in :func:`to_datetime` was not returning input with ``errors='ignore'`` when input was out-of-bounds (:issue:`50587`)
- Bug in :func:`DataFrame.from_records` when given a :class:`DataFrame` input with timezone-aware datetime64 columns incorrectly dropping the timezone-awareness (:issue:`51162`)
- Bug in :func:`to_datetime` was raising ``decimal.InvalidOperation`` when parsing date strings with ``errors='coerce'`` (:issue:`51084`)
- Bug in :func:`to_datetime` with both ``unit`` and ``origin`` specified returning incorrect results (:issue:`42624`)
- Bug in :meth:`Series.astype` and :meth:`DataFrame.astype` when converting an object-dtype object containing timezone-aware datetimes or strings to ``datetime64[ns]`` incorrectly localizing as UTC instead of raising ``TypeError`` (:issue:`50140`)
- Bug in :meth:`.DataFrameGroupBy.quantile` and :meth:`.SeriesGroupBy.quantile` with datetime or timedelta dtypes giving incorrect results for groups containing ``NaT`` (:issue:`51373`)
- Bug in :meth:`.DataFrameGroupBy.quantile` and :meth:`.SeriesGroupBy.quantile` incorrectly raising with :class:`PeriodDtype` or :class:`DatetimeTZDtype` (:issue:`51373`)

Timedelta
^^^^^^^^^
- Bug in :func:`to_timedelta` raising error when input has nullable dtype ``Float64`` (:issue:`48796`)
- Bug in :class:`Timedelta` constructor incorrectly raising instead of returning ``NaT`` when given a ``np.timedelta64("nat")`` (:issue:`48898`)
- Bug in :class:`Timedelta` constructor failing to raise when passed both a :class:`Timedelta` object and keywords (e.g. days, seconds) (:issue:`48898`)
- Bug in :class:`Timedelta` comparisons with very large ``datetime.timedelta`` objects incorrect raising ``OutOfBoundsTimedelta`` (:issue:`49021`)

Timezones
^^^^^^^^^
- Bug in :meth:`Series.astype` and :meth:`DataFrame.astype` with object-dtype containing multiple timezone-aware ``datetime`` objects with heterogeneous timezones to a :class:`DatetimeTZDtype` incorrectly raising (:issue:`32581`)
- Bug in :func:`to_datetime` was failing to parse date strings with timezone name when ``format`` was specified with ``%Z`` (:issue:`49748`)
- Better error message when passing invalid values to ``ambiguous`` parameter in :meth:`Timestamp.tz_localize` (:issue:`49565`)
- Bug in string parsing incorrectly allowing a :class:`Timestamp` to be constructed with an invalid timezone, which would raise when trying to print (:issue:`50668`)
- Corrected TypeError message in :func:`objects_to_datetime64ns` to inform that DatetimeIndex has mixed timezones (:issue:`50974`)

Numeric
^^^^^^^
- Bug in :meth:`DataFrame.add` cannot apply ufunc when inputs contain mixed DataFrame type and Series type (:issue:`39853`)
- Bug in arithmetic operations on :class:`Series` not propagating mask when combining masked dtypes and numpy dtypes (:issue:`45810`, :issue:`42630`)
- Bug in :meth:`DataFrame.sem` and :meth:`Series.sem` where an erroneous ``TypeError`` would always raise when using data backed by an :class:`ArrowDtype` (:issue:`49759`)
- Bug in :meth:`Series.__add__` casting to object for list and masked :class:`Series` (:issue:`22962`)
- Bug in :meth:`~arrays.ArrowExtensionArray.mode` where ``dropna=False`` was not respected when there was ``NA`` values (:issue:`50982`)
- Bug in :meth:`DataFrame.query` with ``engine="numexpr"`` and column names are ``min`` or ``max`` would raise a ``TypeError`` (:issue:`50937`)
- Bug in :meth:`DataFrame.min` and :meth:`DataFrame.max` with tz-aware data containing ``pd.NaT`` and ``axis=1`` would return incorrect results (:issue:`51242`)

Conversion
^^^^^^^^^^
- Bug in constructing :class:`Series` with ``int64`` dtype from a string list raising instead of casting (:issue:`44923`)
- Bug in constructing :class:`Series` with masked dtype and boolean values with ``NA`` raising (:issue:`42137`)
- Bug in :meth:`DataFrame.eval` incorrectly raising an ``AttributeError`` when there are negative values in function call (:issue:`46471`)
- Bug in :meth:`Series.convert_dtypes` not converting dtype to nullable dtype when :class:`Series` contains ``NA`` and has dtype ``object`` (:issue:`48791`)
- Bug where any :class:`ExtensionDtype` subclass with ``kind="M"`` would be interpreted as a timezone type (:issue:`34986`)
- Bug in :class:`.arrays.ArrowExtensionArray` that would raise ``NotImplementedError`` when passed a sequence of strings or binary (:issue:`49172`)
- Bug in :meth:`Series.astype` raising ``pyarrow.ArrowInvalid`` when converting from a non-pyarrow string dtype to a pyarrow numeric type (:issue:`50430`)
- Bug in :meth:`DataFrame.astype` modifying input array inplace when converting to ``string`` and ``copy=False`` (:issue:`51073`)
- Bug in :meth:`Series.to_numpy` converting to NumPy array before applying ``na_value`` (:issue:`48951`)
- Bug in :meth:`DataFrame.astype` not copying data when converting to pyarrow dtype (:issue:`50984`)
- Bug in :func:`to_datetime` was not respecting ``exact`` argument when ``format`` was an ISO8601 format (:issue:`12649`)
- Bug in :meth:`TimedeltaArray.astype` raising ``TypeError`` when converting to a pyarrow duration type (:issue:`49795`)
- Bug in :meth:`DataFrame.eval` and :meth:`DataFrame.query` raising for extension array dtypes (:issue:`29618`, :issue:`50261`, :issue:`31913`)
- Bug in :meth:`Series` not copying data when created from :class:`Index` and ``dtype`` is equal to ``dtype`` from :class:`Index` (:issue:`52008`)

Strings
^^^^^^^
- Bug in :func:`pandas.api.types.is_string_dtype` that would not return ``True`` for :class:`StringDtype` or :class:`ArrowDtype` with ``pyarrow.string()`` (:issue:`15585`)
- Bug in converting string dtypes to "datetime64[ns]" or "timedelta64[ns]" incorrectly raising ``TypeError`` (:issue:`36153`)
- Bug in setting values in a string-dtype column with an array, mutating the array as side effect when it contains missing values (:issue:`51299`)

Interval
^^^^^^^^
- Bug in :meth:`IntervalIndex.is_overlapping` incorrect output if interval has duplicate left boundaries (:issue:`49581`)
- Bug in :meth:`Series.infer_objects` failing to infer :class:`IntervalDtype` for an object series of :class:`Interval` objects (:issue:`50090`)
- Bug in :meth:`Series.shift` with :class:`IntervalDtype` and invalid null ``fill_value`` failing to raise ``TypeError`` (:issue:`51258`)

Indexing
^^^^^^^^
- Bug in :meth:`DataFrame.__setitem__` raising when indexer is a :class:`DataFrame` with ``boolean`` dtype (:issue:`47125`)
- Bug in :meth:`DataFrame.reindex` filling with wrong values when indexing columns and index for ``uint`` dtypes (:issue:`48184`)
- Bug in :meth:`DataFrame.loc` when setting :class:`DataFrame` with different dtypes coercing values to single dtype (:issue:`50467`)
- Bug in :meth:`DataFrame.sort_values` where ``None`` was not returned when ``by`` is empty list and ``inplace=True`` (:issue:`50643`)
- Bug in :meth:`DataFrame.loc` coercing dtypes when setting values with a list indexer (:issue:`49159`)
- Bug in :meth:`Series.loc` raising error for out of bounds end of slice indexer (:issue:`50161`)
- Bug in :meth:`DataFrame.loc` raising ``ValueError`` with all ``False`` ``bool`` indexer and empty object (:issue:`51450`)
- Bug in :meth:`DataFrame.loc` raising ``ValueError`` with ``bool`` indexer and :class:`MultiIndex` (:issue:`47687`)
- Bug in :meth:`DataFrame.loc` raising ``IndexError`` when setting values for a pyarrow-backed column with a non-scalar indexer (:issue:`50085`)
- Bug in :meth:`DataFrame.__getitem__`, :meth:`Series.__getitem__`, :meth:`DataFrame.__setitem__` and :meth:`Series.__setitem__`
  when indexing on indexes with extension float dtypes (:class:`Float64` & :class:`Float64`) or complex dtypes using integers (:issue:`51053`)
- Bug in :meth:`DataFrame.loc` modifying object when setting incompatible value with an empty indexer (:issue:`45981`)
- Bug in :meth:`DataFrame.__setitem__` raising ``ValueError`` when right hand side is :class:`DataFrame` with :class:`MultiIndex` columns (:issue:`49121`)
- Bug in :meth:`DataFrame.reindex` casting dtype to ``object`` when :class:`DataFrame` has single extension array column when re-indexing ``columns`` and ``index`` (:issue:`48190`)
- Bug in :meth:`DataFrame.iloc` raising ``IndexError`` when indexer is a :class:`Series` with numeric extension array dtype (:issue:`49521`)
- Bug in :func:`~DataFrame.describe` when formatting percentiles in the resulting index showed more decimals than needed (:issue:`46362`)
- Bug in :meth:`DataFrame.compare` does not recognize differences when comparing ``NA`` with value in nullable dtypes (:issue:`48939`)
- Bug in :meth:`Series.rename` with :class:`MultiIndex` losing extension array dtypes (:issue:`21055`)
- Bug in :meth:`DataFrame.isetitem` coercing extension array dtypes in :class:`DataFrame` to object (:issue:`49922`)
- Bug in :meth:`Series.__getitem__` returning corrupt object when selecting from an empty pyarrow backed object (:issue:`51734`)
- Bug in :class:`BusinessHour` would cause creation of :class:`DatetimeIndex` to fail when no opening hour was included in the index (:issue:`49835`)

Missing
^^^^^^^
- Bug in :meth:`Index.equals` raising ``TypeError`` when :class:`Index` consists of tuples that contain ``NA`` (:issue:`48446`)
- Bug in :meth:`Series.map` caused incorrect result when data has NaNs and defaultdict mapping was used (:issue:`48813`)
- Bug in :class:`NA` raising a ``TypeError`` instead of return :class:`NA` when performing a binary operation with a ``bytes`` object (:issue:`49108`)
- Bug in :meth:`DataFrame.update` with ``overwrite=False`` raising ``TypeError`` when ``self`` has column with ``NaT`` values and column not present in ``other`` (:issue:`16713`)
- Bug in :meth:`Series.replace` raising ``RecursionError`` when replacing value in object-dtype :class:`Series` containing ``NA`` (:issue:`47480`)
- Bug in :meth:`Series.replace` raising ``RecursionError`` when replacing value in numeric :class:`Series` with ``NA`` (:issue:`50758`)

MultiIndex
^^^^^^^^^^
- Bug in :meth:`MultiIndex.get_indexer` not matching ``NaN`` values (:issue:`29252`, :issue:`37222`, :issue:`38623`, :issue:`42883`, :issue:`43222`, :issue:`46173`, :issue:`48905`)
- Bug in :meth:`MultiIndex.argsort` raising ``TypeError`` when index contains :attr:`NA` (:issue:`48495`)
- Bug in :meth:`MultiIndex.difference` losing extension array dtype (:issue:`48606`)
- Bug in :class:`MultiIndex.set_levels` raising ``IndexError`` when setting empty level (:issue:`48636`)
- Bug in :meth:`MultiIndex.unique` losing extension array dtype (:issue:`48335`)
- Bug in :meth:`MultiIndex.intersection` losing extension array (:issue:`48604`)
- Bug in :meth:`MultiIndex.union` losing extension array (:issue:`48498`, :issue:`48505`, :issue:`48900`)
- Bug in :meth:`MultiIndex.union` not sorting when sort=None and index contains missing values (:issue:`49010`)
- Bug in :meth:`MultiIndex.append` not checking names for equality (:issue:`48288`)
- Bug in :meth:`MultiIndex.symmetric_difference` losing extension array (:issue:`48607`)
- Bug in :meth:`MultiIndex.join` losing dtypes when :class:`MultiIndex` has duplicates (:issue:`49830`)
- Bug in :meth:`MultiIndex.putmask` losing extension array (:issue:`49830`)
- Bug in :meth:`MultiIndex.value_counts` returning a :class:`Series` indexed by flat index of tuples instead of a :class:`MultiIndex` (:issue:`49558`)

I/O
^^^
- Bug in :func:`read_sas` caused fragmentation of :class:`DataFrame` and raised :class:`.errors.PerformanceWarning` (:issue:`48595`)
- Improved error message in :func:`read_excel` by including the offending sheet name when an exception is raised while reading a file (:issue:`48706`)
- Bug when a pickling a subset PyArrow-backed data that would serialize the entire data instead of the subset (:issue:`42600`)
- Bug in :func:`read_sql_query` ignoring ``dtype`` argument when ``chunksize`` is specified and result is empty (:issue:`50245`)
- Bug in :func:`read_csv` for a single-line csv with fewer columns than ``names`` raised :class:`.errors.ParserError` with ``engine="c"`` (:issue:`47566`)
- Bug in :func:`read_json` raising with ``orient="table"`` and ``NA`` value (:issue:`40255`)
- Bug in displaying ``string`` dtypes not showing storage option (:issue:`50099`)
- Bug in :meth:`DataFrame.to_string` with ``header=False`` that printed the index name on the same line as the first row of the data (:issue:`49230`)
- Bug in :meth:`DataFrame.to_string` ignoring float formatter for extension arrays (:issue:`39336`)
- Fixed memory leak which stemmed from the initialization of the internal JSON module (:issue:`49222`)
- Fixed issue where :func:`json_normalize` would incorrectly remove leading characters from column names that matched the ``sep`` argument (:issue:`49861`)
- Bug in :func:`read_csv` unnecessarily overflowing for extension array dtype when containing ``NA`` (:issue:`32134`)
- Bug in :meth:`DataFrame.to_dict` not converting ``NA`` to ``None`` (:issue:`50795`)
- Bug in :meth:`DataFrame.to_json` where it would segfault when failing to encode a string (:issue:`50307`)
- Bug in :meth:`DataFrame.to_html` with ``na_rep`` set when the :class:`DataFrame` contains non-scalar data (:issue:`47103`)
- Bug in :func:`read_xml` where file-like objects failed when iterparse is used (:issue:`50641`)
- Bug in :func:`read_csv` when ``engine="pyarrow"`` where ``encoding`` parameter was not handled correctly (:issue:`51302`)
- Bug in :func:`read_xml` ignored repeated elements when iterparse is used (:issue:`51183`)
- Bug in :class:`ExcelWriter` leaving file handles open if an exception occurred during instantiation (:issue:`51443`)
- Bug in :meth:`DataFrame.to_parquet` where non-string index or columns were raising a ``ValueError`` when ``engine="pyarrow"`` (:issue:`52036`)

Period
^^^^^^
- Bug in :meth:`Period.strftime` and :meth:`PeriodIndex.strftime`, raising ``UnicodeDecodeError`` when a locale-specific directive was passed (:issue:`46319`)
- Bug in adding a :class:`Period` object to an array of :class:`DateOffset` objects incorrectly raising ``TypeError`` (:issue:`50162`)
- Bug in :class:`Period` where passing a string with finer resolution than nanosecond would result in a ``KeyError`` instead of dropping the extra precision (:issue:`50417`)
- Bug in parsing strings representing Week-periods e.g. "2017-01-23/2017-01-29" as minute-frequency instead of week-frequency (:issue:`50803`)
- Bug in :meth:`.DataFrameGroupBy.sum`, :meth:`.DataFrameGroupByGroupBy.cumsum`, :meth:`.DataFrameGroupByGroupBy.prod`, :meth:`.DataFrameGroupByGroupBy.cumprod` with :class:`PeriodDtype` failing to raise ``TypeError`` (:issue:`51040`)
- Bug in parsing empty string with :class:`Period` incorrectly raising ``ValueError`` instead of returning ``NaT`` (:issue:`51349`)

Plotting
^^^^^^^^
- Bug in :meth:`DataFrame.plot.hist`, not dropping elements of ``weights`` corresponding to ``NaN`` values in ``data`` (:issue:`48884`)
- ``ax.set_xlim`` was sometimes raising ``UserWarning`` which users couldn't address due to ``set_xlim`` not accepting parsing arguments - the converter now uses :func:`Timestamp` instead (:issue:`49148`)

Groupby/resample/rolling
^^^^^^^^^^^^^^^^^^^^^^^^
- Bug in :class:`.ExponentialMovingWindow` with ``online`` not raising a ``NotImplementedError`` for unsupported operations (:issue:`48834`)
- Bug in :meth:`.DataFrameGroupBy.sample` raises ``ValueError`` when the object is empty (:issue:`48459`)
- Bug in :meth:`Series.groupby` raises ``ValueError`` when an entry of the index is equal to the name of the index (:issue:`48567`)
- Bug in :meth:`.DataFrameGroupBy.resample` produces inconsistent results when passing empty DataFrame (:issue:`47705`)
- Bug in :class:`.DataFrameGroupBy` and :class:`.SeriesGroupBy` would not include unobserved categories in result when grouping by categorical indexes (:issue:`49354`)
- Bug in :class:`.DataFrameGroupBy` and :class:`.SeriesGroupBy` would change result order depending on the input index when grouping by categoricals (:issue:`49223`)
- Bug in :class:`.DataFrameGroupBy` and :class:`.SeriesGroupBy` when grouping on categorical data would sort result values even when used with ``sort=False`` (:issue:`42482`)
- Bug in :meth:`.DataFrameGroupBy.apply` and :class:`.SeriesGroupBy.apply` with ``as_index=False`` would not attempt the computation without using the grouping keys when using them failed with a ``TypeError`` (:issue:`49256`)
- Bug in :meth:`.DataFrameGroupBy.describe` would describe the group keys (:issue:`49256`)
- Bug in :meth:`.SeriesGroupBy.describe` with ``as_index=False`` would have the incorrect shape (:issue:`49256`)
- Bug in :class:`.DataFrameGroupBy` and :class:`.SeriesGroupBy` with ``dropna=False`` would drop NA values when the grouper was categorical (:issue:`36327`)
- Bug in :meth:`.SeriesGroupBy.nunique` would incorrectly raise when the grouper was an empty categorical and ``observed=True`` (:issue:`21334`)
- Bug in :meth:`.SeriesGroupBy.nth` would raise when grouper contained NA values after subsetting from a :class:`DataFrameGroupBy` (:issue:`26454`)
- Bug in :meth:`DataFrame.groupby` would not include a :class:`.Grouper` specified by ``key`` in the result when ``as_index=False`` (:issue:`50413`)
- Bug in :meth:`.DataFrameGroupBy.value_counts` would raise when used with a :class:`.TimeGrouper` (:issue:`50486`)
- Bug in :meth:`.Resampler.size` caused a wide :class:`DataFrame` to be returned instead of a :class:`Series` with :class:`MultiIndex` (:issue:`46826`)
- Bug in :meth:`.DataFrameGroupBy.transform` and :meth:`.SeriesGroupBy.transform` would raise incorrectly when grouper had ``axis=1`` for ``"idxmin"`` and ``"idxmax"`` arguments (:issue:`45986`)
- Bug in :class:`.DataFrameGroupBy` would raise when used with an empty DataFrame, categorical grouper, and ``dropna=False`` (:issue:`50634`)
- Bug in :meth:`.SeriesGroupBy.value_counts` did not respect ``sort=False`` (:issue:`50482`)
- Bug in :meth:`.DataFrameGroupBy.resample` raises ``KeyError`` when getting the result from a key list when resampling on time index (:issue:`50840`)
- Bug in :meth:`.DataFrameGroupBy.transform` and :meth:`.SeriesGroupBy.transform` would raise incorrectly when grouper had ``axis=1`` for ``"ngroup"`` argument (:issue:`45986`)
- Bug in :meth:`.DataFrameGroupBy.describe` produced incorrect results when data had duplicate columns (:issue:`50806`)
- Bug in :meth:`.DataFrameGroupBy.agg` with ``engine="numba"`` failing to respect ``as_index=False`` (:issue:`51228`)
- Bug in :meth:`.DataFrameGroupBy.agg`, :meth:`.SeriesGroupBy.agg`, and :meth:`.Resampler.agg` would ignore arguments when passed a list of functions (:issue:`50863`)
- Bug in :meth:`.DataFrameGroupBy.ohlc` ignoring ``as_index=False`` (:issue:`51413`)
- Bug in :meth:`DataFrameGroupBy.agg` after subsetting columns (e.g. ``.groupby(...)[["a", "b"]]``) would not include groupings in the result (:issue:`51186`)

Reshaping
^^^^^^^^^
- Bug in :meth:`DataFrame.pivot_table` raising ``TypeError`` for nullable dtype and ``margins=True`` (:issue:`48681`)
- Bug in :meth:`DataFrame.unstack` and :meth:`Series.unstack` unstacking wrong level of :class:`MultiIndex` when :class:`MultiIndex` has mixed names (:issue:`48763`)
- Bug in :meth:`DataFrame.melt` losing extension array dtype (:issue:`41570`)
- Bug in :meth:`DataFrame.pivot` not respecting ``None`` as column name (:issue:`48293`)
- Bug in :meth:`DataFrame.join` when ``left_on`` or ``right_on`` is or includes a :class:`CategoricalIndex` incorrectly raising ``AttributeError`` (:issue:`48464`)
- Bug in :meth:`DataFrame.pivot_table` raising ``ValueError`` with parameter ``margins=True`` when result is an empty :class:`DataFrame` (:issue:`49240`)
- Clarified error message in :func:`merge` when passing invalid ``validate`` option (:issue:`49417`)
- Bug in :meth:`DataFrame.explode` raising ``ValueError`` on multiple columns with ``NaN`` values or empty lists (:issue:`46084`)
- Bug in :meth:`DataFrame.transpose` with ``IntervalDtype`` column with ``timedelta64[ns]`` endpoints (:issue:`44917`)
- Bug in :meth:`DataFrame.agg` and :meth:`Series.agg` would ignore arguments when passed a list of functions (:issue:`50863`)

Sparse
^^^^^^
- Bug in :meth:`Series.astype` when converting a ``SparseDtype`` with ``datetime64[ns]`` subtype to ``int64`` dtype raising, inconsistent with the non-sparse behavior (:issue:`49631`,:issue:`50087`)
- Bug in :meth:`Series.astype` when converting a from ``datetime64[ns]`` to ``Sparse[datetime64[ns]]`` incorrectly raising (:issue:`50082`)
- Bug in :meth:`Series.sparse.to_coo` raising ``SystemError`` when :class:`MultiIndex` contains a ``ExtensionArray`` (:issue:`50996`)

ExtensionArray
^^^^^^^^^^^^^^
- Bug in :meth:`Series.mean` overflowing unnecessarily with nullable integers (:issue:`48378`)
- Bug in :meth:`Series.tolist` for nullable dtypes returning numpy scalars instead of python scalars (:issue:`49890`)
- Bug in :meth:`Series.round` for pyarrow-backed dtypes raising ``AttributeError`` (:issue:`50437`)
- Bug when concatenating an empty DataFrame with an ExtensionDtype to another DataFrame with the same ExtensionDtype, the resulting dtype turned into object (:issue:`48510`)
- Bug in :meth:`array.PandasArray.to_numpy` raising with ``NA`` value when ``na_value`` is specified (:issue:`40638`)
- Bug in :meth:`api.types.is_numeric_dtype` where a custom :class:`ExtensionDtype` would not return ``True`` if ``_is_numeric`` returned ``True`` (:issue:`50563`)
- Bug in :meth:`api.types.is_integer_dtype`, :meth:`api.types.is_unsigned_integer_dtype`, :meth:`api.types.is_signed_integer_dtype`, :meth:`api.types.is_float_dtype` where a custom :class:`ExtensionDtype` would not return ``True`` if ``kind`` returned the corresponding NumPy type (:issue:`50667`)
- Bug in :class:`Series` constructor unnecessarily overflowing for nullable unsigned integer dtypes (:issue:`38798`, :issue:`25880`)
- Bug in setting non-string value into ``StringArray`` raising ``ValueError`` instead of ``TypeError`` (:issue:`49632`)
- Bug in :meth:`DataFrame.reindex` not honoring the default ``copy=True`` keyword in case of columns with ExtensionDtype (and as a result also selecting multiple columns with getitem (``[]``) didn't correctly result in a copy) (:issue:`51197`)
- Bug in :class:`~arrays.ArrowExtensionArray` logical operations ``&`` and ``|`` raising ``KeyError`` (:issue:`51688`)

Styler
^^^^^^
- Fix :meth:`~pandas.io.formats.style.Styler.background_gradient` for nullable dtype :class:`Series` with ``NA`` values (:issue:`50712`)

Metadata
^^^^^^^^
- Fixed metadata propagation in :meth:`DataFrame.corr` and :meth:`DataFrame.cov` (:issue:`28283`)

Other
^^^^^
- Bug in incorrectly accepting dtype strings containing "[pyarrow]" more than once (:issue:`51548`)
- Bug in :meth:`Series.searchsorted` inconsistent behavior when accepting :class:`DataFrame` as parameter ``value`` (:issue:`49620`)
- Bug in :func:`array` failing to raise on :class:`DataFrame` inputs (:issue:`51167`)

.. ---------------------------------------------------------------------------
.. _whatsnew_200.contributors:

Contributors
~~~~~~~~~~~~

.. contributors:: v1.5.0rc0..v2.0.0
