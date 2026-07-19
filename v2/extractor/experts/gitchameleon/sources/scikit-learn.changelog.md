
# ===== SOURCE: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/doc/whats_new/v1.1.rst =====

.. include:: _contributors.rst

.. currentmodule:: sklearn

.. _release_notes_1_1:

===========
Version 1.1
===========

For a short description of the main highlights of the release, please refer to
:ref:`sphx_glr_auto_examples_release_highlights_plot_release_highlights_1_1_0.py`.

.. include:: changelog_legend.inc

.. _changes_1_1_3:

Version 1.1.3
=============

**October 2022**

This bugfix release only includes fixes for compatibility with the latest
SciPy release >= 1.9.2. Notable changes include:

- |Fix| Include `msvcp140.dll` in the scikit-learn wheels since it has been
  removed in the latest SciPy wheels.
  :pr:`24631` by :user:`Chiara Marmo <cmarmo>`.

- |Enhancement| Create wheels for Python 3.11.
  :pr:`24446` by :user:`Chiara Marmo <cmarmo>`.

Other bug fixes will be available in the next 1.2 release, which will be
released in the coming weeks.

Note that support for 32-bit Python on Windows has been dropped in this release. This
is due to the fact that SciPy 1.9.2 also dropped the support for that platform.
Windows users are advised to install the 64-bit version of Python instead.

.. _changes_1_1_2:

Version 1.1.2
=============

**August 2022**

Changed models
--------------

The following estimators and functions, when fit with the same data and
parameters, may produce different models from the previous version. This often
occurs due to changes in the modelling logic (bug fixes or enhancements), or in
random sampling procedures.

- |Fix| :class:`manifold.TSNE` now throws a `ValueError` when fit with
  `perplexity>=n_samples` to ensure mathematical correctness of the algorithm.
  :pr:`10805` by :user:`Mathias Andersen <MrMathias>` and
  :pr:`23471` by :user:`Meekail Zain <micky774>`.

Changelog
---------

- |Fix| A default HTML representation is shown for meta-estimators with invalid
  parameters. :pr:`24015` by `Thomas Fan`_.

- |Fix| Add support for F-contiguous arrays for estimators and functions whose back-end
  have been changed in 1.1.
  :pr:`23990` by :user:`Julien Jerphanion <jjerphan>`.

- |Fix| Wheels are now available for MacOS 10.9 and greater. :pr:`23833` by
  `Thomas Fan`_.

:mod:`sklearn.base`
...................

- |Fix| The `get_params` method of the :class:`base.BaseEstimator` class now supports
  estimators with `type`-type params that have the `get_params` method.
  :pr:`24017` by :user:`Henry Sorsky <hsorsky>`.

:mod:`sklearn.cluster`
......................

- |Fix| Fixed a bug in :class:`cluster.Birch` that could trigger an error when splitting
  a node if there are duplicates in the dataset.
  :pr:`23395` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

:mod:`sklearn.feature_selection`
................................

- |Fix| :class:`feature_selection.SelectFromModel` defaults to selection
  threshold 1e-5 when the estimator is either :class:`linear_model.ElasticNet`
  or :class:`linear_model.ElasticNetCV` with `l1_ratio` equals 1 or
  :class:`linear_model.LassoCV`.
  :pr:`23636` by :user:`Hao Chun Chang <haochunchang>`.

:mod:`sklearn.impute`
.....................

- |Fix| :class:`impute.SimpleImputer` uses the dtype seen in `fit` for
  `transform` when the dtype is object. :pr:`22063` by `Thomas Fan`_.

:mod:`sklearn.linear_model`
...........................

- |Fix| Use dtype-aware tolerances for the validation of gram matrices (passed by users
  or precomputed). :pr:`22059` by :user:`Malte S. Kurz <MalteKurz>`.

- |Fix| Fixed an error in :class:`linear_model.LogisticRegression` with
  `solver="newton-cg"`, `fit_intercept=True`, and a single feature. :pr:`23608`
  by `Tom Dupre la Tour`_.

:mod:`sklearn.manifold`
.......................

- |Fix| :class:`manifold.TSNE` now throws a `ValueError` when fit with
  `perplexity>=n_samples` to ensure mathematical correctness of the algorithm.
  :pr:`10805` by :user:`Mathias Andersen <MrMathias>` and
  :pr:`23471` by :user:`Meekail Zain <micky774>`.

:mod:`sklearn.metrics`
......................

- |Fix| Fixed error message of :class:`metrics.coverage_error` for 1D array input.
  :pr:`23548` by :user:`Hao Chun Chang <haochunchang>`.

:mod:`sklearn.preprocessing`
............................

- |Fix| :meth:`preprocessing.OrdinalEncoder.inverse_transform` correctly handles
  use cases where `unknown_value` or `encoded_missing_value` is `nan`. :pr:`24087`
  by `Thomas Fan`_.

:mod:`sklearn.tree`
...................

- |Fix| Fixed invalid memory access bug during fit in
  :class:`tree.DecisionTreeRegressor` and :class:`tree.DecisionTreeClassifier`.
  :pr:`23273` by `Thomas Fan`_.

.. _changes_1_1_1:

Version 1.1.1
=============

**May 2022**

Changelog
---------

- |Enhancement| The error message is improved when importing
  :class:`model_selection.HalvingGridSearchCV`,
  :class:`model_selection.HalvingRandomSearchCV`, or
  :class:`impute.IterativeImputer` without importing the experimental flag.
  :pr:`23194` by `Thomas Fan`_.

- |Enhancement| Added an extension in doc/conf.py to automatically generate
  the list of estimators that handle NaN values.
  :pr:`23198` by :user:`Lise Kleiber <lisekleiber>`, :user:`Zhehao Liu <MaxwellLZH>`
  and :user:`Chiara Marmo <cmarmo>`.

:mod:`sklearn.datasets`
.......................

- |Fix| Avoid timeouts in :func:`datasets.fetch_openml` by not passing a
  `timeout` argument, :pr:`23358` by :user:`Loïc Estève <lesteve>`.

:mod:`sklearn.decomposition`
............................

- |Fix| Avoid spurious warning in :class:`decomposition.IncrementalPCA` when
  `n_samples == n_components`. :pr:`23264` by :user:`Lucy Liu <lucyleeow>`.

:mod:`sklearn.feature_selection`
................................

- |Fix| The `partial_fit` method of :class:`feature_selection.SelectFromModel`
  now conducts validation for `max_features` and `feature_names_in` parameters.
  :pr:`23299` by :user:`Long Bao <lorentzbao>`.

:mod:`sklearn.metrics`
......................

- |Fix| Fixes :func:`metrics.precision_recall_curve` to compute precision-recall at 100%
  recall. The Precision-Recall curve now displays the last point corresponding to a
  classifier that always predicts the positive class: recall=100% and
  precision=class balance.
  :pr:`23214` by :user:`Stéphane Collot <stephanecollot>` and :user:`Max Baak <mbaak>`.

:mod:`sklearn.preprocessing`
............................

- |Fix| :class:`preprocessing.PolynomialFeatures` with ``degree`` equal to 0
  will raise error when ``include_bias`` is set to False, and outputs a single
  constant array when ``include_bias`` is set to True.
  :pr:`23370` by :user:`Zhehao Liu <MaxwellLZH>`.

:mod:`sklearn.tree`
...................

- |Fix| Fixes performance regression with low cardinality features for
  :class:`tree.DecisionTreeClassifier`,
  :class:`tree.DecisionTreeRegressor`,
  :class:`ensemble.RandomForestClassifier`,
  :class:`ensemble.RandomForestRegressor`,
  :class:`ensemble.GradientBoostingClassifier`, and
  :class:`ensemble.GradientBoostingRegressor`.
  :pr:`23410` by :user:`Loïc Estève <lesteve>`.

:mod:`sklearn.utils`
....................

- |Fix| :func:`utils.class_weight.compute_sample_weight` now works with sparse `y`.
  :pr:`23115` by :user:`kernc <kernc>`.

.. _changes_1_1:

Version 1.1.0
=============

**May 2022**

Minimal dependencies
--------------------

Version 1.1.0 of scikit-learn requires python 3.8+, numpy 1.17.3+ and
scipy 1.3.2+. Optional minimal dependency is matplotlib 3.1.2+.

Changed models
--------------

The following estimators and functions, when fit with the same data and
parameters, may produce different models from the previous version. This often
occurs due to changes in the modelling logic (bug fixes or enhancements), or in
random sampling procedures.

- |Efficiency| :class:`cluster.KMeans` now defaults to ``algorithm="lloyd"``
  instead of ``algorithm="auto"``, which was equivalent to
  ``algorithm="elkan"``. Lloyd's algorithm and Elkan's algorithm converge to the
  same solution, up to numerical rounding errors, but in general Lloyd's
  algorithm uses much less memory, and it is often faster.

- |Efficiency| Fitting :class:`tree.DecisionTreeClassifier`,
  :class:`tree.DecisionTreeRegressor`,
  :class:`ensemble.RandomForestClassifier`,
  :class:`ensemble.RandomForestRegressor`,
  :class:`ensemble.GradientBoostingClassifier`, and
  :class:`ensemble.GradientBoostingRegressor` is on average 15% faster than in
  previous versions thanks to a new sort algorithm to find the best split.
  Models might be different because of a different handling of splits
  with tied criterion values: both the old and the new sorting algorithm
  are unstable sorting algorithms. :pr:`22868` by `Thomas Fan`_.

- |Fix| The eigenvectors initialization for :class:`cluster.SpectralClustering`
  and :class:`manifold.SpectralEmbedding` now samples from a Gaussian when
  using the `'amg'` or `'lobpcg'` solver. This change  improves numerical
  stability of the solver, but may result in a different model.

- |Fix| :func:`feature_selection.f_regression` and
  :func:`feature_selection.r_regression` will now return finite score by
  default instead of `np.nan` and `np.inf` for some corner case. You can use
  `force_finite=False` if you really want to get non-finite values and keep
  the old behavior.

- |Fix| Panda's DataFrames with all non-string columns such as a MultiIndex no
  longer warns when passed into an Estimator. Estimators will continue to
  ignore the column names in DataFrames with non-string columns. For
  `feature_names_in_` to be defined, columns must be all strings. :pr:`22410` by
  `Thomas Fan`_.

- |Fix| :class:`preprocessing.KBinsDiscretizer` changed handling of bin edges
  slightly, which might result in a different encoding with the same data.

- |Fix| :func:`calibration.calibration_curve` changed handling of bin
  edges slightly, which might result in a different output curve given the same
  data.

- |Fix| :class:`discriminant_analysis.LinearDiscriminantAnalysis` now uses
  the correct variance-scaling coefficient which may result in different model
  behavior.

- |Fix| :meth:`feature_selection.SelectFromModel.fit` and
  :meth:`feature_selection.SelectFromModel.partial_fit` can now be called with
  `prefit=True`. `estimators_` will be a deep copy of `estimator` when
  `prefit=True`. :pr:`23271` by :user:`Guillaume Lemaitre <glemaitre>`.

Changelog
---------

..
    Entries should be grouped by module (in alphabetic order) and prefixed with
    one of the labels: |MajorFeature|, |Feature|, |Efficiency|, |Enhancement|,
    |Fix| or |API| (see whats_new.rst for descriptions).
    Entries should be ordered by those labels (e.g. |Fix| after |Efficiency|).
    Changes not specific to a module should be listed under *Multiple Modules*
    or *Miscellaneous*.
    Entries should end with:
    :pr:`123456` by :user:`Joe Bloggs <joeongithub>`.
    where 123456 is the *pull request* number, not the issue number.


- |Efficiency| Low-level routines for reductions on pairwise distances
  for dense float64 datasets have been refactored. The following functions
  and estimators now benefit from improved performances in terms of hardware
  scalability and speed-ups:

  - :func:`sklearn.metrics.pairwise_distances_argmin`
  - :func:`sklearn.metrics.pairwise_distances_argmin_min`
  - :class:`sklearn.cluster.AffinityPropagation`
  - :class:`sklearn.cluster.Birch`
  - :class:`sklearn.cluster.MeanShift`
  - :class:`sklearn.cluster.OPTICS`
  - :class:`sklearn.cluster.SpectralClustering`
  - :func:`sklearn.feature_selection.mutual_info_regression`
  - :class:`sklearn.neighbors.KNeighborsClassifier`
  - :class:`sklearn.neighbors.KNeighborsRegressor`
  - :class:`sklearn.neighbors.RadiusNeighborsClassifier`
  - :class:`sklearn.neighbors.RadiusNeighborsRegressor`
  - :class:`sklearn.neighbors.LocalOutlierFactor`
  - :class:`sklearn.neighbors.NearestNeighbors`
  - :class:`sklearn.manifold.Isomap`
  - :class:`sklearn.manifold.LocallyLinearEmbedding`
  - :class:`sklearn.manifold.TSNE`
  - :func:`sklearn.manifold.trustworthiness`
  - :class:`sklearn.semi_supervised.LabelPropagation`
  - :class:`sklearn.semi_supervised.LabelSpreading`

  For instance :class:`sklearn.neighbors.NearestNeighbors.kneighbors` and
  :class:`sklearn.neighbors.NearestNeighbors.radius_neighbors`
  can respectively be up to ×20 and ×5 faster than previously on a laptop.

  Moreover, implementations of those two algorithms are now suitable
  for machine with many cores, making them usable for datasets consisting
  of millions of samples.

  :pr:`21987`, :pr:`22064`, :pr:`22065`, :pr:`22288` and :pr:`22320`
  by :user:`Julien Jerphanion <jjerphan>`.

- |Enhancement| All scikit-learn models now generate a more informative
  error message when some input contains unexpected `NaN` or infinite values.
  In particular the message contains the input name ("X", "y" or
  "sample_weight") and if an unexpected `NaN` value is found in `X`, the error
  message suggests potential solutions.
  :pr:`21219` by :user:`Olivier Grisel <ogrisel>`.

- |Enhancement| All scikit-learn models now generate a more informative
  error message when setting invalid hyper-parameters with `set_params`.
  :pr:`21542` by :user:`Olivier Grisel <ogrisel>`.

- |Enhancement| Removes random unique identifiers in the HTML representation.
  With this change, jupyter notebooks are reproducible as long as the cells are
  run in the same order. :pr:`23098` by `Thomas Fan`_.

- |Fix| Estimators with `non_deterministic` tag set to `True` will skip both
  `check_methods_sample_order_invariance` and `check_methods_subset_invariance` tests.
  :pr:`22318` by :user:`Zhehao Liu <MaxwellLZH>`.

- |API| The option for using the log loss, aka binomial or multinomial deviance, via
  the `loss` parameters was made more consistent. The preferred way is by
  setting the value to `"log_loss"`. Old option names are still valid and
  produce the same models, but are deprecated and will be removed in version
  1.3.

  - For :class:`ensemble.GradientBoostingClassifier`, the `loss` parameter name
    "deviance" is deprecated in favor of the new name "log_loss", which is now the
    default.
    :pr:`23036` by :user:`Christian Lorentzen <lorentzenchr>`.

  - For :class:`ensemble.HistGradientBoostingClassifier`, the `loss` parameter names
    "auto", "binary_crossentropy" and "categorical_crossentropy" are deprecated in
    favor of the new name "log_loss", which is now the default.
    :pr:`23040` by :user:`Christian Lorentzen <lorentzenchr>`.

  - For :class:`linear_model.SGDClassifier`, the `loss` parameter name
    "log" is deprecated in favor of the new name "log_loss".
    :pr:`23046` by :user:`Christian Lorentzen <lorentzenchr>`.

- |API| Rich html representation of estimators is now enabled by default in Jupyter
  notebooks. It can be deactivated by setting `display='text'` in
  :func:`sklearn.set_config`.
  :pr:`22856` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

:mod:`sklearn.calibration`
..........................

- |Enhancement| :func:`calibration.calibration_curve` accepts a parameter
  `pos_label` to specify the positive class label.
  :pr:`21032` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Enhancement| :meth:`calibration.CalibratedClassifierCV.fit` now supports passing
  `fit_params`, which are routed to the `base_estimator`.
  :pr:`18170` by :user:`Benjamin Bossan <BenjaminBossan>`.

- |Enhancement| :class:`calibration.CalibrationDisplay` accepts a parameter `pos_label`
  to add this information to the plot.
  :pr:`21038` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| :func:`calibration.calibration_curve` handles bin edges more consistently now.
  :pr:`14975` by `Andreas Müller`_ and :pr:`22526` by :user:`Meekail Zain <micky774>`.

- |API| :func:`calibration.calibration_curve`'s `normalize` parameter is
  now deprecated and will be removed in version 1.3. It is recommended that
  a proper probability (i.e. a classifier's :term:`predict_proba` positive
  class) is used for `y_prob`.
  :pr:`23095` by :user:`Jordan Silke <jsilke>`.

:mod:`sklearn.cluster`
......................

- |MajorFeature| :class:`cluster.BisectingKMeans` introducing Bisecting K-Means algorithm
  :pr:`20031` by :user:`Michal Krawczyk <michalkrawczyk>`,
  :user:`Tom Dupre la Tour <TomDLT>`
  and :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Enhancement| :class:`cluster.SpectralClustering` and
  :func:`cluster.spectral_clustering` now include the new `'cluster_qr'` method that
  clusters samples in the embedding space as an alternative to the existing `'kmeans'`
  and `'discrete'` methods. See :func:`cluster.spectral_clustering` for more details.
  :pr:`21148` by :user:`Andrew Knyazev <lobpcg>`.

- |Enhancement| Adds :term:`get_feature_names_out` to :class:`cluster.Birch`,
  :class:`cluster.FeatureAgglomeration`, :class:`cluster.KMeans`,
  :class:`cluster.MiniBatchKMeans`. :pr:`22255` by `Thomas Fan`_.

- |Enhancement| :class:`cluster.SpectralClustering` now raises consistent
  error messages when passed invalid values for `n_clusters`, `n_init`,
  `gamma`, `n_neighbors`, `eigen_tol` or `degree`.
  :pr:`21881` by :user:`Hugo Vassard <hvassard>`.

- |Enhancement| :class:`cluster.AffinityPropagation` now returns cluster
  centers and labels if they exist, even if the model has not fully converged.
  When returning these potentially-degenerate cluster centers and labels, a new
  warning message is shown. If no cluster centers were constructed,
  then the cluster centers remain an empty list with labels set to
  `-1` and the original warning message is shown.
  :pr:`22217` by :user:`Meekail Zain <micky774>`.

- |Efficiency| In :class:`cluster.KMeans`, the default ``algorithm`` is now
  ``"lloyd"`` which is the full classical EM-style algorithm. Both ``"auto"``
  and ``"full"`` are deprecated and will be removed in version 1.3. They are
  now aliases for ``"lloyd"``. The previous default was ``"auto"``, which relied
  on Elkan's algorithm. Lloyd's algorithm uses less memory than Elkan's, it
  is faster on many datasets, and its results are identical, hence the change.
  :pr:`21735` by :user:`Aurélien Geron <ageron>`.

- |Fix| :class:`cluster.KMeans`'s `init` parameter now properly supports
  array-like input and NumPy string scalars. :pr:`22154` by `Thomas Fan`_.

:mod:`sklearn.compose`
......................

- |Fix| :class:`compose.ColumnTransformer` now removes validation errors from
  `__init__` and `set_params` methods.
  :pr:`22537` by :user:`iofall <iofall>` and :user:`Arisa Y. <arisayosh>`.

- |Fix| :term:`get_feature_names_out` functionality in
  :class:`compose.ColumnTransformer` was broken when columns were specified
  using `slice`. This is fixed in :pr:`22775` and :pr:`22913` by
  :user:`randomgeek78 <randomgeek78>`.

:mod:`sklearn.covariance`
.........................

- |Fix| :class:`covariance.GraphicalLassoCV` now accepts NumPy array for the
  parameter `alphas`.
  :pr:`22493` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.cross_decomposition`
..................................

- |Enhancement| the `inverse_transform` method of
  :class:`cross_decomposition.PLSRegression`, :class:`cross_decomposition.PLSCanonical`
  and :class:`cross_decomposition.CCA` now allows reconstruction of a `X` target when
  a `Y` parameter is given. :pr:`19680` by
  :user:`Robin Thibaut <robinthibaut>`.

- |Enhancement| Adds :term:`get_feature_names_out` to all transformers in the
  :mod:`~sklearn.cross_decomposition` module:
  :class:`cross_decomposition.CCA`,
  :class:`cross_decomposition.PLSSVD`,
  :class:`cross_decomposition.PLSRegression`,
  and :class:`cross_decomposition.PLSCanonical`. :pr:`22119` by `Thomas Fan`_.

- |Fix| The shape of the :term:`coef_` attribute of :class:`cross_decomposition.CCA`,
  :class:`cross_decomposition.PLSCanonical` and
  :class:`cross_decomposition.PLSRegression` will change in version 1.3, from
  `(n_features, n_targets)` to `(n_targets, n_features)`, to be consistent
  with other linear models and to make it work with interface expecting a
  specific shape for `coef_` (e.g. :class:`feature_selection.RFE`).
  :pr:`22016` by :user:`Guillaume Lemaitre <glemaitre>`.

- |API| add the fitted attribute `intercept_` to
  :class:`cross_decomposition.PLSCanonical`,
  :class:`cross_decomposition.PLSRegression`, and
  :class:`cross_decomposition.CCA`. The method `predict` is indeed equivalent to
  `Y = X @ coef_ + intercept_`.
  :pr:`22015` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.datasets`
.......................

- |Feature| :func:`datasets.load_files` now accepts an ignore list and
  an allow list based on file extensions.
  :pr:`19747` by :user:`Tony Attalla <tonyattalla>` and :pr:`22498` by
  :user:`Meekail Zain <micky774>`.

- |Enhancement| :func:`datasets.make_swiss_roll` now supports the optional argument
  hole; when set to True, it returns the swiss-hole dataset. :pr:`21482` by
  :user:`Sebastian Pujalte <pujaltes>`.

- |Enhancement| :func:`datasets.make_blobs` no longer copies data during the generation
  process, therefore uses less memory.
  :pr:`22412` by :user:`Zhehao Liu <MaxwellLZH>`.

- |Enhancement| :func:`datasets.load_diabetes` now accepts the parameter
  ``scaled``, to allow loading unscaled data. The scaled version of this
  dataset is now computed from the unscaled data, and can produce slightly
  different results than in previous version (within a 1e-4 absolute
  tolerance).
  :pr:`16605` by :user:`Mandy Gu <happilyeverafter95>`.

- |Enhancement| :func:`datasets.fetch_openml` now has two optional arguments
  `n_retries` and `delay`. By default, :func:`datasets.fetch_openml` will retry
  3 times in case of a network failure with a delay between each try.
  :pr:`21901` by :user:`Rileran <rileran>`.

- |Fix| :func:`datasets.fetch_covtype` is now concurrent-safe: data is downloaded
  to a temporary directory before being moved to the data directory.
  :pr:`23113` by :user:`Ilion Beyst <iasoon>`.

- |API| :func:`datasets.make_sparse_coded_signal` now accepts a parameter
  `data_transposed` to explicitly specify the shape of matrix `X`. The default
  behavior `True` is to return a transposed matrix `X` corresponding to a
  `(n_features, n_samples)` shape. The default value will change to `False` in
  version 1.3. :pr:`21425` by :user:`Gabriel Stefanini Vicente <g4brielvs>`.

:mod:`sklearn.decomposition`
............................

- |MajorFeature| Added a new estimator :class:`decomposition.MiniBatchNMF`. It is a
  faster but less accurate version of non-negative matrix factorization, better suited
  for large datasets. :pr:`16948` by :user:`Chiara Marmo <cmarmo>`,
  :user:`Patricio Cerda <pcerda>` and :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Enhancement| :func:`decomposition.dict_learning`,
  :func:`decomposition.dict_learning_online`
  and :func:`decomposition.sparse_encode` preserve dtype for `numpy.float32`.
  :class:`decomposition.DictionaryLearning`,
  :class:`decomposition.MiniBatchDictionaryLearning`
  and :class:`decomposition.SparseCoder` preserve dtype for `numpy.float32`.
  :pr:`22002` by :user:`Takeshi Oura <takoika>`.

- |Enhancement| :class:`decomposition.PCA` exposes a parameter `n_oversamples` to tune
  :func:`utils.extmath.randomized_svd` and get accurate results when the number of
  features is large.
  :pr:`21109` by :user:`Smile <x-shadow-man>`.

- |Enhancement| The :class:`decomposition.MiniBatchDictionaryLearning` and
  :func:`decomposition.dict_learning_online` have been refactored and now have a
  stopping criterion based on a small change of the dictionary or objective function,
  controlled by the new `max_iter`, `tol` and `max_no_improvement` parameters. In
  addition, some of their parameters and attributes are deprecated.

  - the `n_iter` parameter of both is deprecated. Use `max_iter` instead.
  - the `iter_offset`, `return_inner_stats`, `inner_stats` and `return_n_iter`
    parameters of :func:`decomposition.dict_learning_online` serve internal purpose
    and are deprecated.
  - the `inner_stats_`, `iter_offset_` and `random_state_` attributes of
    :class:`decomposition.MiniBatchDictionaryLearning` serve internal purpose and are
    deprecated.
  - the default value of the `batch_size` parameter of both will change from 3 to 256
    in version 1.3.

  :pr:`18975` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Enhancement| :class:`decomposition.SparsePCA` and :class:`decomposition.MiniBatchSparsePCA`
  preserve dtype for `numpy.float32`.
  :pr:`22111` by :user:`Takeshi Oura <takoika>`.

- |Enhancement| :class:`decomposition.TruncatedSVD` now allows
  `n_components == n_features`, if `algorithm='randomized'`.
  :pr:`22181` by :user:`Zach Deane-Mayer <zachmayer>`.

- |Enhancement| Adds :term:`get_feature_names_out` to all transformers in the
  :mod:`~sklearn.decomposition` module:
  :class:`decomposition.DictionaryLearning`,
  :class:`decomposition.FactorAnalysis`,
  :class:`decomposition.FastICA`,
  :class:`decomposition.IncrementalPCA`,
  :class:`decomposition.KernelPCA`,
  :class:`decomposition.LatentDirichletAllocation`,
  :class:`decomposition.MiniBatchDictionaryLearning`,
  :class:`decomposition.MiniBatchSparsePCA`,
  :class:`decomposition.NMF`,
  :class:`decomposition.PCA`,
  :class:`decomposition.SparsePCA`,
  and :class:`decomposition.TruncatedSVD`. :pr:`21334` by
  `Thomas Fan`_.

- |Enhancement| :class:`decomposition.TruncatedSVD` exposes the parameter
  `n_oversamples` and `power_iteration_normalizer` to tune
  :func:`utils.extmath.randomized_svd` and get accurate results when the number
  of features is large, the rank of the matrix is high, or other features of
  the matrix make low rank approximation difficult.
  :pr:`21705` by :user:`Jay S. Stanley III <stanleyjs>`.

- |Enhancement| :class:`decomposition.PCA` exposes the parameter
  `power_iteration_normalizer` to tune :func:`utils.extmath.randomized_svd` and
  get more accurate results when low rank approximation is difficult.
  :pr:`21705` by :user:`Jay S. Stanley III <stanleyjs>`.

- |Fix| :class:`decomposition.FastICA` now validates input parameters in `fit`
  instead of `__init__`.
  :pr:`21432` by :user:`Hannah Bohle <hhnnhh>` and
  :user:`Maren Westermann <marenwestermann>`.

- |Fix| :class:`decomposition.FastICA` now accepts `np.float32` data without
  silent upcasting. The dtype is preserved by `fit` and `fit_transform` and the
  main fitted attributes use a dtype of the same precision as the training
  data. :pr:`22806` by :user:`Jihane Bennis <JihaneBennis>` and
  :user:`Olivier Grisel <ogrisel>`.

- |Fix| :class:`decomposition.FactorAnalysis` now validates input parameters
  in `fit` instead of `__init__`.
  :pr:`21713` by :user:`Haya <HayaAlmutairi>` and :user:`Krum Arnaudov <krumeto>`.

- |Fix| :class:`decomposition.KernelPCA` now validates input parameters in
  `fit` instead of `__init__`.
  :pr:`21567` by :user:`Maggie Chege <MaggieChege>`.

- |Fix| :class:`decomposition.PCA` and :class:`decomposition.IncrementalPCA`
  more safely calculate precision using the inverse of the covariance matrix
  if `self.noise_variance_` is zero.
  :pr:`22300` by :user:`Meekail Zain <micky774>` and :pr:`15948` by :user:`sysuresh`.

- |Fix| Greatly reduced peak memory usage in :class:`decomposition.PCA` when
  calling `fit` or `fit_transform`.
  :pr:`22553` by :user:`Meekail Zain <micky774>`.

- |API| :func:`decomposition.FastICA` now supports unit variance for whitening.
  The default value of its `whiten` argument will change from `True`
  (which behaves like `'arbitrary-variance'`) to `'unit-variance'` in version 1.3.
  :pr:`19490` by :user:`Facundo Ferrin <fferrin>` and
  :user:`Julien Jerphanion <jjerphan>`.

:mod:`sklearn.discriminant_analysis`
....................................

- |Enhancement| Adds :term:`get_feature_names_out` to
  :class:`discriminant_analysis.LinearDiscriminantAnalysis`. :pr:`22120` by
  `Thomas Fan`_.

- |Fix| :class:`discriminant_analysis.LinearDiscriminantAnalysis` now uses
  the correct variance-scaling coefficient which may result in different model
  behavior. :pr:`15984` by :user:`Okon Samuel <OkonSamuel>` and :pr:`22696` by
  :user:`Meekail Zain <micky774>`.

:mod:`sklearn.dummy`
....................

- |Fix| :class:`dummy.DummyRegressor` no longer overrides the `constant`
  parameter during `fit`. :pr:`22486` by `Thomas Fan`_.

:mod:`sklearn.ensemble`
.......................

- |MajorFeature| Added additional option `loss="quantile"` to
  :class:`ensemble.HistGradientBoostingRegressor` for modelling quantiles.
  The quantile level can be specified with the new parameter `quantile`.
  :pr:`21800` and :pr:`20567` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Efficiency| `fit` of :class:`ensemble.GradientBoostingClassifier`
  and :class:`ensemble.GradientBoostingRegressor` now calls :func:`utils.check_array`
  with parameter `force_all_finite=False` for non initial warm-start runs as it has
  already been checked before.
  :pr:`22159` by :user:`Geoffrey Paris <Geoffrey-Paris>`.

- |Enhancement| :class:`ensemble.HistGradientBoostingClassifier` is faster,
  for binary and in particular for multiclass problems thanks to the new private loss
  function module.
  :pr:`20811`, :pr:`20567` and :pr:`21814` by
  :user:`Christian Lorentzen <lorentzenchr>`.

- |Enhancement| Adds support to use pre-fit models with `cv="prefit"`
  in :class:`ensemble.StackingClassifier` and :class:`ensemble.StackingRegressor`.
  :pr:`16748` by :user:`Siqi He <siqi-he>` and :pr:`22215` by
  :user:`Meekail Zain <micky774>`.

- |Enhancement| :class:`ensemble.RandomForestClassifier` and
  :class:`ensemble.ExtraTreesClassifier` have the new `criterion="log_loss"`, which is
  equivalent to `criterion="entropy"`.
  :pr:`23047` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Enhancement| Adds :term:`get_feature_names_out` to
  :class:`ensemble.VotingClassifier`, :class:`ensemble.VotingRegressor`,
  :class:`ensemble.StackingClassifier`, and
  :class:`ensemble.StackingRegressor`. :pr:`22695` and :pr:`22697`  by `Thomas Fan`_.

- |Enhancement| :class:`ensemble.RandomTreesEmbedding` now has an informative
  :term:`get_feature_names_out` function that includes both tree index and leaf index in
  the output feature names.
  :pr:`21762` by :user:`Zhehao Liu <MaxwellLZH>` and `Thomas Fan`_.

- |Efficiency| Fitting a :class:`ensemble.RandomForestClassifier`,
  :class:`ensemble.RandomForestRegressor`, :class:`ensemble.ExtraTreesClassifier`,
  :class:`ensemble.ExtraTreesRegressor`, and :class:`ensemble.RandomTreesEmbedding`
  is now faster in a multiprocessing setting, especially for subsequent fits with
  `warm_start` enabled.
  :pr:`22106` by :user:`Pieter Gijsbers <PGijsbers>`.

- |Fix| Change the parameter `validation_fraction` in
  :class:`ensemble.GradientBoostingClassifier` and
  :class:`ensemble.GradientBoostingRegressor` so that an error is raised if anything
  other than a float is passed in as an argument.
  :pr:`21632` by :user:`Genesis Valencia <genvalen>`.

- |Fix| Removed a potential source of CPU oversubscription in
  :class:`ensemble.HistGradientBoostingClassifier` and
  :class:`ensemble.HistGradientBoostingRegressor` when CPU resource usage is limited,
  for instance using cgroups quota in a docker container. :pr:`22566` by
  :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Fix| :class:`ensemble.HistGradientBoostingClassifier` and
  :class:`ensemble.HistGradientBoostingRegressor` no longer warn when
  fitting on a pandas DataFrame with a non-default `scoring` parameter and
  early_stopping enabled. :pr:`22908` by `Thomas Fan`_.

- |Fix| Fixes HTML repr for :class:`ensemble.StackingClassifier` and
  :class:`ensemble.StackingRegressor`. :pr:`23097` by `Thomas Fan`_.

- |API| The attribute `loss_` of :class:`ensemble.GradientBoostingClassifier` and
  :class:`ensemble.GradientBoostingRegressor` has been deprecated and will be removed
  in version 1.3.
  :pr:`23079` by :user:`Christian Lorentzen <lorentzenchr>`.

- |API| Changed the default of `max_features` to 1.0 for
  :class:`ensemble.RandomForestRegressor` and to `"sqrt"` for
  :class:`ensemble.RandomForestClassifier`. Note that these give the same fit
  results as before, but are much easier to understand. The old default value
  `"auto"` has been deprecated and will be removed in version 1.3. The same
  changes are also applied for :class:`ensemble.ExtraTreesRegressor` and
  :class:`ensemble.ExtraTreesClassifier`.
  :pr:`20803` by :user:`Brian Sun <bsun94>`.

- |Efficiency| Improve runtime performance of :class:`ensemble.IsolationForest`
  by skipping repetitive input checks. :pr:`23149` by :user:`Zhehao Liu <MaxwellLZH>`.

:mod:`sklearn.feature_extraction`
.................................

- |Feature| :class:`feature_extraction.FeatureHasher` now supports PyPy.
  :pr:`23023` by `Thomas Fan`_.

- |Fix| :class:`feature_extraction.FeatureHasher` now validates input parameters
  in `transform` instead of `__init__`. :pr:`21573` by
  :user:`Hannah Bohle <hhnnhh>` and :user:`Maren Westermann <marenwestermann>`.

- |Fix| :class:`feature_extraction.text.TfidfVectorizer` now does not create
  a :class:`feature_extraction.text.TfidfTransformer` at `__init__` as required
  by our API.
  :pr:`21832` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.feature_selection`
................................

- |Feature| Added auto mode to :class:`feature_selection.SequentialFeatureSelector`.
  If the argument `n_features_to_select` is `'auto'`, select features until the score
  improvement does not exceed the argument `tol`. The default value of
  `n_features_to_select` changed from `None` to `'warn'` in 1.1 and will become
  `'auto'` in 1.3. `None` and `'warn'` will be removed in 1.3. :pr:`20145` by
  :user:`murata-yu <murata-yu>`.

- |Feature| Added the ability to pass callables to the `max_features` parameter
  of :class:`feature_selection.SelectFromModel`. Also introduced new attribute
  `max_features_` which is inferred from `max_features` and the data during
  `fit`. If `max_features` is an integer, then `max_features_ = max_features`.
  If `max_features` is a callable, then `max_features_ = max_features(X)`.
  :pr:`22356` by :user:`Meekail Zain <micky774>`.

- |Enhancement| :class:`feature_selection.GenericUnivariateSelect` preserves
  float32 dtype. :pr:`18482` by :user:`Thierry Gameiro <titigmr>`
  and :user:`Daniel Kharsa <aflatoune>` and :pr:`22370` by
  :user:`Meekail Zain <micky774>`.

- |Enhancement| Add a parameter `force_finite` to
  :func:`feature_selection.f_regression` and
  :func:`feature_selection.r_regression`. This parameter allows to force the
  output to be finite in the case where a feature or the target is constant
  or that the feature and target are perfectly correlated (only for the
  F-statistic).
  :pr:`17819` by :user:`Juan Carlos Alfaro Jiménez <alfaro96>`.

- |Efficiency| Improve runtime performance of :func:`feature_selection.chi2`
  with boolean arrays. :pr:`22235` by `Thomas Fan`_.

- |Efficiency| Reduced memory usage of :func:`feature_selection.chi2`.
  :pr:`21837` by :user:`Louis Wagner <lrwagner>`.

:mod:`sklearn.gaussian_process`
...............................

- |Fix| `predict` and `sample_y` methods of
  :class:`gaussian_process.GaussianProcessRegressor` now return
  arrays of the correct shape in single-target and multi-target cases, and for
  both `normalize_y=False` and `normalize_y=True`.
  :pr:`22199` by :user:`Guillaume Lemaitre <glemaitre>`,
  :user:`Aidar Shakerimoff <AidarShakerimoff>` and
  :user:`Tenavi Nakamura-Zimmerer <Tenavi>`.

- |Fix| :class:`gaussian_process.GaussianProcessClassifier` raises
  a more informative error if `CompoundKernel` is passed via `kernel`.
  :pr:`22223` by :user:`MarcoM <marcozzxx810>`.

:mod:`sklearn.impute`
.....................

- |Enhancement| :class:`impute.SimpleImputer` now warns with feature names when features
  which are skipped due to the lack of any observed values in the training set.
  :pr:`21617` by :user:`Christian Ritter <chritter>`.

- |Enhancement| Added support for `pd.NA` in :class:`impute.SimpleImputer`.
  :pr:`21114` by :user:`Ying Xiong <yxiong>`.

- |Enhancement| Adds :term:`get_feature_names_out` to
  :class:`impute.SimpleImputer`, :class:`impute.KNNImputer`,
  :class:`impute.IterativeImputer`, and :class:`impute.MissingIndicator`.
  :pr:`21078` by `Thomas Fan`_.

- |API| The `verbose` parameter was deprecated for :class:`impute.SimpleImputer`.
  A warning will always be raised upon the removal of empty columns.
  :pr:`21448` by :user:`Oleh Kozynets <OlehKSS>` and
  :user:`Christian Ritter <chritter>`.

:mod:`sklearn.inspection`
.........................

- |Feature| Add a display to plot the boundary decision of a classifier by
  using the method :func:`inspection.DecisionBoundaryDisplay.from_estimator`.
  :pr:`16061` by `Thomas Fan`_.

- |Enhancement| In
  :meth:`inspection.PartialDependenceDisplay.from_estimator`, allow
  `kind` to accept a list of strings to specify  which type of
  plot to draw for each feature interaction.
  :pr:`19438` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Enhancement| :meth:`inspection.PartialDependenceDisplay.from_estimator`,
  :meth:`inspection.PartialDependenceDisplay.plot`, and
  `inspection.plot_partial_dependence` now support plotting centered
  Individual Conditional Expectation (cICE) and centered PDP curves controlled
  by setting the parameter `centered`.
  :pr:`18310` by :user:`Johannes Elfner <JoElfner>` and
  :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.isotonic`
.......................

- |Enhancement| Adds :term:`get_feature_names_out` to
  :class:`isotonic.IsotonicRegression`.
  :pr:`22249` by `Thomas Fan`_.

:mod:`sklearn.kernel_approximation`
...................................

- |Enhancement| Adds :term:`get_feature_names_out` to
  :class:`kernel_approximation.AdditiveChi2Sampler`.
  :class:`kernel_approximation.Nystroem`,
  :class:`kernel_approximation.PolynomialCountSketch`,
  :class:`kernel_approximation.RBFSampler`, and
  :class:`kernel_approximation.SkewedChi2Sampler`.
  :pr:`22137` and :pr:`22694` by `Thomas Fan`_.

:mod:`sklearn.linear_model`
...........................

- |Feature| :class:`linear_model.ElasticNet`, :class:`linear_model.ElasticNetCV`,
  :class:`linear_model.Lasso` and :class:`linear_model.LassoCV` support `sample_weight`
  for sparse input `X`.
  :pr:`22808` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Feature| :class:`linear_model.Ridge` with `solver="lsqr"` now supports to fit sparse
  input with `fit_intercept=True`.
  :pr:`22950` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Enhancement| :class:`linear_model.QuantileRegressor` support sparse input
  for the highs based solvers.
  :pr:`21086` by :user:`Venkatachalam Natchiappan <venkyyuvy>`.
  In addition, those solvers now use the CSC matrix right from the
  beginning which speeds up fitting.
  :pr:`22206` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Enhancement| :class:`linear_model.LogisticRegression` is faster for
  ``solvers="lbfgs"`` and ``solver="newton-cg"``, for binary and in particular for
  multiclass problems thanks to the new private loss function module. In the multiclass
  case, the memory consumption has also been reduced for these solvers as the target is
  now label encoded (mapped to integers) instead of label binarized (one-hot encoded).
  The more classes, the larger the benefit.
  :pr:`21808`, :pr:`20567` and :pr:`21814` by
  :user:`Christian Lorentzen <lorentzenchr>`.

- |Enhancement| :class:`linear_model.GammaRegressor`,
  :class:`linear_model.PoissonRegressor` and :class:`linear_model.TweedieRegressor`
  are faster for ``solvers="lbfgs"``.
  :pr:`22548`, :pr:`21808` and :pr:`20567` by
  :user:`Christian Lorentzen <lorentzenchr>`.

- |Enhancement| Rename parameter `base_estimator` to `estimator` in
  :class:`linear_model.RANSACRegressor` to improve readability and consistency.
  `base_estimator` is deprecated and will be removed in 1.3.
  :pr:`22062` by :user:`Adrian Trujillo <trujillo9616>`.

- |Enhancement| :func:`linear_model.ElasticNet` and
  other linear model classes using coordinate descent show error
  messages when non-finite parameter weights are produced. :pr:`22148`
  by :user:`Christian Ritter <chritter>` and :user:`Norbert Preining <norbusan>`.

- |Enhancement| :class:`linear_model.ElasticNet` and :class:`linear_model.Lasso`
  now raise consistent error messages when passed invalid values for `l1_ratio`,
  `alpha`, `max_iter` and `tol`.
  :pr:`22240` by :user:`Arturo Amor <ArturoAmorQ>`.

- |Enhancement| :class:`linear_model.BayesianRidge` and
  :class:`linear_model.ARDRegression` now preserve float32 dtype. :pr:`9087` by
  :user:`Arthur Imbert <Henley13>` and :pr:`22525` by :user:`Meekail Zain <micky774>`.

- |Enhancement| :class:`linear_model.RidgeClassifier` is now supporting
  multilabel classification.
  :pr:`19689` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Enhancement| :class:`linear_model.RidgeCV` and
  :class:`linear_model.RidgeClassifierCV` now raise consistent error message
  when passed invalid values for `alphas`.
  :pr:`21606` by :user:`Arturo Amor <ArturoAmorQ>`.

- |Enhancement| :class:`linear_model.Ridge` and :class:`linear_model.RidgeClassifier`
  now raise consistent error message when passed invalid values for `alpha`,
  `max_iter` and `tol`.
  :pr:`21341` by :user:`Arturo Amor <ArturoAmorQ>`.

- |Enhancement| :func:`linear_model.orthogonal_mp_gram` preserves dtype for
  `numpy.float32`.
  :pr:`22002` by :user:`Takeshi Oura <takoika>`.

- |Fix| :class:`linear_model.LassoLarsIC` now correctly computes AIC
  and BIC. An error is now raised when `n_features > n_samples` and
  when the noise variance is not provided.
  :pr:`21481` by :user:`Guillaume Lemaitre <glemaitre>` and
  :user:`Andrés Babino <ababino>`.

- |Fix| :class:`linear_model.TheilSenRegressor` now validates input parameter
  ``max_subpopulation`` in `fit` instead of `__init__`.
  :pr:`21767` by :user:`Maren Westermann <marenwestermann>`.

- |Fix| :class:`linear_model.ElasticNetCV` now produces correct
  warning when `l1_ratio=0`.
  :pr:`21724` by :user:`Yar Khine Phyo <yarkhinephyo>`.

- |Fix| :class:`linear_model.LogisticRegression` and
  :class:`linear_model.LogisticRegressionCV` now set the `n_iter_` attribute
  with a shape that respects the docstring and that is consistent with the shape
  obtained when using the other solvers in the one-vs-rest setting. Previously,
  it would record only the maximum of the number of iterations for each binary
  sub-problem while now all of them are recorded. :pr:`21998` by
  :user:`Olivier Grisel <ogrisel>`.

- |Fix| The property `family` of :class:`linear_model.TweedieRegressor` is not
  validated in `__init__` anymore. Instead, this (private) property is deprecated in
  :class:`linear_model.GammaRegressor`, :class:`linear_model.PoissonRegressor` and
  :class:`linear_model.TweedieRegressor`, and will be removed in 1.3.
  :pr:`22548` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Fix| The `coef_` and `intercept_` attributes of
  :class:`linear_model.LinearRegression` are now correctly computed in the presence of
  sample weights when the input is sparse.
  :pr:`22891` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Fix| The `coef_` and `intercept_` attributes of :class:`linear_model.Ridge` with
  `solver="sparse_cg"` and `solver="lbfgs"` are now correctly computed in the presence
  of sample weights when the input is sparse.
  :pr:`22899` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Fix| :class:`linear_model.SGDRegressor` and :class:`linear_model.SGDClassifier` now
  compute the validation error correctly when early stopping is enabled.
  :pr:`23256` by :user:`Zhehao Liu <MaxwellLZH>`.

- |API| :class:`linear_model.LassoLarsIC` now exposes `noise_variance` as
  a parameter in order to provide an estimate of the noise variance.
  This is particularly relevant when `n_features > n_samples` and the
  estimator of the noise variance cannot be computed.
  :pr:`21481` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.manifold`
.......................

- |Feature| :class:`manifold.Isomap` now supports radius-based
  neighbors via the `radius` argument.
  :pr:`19794` by :user:`Zhehao Liu <MaxwellLZH>`.

- |Enhancement| :func:`manifold.spectral_embedding` and
  :class:`manifold.SpectralEmbedding` support `np.float32` dtype and will
  preserve this dtype.
  :pr:`21534` by :user:`Andrew Knyazev <lobpcg>`.

- |Enhancement| Adds :term:`get_feature_names_out` to :class:`manifold.Isomap`
  and :class:`manifold.LocallyLinearEmbedding`. :pr:`22254` by `Thomas Fan`_.

- |Enhancement| added `metric_params` to :class:`manifold.TSNE` constructor for
  additional parameters of distance metric to use in optimization.
  :pr:`21805` by :user:`Jeanne Dionisi <jeannedionisi>` and :pr:`22685` by
  :user:`Meekail Zain <micky774>`.

- |Enhancement| :func:`manifold.trustworthiness` raises an error if
  `n_neighbours >= n_samples / 2` to ensure a correct support for the function.
  :pr:`18832` by :user:`Hong Shao Yang <hongshaoyang>` and :pr:`23033` by
  :user:`Meekail Zain <micky774>`.

- |Fix| :func:`manifold.spectral_embedding` now uses Gaussian instead of
  the previous uniform on [0, 1] random initial approximations to eigenvectors
  in eigen_solvers `lobpcg` and `amg` to improve their numerical stability.
  :pr:`21565` by :user:`Andrew Knyazev <lobpcg>`.

:mod:`sklearn.metrics`
......................

- |Feature| :func:`metrics.r2_score` and :func:`metrics.explained_variance_score` have a
  new `force_finite` parameter. Setting this parameter to `False` will return the
  actual non-finite score in case of perfect predictions or constant `y_true`,
  instead of the finite approximation (`1.0` and `0.0` respectively) currently
  returned by default. :pr:`17266` by :user:`Sylvain Marié <smarie>`.

- |Feature| :func:`metrics.d2_pinball_score` and :func:`metrics.d2_absolute_error_score`
  calculate the :math:`D^2` regression score for the pinball loss and the
  absolute error respectively. :func:`metrics.d2_absolute_error_score` is a special case
  of :func:`metrics.d2_pinball_score` with a fixed quantile parameter `alpha=0.5`
  for ease of use and discovery. The :math:`D^2` scores are generalizations
  of the `r2_score` and can be interpreted as the fraction of deviance explained.
  :pr:`22118` by :user:`Ohad Michel <ohadmich>`.

- |Enhancement| :func:`metrics.top_k_accuracy_score` raises an improved error
  message when `y_true` is binary and `y_score` is 2d. :pr:`22284` by `Thomas Fan`_.

- |Enhancement| :func:`metrics.roc_auc_score` now supports ``average=None``
  in the multiclass case when ``multiclass='ovr'`` which will return the score
  per class. :pr:`19158` by :user:`Nicki Skafte <SkafteNicki>`.

- |Enhancement| Adds `im_kw` parameter to
  :meth:`metrics.ConfusionMatrixDisplay.from_estimator`
  :meth:`metrics.ConfusionMatrixDisplay.from_predictions`, and
  :meth:`metrics.ConfusionMatrixDisplay.plot`. The `im_kw` parameter is passed
  to the `matplotlib.pyplot.imshow` call when plotting the confusion matrix.
  :pr:`20753` by `Thomas Fan`_.

- |Fix| :func:`metrics.silhouette_score` now supports integer input for precomputed
  distances. :pr:`22108` by `Thomas Fan`_.

- |Fix| Fixed a bug in :func:`metrics.normalized_mutual_info_score` which could return
  unbounded values. :pr:`22635` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Fix| Fixes :func:`metrics.precision_recall_curve` and
  :func:`metrics.average_precision_score` when true labels are all negative.
  :pr:`19085` by :user:`Varun Agrawal <varunagrawal>`.

- |API| `metrics.SCORERS` is now deprecated and will be removed in 1.3. Please
  use :func:`metrics.get_scorer_names` to retrieve the names of all available
  scorers. :pr:`22866` by `Adrin Jalali`_.

- |API| Parameters ``sample_weight`` and ``multioutput`` of
  :func:`metrics.mean_absolute_percentage_error` are now keyword-only, in accordance
  with `SLEP009 <https://scikit-learn-enhancement-proposals.readthedocs.io/en/latest/slep009/proposal.html>`_.
  A deprecation cycle was introduced.
  :pr:`21576` by :user:`Paul-Emile Dugnat <pedugnat>`.

- |API| The `"wminkowski"` metric of :class:`metrics.DistanceMetric` is deprecated
  and will be removed in version 1.3. Instead the existing `"minkowski"` metric now takes
  in an optional `w` parameter for weights. This deprecation aims at remaining consistent
  with SciPy 1.8 convention. :pr:`21873` by :user:`Yar Khine Phyo <yarkhinephyo>`.

- |API| :class:`metrics.DistanceMetric` has been moved from
  :mod:`sklearn.neighbors` to :mod:`sklearn.metrics`.
  Using `neighbors.DistanceMetric` for imports is still valid for
  backward compatibility, but this alias will be removed in 1.3.
  :pr:`21177` by :user:`Julien Jerphanion <jjerphan>`.

:mod:`sklearn.mixture`
......................

- |Enhancement| :class:`mixture.GaussianMixture` and
  :class:`mixture.BayesianGaussianMixture` can now be initialized using
  k-means++ and random data points. :pr:`20408` by
  :user:`Gordon Walsh <g-walsh>`, :user:`Alberto Ceballos<alceballosa>`
  and :user:`Andres Rios<ariosramirez>`.

- |Fix| Fix a bug that correctly initializes `precisions_cholesky_` in
  :class:`mixture.GaussianMixture` when providing `precisions_init` by taking
  its square root.
  :pr:`22058` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| :class:`mixture.GaussianMixture` now normalizes `weights_` more safely,
  preventing rounding errors when calling :meth:`mixture.GaussianMixture.sample` with
  `n_components=1`.
  :pr:`23034` by :user:`Meekail Zain <micky774>`.

:mod:`sklearn.model_selection`
..............................

- |Enhancement| it is now possible to pass `scoring="matthews_corrcoef"` to all
  model selection tools with a `scoring` argument to use the Matthews
  correlation coefficient (MCC).
  :pr:`22203` by :user:`Olivier Grisel <ogrisel>`.

- |Enhancement| raise an error during cross-validation when the fits for all the
  splits failed. Similarly raise an error during grid-search when the fits for
  all the models and all the splits failed.
  :pr:`21026` by :user:`Loïc Estève <lesteve>`.

- |Fix| :class:`model_selection.GridSearchCV`,
  :class:`model_selection.HalvingGridSearchCV`
  now validates input parameters in `fit` instead of `__init__`.
  :pr:`21880` by :user:`Mrinal Tyagi <MrinalTyagi>`.

- |Fix| :func:`model_selection.learning_curve` now supports `partial_fit`
  with regressors. :pr:`22982` by `Thomas Fan`_.

:mod:`sklearn.multiclass`
.........................

- |Enhancement| :class:`multiclass.OneVsRestClassifier` now supports a `verbose`
  parameter so progress on fitting can be seen.
  :pr:`22508` by :user:`Chris Combs <combscCode>`.

- |Fix| :meth:`multiclass.OneVsOneClassifier.predict` returns correct predictions when
  the inner classifier only has a :term:`predict_proba`. :pr:`22604` by `Thomas Fan`_.

:mod:`sklearn.neighbors`
........................

- |Enhancement| Adds :term:`get_feature_names_out` to
  :class:`neighbors.RadiusNeighborsTransformer`,
  :class:`neighbors.KNeighborsTransformer`
  and :class:`neighbors.NeighborhoodComponentsAnalysis`.
  :pr:`22212` by :user:`Meekail Zain <micky774>`.

- |Fix| :class:`neighbors.KernelDensity` now validates input parameters in `fit`
  instead of `__init__`. :pr:`21430` by :user:`Desislava Vasileva <DessyVV>` and
  :user:`Lucy Jimenez <LucyJimenez>`.

- |Fix| :func:`neighbors.KNeighborsRegressor.predict` now works properly when
  given an array-like input if `KNeighborsRegressor` is first constructed with a
  callable passed to the `weights` parameter. :pr:`22687` by
  :user:`Meekail Zain <micky774>`.

:mod:`sklearn.neural_network`
.............................

- |Enhancement| :func:`neural_network.MLPClassifier` and
  :func:`neural_network.MLPRegressor` show error
  messages when optimizers produce non-finite parameter weights. :pr:`22150`
  by :user:`Christian Ritter <chritter>` and :user:`Norbert Preining <norbusan>`.

- |Enhancement| Adds :term:`get_feature_names_out` to
  :class:`neural_network.BernoulliRBM`. :pr:`22248` by `Thomas Fan`_.

:mod:`sklearn.pipeline`
.......................

- |Enhancement| Added support for "passthrough" in :class:`pipeline.FeatureUnion`.
  Setting a transformer to "passthrough" will pass the features unchanged.
  :pr:`20860` by :user:`Shubhraneel Pal <shubhraneel>`.

- |Fix| :class:`pipeline.Pipeline` now does not validate hyper-parameters in
  `__init__` but in `.fit()`.
  :pr:`21888` by :user:`iofall <iofall>` and :user:`Arisa Y. <arisayosh>`.

- |Fix| :class:`pipeline.FeatureUnion` does not validate hyper-parameters in
  `__init__`. Validation is now handled in `.fit()` and `.fit_transform()`.
  :pr:`21954` by :user:`iofall <iofall>` and :user:`Arisa Y. <arisayosh>`.

- |Fix| Defines `__sklearn_is_fitted__` in :class:`pipeline.FeatureUnion` to
  return correct result with :func:`utils.validation.check_is_fitted`.
  :pr:`22953` by :user:`randomgeek78 <randomgeek78>`.

:mod:`sklearn.preprocessing`
............................

- |Feature| :class:`preprocessing.OneHotEncoder` now supports grouping
  infrequent categories into a single feature. Grouping infrequent categories
  is enabled by specifying how to select infrequent categories with
  `min_frequency` or `max_categories`. :pr:`16018` by `Thomas Fan`_.

- |Enhancement| Adds a `subsample` parameter to :class:`preprocessing.KBinsDiscretizer`.
  This allows specifying a maximum number of samples to be used while fitting
  the model. The option is only available when `strategy` is set to `quantile`.
  :pr:`21445` by :user:`Felipe Bidu <fbidu>` and :user:`Amanda Dsouza <amy12xx>`.

- |Enhancement| Adds `encoded_missing_value` to :class:`preprocessing.OrdinalEncoder`
  to configure the encoded value for missing data. :pr:`21988` by `Thomas Fan`_.

- |Enhancement| Added the `get_feature_names_out` method and a new parameter
  `feature_names_out` to :class:`preprocessing.FunctionTransformer`. You can set
  `feature_names_out` to 'one-to-one' to use the input features names as the
  output feature names, or you can set it to a callable that returns the output
  feature names. This is especially useful when the transformer changes the
  number of features. If `feature_names_out` is None (which is the default),
  then `get_output_feature_names` is not defined.
  :pr:`21569` by :user:`Aurélien Geron <ageron>`.

- |Enhancement| Adds :term:`get_feature_names_out` to
  :class:`preprocessing.Normalizer`,
  :class:`preprocessing.KernelCenterer`,
  :class:`preprocessing.OrdinalEncoder`, and
  :class:`preprocessing.Binarizer`. :pr:`21079` by `Thomas Fan`_.

- |Fix| :class:`preprocessing.PowerTransformer` with `method='yeo-johnson'`
  better supports significantly non-Gaussian data when searching for an optimal
  lambda. :pr:`20653` by `Thomas Fan`_.

- |Fix| :class:`preprocessing.LabelBinarizer` now validates input parameters in
  `fit` instead of `__init__`.
  :pr:`21434` by :user:`Krum Arnaudov <krumeto>`.

- |Fix| :class:`preprocessing.FunctionTransformer` with `check_inverse=True`
  now provides informative error message when input has mixed dtypes. :pr:`19916` by
  :user:`Zhehao Liu <MaxwellLZH>`.

- |Fix| :class:`preprocessing.KBinsDiscretizer` handles bin edges more consistently now.
  :pr:`14975` by `Andreas Müller`_ and :pr:`22526` by :user:`Meekail Zain <micky774>`.

- |Fix| Adds :meth:`preprocessing.KBinsDiscretizer.get_feature_names_out` support when
  `encode="ordinal"`. :pr:`22735` by `Thomas Fan`_.

:mod:`sklearn.random_projection`
................................

- |Enhancement| Adds an `inverse_transform` method and a `compute_inverse_transform`
  parameter to :class:`random_projection.GaussianRandomProjection` and
  :class:`random_projection.SparseRandomProjection`. When the parameter is set
  to True, the pseudo-inverse of the components is computed during `fit` and stored as
  `inverse_components_`. :pr:`21701` by :user:`Aurélien Geron <ageron>`.

- |Enhancement| :class:`random_projection.SparseRandomProjection` and
  :class:`random_projection.GaussianRandomProjection` preserve dtype for
  `numpy.float32`. :pr:`22114` by :user:`Takeshi Oura <takoika>`.

- |Enhancement| Adds :term:`get_feature_names_out` to all transformers in the
  :mod:`sklearn.random_projection` module:
  :class:`random_projection.GaussianRandomProjection` and
  :class:`random_projection.SparseRandomProjection`. :pr:`21330` by
  :user:`Loïc Estève <lesteve>`.

:mod:`sklearn.svm`
..................

- |Enhancement| :class:`svm.OneClassSVM`, :class:`svm.NuSVC`,
  :class:`svm.NuSVR`, :class:`svm.SVC` and :class:`svm.SVR` now expose
  `n_iter_`, the number of iterations of the libsvm optimization routine.
  :pr:`21408` by :user:`Juan Martín Loyola <jmloyola>`.

- |Enhancement| :func:`svm.SVR`, :func:`svm.SVC`, :func:`svm.NuSVR`,
  :func:`svm.OneClassSVM`, :func:`svm.NuSVC` now raise an error
  when the dual-gap estimation produces non-finite parameter weights.
  :pr:`22149` by :user:`Christian Ritter <chritter>` and
  :user:`Norbert Preining <norbusan>`.

- |Fix| :class:`svm.NuSVC`, :class:`svm.NuSVR`, :class:`svm.SVC`,
  :class:`svm.SVR`, :class:`svm.OneClassSVM` now validate input
  parameters in `fit` instead of `__init__`.
  :pr:`21436` by :user:`Haidar Almubarak <Haidar13 >`.

:mod:`sklearn.tree`
...................

- |Enhancement| :class:`tree.DecisionTreeClassifier` and
  :class:`tree.ExtraTreeClassifier` have the new `criterion="log_loss"`, which is
  equivalent to `criterion="entropy"`.
  :pr:`23047` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Fix| Fix a bug in the Poisson splitting criterion for
  :class:`tree.DecisionTreeRegressor`.
  :pr:`22191` by :user:`Christian Lorentzen <lorentzenchr>`.

- |API| Changed the default value of `max_features` to 1.0 for
  :class:`tree.ExtraTreeRegressor` and to `"sqrt"` for
  :class:`tree.ExtraTreeClassifier`, which will not change the fit result. The original
  default value `"auto"` has been deprecated and will be removed in version 1.3.
  Setting `max_features` to `"auto"` is also deprecated
  for :class:`tree.DecisionTreeClassifier` and :class:`tree.DecisionTreeRegressor`.
  :pr:`22476` by :user:`Zhehao Liu <MaxwellLZH>`.

:mod:`sklearn.utils`
....................

- |Enhancement| :func:`utils.check_array` and
  :func:`utils.multiclass.type_of_target` now accept an `input_name` parameter to make
  the error message more informative when passed invalid input data (e.g. with NaN or
  infinite values).
  :pr:`21219` by :user:`Olivier Grisel <ogrisel>`.

- |Enhancement| :func:`utils.check_array` returns a float
  ndarray with `np.nan` when passed a `Float32` or `Float64` pandas extension
  array with `pd.NA`. :pr:`21278` by `Thomas Fan`_.

- |Enhancement| :func:`utils.estimator_html_repr` shows a more helpful error
  message when running in a jupyter notebook that is not trusted. :pr:`21316`
  by `Thomas Fan`_.

- |Enhancement| :func:`utils.estimator_html_repr` displays an arrow on the top
  left corner of the HTML representation to show how the elements are
  clickable. :pr:`21298` by `Thomas Fan`_.

- |Enhancement| :func:`utils.check_array` with `dtype=None` returns numeric
  arrays when passed in a pandas DataFrame with mixed dtypes. `dtype="numeric"`
  will also make better infer the dtype when the DataFrame has mixed dtypes.
  :pr:`22237` by `Thomas Fan`_.

- |Enhancement| :func:`utils.check_scalar` now has better messages
  when displaying the type. :pr:`22218` by `Thomas Fan`_.

- |Fix| Changes the error message of the `ValidationError` raised by
  :func:`utils.check_X_y` when y is None so that it is compatible
  with the `check_requires_y_none` estimator check. :pr:`22578` by
  :user:`Claudio Salvatore Arcidiacono <ClaudioSalvatoreArcidiacono>`.

- |Fix| :func:`utils.class_weight.compute_class_weight` now only requires that
  all classes in `y` have a weight in `class_weight`. An error is still raised
  when a class is present in `y` but not in `class_weight`. :pr:`22595` by
  `Thomas Fan`_.

- |Fix| :func:`utils.estimator_html_repr` has an improved visualization for nested
  meta-estimators. :pr:`21310` by `Thomas Fan`_.

- |Fix| :func:`utils.check_scalar` raises an error when
  `include_boundaries={"left", "right"}` and the boundaries are not set.
  :pr:`22027` by :user:`Marie Lanternier <mlant>`.

- |Fix| :func:`utils.metaestimators.available_if` correctly returns a bounded
  method that can be pickled. :pr:`23077` by `Thomas Fan`_.

- |API| :func:`utils.estimator_checks.check_estimator`'s argument is now called
  `estimator` (previous name was `Estimator`). :pr:`22188` by
  :user:`Mathurin Massias <mathurinm>`.

- |API| ``utils.metaestimators.if_delegate_has_method`` is deprecated and will be
  removed in version 1.3. Use :func:`utils.metaestimators.available_if` instead.
  :pr:`22830` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

.. rubric:: Code and documentation contributors

Thanks to everyone who has contributed to the maintenance and improvement of
the project since version 1.0, including:

2357juan, Abhishek Gupta, adamgonzo, Adam Li, adijohar, Aditya Kumawat, Aditya
Raghuwanshi, Aditya Singh, Adrian Trujillo Duron, Adrin Jalali, ahmadjubair33,
AJ Druck, aj-white, Alan Peixinho, Alberto Mario Ceballos-Arroyo, Alek
Lefebvre, Alex, Alexandr, Alexandre Gramfort, alexanmv, almeidayoel, Amanda
Dsouza, Aman Sharma, Amar pratap singh, Amit, amrcode, András Simon, Andreas
Grivas, Andreas Mueller, Andrew Knyazev, Andriy, Angus L'Herrou, Ankit Sharma,
Anne Ducout, Arisa, Arth, arthurmello, Arturo Amor, ArturoAmor, Atharva Patil,
aufarkari, Aurélien Geron, avm19, Ayan Bag, baam, Bardiya Ak, Behrouz B,
Ben3940, Benjamin Bossan, Bharat Raghunathan, Bijil Subhash, bmreiniger,
Brandon Truth, Brenden Kadota, Brian Sun, cdrig, Chalmer Lowe, Chiara Marmo,
Chitteti Srinath Reddy, Chloe-Agathe Azencott, Christian Lorentzen, Christian
Ritter, christopherlim98, Christoph T. Weidemann, Christos Aridas, Claudio
Salvatore Arcidiacono, combscCode, Daniela Fernandes, darioka, Darren Nguyen,
Dave Eargle, David Gilbertson, David Poznik, Dea María Léon, Dennis Osei,
DessyVV, Dev514, Dimitri Papadopoulos Orfanos, Diwakar Gupta, Dr. Felix M.
Riese, drskd, Emiko Sano, Emmanouil Gionanidis, EricEllwanger, Erich Schubert,
Eric Larson, Eric Ndirangu, ErmolaevPA, Estefania Barreto-Ojeda, eyast, Fatima
GASMI, Federico Luna, Felix Glushchenkov, fkaren27, Fortune Uwha, FPGAwesome,
francoisgoupil, Frans Larsson, ftorres16, Gabor Berei, Gabor Kertesz, Gabriel
Stefanini Vicente, Gabriel S Vicente, Gael Varoquaux, GAURAV CHOUDHARY,
Gauthier I, genvalen, Geoffrey-Paris, Giancarlo Pablo, glennfrutiz, gpapadok,
Guillaume Lemaitre, Guillermo Tomás Fernández Martín, Gustavo Oliveira, Haidar
Almubarak, Hannah Bohle, Hansin Ahuja, Haoyin Xu, Haya, Helder Geovane Gomes de
Lima, henrymooresc, Hideaki Imamura, Himanshu Kumar, Hind-M, hmasdev, hvassard,
i-aki-y, iasoon, Inclusive Coding Bot, Ingela, iofall, Ishan Kumar, Jack Liu,
Jake Cowton, jalexand3r, J Alexander, Jauhar, Jaya Surya Kommireddy, Jay
Stanley, Jeff Hale, je-kr, JElfner, Jenny Vo, Jérémie du Boisberranger, Jihane,
Jirka Borovec, Joel Nothman, Jon Haitz Legarreta Gorroño, Jordan Silke, Jorge
Ciprián, Jorge Loayza, Joseph Chazalon, Joseph Schwartz-Messing, Jovan
Stojanovic, JSchuerz, Juan Carlos Alfaro Jiménez, Juan Martin Loyola, Julien
Jerphanion, katotten, Kaushik Roy Chowdhury, Ken4git, Kenneth Prabakaran,
kernc, Kevin Doucet, KimAYoung, Koushik Joshi, Kranthi Sedamaki, krishna kumar,
krumetoft, lesnee, Lisa Casino, Logan Thomas, Loic Esteve, Louis Wagner,
LucieClair, Lucy Liu, Luiz Eduardo Amaral, Magali, MaggieChege, Mai,
mandjevant, Mandy Gu, Manimaran, MarcoM, Marco Wurps, Maren Westermann, Maria
Boerner, MarieS-WiMLDS, Martel Corentin, martin-kokos, mathurinm, Matías,
matjansen, Matteo Francia, Maxwell, Meekail Zain, Megabyte, Mehrdad
Moradizadeh, melemo2, Michael I Chen, michalkrawczyk, Micky774, milana2,
millawell, Ming-Yang Ho, Mitzi, miwojc, Mizuki, mlant, Mohamed Haseeb, Mohit
Sharma, Moonkyung94, mpoemsl, MrinalTyagi, Mr. Leu, msabatier, murata-yu, N,
Nadirhan Şahin, Naipawat Poolsawat, NartayXD, nastegiano, nathansquan,
nat-salt, Nicki Skafte Detlefsen, Nicolas Hug, Niket Jain, Nikhil Suresh,
Nikita Titov, Nikolay Kondratyev, Ohad Michel, Oleksandr Husak, Olivier Grisel,
partev, Patrick Ferreira, Paul, pelennor, PierreAttard, Piet Brömmel, Pieter
Gijsbers, Pinky, poloso, Pramod Anantharam, puhuk, Purna Chandra Mansingh,
QuadV, Rahil Parikh, Randall Boyes, randomgeek78, Raz Hoshia, Reshama Shaikh,
Ricardo Ferreira, Richard Taylor, Rileran, Rishabh, Robin Thibaut, Rocco Meli,
Roman Feldbauer, Roman Yurchak, Ross Barnowski, rsnegrin, Sachin Yadav,
sakinaOuisrani, Sam Adam Day, Sanjay Marreddi, Sebastian Pujalte, SEELE, SELEE,
Seyedsaman (Sam) Emami, ShanDeng123, Shao Yang Hong, sharmadharmpal,
shaymerNaturalint, Shuangchi He, Shubhraneel Pal, siavrez, slishak, Smile,
spikebh, sply88, Srinath Kailasa, Stéphane Collot, Sultan Orazbayev, Sumit
Saha, Sven Eschlbeck, Sven Stehle, Swapnil Jha, Sylvain Marié, Takeshi Oura,
Tamires Santana, Tenavi, teunpe, Theis Ferré Hjortkjær, Thiruvenkadam, Thomas
J. Fan, t-jakubek, toastedyeast, Tom Dupré la Tour, Tom McTiernan, TONY GEORGE,
Tyler Martin, Tyler Reddy, Udit Gupta, Ugo Marchand, Varun Agrawal,
Venkatachalam N, Vera Komeyer, victoirelouis, Vikas Vishwakarma, Vikrant
khedkar, Vladimir Chernyy, Vladimir Kim, WeijiaDu, Xiao Yuan, Yar Khine Phyo,
Ying Xiong, yiyangq, Yosshi999, Yuki Koyama, Zach Deane-Mayer, Zeel B Patel,
zempleni, zhenfisher, 赵丰 (Zhao Feng)

# ===== SOURCE: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/doc/whats_new/v1.2.rst =====

.. include:: _contributors.rst

.. currentmodule:: sklearn

.. _release_notes_1_2:

===========
Version 1.2
===========

For a short description of the main highlights of the release, please refer to
:ref:`sphx_glr_auto_examples_release_highlights_plot_release_highlights_1_2_0.py`.

.. include:: changelog_legend.inc

.. _changes_1_2_2:

Version 1.2.2
=============

**March 2023**

Changelog
---------

:mod:`sklearn.base`
...................

- |Fix| When `set_output(transform="pandas")`, :class:`base.TransformerMixin` maintains
  the index if the :term:`transform` output is already a DataFrame. :pr:`25747` by
  `Thomas Fan`_.

:mod:`sklearn.calibration`
..........................

- |Fix| A deprecation warning is raised when using the `base_estimator__` prefix to
  set parameters of the estimator used in :class:`calibration.CalibratedClassifierCV`.
  :pr:`25477` by :user:`Tim Head <betatim>`.

:mod:`sklearn.cluster`
......................

- |Fix| Fixed a bug in :class:`cluster.BisectingKMeans`, preventing `fit` from randomly
  failing due to a permutation of the labels when running multiple inits.
  :pr:`25563` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

:mod:`sklearn.compose`
......................

- |Fix| Fixes a bug in :class:`compose.ColumnTransformer` which now supports
  empty selection of columns when `set_output(transform="pandas")`.
  :pr:`25570` by `Thomas Fan`_.

:mod:`sklearn.ensemble`
.......................

- |Fix| A deprecation warning is raised when using the `base_estimator__` prefix
  to set parameters of the estimator used in :class:`ensemble.AdaBoostClassifier`,
  :class:`ensemble.AdaBoostRegressor`, :class:`ensemble.BaggingClassifier`,
  and :class:`ensemble.BaggingRegressor`.
  :pr:`25477` by :user:`Tim Head <betatim>`.

:mod:`sklearn.feature_selection`
................................

- |Fix| Fixed a regression where a negative `tol` would not be accepted any more by
  :class:`feature_selection.SequentialFeatureSelector`.
  :pr:`25664` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

:mod:`sklearn.inspection`
.........................

- |Fix| Raise a more informative error message in :func:`inspection.partial_dependence`
  when dealing with mixed data type categories that cannot be sorted by
  :func:`numpy.unique`. This problem usually happens when categories are `str` and
  missing values are present using `np.nan`.
  :pr:`25774` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.isotonic`
.......................

- |Fix| Fixes a bug in :class:`isotonic.IsotonicRegression` where
  :meth:`isotonic.IsotonicRegression.predict` would return a pandas DataFrame
  when the global configuration sets `transform_output="pandas"`.
  :pr:`25500` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.preprocessing`
............................

- |Fix| `preprocessing.OneHotEncoder.drop_idx_` now properly
  references the dropped category in the `categories_` attribute
  when there are infrequent categories. :pr:`25589` by `Thomas Fan`_.

- |Fix| :class:`preprocessing.OrdinalEncoder` now correctly supports
  `encoded_missing_value` or `unknown_value` set to a categories' cardinality
  when there is missing values in the training data. :pr:`25704` by `Thomas Fan`_.

:mod:`sklearn.tree`
...................

- |Fix| Fixed a regression in :class:`tree.DecisionTreeClassifier`,
  :class:`tree.DecisionTreeRegressor`, :class:`tree.ExtraTreeClassifier` and
  :class:`tree.ExtraTreeRegressor` where an error was no longer raised in version
  1.2 when `min_sample_split=1`.
  :pr:`25744` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

:mod:`sklearn.utils`
....................

- |Fix| Fixes a bug in :func:`utils.check_array` which now correctly performs
  non-finite validation with the Array API specification. :pr:`25619` by
  `Thomas Fan`_.

- |Fix| :func:`utils.multiclass.type_of_target` can identify pandas
  nullable data types as classification targets. :pr:`25638` by `Thomas Fan`_.

.. _changes_1_2_1:

Version 1.2.1
=============

**January 2023**

Changed models
--------------

The following estimators and functions, when fit with the same data and
parameters, may produce different models from the previous version. This often
occurs due to changes in the modelling logic (bug fixes or enhancements), or in
random sampling procedures.

- |Fix| The fitted components in
  :class:`decomposition.MiniBatchDictionaryLearning` might differ. The online
  updates of the sufficient statistics now properly take the sizes of the
  batches into account.
  :pr:`25354` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Fix| The `categories_` attribute of :class:`preprocessing.OneHotEncoder` now
  always contains an array of `object`s when using predefined categories that
  are strings. Predefined categories encoded as bytes will no longer work
  with `X` encoded as strings. :pr:`25174` by :user:`Tim Head <betatim>`.

Changes impacting all modules
-----------------------------

- |Fix| Support `pandas.Int64` dtyped `y` for classifiers and regressors.
  :pr:`25089` by :user:`Tim Head <betatim>`.

- |Fix| Remove spurious warnings for estimators internally using neighbors search methods.
  :pr:`25129` by :user:`Julien Jerphanion <jjerphan>`.

- |Fix| Fix a bug where the current configuration was ignored in estimators using
  `n_jobs > 1`. This bug was triggered for tasks dispatched by the auxiliary
  thread of `joblib` as :func:`sklearn.get_config` used to access an empty thread
  local configuration instead of the configuration visible from the thread where
  `joblib.Parallel` was first called.
  :pr:`25363` by :user:`Guillaume Lemaitre <glemaitre>`.

Changelog
---------

:mod:`sklearn.base`
...................

- |Fix| Fix a regression in `BaseEstimator.__getstate__` that would prevent
  certain estimators from being pickled when using Python 3.11. :pr:`25188` by
  :user:`Benjamin Bossan <BenjaminBossan>`.

- |Fix| Inheriting from :class:`base.TransformerMixin` will only wrap the `transform`
  method if the class defines `transform` itself. :pr:`25295` by `Thomas Fan`_.

:mod:`sklearn.datasets`
.......................

- |Fix| Fixes an inconsistency in :func:`datasets.fetch_openml` between liac-arff
  and pandas parser when a leading space is introduced after the delimiter.
  The ARFF specs require ignoring the leading space.
  :pr:`25312` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| Fixes a bug in :func:`datasets.fetch_openml` when using `parser="pandas"`
  where single quote and backslash escape characters were not properly handled.
  :pr:`25511` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.decomposition`
............................

- |Fix| Fixed a bug in :class:`decomposition.MiniBatchDictionaryLearning` where the
  online updates of the sufficient statistics were not correct when calling
  `partial_fit` on batches of different sizes.
  :pr:`25354` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Fix| :class:`decomposition.DictionaryLearning` better supports readonly NumPy
  arrays. In particular, it better supports large datasets which are memory-mapped
  when it is used with coordinate descent algorithms (i.e. when `fit_algorithm='cd'`).
  :pr:`25172` by :user:`Julien Jerphanion <jjerphan>`.

:mod:`sklearn.ensemble`
.......................

- |Fix| :class:`ensemble.RandomForestClassifier`,
  :class:`ensemble.RandomForestRegressor`, :class:`ensemble.ExtraTreesClassifier`
  and :class:`ensemble.ExtraTreesRegressor` now support sparse readonly datasets.
  :pr:`25341` by :user:`Julien Jerphanion <jjerphan>`

:mod:`sklearn.feature_extraction`
.................................

- |Fix| :class:`feature_extraction.FeatureHasher` raises an informative error
  when the input is a list of strings. :pr:`25094` by `Thomas Fan`_.

:mod:`sklearn.linear_model`
...........................

- |Fix| Fix a regression in :class:`linear_model.SGDClassifier` and
  :class:`linear_model.SGDRegressor` that makes them unusable with the
  `verbose` parameter set to a value greater than 0.
  :pr:`25250` by :user:`Jérémie Du Boisberranger <jeremiedbb>`.

:mod:`sklearn.manifold`
.......................

- |Fix| :class:`manifold.TSNE` now works correctly when output type is
  set to pandas :pr:`25370` by :user:`Tim Head <betatim>`.

:mod:`sklearn.model_selection`
..............................

- |Fix| :func:`model_selection.cross_validate` with multimetric scoring in
  case of some failing scorers the non-failing scorers now return proper
  scores instead of `error_score` values.
  :pr:`23101` by :user:`András Simon <simonandras>` and `Thomas Fan`_.

:mod:`sklearn.neural_network`
.............................

- |Fix| :class:`neural_network.MLPClassifier` and :class:`neural_network.MLPRegressor`
  no longer raise warnings when fitting data with feature names.
  :pr:`24873` by :user:`Tim Head <betatim>`.

- |Fix| Improves error message in :class:`neural_network.MLPClassifier` and
  :class:`neural_network.MLPRegressor`, when `early_stopping=True` and
  `partial_fit` is called. :pr:`25694` by `Thomas Fan`_.

:mod:`sklearn.preprocessing`
............................

- |Fix| :meth:`preprocessing.FunctionTransformer.inverse_transform` correctly
  supports DataFrames that are all numerical when `check_inverse=True`.
  :pr:`25274` by `Thomas Fan`_.

- |Fix| :meth:`preprocessing.SplineTransformer.get_feature_names_out` correctly
  returns feature names when `extrapolations="periodic"`. :pr:`25296` by
  `Thomas Fan`_.

:mod:`sklearn.tree`
...................

- |Fix| :class:`tree.DecisionTreeClassifier`, :class:`tree.DecisionTreeRegressor`
  :class:`tree.ExtraTreeClassifier` and :class:`tree.ExtraTreeRegressor`
  now support sparse readonly datasets.
  :pr:`25341` by :user:`Julien Jerphanion <jjerphan>`

:mod:`sklearn.utils`
....................

- |Fix| Restore :func:`utils.check_array`'s behaviour for pandas Series of type
  boolean. The type is maintained, instead of converting to `float64.`
  :pr:`25147` by :user:`Tim Head <betatim>`.

- |API| `utils.fixes.delayed` is deprecated in 1.2.1 and will be removed
  in 1.5. Instead, import :func:`utils.parallel.delayed` and use it in
  conjunction with the newly introduced :func:`utils.parallel.Parallel`
  to ensure proper propagation of the scikit-learn configuration to
  the workers.
  :pr:`25363` by :user:`Guillaume Lemaitre <glemaitre>`.

.. _changes_1_2:

Version 1.2.0
=============

**December 2022**

Changed models
--------------

The following estimators and functions, when fit with the same data and
parameters, may produce different models from the previous version. This often
occurs due to changes in the modelling logic (bug fixes or enhancements), or in
random sampling procedures.

- |Enhancement| The default `eigen_tol` for :class:`cluster.SpectralClustering`,
  :class:`manifold.SpectralEmbedding`, :func:`cluster.spectral_clustering`,
  and :func:`manifold.spectral_embedding` is now `None` when using the `'amg'`
  or `'lobpcg'` solvers. This change improves numerical stability of the
  solver, but may result in a different model.

- |Enhancement| :class:`linear_model.GammaRegressor`,
  :class:`linear_model.PoissonRegressor` and :class:`linear_model.TweedieRegressor`
  can reach higher precision with the lbfgs solver, in particular when `tol` is set
  to a tiny value. Moreover, `verbose` is now properly propagated to L-BFGS-B.
  :pr:`23619` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Enhancement| The default value for `eps` :func:`metrics.log_loss` has changed
  from `1e-15` to `"auto"`. `"auto"` sets `eps` to `np.finfo(y_pred.dtype).eps`.
  :pr:`24354` by :user:`Safiuddin Khaja <Safikh>` and :user:`gsiisg <gsiisg>`.

- |Fix| Make sign of `components_` deterministic in :class:`decomposition.SparsePCA`.
  :pr:`23935` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| The `components_` signs in :class:`decomposition.FastICA` might differ.
  It is now consistent and deterministic with all SVD solvers.
  :pr:`22527` by :user:`Meekail Zain <micky774>` and `Thomas Fan`_.

- |Fix| The condition for early stopping has now been changed in
  `linear_model._sgd_fast._plain_sgd` which is used by
  :class:`linear_model.SGDRegressor` and :class:`linear_model.SGDClassifier`. The old
  condition did not disambiguate between
  training and validation set and had an effect of overscaling the error tolerance.
  This has been fixed in :pr:`23798` by :user:`Harsh Agrawal <Harsh14901>`.

- |Fix| For :class:`model_selection.GridSearchCV` and
  :class:`model_selection.RandomizedSearchCV` ranks corresponding to nan
  scores will all be set to the maximum possible rank.
  :pr:`24543` by :user:`Guillaume Lemaitre <glemaitre>`.

- |API| The default value of `tol` was changed from `1e-3` to `1e-4` for
  :func:`linear_model.ridge_regression`, :class:`linear_model.Ridge` and
  :class:`linear_model.RidgeClassifier`.
  :pr:`24465` by :user:`Christian Lorentzen <lorentzenchr>`.

Changes impacting all modules
-----------------------------

- |MajorFeature| The `set_output` API has been adopted by all transformers.
  Meta-estimators that contain transformers such as :class:`pipeline.Pipeline`
  or :class:`compose.ColumnTransformer` also define a `set_output`.
  For details, see
  `SLEP018 <https://scikit-learn-enhancement-proposals.readthedocs.io/en/latest/slep018/proposal.html>`__.
  :pr:`23734` and :pr:`24699` by `Thomas Fan`_.

- |Efficiency| Low-level routines for reductions on pairwise distances
  for dense float32 datasets have been refactored. The following functions
  and estimators now benefit from improved performances in terms of hardware
  scalability and speed-ups:

  - :func:`sklearn.metrics.pairwise_distances_argmin`
  - :func:`sklearn.metrics.pairwise_distances_argmin_min`
  - :class:`sklearn.cluster.AffinityPropagation`
  - :class:`sklearn.cluster.Birch`
  - :class:`sklearn.cluster.MeanShift`
  - :class:`sklearn.cluster.OPTICS`
  - :class:`sklearn.cluster.SpectralClustering`
  - :func:`sklearn.feature_selection.mutual_info_regression`
  - :class:`sklearn.neighbors.KNeighborsClassifier`
  - :class:`sklearn.neighbors.KNeighborsRegressor`
  - :class:`sklearn.neighbors.RadiusNeighborsClassifier`
  - :class:`sklearn.neighbors.RadiusNeighborsRegressor`
  - :class:`sklearn.neighbors.LocalOutlierFactor`
  - :class:`sklearn.neighbors.NearestNeighbors`
  - :class:`sklearn.manifold.Isomap`
  - :class:`sklearn.manifold.LocallyLinearEmbedding`
  - :class:`sklearn.manifold.TSNE`
  - :func:`sklearn.manifold.trustworthiness`
  - :class:`sklearn.semi_supervised.LabelPropagation`
  - :class:`sklearn.semi_supervised.LabelSpreading`

  For instance :meth:`sklearn.neighbors.NearestNeighbors.kneighbors` and
  :meth:`sklearn.neighbors.NearestNeighbors.radius_neighbors`
  can respectively be up to ×20 and ×5 faster than previously on a laptop.

  Moreover, implementations of those two algorithms are now suitable
  for machine with many cores, making them usable for datasets consisting
  of millions of samples.

  :pr:`23865` by :user:`Julien Jerphanion <jjerphan>`.

- |Enhancement| Finiteness checks (detection of NaN and infinite values) in all
  estimators are now significantly more efficient for float32 data by leveraging
  NumPy's SIMD optimized primitives.
  :pr:`23446` by :user:`Meekail Zain <micky774>`

- |Enhancement| Finiteness checks (detection of NaN and infinite values) in all
  estimators are now faster by utilizing a more efficient stop-on-first
  second-pass algorithm.
  :pr:`23197` by :user:`Meekail Zain <micky774>`

- |Enhancement| Support for combinations of dense and sparse datasets pairs
  for all distance metrics and for float32 and float64 datasets has been added
  or has seen its performance improved for the following estimators:

  - :func:`sklearn.metrics.pairwise_distances_argmin`
  - :func:`sklearn.metrics.pairwise_distances_argmin_min`
  - :class:`sklearn.cluster.AffinityPropagation`
  - :class:`sklearn.cluster.Birch`
  - :class:`sklearn.cluster.SpectralClustering`
  - :class:`sklearn.neighbors.KNeighborsClassifier`
  - :class:`sklearn.neighbors.KNeighborsRegressor`
  - :class:`sklearn.neighbors.RadiusNeighborsClassifier`
  - :class:`sklearn.neighbors.RadiusNeighborsRegressor`
  - :class:`sklearn.neighbors.LocalOutlierFactor`
  - :class:`sklearn.neighbors.NearestNeighbors`
  - :class:`sklearn.manifold.Isomap`
  - :class:`sklearn.manifold.TSNE`
  - :func:`sklearn.manifold.trustworthiness`

  :pr:`23604` and :pr:`23585` by :user:`Julien Jerphanion <jjerphan>`,
  :user:`Olivier Grisel <ogrisel>`, and `Thomas Fan`_,
  :pr:`24556` by :user:`Vincent Maladière <Vincent-Maladiere>`.

- |Fix| Systematically check the sha256 digest of dataset tarballs used in code
  examples in the documentation.
  :pr:`24617` by :user:`Olivier Grisel <ogrisel>` and `Thomas Fan`_. Thanks to
  `Sim4n6 <https://huntr.dev/users/sim4n6>`_ for the report.

Changelog
---------

..
    Entries should be grouped by module (in alphabetic order) and prefixed with
    one of the labels: |MajorFeature|, |Feature|, |Efficiency|, |Enhancement|,
    |Fix| or |API| (see whats_new.rst for descriptions).
    Entries should be ordered by those labels (e.g. |Fix| after |Efficiency|).
    Changes not specific to a module should be listed under *Multiple Modules*
    or *Miscellaneous*.
    Entries should end with:
    :pr:`123456` by :user:`Joe Bloggs <joeongithub>`.
    where 123456 is the *pull request* number, not the issue number.

:mod:`sklearn.base`
...................

- |Enhancement| Introduces :class:`base.ClassNamePrefixFeaturesOutMixin` and
  :class:`base.ClassNamePrefixFeaturesOutMixin` mixins that define
  :term:`get_feature_names_out` for common transformer use cases.
  :pr:`24688` by `Thomas Fan`_.

:mod:`sklearn.calibration`
..........................

- |API| Rename `base_estimator` to `estimator` in
  :class:`calibration.CalibratedClassifierCV` to improve readability and consistency.
  The parameter `base_estimator` is deprecated and will be removed in 1.4.
  :pr:`22054` by :user:`Kevin Roice <kevroi>`.

:mod:`sklearn.cluster`
......................

- |Efficiency| :class:`cluster.KMeans` with `algorithm="lloyd"` is now faster
  and uses less memory. :pr:`24264` by
  :user:`Vincent Maladiere <Vincent-Maladiere>`.

- |Enhancement| The `predict` and `fit_predict` methods of :class:`cluster.OPTICS` now
  accept sparse data type for input data. :pr:`14736` by :user:`Hunt Zhan <huntzhan>`,
  :pr:`20802` by :user:`Brandon Pokorny <Clickedbigfoot>`,
  and :pr:`22965` by :user:`Meekail Zain <micky774>`.

- |Enhancement| :class:`cluster.Birch` now preserves dtype for `numpy.float32`
  inputs. :pr:`22968` by `Meekail Zain <micky774>`.

- |Enhancement| :class:`cluster.KMeans` and :class:`cluster.MiniBatchKMeans`
  now accept a new `'auto'` option for `n_init` which changes the number of
  random initializations to one when using `init='k-means++'` for efficiency.
  This begins deprecation for the default values of `n_init` in the two classes
  and both will have their defaults changed to `n_init='auto'` in 1.4.
  :pr:`23038` by :user:`Meekail Zain <micky774>`.

- |Enhancement| :class:`cluster.SpectralClustering` and
  :func:`cluster.spectral_clustering` now propagate the `eigen_tol` parameter
  to all choices of `eigen_solver`. Includes a new option `eigen_tol="auto"`
  and begins deprecation to change the default from `eigen_tol=0` to
  `eigen_tol="auto"` in version 1.3.
  :pr:`23210` by :user:`Meekail Zain <micky774>`.

- |Fix| :class:`cluster.KMeans` now supports readonly attributes when predicting.
  :pr:`24258` by `Thomas Fan`_

- |API| The `affinity` attribute is now deprecated for
  :class:`cluster.AgglomerativeClustering` and will be renamed to `metric` in v1.4.
  :pr:`23470` by :user:`Meekail Zain <micky774>`.

:mod:`sklearn.datasets`
.......................

- |Enhancement| Introduce the new parameter `parser` in
  :func:`datasets.fetch_openml`. `parser="pandas"` allows to use the very CPU
  and memory efficient `pandas.read_csv` parser to load dense ARFF
  formatted dataset files. It is possible to pass `parser="liac-arff"`
  to use the old LIAC parser.
  When `parser="auto"`, dense datasets are loaded with "pandas" and sparse
  datasets are loaded with "liac-arff".
  Currently, `parser="liac-arff"` by default and will change to `parser="auto"`
  in version 1.4
  :pr:`21938` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Enhancement| :func:`datasets.dump_svmlight_file` is now accelerated with a
  Cython implementation, providing 2-4x speedups.
  :pr:`23127` by :user:`Meekail Zain <micky774>`

- |Enhancement| Path-like objects, such as those created with pathlib are now
  allowed as paths in :func:`datasets.load_svmlight_file` and
  :func:`datasets.load_svmlight_files`.
  :pr:`19075` by :user:`Carlos Ramos Carreño <vnmabus>`.

- |Fix| Make sure that :func:`datasets.fetch_lfw_people` and
  :func:`datasets.fetch_lfw_pairs` internally crop images based on the
  `slice_` parameter.
  :pr:`24951` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.decomposition`
............................

- |Efficiency| :func:`decomposition.FastICA.fit` has been optimised w.r.t
  its memory footprint and runtime.
  :pr:`22268` by :user:`MohamedBsh <Bsh>`.

- |Enhancement| :class:`decomposition.SparsePCA` and
  :class:`decomposition.MiniBatchSparsePCA` now implement an `inverse_transform`
  function.
  :pr:`23905` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Enhancement| :class:`decomposition.FastICA` now allows the user to select
  how whitening is performed through the new `whiten_solver` parameter, which
  supports `svd` and `eigh`. `whiten_solver` defaults to `svd` although `eigh`
  may be faster and more memory efficient in cases where
  `num_features > num_samples`.
  :pr:`11860` by :user:`Pierre Ablin <pierreablin>`,
  :pr:`22527` by :user:`Meekail Zain <micky774>` and `Thomas Fan`_.

- |Enhancement| :class:`decomposition.LatentDirichletAllocation` now preserves dtype
  for `numpy.float32` input. :pr:`24528` by :user:`Takeshi Oura <takoika>` and
  :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Fix| Make sign of `components_` deterministic in :class:`decomposition.SparsePCA`.
  :pr:`23935` by :user:`Guillaume Lemaitre <glemaitre>`.

- |API| The `n_iter` parameter of :class:`decomposition.MiniBatchSparsePCA` is
  deprecated and replaced by the parameters `max_iter`, `tol`, and
  `max_no_improvement` to be consistent with
  :class:`decomposition.MiniBatchDictionaryLearning`. `n_iter` will be removed
  in version 1.3. :pr:`23726` by :user:`Guillaume Lemaitre <glemaitre>`.

- |API| The `n_features_` attribute of
  :class:`decomposition.PCA` is deprecated in favor of
  `n_features_in_` and will be removed in 1.4. :pr:`24421` by
  :user:`Kshitij Mathur <Kshitij68>`.

:mod:`sklearn.discriminant_analysis`
....................................

- |MajorFeature| :class:`discriminant_analysis.LinearDiscriminantAnalysis` now
  supports the `Array API <https://data-apis.org/array-api/latest/>`_ for
  `solver="svd"`. Array API support is considered experimental and might evolve
  without being subjected to our usual rolling deprecation cycle policy. See
  :ref:`array_api` for more details. :pr:`22554` by `Thomas Fan`_.

- |Fix| Validate parameters only in `fit` and not in `__init__`
  for :class:`discriminant_analysis.QuadraticDiscriminantAnalysis`.
  :pr:`24218` by :user:`Stefanie Molin <stefmolin>`.

:mod:`sklearn.ensemble`
.......................

- |MajorFeature| :class:`ensemble.HistGradientBoostingClassifier` and
  :class:`ensemble.HistGradientBoostingRegressor` now support
  interaction constraints via the argument `interaction_cst` of their
  constructors.
  :pr:`21020` by :user:`Christian Lorentzen <lorentzenchr>`.
  Using interaction constraints also makes fitting faster.
  :pr:`24856` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Feature| Adds `class_weight` to :class:`ensemble.HistGradientBoostingClassifier`.
  :pr:`22014` by `Thomas Fan`_.

- |Efficiency| Improve runtime performance of :class:`ensemble.IsolationForest`
  by avoiding data copies. :pr:`23252` by :user:`Zhehao Liu <MaxwellLZH>`.

- |Enhancement| :class:`ensemble.StackingClassifier` now accepts any kind of
  base estimator.
  :pr:`24538` by :user:`Guillem G Subies <GuillemGSubies>`.

- |Enhancement| Make it possible to pass the `categorical_features` parameter
  of :class:`ensemble.HistGradientBoostingClassifier` and
  :class:`ensemble.HistGradientBoostingRegressor` as feature names.
  :pr:`24889` by :user:`Olivier Grisel <ogrisel>`.

- |Enhancement| :class:`ensemble.StackingClassifier` now supports
  multilabel-indicator target
  :pr:`24146` by :user:`Nicolas Peretti <nicoperetti>`,
  :user:`Nestor Navarro <nestornav>`, :user:`Nati Tomattis <natitomattis>`,
  and :user:`Vincent Maladiere <Vincent-Maladiere>`.

- |Enhancement| :class:`ensemble.HistGradientBoostingClassifier` and
  :class:`ensemble.HistGradientBoostingRegressor` now accept their
  `monotonic_cst` parameter to be passed as a dictionary in addition
  to the previously supported array-like format.
  Such dictionary have feature names as keys and one of `-1`, `0`, `1`
  as value to specify monotonicity constraints for each feature.
  :pr:`24855` by :user:`Olivier Grisel <ogrisel>`.

- |Enhancement| Interaction constraints for
  :class:`ensemble.HistGradientBoostingClassifier`
  and :class:`ensemble.HistGradientBoostingRegressor` can now be specified
  as strings for two common cases: "no_interactions" and "pairwise" interactions.
  :pr:`24849` by :user:`Tim Head <betatim>`.

- |Fix| Fixed the issue where :class:`ensemble.AdaBoostClassifier` outputs
  NaN in feature importance when fitted with very small sample weight.
  :pr:`20415` by :user:`Zhehao Liu <MaxwellLZH>`.

- |Fix| :class:`ensemble.HistGradientBoostingClassifier` and
  :class:`ensemble.HistGradientBoostingRegressor` no longer error when predicting
  on categories encoded as negative values and instead consider them a member
  of the "missing category". :pr:`24283` by `Thomas Fan`_.

- |Fix| :class:`ensemble.HistGradientBoostingClassifier` and
  :class:`ensemble.HistGradientBoostingRegressor`, with `verbose>=1`, print detailed
  timing information on computing histograms and finding best splits. The time spent in
  the root node was previously missing and is now included in the printed information.
  :pr:`24894` by :user:`Christian Lorentzen <lorentzenchr>`.

- |API| Rename the constructor parameter `base_estimator` to `estimator` in
  the following classes:
  :class:`ensemble.BaggingClassifier`,
  :class:`ensemble.BaggingRegressor`,
  :class:`ensemble.AdaBoostClassifier`,
  :class:`ensemble.AdaBoostRegressor`.
  `base_estimator` is deprecated in 1.2 and will be removed in 1.4.
  :pr:`23819` by :user:`Adrian Trujillo <trujillo9616>` and
  :user:`Edoardo Abati <EdAbati>`.

- |API| Rename the fitted attribute `base_estimator_` to `estimator_` in
  the following classes:
  :class:`ensemble.BaggingClassifier`,
  :class:`ensemble.BaggingRegressor`,
  :class:`ensemble.AdaBoostClassifier`,
  :class:`ensemble.AdaBoostRegressor`,
  :class:`ensemble.RandomForestClassifier`,
  :class:`ensemble.RandomForestRegressor`,
  :class:`ensemble.ExtraTreesClassifier`,
  :class:`ensemble.ExtraTreesRegressor`,
  :class:`ensemble.RandomTreesEmbedding`,
  :class:`ensemble.IsolationForest`.
  `base_estimator_` is deprecated in 1.2 and will be removed in 1.4.
  :pr:`23819` by :user:`Adrian Trujillo <trujillo9616>` and
  :user:`Edoardo Abati <EdAbati>`.

:mod:`sklearn.feature_selection`
................................

- |Fix| Fix a bug in :func:`feature_selection.mutual_info_regression` and
  :func:`feature_selection.mutual_info_classif`, where the continuous features
  in `X` should be scaled to a unit variance independently if the target `y` is
  continuous or discrete.
  :pr:`24747` by :user:`Guillaume Lemaitre <glemaitre>`

:mod:`sklearn.gaussian_process`
...............................

- |Fix| Fix :class:`gaussian_process.kernels.Matern` gradient computation with
  `nu=0.5` for PyPy (and possibly other non CPython interpreters). :pr:`24245`
  by :user:`Loïc Estève <lesteve>`.

- |Fix| The `fit` method of :class:`gaussian_process.GaussianProcessRegressor`
  will not modify the input X in case a custom kernel is used, with a `diag`
  method that returns part of the input X. :pr:`24405`
  by :user:`Omar Salman <OmarManzoor>`.

:mod:`sklearn.impute`
.....................

- |Enhancement| Added `keep_empty_features` parameter to
  :class:`impute.SimpleImputer`, :class:`impute.KNNImputer` and
  :class:`impute.IterativeImputer`, preventing removal of features
  containing only missing values when transforming.
  :pr:`16695` by :user:`Vitor Santa Rosa <vitorsrg>`.

:mod:`sklearn.inspection`
.........................

- |MajorFeature| Extended :func:`inspection.partial_dependence` and
  :class:`inspection.PartialDependenceDisplay` to handle categorical features.
  :pr:`18298` by :user:`Madhura Jayaratne <madhuracj>` and
  :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| :class:`inspection.DecisionBoundaryDisplay` now raises error if input
  data is not 2-dimensional.
  :pr:`25077` by :user:`Arturo Amor <ArturoAmorQ>`.

:mod:`sklearn.kernel_approximation`
...................................

- |Enhancement| :class:`kernel_approximation.RBFSampler` now preserves
  dtype for `numpy.float32` inputs. :pr:`24317` by `Tim Head <betatim>`.

- |Enhancement| :class:`kernel_approximation.SkewedChi2Sampler` now preserves
  dtype for `numpy.float32` inputs. :pr:`24350` by :user:`Rahil Parikh <rprkh>`.

- |Enhancement| :class:`kernel_approximation.RBFSampler` now accepts
  `'scale'` option for parameter `gamma`.
  :pr:`24755` by :user:`Hleb Levitski <glevv>`.

:mod:`sklearn.linear_model`
...........................

- |Enhancement| :class:`linear_model.LogisticRegression`,
  :class:`linear_model.LogisticRegressionCV`, :class:`linear_model.GammaRegressor`,
  :class:`linear_model.PoissonRegressor` and :class:`linear_model.TweedieRegressor` got
  a new solver `solver="newton-cholesky"`. This is a 2nd order (Newton) optimisation
  routine that uses a Cholesky decomposition of the hessian matrix.
  When `n_samples >> n_features`, the `"newton-cholesky"` solver has been observed to
  converge both faster and to a higher precision solution than the `"lbfgs"` solver on
  problems with one-hot encoded categorical variables with some rare categorical
  levels.
  :pr:`24637` and :pr:`24767` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Enhancement| :class:`linear_model.GammaRegressor`,
  :class:`linear_model.PoissonRegressor` and :class:`linear_model.TweedieRegressor`
  can reach higher precision with the lbfgs solver, in particular when `tol` is set
  to a tiny value. Moreover, `verbose` is now properly propagated to L-BFGS-B.
  :pr:`23619` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Fix| :class:`linear_model.SGDClassifier` and :class:`linear_model.SGDRegressor` will
  raise an error when all the validation samples have zero sample weight.
  :pr:`23275` by `Zhehao Liu <MaxwellLZH>`.

- |Fix| :class:`linear_model.SGDOneClassSVM` no longer performs parameter
  validation in the constructor. All validation is now handled in `fit()` and
  `partial_fit()`.
  :pr:`24433` by :user:`Yogendrasingh <iofall>`, :user:`Arisa Y. <arisayosh>`
  and :user:`Tim Head <betatim>`.

- |Fix| Fix average loss calculation when early stopping is enabled in
  :class:`linear_model.SGDRegressor` and :class:`linear_model.SGDClassifier`.
  Also updated the condition for early stopping accordingly.
  :pr:`23798` by :user:`Harsh Agrawal <Harsh14901>`.

- |API| The default value for the `solver` parameter in
  :class:`linear_model.QuantileRegressor` will change from `"interior-point"`
  to `"highs"` in version 1.4.
  :pr:`23637` by :user:`Guillaume Lemaitre <glemaitre>`.

- |API| String option `"none"` is deprecated for `penalty` argument
  in :class:`linear_model.LogisticRegression`, and will be removed in version 1.4.
  Use `None` instead. :pr:`23877` by :user:`Zhehao Liu <MaxwellLZH>`.

- |API| The default value of `tol` was changed from `1e-3` to `1e-4` for
  :func:`linear_model.ridge_regression`, :class:`linear_model.Ridge` and
  :class:`linear_model.RidgeClassifier`.
  :pr:`24465` by :user:`Christian Lorentzen <lorentzenchr>`.

:mod:`sklearn.manifold`
.......................

- |Feature| Adds option to use the normalized stress in :class:`manifold.MDS`. This is
  enabled by setting the new `normalize` parameter to `True`.
  :pr:`10168` by :user:`Łukasz Borchmann <Borchmann>`,
  :pr:`12285` by :user:`Matthias Miltenberger <mattmilten>`,
  :pr:`13042` by :user:`Matthieu Parizy <matthieu-pa>`,
  :pr:`18094` by :user:`Roth E Conrad <rotheconrad>` and
  :pr:`22562` by :user:`Meekail Zain <micky774>`.

- |Enhancement| Adds `eigen_tol` parameter to
  :class:`manifold.SpectralEmbedding`. Both :func:`manifold.spectral_embedding`
  and :class:`manifold.SpectralEmbedding` now propagate `eigen_tol` to all
  choices of `eigen_solver`. Includes a new option `eigen_tol="auto"`
  and begins deprecation to change the default from `eigen_tol=0` to
  `eigen_tol="auto"` in version 1.3.
  :pr:`23210` by :user:`Meekail Zain <micky774>`.

- |Enhancement| :class:`manifold.Isomap` now preserves
  dtype for `np.float32` inputs. :pr:`24714` by :user:`Rahil Parikh <rprkh>`.

- |API| Added an `"auto"` option to the `normalized_stress` argument in
  :class:`manifold.MDS` and :func:`manifold.smacof`. Note that
  `normalized_stress` is only valid for non-metric MDS, therefore the `"auto"`
  option enables `normalized_stress` when `metric=False` and disables it when
  `metric=True`. `"auto"` will become the default value for `normalized_stress`
  in version 1.4.
  :pr:`23834` by :user:`Meekail Zain <micky774>`

:mod:`sklearn.metrics`
......................

- |Feature| :func:`metrics.ConfusionMatrixDisplay.from_estimator`,
  :func:`metrics.ConfusionMatrixDisplay.from_predictions`, and
  :meth:`metrics.ConfusionMatrixDisplay.plot` accepts a `text_kw` parameter which is
  passed to matplotlib's `text` function. :pr:`24051` by `Thomas Fan`_.

- |Feature| :func:`metrics.class_likelihood_ratios` is added to compute the positive and
  negative likelihood ratios derived from the confusion matrix
  of a binary classification problem. :pr:`22518` by
  :user:`Arturo Amor <ArturoAmorQ>`.

- |Feature| Add :class:`metrics.PredictionErrorDisplay` to plot residuals vs
  predicted and actual vs predicted to qualitatively assess the behavior of a
  regressor. The display can be created with the class methods
  :func:`metrics.PredictionErrorDisplay.from_estimator` and
  :func:`metrics.PredictionErrorDisplay.from_predictions`. :pr:`18020` by
  :user:`Guillaume Lemaitre <glemaitre>`.

- |Feature| :func:`metrics.roc_auc_score` now supports micro-averaging
  (`average="micro"`) for the One-vs-Rest multiclass case (`multi_class="ovr"`).
  :pr:`24338` by :user:`Arturo Amor <ArturoAmorQ>`.

- |Enhancement| Adds an `"auto"` option to `eps` in :func:`metrics.log_loss`.
  This option will automatically set the `eps` value depending on the data
  type of `y_pred`. In addition, the default value of `eps` is changed from
  `1e-15` to the new `"auto"` option.
  :pr:`24354` by :user:`Safiuddin Khaja <Safikh>` and :user:`gsiisg <gsiisg>`.

- |Fix| Allows `csr_matrix` as input for parameter: `y_true` of
  the :func:`metrics.label_ranking_average_precision_score` metric.
  :pr:`23442` by :user:`Sean Atukorala <ShehanAT>`

- |Fix| :func:`metrics.ndcg_score` will now trigger a warning when the `y_true`
  value contains a negative value. Users may still use negative values, but the
  result may not be between 0 and 1. Starting in v1.4, passing in negative
  values for `y_true` will raise an error.
  :pr:`22710` by :user:`Conroy Trinh <trinhcon>` and
  :pr:`23461` by :user:`Meekail Zain <micky774>`.

- |Fix| :func:`metrics.log_loss` with `eps=0` now returns a correct value of 0 or
  `np.inf` instead of `nan` for predictions at the boundaries (0 or 1). It also accepts
  integer input.
  :pr:`24365` by :user:`Christian Lorentzen <lorentzenchr>`.

- |API| The parameter `sum_over_features` of
  :func:`metrics.pairwise.manhattan_distances` is deprecated and will be removed in 1.4.
  :pr:`24630` by :user:`Rushil Desai <rusdes>`.

:mod:`sklearn.model_selection`
..............................

- |Feature| Added the class :class:`model_selection.LearningCurveDisplay`
  that allows to make easy plotting of learning curves obtained by the function
  :func:`model_selection.learning_curve`.
  :pr:`24084` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| For all `SearchCV` classes and scipy >= 1.10, rank corresponding to a
  nan score is correctly set to the maximum possible rank, rather than
  `np.iinfo(np.int32).min`. :pr:`24141` by :user:`Loïc Estève <lesteve>`.

- |Fix| In both :class:`model_selection.HalvingGridSearchCV` and
  :class:`model_selection.HalvingRandomSearchCV` parameter
  combinations with a NaN score now share the lowest rank.
  :pr:`24539` by :user:`Tim Head <betatim>`.

- |Fix| For :class:`model_selection.GridSearchCV` and
  :class:`model_selection.RandomizedSearchCV` ranks corresponding to nan
  scores will all be set to the maximum possible rank.
  :pr:`24543` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.multioutput`
..........................

- |Feature| Added boolean `verbose` flag to classes:
  :class:`multioutput.ClassifierChain` and :class:`multioutput.RegressorChain`.
  :pr:`23977` by :user:`Eric Fiegel <efiegel>`,
  :user:`Chiara Marmo <cmarmo>`,
  :user:`Lucy Liu <lucyleeow>`, and
  :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.naive_bayes`
..........................

- |Feature| Add methods `predict_joint_log_proba` to all naive Bayes classifiers.
  :pr:`23683` by :user:`Andrey Melnik <avm19>`.

- |Enhancement| A new parameter `force_alpha` was added to
  :class:`naive_bayes.BernoulliNB`, :class:`naive_bayes.ComplementNB`,
  :class:`naive_bayes.CategoricalNB`, and :class:`naive_bayes.MultinomialNB`,
  allowing user to set parameter alpha to a very small number, greater or equal
  0, which was earlier automatically changed to `1e-10` instead.
  :pr:`16747` by :user:`arka204`,
  :pr:`18805` by :user:`hongshaoyang`,
  :pr:`22269` by :user:`Meekail Zain <micky774>`.

:mod:`sklearn.neighbors`
........................

- |Feature| Adds new function :func:`neighbors.sort_graph_by_row_values` to
  sort a CSR sparse graph such that each row is stored with increasing values.
  This is useful to improve efficiency when using precomputed sparse distance
  matrices in a variety of estimators and avoid an `EfficiencyWarning`.
  :pr:`23139` by `Tom Dupre la Tour`_.

- |Efficiency| :class:`neighbors.NearestCentroid` is faster and requires
  less memory as it better leverages CPUs' caches to compute predictions.
  :pr:`24645` by :user:`Olivier Grisel <ogrisel>`.

- |Enhancement| :class:`neighbors.KernelDensity` bandwidth parameter now accepts
  definition using Scott's and Silverman's estimation methods.
  :pr:`10468` by :user:`Ruben <icfly2>` and :pr:`22993` by
  :user:`Jovan Stojanovic <jovan-stojanovic>`.

- |Enhancement| `neighbors.NeighborsBase` now accepts
  Minkowski semi-metric (i.e. when :math:`0 < p < 1` for
  `metric="minkowski"`) for `algorithm="auto"` or `algorithm="brute"`.
  :pr:`24750` by :user:`Rudresh Veerkhare <RudreshVeerkhare>`

- |Fix| :class:`neighbors.NearestCentroid` now raises an informative error message at fit-time
  instead of failing with a low-level error message at predict-time.
  :pr:`23874` by :user:`Juan Gomez <2357juan>`.

- |Fix| Set `n_jobs=None` by default (instead of `1`) for
  :class:`neighbors.KNeighborsTransformer` and
  :class:`neighbors.RadiusNeighborsTransformer`.
  :pr:`24075` by :user:`Valentin Laurent <Valentin-Laurent>`.

- |Enhancement| :class:`neighbors.LocalOutlierFactor` now preserves
  dtype for `numpy.float32` inputs.
  :pr:`22665` by :user:`Julien Jerphanion <jjerphan>`.

:mod:`sklearn.neural_network`
.............................

- |Fix| :class:`neural_network.MLPClassifier` and
  :class:`neural_network.MLPRegressor` always expose the parameters `best_loss_`,
  `validation_scores_`, and `best_validation_score_`. `best_loss_` is set to
  `None` when `early_stopping=True`, while `validation_scores_` and
  `best_validation_score_` are set to `None` when `early_stopping=False`.
  :pr:`24683` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.pipeline`
.......................

- |Enhancement| :meth:`pipeline.FeatureUnion.get_feature_names_out` can now
  be used when one of the transformers in the :class:`pipeline.FeatureUnion` is
  `"passthrough"`. :pr:`24058` by :user:`Diederik Perdok <diederikwp>`

- |Enhancement| The :class:`pipeline.FeatureUnion` class now has a `named_transformers`
  attribute for accessing transformers by name.
  :pr:`20331` by :user:`Christopher Flynn <crflynn>`.

:mod:`sklearn.preprocessing`
............................

- |Enhancement| :class:`preprocessing.FunctionTransformer` will always try to set
  `n_features_in_` and `feature_names_in_` regardless of the `validate` parameter.
  :pr:`23993` by `Thomas Fan`_.

- |Fix| :class:`preprocessing.LabelEncoder` correctly encodes NaNs in `transform`.
  :pr:`22629` by `Thomas Fan`_.

- |API| The `sparse` parameter of :class:`preprocessing.OneHotEncoder`
  is now deprecated and will be removed in version 1.4. Use `sparse_output` instead.
  :pr:`24412` by :user:`Rushil Desai <rusdes>`.

:mod:`sklearn.svm`
..................

- |API| The `class_weight_` attribute is now deprecated for
  :class:`svm.NuSVR`, :class:`svm.SVR`, :class:`svm.OneClassSVM`.
  :pr:`22898` by :user:`Meekail Zain <micky774>`.

:mod:`sklearn.tree`
...................

- |Enhancement| :func:`tree.plot_tree`, :func:`tree.export_graphviz` now uses
  a lower case `x[i]` to represent feature `i`. :pr:`23480` by `Thomas Fan`_.

:mod:`sklearn.utils`
....................

- |Feature| A new module exposes development tools to discover estimators (i.e.
  :func:`utils.discovery.all_estimators`), displays (i.e.
  :func:`utils.discovery.all_displays`) and functions (i.e.
  :func:`utils.discovery.all_functions`) in scikit-learn.
  :pr:`21469` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Enhancement| :func:`utils.extmath.randomized_svd` now accepts an argument,
  `lapack_svd_driver`, to specify the lapack driver used in the internal
  deterministic SVD used by the randomized SVD algorithm.
  :pr:`20617` by :user:`Srinath Kailasa <skailasa>`

- |Enhancement| :func:`utils.validation.column_or_1d` now accepts a `dtype`
  parameter to specific `y`'s dtype. :pr:`22629` by `Thomas Fan`_.

- |Enhancement| `utils.extmath.cartesian` now accepts arrays with different
  `dtype` and will cast the output to the most permissive `dtype`.
  :pr:`25067` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| :func:`utils.multiclass.type_of_target` now properly handles sparse matrices.
  :pr:`14862` by :user:`Léonard Binet <leonardbinet>`.

- |Fix| HTML representation no longer errors when an estimator class is a value in
  `get_params`. :pr:`24512` by `Thomas Fan`_.

- |Fix| :func:`utils.estimator_checks.check_estimator` now takes into account
  the `requires_positive_X` tag correctly. :pr:`24667` by `Thomas Fan`_.

- |Fix| :func:`utils.check_array` now supports Pandas Series with `pd.NA`
  by raising a better error message or returning a compatible `ndarray`.
  :pr:`25080` by `Thomas Fan`_.

- |API| The extra keyword parameters of :func:`utils.extmath.density` are deprecated
  and will be removed in 1.4.
  :pr:`24523` by :user:`Mia Bajic <clytaemnestra>`.

.. rubric:: Code and documentation contributors

Thanks to everyone who has contributed to the maintenance and improvement of
the project since version 1.1, including:

2357juan, 3lLobo, Adam J. Stewart, Adam Kania, Adam Li, Aditya Anulekh, Admir
Demiraj, adoublet, Adrin Jalali, Ahmedbgh, Aiko, Akshita Prasanth, Ala-Na,
Alessandro Miola, Alex, Alexandr, Alexandre Perez-Lebel, Alex Buzenet, Ali H.
El-Kassas, aman kumar, Amit Bera, András Simon, Andreas Grivas, Andreas
Mueller, Andrew Wang, angela-maennel, Aniket Shirsat, Anthony22-dev, Antony
Lee, anupam, Apostolos Tsetoglou, Aravindh R, Artur Hermano, Arturo Amor,
as-90, ashah002, Ashwin Mathur, avm19, Azaria Gebremichael, b0rxington, Badr
MOUFAD, Bardiya Ak, Bartłomiej Gońda, BdeGraaff, Benjamin Bossan, Benjamin
Carter, berkecanrizai, Bernd Fritzke, Bhoomika, Biswaroop Mitra, Brandon TH
Chen, Brett Cannon, Bsh, cache-missing, carlo, Carlos Ramos Carreño, ceh,
chalulu, Changyao Chen, Charles Zablit, Chiara Marmo, Christian Lorentzen,
Christian Ritter, Christian Veenhuis, christianwaldmann, Christine P. Chai,
Claudio Salvatore Arcidiacono, Clément Verrier, crispinlogan, Da-Lan,
DanGonite57, Daniela Fernandes, DanielGaerber, darioka, Darren Nguyen,
davidblnc, david-cortes, David Gilbertson, David Poznik, Dayne, Dea María
Léon, Denis, Dev Khant, Dhanshree Arora, Diadochokinetic, diederikwp, Dimitri
Papadopoulos Orfanos, Dimitris Litsidis, drewhogg, Duarte OC, Dwight Lindquist,
Eden Brekke, Edern, Edoardo Abati, Eleanore Denies, EliaSchiavon, Emir,
ErmolaevPA, Fabrizio Damicelli, fcharras, Felipe Siola, Flynn,
francesco-tuveri, Franck Charras, ftorres16, Gael Varoquaux, Geevarghese
George, genvalen, GeorgiaMayDay, Gianr Lazz, Hleb Levitski, Glòria Macià
Muñoz, Guillaume Lemaitre, Guillem García Subies, Guitared, gunesbayir,
Haesun Park, Hansin Ahuja, Hao Chun Chang, Harsh Agrawal, harshit5674,
hasan-yaman, henrymooresc, Henry Sorsky, Hristo Vrigazov, htsedebenham, humahn,
i-aki-y, Ian Thompson, Ido M, Iglesys, Iliya Zhechev, Irene, ivanllt, Ivan
Sedykh, Jack McIvor, jakirkham, JanFidor, Jason G, Jérémie du Boisberranger,
Jiten Sidhpura, jkarolczak, João David, JohnathanPi, John Koumentis, John P,
John Pangas, johnthagen, Jordan Fleming, Joshua Choo Yun Keat, Jovan
Stojanovic, Juan Carlos Alfaro Jiménez, juanfe88, Juan Felipe Arias,
JuliaSchoepp, Julien Jerphanion, jygerardy, ka00ri, Kanishk Sachdev, Kanissh,
Kaushik Amar Das, Kendall, Kenneth Prabakaran, Kento Nozawa, kernc, Kevin
Roice, Kian Eliasi, Kilian Kluge, Kilian Lieret, Kirandevraj, Kraig, krishna
kumar, krishna vamsi, Kshitij Kapadni, Kshitij Mathur, Lauren Burke, Léonard
Binet, lingyi1110, Lisa Casino, Logan Thomas, Loic Esteve, Luciano Mantovani,
Lucy Liu, Maascha, Madhura Jayaratne, madinak, Maksym, Malte S. Kurz, Mansi
Agrawal, Marco Edward Gorelli, Marco Wurps, Maren Westermann, Maria Telenczuk,
Mario Kostelac, martin-kokos, Marvin Krawutschke, Masanori Kanazu, mathurinm,
Matt Haberland, mauroantonioserrano, Max Halford, Maxi Marufo, maximeSaur,
Maxim Smolskiy, Maxwell, m. bou, Meekail Zain, Mehgarg, mehmetcanakbay, Mia
Bajić, Michael Flaks, Michael Hornstein, Michel de Ruiter, Michelle Paradis,
Mikhail Iljin, Misa Ogura, Moritz Wilksch, mrastgoo, Naipawat Poolsawat, Naoise
Holohan, Nass, Nathan Jacobi, Nawazish Alam, Nguyễn Văn Diễn, Nicola
Fanelli, Nihal Thukarama Rao, Nikita Jare, nima10khodaveisi, Nima Sarajpoor,
nitinramvelraj, NNLNR, npache, Nwanna-Joseph, Nymark Kho, o-holman, Olivier
Grisel, Olle Lukowski, Omar Hassoun, Omar Salman, osman tamer, ouss1508,
Oyindamola Olatunji, PAB, Pandata, partev, Paulo Sergio  Soares, Petar
Mlinarić, Peter Jansson, Peter Steinbach, Philipp Jung, Piet Brömmel, Pooja
M, Pooja Subramaniam, priyam kakati, puhuk, Rachel Freeland, Rachit Keerti Das,
Rafal Wojdyla, Raghuveer Bhat, Rahil Parikh, Ralf Gommers, ram vikram singh,
Ravi Makhija, Rehan Guha, Reshama Shaikh, Richard Klima, Rob Crockett, Robert
Hommes, Robert Juergens, Robin Lenz, Rocco Meli, Roman4oo, Ross Barnowski,
Rowan Mankoo, Rudresh Veerkhare, Rushil Desai, Sabri Monaf Sabri, Safikh,
Safiuddin Khaja, Salahuddin, Sam Adam Day, Sandra Yojana Meneses, Sandro
Ephrem, Sangam, SangamSwadik, SANJAI_3, SarahRemus, Sashka Warner, SavkoMax,
Scott Gigante, Scott Gustafson, Sean Atukorala, sec65, SELEE, seljaks, Shady el
Gewily, Shane, shellyfung, Shinsuke Mori, Shiva chauhan, Shoaib Khan, Shogo
Hida, Shrankhla Srivastava, Shuangchi He, Simon, sonnivs, Sortofamudkip,
Srinath Kailasa, Stanislav (Stanley) Modrak, Stefanie Molin, stellalin7,
Stéphane Collot, Steven Van Vaerenbergh, Steve Schmerler, Sven Stehle, Tabea
Kossen, TheDevPanda, the-syd-sre, Thijs van Weezel, Thomas Bonald, Thomas
Germer, Thomas J. Fan, Ti-Ion, Tim Head, Timofei Kornev, toastedyeast, Tobias
Pitters, Tom Dupré la Tour, tomiock, Tom Mathews, Tom McTiernan, tspeng, Tyler
Egashira, Valentin Laurent, Varun Jain, Vera Komeyer, Vicente Reyes-Puerta,
Vinayak Mehta, Vincent M, Vishal, Vyom Pathak, wattai, wchathura, WEN Hao,
William M, x110, Xiao Yuan, Xunius, yanhong-zhao-ef, Yusuf Raji, Z Adil Khwaja,
zeeshan lone

# ===== SOURCE: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/doc/whats_new/v1.3.rst =====

.. include:: _contributors.rst

.. currentmodule:: sklearn

.. _release_notes_1_3:

===========
Version 1.3
===========

For a short description of the main highlights of the release, please refer to
:ref:`sphx_glr_auto_examples_release_highlights_plot_release_highlights_1_3_0.py`.

.. include:: changelog_legend.inc

.. _changes_1_3_2:

Version 1.3.2
=============

**October 2023**

Changelog
---------

:mod:`sklearn.datasets`
.......................

- |Fix| All dataset fetchers now accept `data_home` as any object that implements
  the :class:`os.PathLike` interface, for instance, :class:`pathlib.Path`.
  :pr:`27468` by :user:`Yao Xiao <Charlie-XIAO>`.

:mod:`sklearn.decomposition`
............................

- |Fix| Fixes a bug in :class:`decomposition.KernelPCA` by forcing the output of
  the internal :class:`preprocessing.KernelCenterer` to be a default array. When the
  arpack solver is used, it expects an array with a `dtype` attribute.
  :pr:`27583` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.metrics`
......................

- |Fix| Fixes a bug for metrics using `zero_division=np.nan`
  (e.g. :func:`~metrics.precision_score`) within a parallel loop
  (e.g. :func:`~model_selection.cross_val_score`) where the singleton for `np.nan`
  will be different in the sub-processes.
  :pr:`27573` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.tree`
...................

- |Fix| Do not leak data via non-initialized memory in decision tree pickle files and make
  the generation of those files deterministic. :pr:`27580` by :user:`Loïc Estève <lesteve>`.


.. _changes_1_3_1:

Version 1.3.1
=============

**September 2023**

Changed models
--------------

The following estimators and functions, when fit with the same data and
parameters, may produce different models from the previous version. This often
occurs due to changes in the modelling logic (bug fixes or enhancements), or in
random sampling procedures.

- |Fix| Ridge models with `solver='sparse_cg'` may have slightly different
  results with scipy>=1.12, because of an underlying change in the scipy solver
  (see `scipy#18488 <https://github.com/scipy/scipy/pull/18488>`_ for more
  details)
  :pr:`26814` by :user:`Loïc Estève <lesteve>`

Changes impacting all modules
-----------------------------

- |Fix| The `set_output` API correctly works with list input. :pr:`27044` by
  `Thomas Fan`_.

Changelog
---------

:mod:`sklearn.calibration`
..........................

- |Fix| :class:`calibration.CalibratedClassifierCV` can now handle models that
  produce large prediction scores. Before it was numerically unstable.
  :pr:`26913` by :user:`Omar Salman <OmarManzoor>`.

:mod:`sklearn.cluster`
......................

- |Fix| :class:`cluster.BisectingKMeans` could crash when predicting on data
  with a different scale than the data used to fit the model.
  :pr:`27167` by `Olivier Grisel`_.

- |Fix| :class:`cluster.BisectingKMeans` now works with data that has a single feature.
  :pr:`27243` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

:mod:`sklearn.cross_decomposition`
..................................

- |Fix| :class:`cross_decomposition.PLSRegression` now automatically ravels the output
  of `predict` if fitted with one dimensional `y`.
  :pr:`26602` by :user:`Yao Xiao <Charlie-XIAO>`.

:mod:`sklearn.ensemble`
.......................

- |Fix| Fix a bug in :class:`ensemble.AdaBoostClassifier` with `algorithm="SAMME"`
  where the decision function of each weak learner should be symmetric (i.e.
  the sum of the scores should sum to zero for a sample).
  :pr:`26521` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.feature_selection`
................................

- |Fix| :func:`feature_selection.mutual_info_regression` now correctly computes the
  result when `X` is of integer dtype. :pr:`26748` by :user:`Yao Xiao <Charlie-XIAO>`.

:mod:`sklearn.impute`
.....................

- |Fix| :class:`impute.KNNImputer` now correctly adds a missing indicator column in
  ``transform`` when ``add_indicator`` is set to ``True`` and missing values are observed
  during ``fit``. :pr:`26600` by :user:`Shreesha Kumar Bhat <Shreesha3112>`.

:mod:`sklearn.metrics`
......................

- |Fix| Scorers used with :func:`metrics.get_scorer` handle properly
  multilabel-indicator matrix.
  :pr:`27002` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.mixture`
......................

- |Fix| The initialization of :class:`mixture.GaussianMixture` from user-provided
  `precisions_init` for `covariance_type` of `full` or `tied` was not correct,
  and has been fixed.
  :pr:`26416` by :user:`Yang Tao <mchikyt3>`.

:mod:`sklearn.neighbors`
........................

- |Fix| :meth:`neighbors.KNeighborsClassifier.predict` no longer raises an
  exception for `pandas.DataFrames` input.
  :pr:`26772` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Fix| Reintroduce `sklearn.neighbors.BallTree.valid_metrics` and
  `sklearn.neighbors.KDTree.valid_metrics` as public class attributes.
  :pr:`26754` by :user:`Julien Jerphanion <jjerphan>`.

- |Fix| :class:`sklearn.model_selection.HalvingRandomSearchCV` no longer raises
  when the input to the `param_distributions` parameter is a list of dicts.
  :pr:`26893` by :user:`Stefanie Senger <StefanieSenger>`.

- |Fix| Neighbors based estimators now correctly work when `metric="minkowski"` and the
  metric parameter `p` is in the range `0 < p < 1`, regardless of the `dtype` of `X`.
  :pr:`26760` by :user:`Shreesha Kumar Bhat <Shreesha3112>`.

:mod:`sklearn.preprocessing`
............................

- |Fix| :class:`preprocessing.LabelEncoder` correctly accepts `y` as a keyword
  argument. :pr:`26940` by `Thomas Fan`_.

- |Fix| :class:`preprocessing.OneHotEncoder` shows a more informative error message
  when `sparse_output=True` and the output is configured to be pandas.
  :pr:`26931` by `Thomas Fan`_.

:mod:`sklearn.tree`
...................

- |Fix| :func:`tree.plot_tree` now accepts `class_names=True` as documented.
  :pr:`26903` by :user:`Thomas Roehr <2maz>`

- |Fix| The `feature_names` parameter of :func:`tree.plot_tree` now accepts any kind of
  array-like instead of just a list. :pr:`27292` by :user:`Rahil Parikh <rprkh>`.

.. _changes_1_3:

Version 1.3.0
=============

**June 2023**

Changed models
--------------

The following estimators and functions, when fit with the same data and
parameters, may produce different models from the previous version. This often
occurs due to changes in the modelling logic (bug fixes or enhancements), or in
random sampling procedures.

- |Enhancement| :meth:`multiclass.OutputCodeClassifier.predict` now uses a more
  efficient pairwise distance reduction. As a consequence, the tie-breaking
  strategy is different and thus the predicted labels may be different.
  :pr:`25196` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Enhancement| The `fit_transform` method of :class:`decomposition.DictionaryLearning`
  is more efficient but may produce different results as in previous versions when
  `transform_algorithm` is not the same as `fit_algorithm` and the number of iterations
  is small. :pr:`24871` by :user:`Omar Salman <OmarManzoor>`.

- |Enhancement| The `sample_weight` parameter now will be used in centroids
  initialization for :class:`cluster.KMeans`, :class:`cluster.BisectingKMeans`
  and :class:`cluster.MiniBatchKMeans`.
  This change will break backward compatibility, since numbers generated
  from same random seeds will be different.
  :pr:`25752` by :user:`Hleb Levitski <glevv>`,
  :user:`Jérémie du Boisberranger <jeremiedbb>`,
  :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| Treat more consistently small values in the `W` and `H` matrices during the
  `fit` and `transform` steps of :class:`decomposition.NMF` and
  :class:`decomposition.MiniBatchNMF` which can produce different results than previous
  versions. :pr:`25438` by :user:`Yotam Avidar-Constantini <yotamcons>`.

- |Fix| :class:`decomposition.KernelPCA` may produce different results through
  `inverse_transform` if `gamma` is `None`. Now it will be chosen correctly as
  `1/n_features` of the data that it is fitted on, while previously it might be
  incorrectly chosen as `1/n_features` of the data passed to `inverse_transform`.
  A new attribute `gamma_` is provided for revealing the actual value of `gamma`
  used each time the kernel is called.
  :pr:`26337` by :user:`Yao Xiao <Charlie-XIAO>`.

Changed displays
----------------

- |Enhancement| :class:`model_selection.LearningCurveDisplay` displays both the
  train and test curves by default. You can set `score_type="test"` to keep the
  past behaviour.
  :pr:`25120` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| :class:`model_selection.ValidationCurveDisplay` now accepts passing a
  list to the `param_range` parameter.
  :pr:`27311` by :user:`Arturo Amor <ArturoAmorQ>`.

Changes impacting all modules
-----------------------------

- |Enhancement| The `get_feature_names_out` method of the following classes now
  raises a `NotFittedError` if the instance is not fitted. This ensures the error is
  consistent in all estimators with the `get_feature_names_out` method.

  - :class:`impute.MissingIndicator`
  - :class:`feature_extraction.DictVectorizer`
  - :class:`feature_extraction.text.TfidfTransformer`
  - :class:`feature_selection.GenericUnivariateSelect`
  - :class:`feature_selection.RFE`
  - :class:`feature_selection.RFECV`
  - :class:`feature_selection.SelectFdr`
  - :class:`feature_selection.SelectFpr`
  - :class:`feature_selection.SelectFromModel`
  - :class:`feature_selection.SelectFwe`
  - :class:`feature_selection.SelectKBest`
  - :class:`feature_selection.SelectPercentile`
  - :class:`feature_selection.SequentialFeatureSelector`
  - :class:`feature_selection.VarianceThreshold`
  - :class:`kernel_approximation.AdditiveChi2Sampler`
  - :class:`impute.IterativeImputer`
  - :class:`impute.KNNImputer`
  - :class:`impute.SimpleImputer`
  - :class:`isotonic.IsotonicRegression`
  - :class:`preprocessing.Binarizer`
  - :class:`preprocessing.KBinsDiscretizer`
  - :class:`preprocessing.MaxAbsScaler`
  - :class:`preprocessing.MinMaxScaler`
  - :class:`preprocessing.Normalizer`
  - :class:`preprocessing.OrdinalEncoder`
  - :class:`preprocessing.PowerTransformer`
  - :class:`preprocessing.QuantileTransformer`
  - :class:`preprocessing.RobustScaler`
  - :class:`preprocessing.SplineTransformer`
  - :class:`preprocessing.StandardScaler`
  - :class:`random_projection.GaussianRandomProjection`
  - :class:`random_projection.SparseRandomProjection`

  The `NotFittedError` displays an informative message asking to fit the instance
  with the appropriate arguments.

  :pr:`25294`, :pr:`25308`, :pr:`25291`, :pr:`25367`, :pr:`25402`,
  by :user:`John Pangas <jpangas>`, :user:`Rahil Parikh <rprkh>` ,
  and :user:`Alex Buzenet <albuzenet>`.

- |Enhancement| Added a multi-threaded Cython routine to the compute squared
  Euclidean distances (sometimes followed by a fused reduction operation) for a
  pair of datasets consisting of a sparse CSR matrix and a dense NumPy.

  This can improve the performance of following functions and estimators:

  - :func:`sklearn.metrics.pairwise_distances_argmin`
  - :func:`sklearn.metrics.pairwise_distances_argmin_min`
  - :class:`sklearn.cluster.AffinityPropagation`
  - :class:`sklearn.cluster.Birch`
  - :class:`sklearn.cluster.MeanShift`
  - :class:`sklearn.cluster.OPTICS`
  - :class:`sklearn.cluster.SpectralClustering`
  - :func:`sklearn.feature_selection.mutual_info_regression`
  - :class:`sklearn.neighbors.KNeighborsClassifier`
  - :class:`sklearn.neighbors.KNeighborsRegressor`
  - :class:`sklearn.neighbors.RadiusNeighborsClassifier`
  - :class:`sklearn.neighbors.RadiusNeighborsRegressor`
  - :class:`sklearn.neighbors.LocalOutlierFactor`
  - :class:`sklearn.neighbors.NearestNeighbors`
  - :class:`sklearn.manifold.Isomap`
  - :class:`sklearn.manifold.LocallyLinearEmbedding`
  - :class:`sklearn.manifold.TSNE`
  - :func:`sklearn.manifold.trustworthiness`
  - :class:`sklearn.semi_supervised.LabelPropagation`
  - :class:`sklearn.semi_supervised.LabelSpreading`

  A typical example of this performance improvement happens when passing a sparse
  CSR matrix to the `predict` or `transform` method of estimators that rely on
  a dense NumPy representation to store their fitted parameters (or the reverse).

  For instance, :meth:`sklearn.neighbors.NearestNeighbors.kneighbors` is now up
  to 2 times faster for this case on commonly available laptops.

  :pr:`25044` by :user:`Julien Jerphanion <jjerphan>`.

- |Enhancement| All estimators that internally rely on OpenMP multi-threading
  (via Cython) now use a number of threads equal to the number of physical
  (instead of logical) cores by default. In the past, we observed that using as
  many threads as logical cores on SMT hosts could sometimes cause severe
  performance problems depending on the algorithms and the shape of the data.
  Note that it is still possible to manually adjust the number of threads used
  by OpenMP as documented in :ref:`parallelism`.

  :pr:`26082` by :user:`Jérémie du Boisberranger <jeremiedbb>` and
  :user:`Olivier Grisel <ogrisel>`.

Experimental / Under Development
--------------------------------

- |MajorFeature| :ref:`Metadata routing <metadata_routing>`'s related base
  methods are included in this release. This feature is only available via the
  `enable_metadata_routing` feature flag which can be enabled using
  :func:`sklearn.set_config` and :func:`sklearn.config_context`. For now this
  feature is mostly useful for third party developers to prepare their code
  base for metadata routing, and we strongly recommend that they also hide it
  behind the same feature flag, rather than having it enabled by default.
  :pr:`24027` by `Adrin Jalali`_, :user:`Benjamin Bossan <BenjaminBossan>`, and
  :user:`Omar Salman <OmarManzoor>`.

Changelog
---------

..
    Entries should be grouped by module (in alphabetic order) and prefixed with
    one of the labels: |MajorFeature|, |Feature|, |Efficiency|, |Enhancement|,
    |Fix| or |API| (see whats_new.rst for descriptions).
    Entries should be ordered by those labels (e.g. |Fix| after |Efficiency|).
    Changes not specific to a module should be listed under *Multiple Modules*
    or *Miscellaneous*.
    Entries should end with:
    :pr:`123456` by :user:`Joe Bloggs <joeongithub>`.
    where 123456 is the *pull request* number, not the issue number.

`sklearn`
.........

- |Feature| Added a new option `skip_parameter_validation`, to the function
  :func:`sklearn.set_config` and context manager :func:`sklearn.config_context`, that
  allows to skip the validation of the parameters passed to the estimators and public
  functions. This can be useful to speed up the code but should be used with care
  because it can lead to unexpected behaviors or raise obscure error messages when
  setting invalid parameters.
  :pr:`25815` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

:mod:`sklearn.base`
...................

- |Feature| A `__sklearn_clone__` protocol is now available to override the
  default behavior of :func:`base.clone`. :pr:`24568` by `Thomas Fan`_.

- |Fix| :class:`base.TransformerMixin` now currently keeps a namedtuple's class
  if `transform` returns a namedtuple. :pr:`26121` by `Thomas Fan`_.

:mod:`sklearn.calibration`
..........................

- |Fix| :class:`calibration.CalibratedClassifierCV` now does not enforce sample
  alignment on `fit_params`. :pr:`25805` by `Adrin Jalali`_.

:mod:`sklearn.cluster`
......................

- |MajorFeature| Added :class:`cluster.HDBSCAN`, a modern hierarchical density-based
  clustering algorithm. Similarly to :class:`cluster.OPTICS`, it can be seen as a
  generalization of :class:`cluster.DBSCAN` by allowing for hierarchical instead of flat
  clustering, however it varies in its approach from :class:`cluster.OPTICS`. This
  algorithm is very robust with respect to its hyperparameters' values and can
  be used on a wide variety of data without much, if any, tuning.

  This implementation is an adaptation from the original implementation of HDBSCAN in
  `scikit-learn-contrib/hdbscan <https://github.com/scikit-learn-contrib/hdbscan>`_,
  by :user:`Leland McInnes <lmcinnes>` et al.

  :pr:`26385` by :user:`Meekail Zain <micky774>`

- |Enhancement| The `sample_weight` parameter now will be used in centroids
  initialization for :class:`cluster.KMeans`, :class:`cluster.BisectingKMeans`
  and :class:`cluster.MiniBatchKMeans`.
  This change will break backward compatibility, since numbers generated
  from same random seeds will be different.
  :pr:`25752` by :user:`Hleb Levitski <glevv>`,
  :user:`Jérémie du Boisberranger <jeremiedbb>`,
  :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| :class:`cluster.KMeans`, :class:`cluster.MiniBatchKMeans` and
  :func:`cluster.k_means` now correctly handle the combination of `n_init="auto"`
  and `init` being an array-like, running one initialization in that case.
  :pr:`26657` by :user:`Binesh Bannerjee <bnsh>`.

- |API| The `sample_weight` parameter in `predict` for
  :meth:`cluster.KMeans.predict` and :meth:`cluster.MiniBatchKMeans.predict`
  is now deprecated and will be removed in v1.5.
  :pr:`25251` by :user:`Hleb Levitski <glevv>`.

- |API| The `Xred` argument in :func:`cluster.FeatureAgglomeration.inverse_transform`
  is renamed to `Xt` and will be removed in v1.5. :pr:`26503` by `Adrin Jalali`_.

:mod:`sklearn.compose`
......................

- |Fix| :class:`compose.ColumnTransformer` raises an informative error when the individual
  transformers of `ColumnTransformer` output pandas dataframes with indexes that are
  not consistent with each other and the output is configured to be pandas.
  :pr:`26286` by `Thomas Fan`_.

- |Fix| :class:`compose.ColumnTransformer` correctly sets the output of the
  remainder when `set_output` is called. :pr:`26323` by `Thomas Fan`_.

:mod:`sklearn.covariance`
.........................

- |Fix| Allows `alpha=0` in :class:`covariance.GraphicalLasso` to be
  consistent with :func:`covariance.graphical_lasso`.
  :pr:`26033` by :user:`Genesis Valencia <genvalen>`.

- |Fix| :func:`covariance.empirical_covariance` now gives an informative
  error message when input is not appropriate.
  :pr:`26108` by :user:`Quentin Barthélemy <qbarthelemy>`.

- |API| Deprecates `cov_init` in :func:`covariance.graphical_lasso` in 1.3 since
  the parameter has no effect. It will be removed in 1.5.
  :pr:`26033` by :user:`Genesis Valencia <genvalen>`.

- |API| Adds `costs_` fitted attribute in :class:`covariance.GraphicalLasso` and
  :class:`covariance.GraphicalLassoCV`.
  :pr:`26033` by :user:`Genesis Valencia <genvalen>`.

- |API| Adds `covariance` parameter in :class:`covariance.GraphicalLasso`.
  :pr:`26033` by :user:`Genesis Valencia <genvalen>`.

- |API| Adds `eps` parameter in :class:`covariance.GraphicalLasso`,
  :func:`covariance.graphical_lasso`, and :class:`covariance.GraphicalLassoCV`.
  :pr:`26033` by :user:`Genesis Valencia <genvalen>`.

:mod:`sklearn.datasets`
.......................

- |Enhancement| Allows to overwrite the parameters used to open the ARFF file using
  the parameter `read_csv_kwargs` in :func:`datasets.fetch_openml` when using the
  pandas parser.
  :pr:`26433` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| :func:`datasets.fetch_openml` returns improved data types when
  `as_frame=True` and `parser="liac-arff"`. :pr:`26386` by `Thomas Fan`_.

- |Fix| Following the ARFF specs, only the marker `"?"` is now considered as a missing
  values when opening ARFF files fetched using :func:`datasets.fetch_openml` when using
  the pandas parser. The parameter `read_csv_kwargs` allows to overwrite this behaviour.
  :pr:`26551` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| :func:`datasets.fetch_openml` will consistently use `np.nan` as missing marker
  with both parsers `"pandas"` and `"liac-arff"`.
  :pr:`26579` by :user:`Guillaume Lemaitre <glemaitre>`.

- |API| The `data_transposed` argument of :func:`datasets.make_sparse_coded_signal`
  is deprecated and will be removed in v1.5.
  :pr:`25784` by :user:`Jérémie du Boisberranger`.

:mod:`sklearn.decomposition`
............................

- |Efficiency| :class:`decomposition.MiniBatchDictionaryLearning` and
  :class:`decomposition.MiniBatchSparsePCA` are now faster for small batch sizes by
  avoiding duplicate validations.
  :pr:`25490` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Enhancement| :class:`decomposition.DictionaryLearning` now accepts the parameter
  `callback` for consistency with the function :func:`decomposition.dict_learning`.
  :pr:`24871` by :user:`Omar Salman <OmarManzoor>`.

- |Fix| Treat more consistently small values in the `W` and `H` matrices during the
  `fit` and `transform` steps of :class:`decomposition.NMF` and
  :class:`decomposition.MiniBatchNMF` which can produce different results than previous
  versions. :pr:`25438` by :user:`Yotam Avidar-Constantini <yotamcons>`.

- |API| The `W` argument in :func:`decomposition.NMF.inverse_transform` and
  :class:`decomposition.MiniBatchNMF.inverse_transform` is renamed to `Xt` and
  will be removed in v1.5. :pr:`26503` by `Adrin Jalali`_.

:mod:`sklearn.discriminant_analysis`
....................................

- |Enhancement| :class:`discriminant_analysis.LinearDiscriminantAnalysis` now
  supports the `PyTorch <https://pytorch.org/>`__. See
  :ref:`array_api` for more details. :pr:`25956` by `Thomas Fan`_.

:mod:`sklearn.ensemble`
.......................

- |Feature| :class:`ensemble.HistGradientBoostingRegressor` now supports
  the Gamma deviance loss via `loss="gamma"`.
  Using the Gamma deviance as loss function comes in handy for modelling skewed
  distributed, strictly positive valued targets.
  :pr:`22409` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Feature| Compute a custom out-of-bag score by passing a callable to
  :class:`ensemble.RandomForestClassifier`, :class:`ensemble.RandomForestRegressor`,
  :class:`ensemble.ExtraTreesClassifier` and :class:`ensemble.ExtraTreesRegressor`.
  :pr:`25177` by `Tim Head`_.

- |Feature| :class:`ensemble.GradientBoostingClassifier` now exposes
  out-of-bag scores via the `oob_scores_` or `oob_score_` attributes.
  :pr:`24882` by :user:`Ashwin Mathur <awinml>`.

- |Efficiency| :class:`ensemble.IsolationForest` predict time is now faster
  (typically by a factor of 8 or more). Internally, the estimator now precomputes
  decision path lengths per tree at `fit` time. It is therefore not possible
  to load an estimator trained with scikit-learn 1.2 to make it predict with
  scikit-learn 1.3: retraining with scikit-learn 1.3 is required.
  :pr:`25186` by :user:`Felipe Breve Siola <fsiola>`.

- |Efficiency| :class:`ensemble.RandomForestClassifier` and
  :class:`ensemble.RandomForestRegressor` with `warm_start=True` now only
  recomputes out-of-bag scores when there are actually more `n_estimators`
  in subsequent `fit` calls.
  :pr:`26318` by :user:`Joshua Choo Yun Keat <choo8>`.

- |Enhancement| :class:`ensemble.BaggingClassifier` and
  :class:`ensemble.BaggingRegressor` expose the `allow_nan` tag from the
  underlying estimator. :pr:`25506` by `Thomas Fan`_.

- |Fix| :meth:`ensemble.RandomForestClassifier.fit` sets `max_samples = 1`
  when `max_samples` is a float and `round(n_samples * max_samples) < 1`.
  :pr:`25601` by :user:`Jan Fidor <JanFidor>`.

- |Fix| :meth:`ensemble.IsolationForest.fit` no longer warns about missing
  feature names when called with `contamination` not `"auto"` on a pandas
  dataframe.
  :pr:`25931` by :user:`Yao Xiao <Charlie-XIAO>`.

- |Fix| :class:`ensemble.HistGradientBoostingRegressor` and
  :class:`ensemble.HistGradientBoostingClassifier` treats negative values for
  categorical features consistently as missing values, following LightGBM's and
  pandas' conventions.
  :pr:`25629` by `Thomas Fan`_.

- |Fix| Fix deprecation of `base_estimator` in :class:`ensemble.AdaBoostClassifier`
  and :class:`ensemble.AdaBoostRegressor` that was introduced in :pr:`23819`.
  :pr:`26242` by :user:`Marko Toplak <markotoplak>`.

:mod:`sklearn.exceptions`
.........................

- |Feature| Added :class:`exceptions.InconsistentVersionWarning` which is raised
  when a scikit-learn estimator is unpickled with a scikit-learn version that is
  inconsistent with the scikit-learn version the estimator was pickled with.
  :pr:`25297` by `Thomas Fan`_.

:mod:`sklearn.feature_extraction`
.................................

- |API| :class:`feature_extraction.image.PatchExtractor` now follows the
  transformer API of scikit-learn. This class is defined as a stateless transformer
  meaning that it is not required to call `fit` before calling `transform`.
  Parameter validation only happens at `fit` time.
  :pr:`24230` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.feature_selection`
................................

- |Enhancement| All selectors in :mod:`sklearn.feature_selection` will preserve
  a DataFrame's dtype when transformed. :pr:`25102` by `Thomas Fan`_.

- |Fix| :class:`feature_selection.SequentialFeatureSelector`'s `cv` parameter
  now supports generators. :pr:`25973` by `Yao Xiao <Charlie-XIAO>`.

:mod:`sklearn.impute`
.....................

- |Enhancement| Added the parameter `fill_value` to :class:`impute.IterativeImputer`.
  :pr:`25232` by :user:`Thijs van Weezel <ValueInvestorThijs>`.

- |Fix| :class:`impute.IterativeImputer` now correctly preserves the Pandas
  Index when the `set_config(transform_output="pandas")`. :pr:`26454` by `Thomas Fan`_.

:mod:`sklearn.inspection`
.........................

- |Enhancement| Added support for `sample_weight` in
  :func:`inspection.partial_dependence` and
  :meth:`inspection.PartialDependenceDisplay.from_estimator`. This allows for
  weighted averaging when aggregating for each value of the grid we are making the
  inspection on. The option is only available when `method` is set to `brute`.
  :pr:`25209` and :pr:`26644` by :user:`Carlo Lemos <vitaliset>`.

- |API| :func:`inspection.partial_dependence` returns a :class:`utils.Bunch` with
  new key: `grid_values`. The `values` key is deprecated in favor of `grid_values`
  and the `values` key will be removed in 1.5.
  :pr:`21809` and :pr:`25732` by `Thomas Fan`_.

:mod:`sklearn.kernel_approximation`
...................................

- |Fix| :class:`kernel_approximation.AdditiveChi2Sampler` is now stateless.
  The `sample_interval_` attribute is deprecated and will be removed in 1.5.
  :pr:`25190` by :user:`Vincent Maladière <Vincent-Maladiere>`.

:mod:`sklearn.linear_model`
...........................

- |Efficiency| Avoid data scaling when `sample_weight=None` and other
  unnecessary data copies and unexpected dense to sparse data conversion in
  :class:`linear_model.LinearRegression`.
  :pr:`26207` by :user:`Olivier Grisel <ogrisel>`.

- |Enhancement| :class:`linear_model.SGDClassifier`,
  :class:`linear_model.SGDRegressor` and :class:`linear_model.SGDOneClassSVM`
  now preserve dtype for `numpy.float32`.
  :pr:`25587` by :user:`Omar Salman <OmarManzoor>`.

- |Enhancement| The `n_iter_` attribute has been included in
  :class:`linear_model.ARDRegression` to expose the actual number of iterations
  required to reach the stopping criterion.
  :pr:`25697` by :user:`John Pangas <jpangas>`.

- |Fix| Use a more robust criterion to detect convergence of
  :class:`linear_model.LogisticRegression` with `penalty="l1"` and `solver="liblinear"`
  on linearly separable problems.
  :pr:`25214` by `Tom Dupre la Tour`_.

- |Fix| Fix a crash when calling `fit` on
  :class:`linear_model.LogisticRegression` with `solver="newton-cholesky"` and
  `max_iter=0` which failed to inspect the state of the model prior to the
  first parameter update.
  :pr:`26653` by :user:`Olivier Grisel <ogrisel>`.

- |API| Deprecates `n_iter` in favor of `max_iter` in
  :class:`linear_model.BayesianRidge` and :class:`linear_model.ARDRegression`.
  `n_iter` will be removed in scikit-learn 1.5. This change makes those
  estimators consistent with the rest of estimators.
  :pr:`25697` by :user:`John Pangas <jpangas>`.

:mod:`sklearn.manifold`
.......................

- |Fix| :class:`manifold.Isomap` now correctly preserves the Pandas
  Index when the `set_config(transform_output="pandas")`. :pr:`26454` by `Thomas Fan`_.

:mod:`sklearn.metrics`
......................

- |Feature| Adds `zero_division=np.nan` to multiple classification metrics:
  :func:`metrics.precision_score`, :func:`metrics.recall_score`,
  :func:`metrics.f1_score`, :func:`metrics.fbeta_score`,
  :func:`metrics.precision_recall_fscore_support`,
  :func:`metrics.classification_report`. When `zero_division=np.nan` and there is a
  zero division, the metric is undefined and is excluded from averaging. When not used
  for averages, the value returned is `np.nan`.
  :pr:`25531` by :user:`Marc Torrellas Socastro <marctorsoc>`.

- |Feature| :func:`metrics.average_precision_score` now supports the
  multiclass case.
  :pr:`17388` by :user:`Geoffrey Bolmier <gbolmier>` and
  :pr:`24769` by :user:`Ashwin Mathur <awinml>`.

- |Efficiency| The computation of the expected mutual information in
  :func:`metrics.adjusted_mutual_info_score` is now faster when the number of
  unique labels is large and its memory usage is reduced in general.
  :pr:`25713` by :user:`Kshitij Mathur <Kshitij68>`,
  :user:`Guillaume Lemaitre <glemaitre>`, :user:`Omar Salman <OmarManzoor>` and
  :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Enhancement| :class:`metrics.silhouette_samples` now accepts a sparse
  matrix of pairwise distances between samples, or a feature array.
  :pr:`18723` by :user:`Sahil Gupta <sahilgupta2105>` and
  :pr:`24677` by :user:`Ashwin Mathur <awinml>`.

- |Enhancement| A new parameter `drop_intermediate` was added to
  :func:`metrics.precision_recall_curve`,
  :func:`metrics.PrecisionRecallDisplay.from_estimator`,
  :func:`metrics.PrecisionRecallDisplay.from_predictions`,
  which drops some suboptimal thresholds to create lighter precision-recall
  curves.
  :pr:`24668` by :user:`dberenbaum`.

- |Enhancement| :meth:`metrics.RocCurveDisplay.from_estimator` and
  :meth:`metrics.RocCurveDisplay.from_predictions` now accept two new keywords,
  `plot_chance_level` and `chance_level_kw` to plot the baseline chance
  level. This line is exposed in the `chance_level_` attribute.
  :pr:`25987` by :user:`Yao Xiao <Charlie-XIAO>`.

- |Enhancement| :meth:`metrics.PrecisionRecallDisplay.from_estimator` and
  :meth:`metrics.PrecisionRecallDisplay.from_predictions` now accept two new
  keywords, `plot_chance_level` and `chance_level_kw` to plot the baseline
  chance level. This line is exposed in the `chance_level_` attribute.
  :pr:`26019` by :user:`Yao Xiao <Charlie-XIAO>`.

- |Fix| :func:`metrics.pairwise.manhattan_distances` now supports readonly sparse datasets.
  :pr:`25432` by :user:`Julien Jerphanion <jjerphan>`.

- |Fix| Fixed :func:`metrics.classification_report` so that empty input will return
  `np.nan`. Previously, "macro avg" and `weighted avg` would return
  e.g. `f1-score=np.nan` and `f1-score=0.0`, being inconsistent. Now, they
  both return `np.nan`.
  :pr:`25531` by :user:`Marc Torrellas Socastro <marctorsoc>`.

- |Fix| :func:`metrics.ndcg_score` now gives a meaningful error message for input of
  length 1.
  :pr:`25672` by :user:`Lene Preuss <lene>` and :user:`Wei-Chun Chu <wcchu>`.

- |Fix| :func:`metrics.log_loss` raises a warning if the values of the parameter
  `y_pred` are not normalized, instead of actually normalizing them in the metric.
  Starting from 1.5 this will raise an error.
  :pr:`25299` by :user:`Omar Salman <OmarManzoor`.

- |Fix| In :func:`metrics.roc_curve`, use the threshold value `np.inf` instead of
  arbitrary `max(y_score) + 1`. This threshold is associated with the ROC curve point
  `tpr=0` and `fpr=0`.
  :pr:`26194` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Fix| The `'matching'` metric has been removed when using SciPy>=1.9
  to be consistent with `scipy.spatial.distance` which does not support
  `'matching'` anymore.
  :pr:`26264` by :user:`Barata T. Onggo <magnusbarata>`

- |API| The `eps` parameter of the :func:`metrics.log_loss` has been deprecated and
  will be removed in 1.5. :pr:`25299` by :user:`Omar Salman <OmarManzoor>`.

:mod:`sklearn.gaussian_process`
...............................

- |Fix| :class:`gaussian_process.GaussianProcessRegressor` has a new argument
  `n_targets`, which is used to decide the number of outputs when sampling
  from the prior distributions. :pr:`23099` by :user:`Zhehao Liu <MaxwellLZH>`.

:mod:`sklearn.mixture`
......................

- |Efficiency| :class:`mixture.GaussianMixture` is more efficient now and will bypass
  unnecessary initialization if the weights, means, and precisions are
  given by users.
  :pr:`26021` by :user:`Jiawei Zhang <jiawei-zhang-a>`.

:mod:`sklearn.model_selection`
..............................

- |MajorFeature| Added the class :class:`model_selection.ValidationCurveDisplay`
  that allows easy plotting of validation curves obtained by the function
  :func:`model_selection.validation_curve`.
  :pr:`25120` by :user:`Guillaume Lemaitre <glemaitre>`.

- |API| The parameter `log_scale` in the method `plot` of the class
  :class:`model_selection.LearningCurveDisplay` has been deprecated in 1.3 and
  will be removed in 1.5. The default scale can be overridden by setting it
  directly on the `ax` object and will be set automatically from the spacing
  of the data points otherwise.
  :pr:`25120` by :user:`Guillaume Lemaitre <glemaitre>`.

- |Enhancement| :func:`model_selection.cross_validate` accepts a new parameter
  `return_indices` to return the train-test indices of each cv split.
  :pr:`25659` by :user:`Guillaume Lemaitre <glemaitre>`.

:mod:`sklearn.multioutput`
..........................

- |Fix| :func:`getattr` on :meth:`multioutput.MultiOutputRegressor.partial_fit`
  and :meth:`multioutput.MultiOutputClassifier.partial_fit` now correctly raise
  an `AttributeError` if done before calling `fit`. :pr:`26333` by `Adrin
  Jalali`_.

:mod:`sklearn.naive_bayes`
..........................

- |Fix| :class:`naive_bayes.GaussianNB` does not raise anymore a `ZeroDivisionError`
  when the provided `sample_weight` reduces the problem to a single class in `fit`.
  :pr:`24140` by :user:`Jonathan Ohayon <Johayon>` and :user:`Chiara Marmo <cmarmo>`.

:mod:`sklearn.neighbors`
........................

- |Enhancement| The performance of :meth:`neighbors.KNeighborsClassifier.predict`
  and of :meth:`neighbors.KNeighborsClassifier.predict_proba` has been improved
  when `n_neighbors` is large and `algorithm="brute"` with non Euclidean metrics.
  :pr:`24076` by :user:`Meekail Zain <micky774>`, :user:`Julien Jerphanion <jjerphan>`.

- |Fix| Remove support for `KulsinskiDistance` in :class:`neighbors.BallTree`. This
  dissimilarity is not a metric and cannot be supported by the BallTree.
  :pr:`25417` by :user:`Guillaume Lemaitre <glemaitre>`.

- |API| The support for metrics other than `euclidean` and `manhattan` and for
  callables in :class:`neighbors.NearestNeighbors` is deprecated and will be removed in
  version 1.5. :pr:`24083` by :user:`Valentin Laurent <Valentin-Laurent>`.

:mod:`sklearn.neural_network`
.............................

- |Fix| :class:`neural_network.MLPRegressor` and :class:`neural_network.MLPClassifier`
  reports the right `n_iter_` when `warm_start=True`. It corresponds to the number
  of iterations performed on the current call to `fit` instead of the total number
  of iterations performed since the initialization of the estimator.
  :pr:`25443` by :user:`Marvin Krawutschke <Marvvxi>`.

:mod:`sklearn.pipeline`
.......................

- |Feature| :class:`pipeline.FeatureUnion` can now use indexing notation (e.g.
  `feature_union["scalar"]`) to access transformers by name. :pr:`25093` by
  `Thomas Fan`_.

- |Feature| :class:`pipeline.FeatureUnion` can now access the
  `feature_names_in_` attribute if the `X` value seen during `.fit` has a
  `columns` attribute and all columns are strings. e.g. when `X` is a
  `pandas.DataFrame`
  :pr:`25220` by :user:`Ian Thompson <it176131>`.

- |Fix| :meth:`pipeline.Pipeline.fit_transform` now raises an `AttributeError`
  if the last step of the pipeline does not support `fit_transform`.
  :pr:`26325` by `Adrin Jalali`_.

:mod:`sklearn.preprocessing`
............................

- |MajorFeature| Introduces :class:`preprocessing.TargetEncoder` which is a
  categorical encoding based on target mean conditioned on the value of the
  category. :pr:`25334` by `Thomas Fan`_.

- |Feature| :class:`preprocessing.OrdinalEncoder` now supports grouping
  infrequent categories into a single feature. Grouping infrequent categories
  is enabled by specifying how to select infrequent categories with
  `min_frequency` or `max_categories`. :pr:`25677` by `Thomas Fan`_.

- |Enhancement| :class:`preprocessing.PolynomialFeatures` now calculates the
  number of expanded terms a-priori when dealing with sparse `csr` matrices
  in order to optimize the choice of `dtype` for `indices` and `indptr`. It
  can now output `csr` matrices with `np.int32` `indices/indptr` components
  when there are few enough elements, and will automatically use `np.int64`
  for sufficiently large matrices.
  :pr:`20524` by :user:`niuk-a <niuk-a>` and
  :pr:`23731` by :user:`Meekail Zain <micky774>`

- |Enhancement| A new parameter `sparse_output` was added to
  :class:`preprocessing.SplineTransformer`, available as of SciPy 1.8. If
  `sparse_output=True`, :class:`preprocessing.SplineTransformer` returns a sparse
  CSR matrix. :pr:`24145` by :user:`Christian Lorentzen <lorentzenchr>`.

- |Enhancement| Adds a `feature_name_combiner` parameter to
  :class:`preprocessing.OneHotEncoder`. This specifies a custom callable to
  create feature names to be returned by
  :meth:`preprocessing.OneHotEncoder.get_feature_names_out`. The callable
  combines input arguments `(input_feature, category)` to a string.
  :pr:`22506` by :user:`Mario Kostelac <mariokostelac>`.

- |Enhancement| Added support for `sample_weight` in
  :class:`preprocessing.KBinsDiscretizer`. This allows specifying the parameter
  `sample_weight` for each sample to be used while fitting. The option is only
  available when `strategy` is set to `quantile` and `kmeans`.
  :pr:`24935` by :user:`Seladus <seladus>`, :user:`Guillaume Lemaitre <glemaitre>`, and
  :user:`Dea María Léon <deamarialeon>`, :pr:`25257` by :user:`Hleb Levitski <glevv>`.

- |Enhancement| Subsampling through the `subsample` parameter can now be used in
  :class:`preprocessing.KBinsDiscretizer` regardless of the strategy used.
  :pr:`26424` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |Fix| :class:`preprocessing.PowerTransformer` now correctly preserves the Pandas
  Index when the `set_config(transform_output="pandas")`. :pr:`26454` by `Thomas Fan`_.

- |Fix| :class:`preprocessing.PowerTransformer` now correctly raises error when
  using `method="box-cox"` on data with a constant `np.nan` column.
  :pr:`26400` by :user:`Yao Xiao <Charlie-XIAO>`.

- |Fix| :class:`preprocessing.PowerTransformer` with `method="yeo-johnson"` now leaves
  constant features unchanged instead of transforming with an arbitrary value for
  the `lambdas_` fitted parameter.
  :pr:`26566` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

- |API| The default value of the `subsample` parameter of
  :class:`preprocessing.KBinsDiscretizer` will change from `None` to `200_000` in
  version 1.5 when `strategy="kmeans"` or `strategy="uniform"`.
  :pr:`26424` by :user:`Jérémie du Boisberranger <jeremiedbb>`.

:mod:`sklearn.svm`
..................

- |API| `dual` parameter now accepts `auto` option for
  :class:`svm.LinearSVC` and :class:`svm.LinearSVR`.
  :pr:`26093` by :user:`Hleb Levitski <glevv>`.

:mod:`sklearn.tree`
...................

- |MajorFeature| :class:`tree.DecisionTreeRegressor` and
  :class:`tree.DecisionTreeClassifier` support missing values when
  `splitter='best'` and criterion is `gini`, `entropy`, or `log_loss`,
  for classification or `squared_error`, `friedman_mse`, or `poisson`
  for regression. :pr:`23595`, :pr:`26376` by `Thomas Fan`_.

- |Enhancement| Adds a `class_names` parameter to
  :func:`tree.export_text`. This allows specifying the parameter `class_names`
  for each target class in ascending numerical order.
  :pr:`25387` by :user:`William M <Akbeeh>` and :user:`crispinlogan <crispinlogan>`.

- |Fix| :func:`tree.export_graphviz` and :func:`tree.export_text` now accepts
  `feature_names` and `class_names` as array-like rather than lists.
  :pr:`26289` by :user:`Yao Xiao <Charlie-XIAO>`

:mod:`sklearn.utils`
....................

- |FIX| Fixes :func:`utils.check_array` to properly convert pandas
  extension arrays. :pr:`25813` and :pr:`26106` by `Thomas Fan`_.

- |Fix| :func:`utils.check_array` now supports pandas DataFrames with
  extension arrays and object dtypes by returning an ndarray with object dtype.
  :pr:`25814` by `Thomas Fan`_.

- |API| `utils.estimator_checks.check_transformers_unfitted_stateless` has been
  introduced to ensure stateless transformers don't raise `NotFittedError`
  during `transform` with no prior call to `fit` or `fit_transform`.
  :pr:`25190` by :user:`Vincent Maladière <Vincent-Maladiere>`.

- |API| A `FutureWarning` is now raised when instantiating a class which inherits from
  a deprecated base class (i.e. decorated by :class:`utils.deprecated`) and which
  overrides the `__init__` method.
  :pr:`25733` by :user:`Brigitta Sipőcz <bsipocz>` and
  :user:`Jérémie du Boisberranger <jeremiedbb>`.

:mod:`sklearn.semi_supervised`
..............................

- |Enhancement| :meth:`semi_supervised.LabelSpreading.fit` and
  :meth:`semi_supervised.LabelPropagation.fit` now accepts sparse metrics.
  :pr:`19664` by :user:`Kaushik Amar Das <cozek>`.

Miscellaneous
.............

- |Enhancement| Replace obsolete exceptions `EnvironmentError`, `IOError` and
  `WindowsError`.
  :pr:`26466` by :user:`Dimitri Papadopoulos ORfanos <DimitriPapadopoulos>`.

.. rubric:: Code and documentation contributors

Thanks to everyone who has contributed to the maintenance and improvement of
the project since version 1.2, including:

2357juan, Abhishek Singh Kushwah, Adam Handke, Adam Kania, Adam Li, adienes,
Admir Demiraj, adoublet, Adrin Jalali, A.H.Mansouri, Ahmedbgh, Ala-Na, Alex
Buzenet, AlexL, Ali H. El-Kassas, amay, András Simon, André Pedersen, Andrew
Wang, Ankur Singh, annegnx, Ansam Zedan, Anthony22-dev, Artur Hermano, Arturo
Amor, as-90, ashah002, Ashish Dutt, Ashwin Mathur, AymericBasset, Azaria
Gebremichael, Barata Tripramudya Onggo, Benedek Harsanyi, Benjamin Bossan,
Bharat Raghunathan, Binesh Bannerjee, Boris Feld, Brendan Lu, Brevin Kunde,
cache-missing, Camille Troillard, Carla J, carlo, Carlo Lemos, c-git, Changyao
Chen, Chiara Marmo, Christian Lorentzen, Christian Veenhuis, Christine P. Chai,
crispinlogan, Da-Lan, DanGonite57, Dave Berenbaum, davidblnc, david-cortes,
Dayne, Dea María Léon, Denis, Dimitri Papadopoulos Orfanos, Dimitris
Litsidis, Dmitry Nesterov, Dominic Fox, Dominik Prodinger, Edern, Ekaterina
Butyugina, Elabonga Atuo, Emir, farhan khan, Felipe Siola, futurewarning, Gael
Varoquaux, genvalen, Hleb Levitski, Guillaume Lemaitre, gunesbayir, Haesun
Park, hujiahong726, i-aki-y, Ian Thompson, Ido M, Ily, Irene, Jack McIvor,
jakirkham, James Dean, JanFidor, Jarrod Millman, JB Mountford, Jérémie du
Boisberranger, Jessicakk0711, Jiawei Zhang, Joey Ortiz, JohnathanPi, John
Pangas, Joshua Choo Yun Keat, Joshua Hedlund, JuliaSchoepp, Julien Jerphanion,
jygerardy, ka00ri, Kaushik Amar Das, Kento Nozawa, Kian Eliasi, Kilian Kluge,
Lene Preuss, Linus, Logan Thomas, Loic Esteve, Louis Fouquet, Lucy Liu, Madhura
Jayaratne, Marc Torrellas Socastro, Maren Westermann, Mario Kostelac, Mark
Harfouche, Marko Toplak, Marvin Krawutschke, Masanori Kanazu, mathurinm, Matt
Haberland, Max Halford, maximeSaur, Maxwell Liu, m. bou, mdarii, Meekail Zain,
Mikhail Iljin, murezzda, Nawazish Alam, Nicola Fanelli, Nightwalkx, Nikolay
Petrov, Nishu Choudhary, NNLNR, npache, Olivier Grisel, Omar Salman, ouss1508,
PAB, Pandata, partev, Peter Piontek, Phil, pnucci, Pooja M, Pooja Subramaniam,
precondition, Quentin Barthélemy, Rafal Wojdyla, Raghuveer Bhat, Rahil Parikh,
Ralf Gommers, ram vikram singh, Rushil Desai, Sadra Barikbin, SANJAI_3, Sashka
Warner, Scott Gigante, Scott Gustafson, searchforpassion, Seoeun
Hong, Shady el Gewily, Shiva chauhan, Shogo Hida, Shreesha Kumar Bhat, sonnivs,
Sortofamudkip, Stanislav (Stanley) Modrak, Stefanie Senger, Steven Van
Vaerenbergh, Tabea Kossen, Théophile Baranger, Thijs van Weezel, Thomas A
Caswell, Thomas Germer, Thomas J. Fan, Tim Head, Tim P, Tom Dupré la Tour,
tomiock, tspeng, Valentin Laurent, Veghit, VIGNESH D, Vijeth Moudgalya, Vinayak
Mehta, Vincent M, Vincent-violet, Vyom Pathak, William M, windiana42, Xiao
Yuan, Yao Xiao, Yaroslav Halchenko, Yotam Avidar-Constantini, Yuchen Zhou,
Yusuf Raji, zeeshan lone
