
# ===== SOURCE: https://raw.githubusercontent.com/scipy/scipy/main/doc/source/release/1.7.0-notes.rst =====

==========================
SciPy 1.7.0 Release Notes
==========================

.. contents::

SciPy 1.7.0 is the culmination of 6 months of hard work. It contains
many new features, numerous bug-fixes, improved test coverage and better
documentation. There have been a number of deprecations and API changes
in this release, which are documented below. All users are encouraged to
upgrade to this release, as there are a large number of bug-fixes and
optimizations. Before upgrading, we recommend that users check that
their own code does not use deprecated SciPy functionality (to do so,
run your code with ``python -Wd`` and check for ``DeprecationWarning`` s).
Our development attention will now shift to bug-fix releases on the
1.7.x branch, and on adding new features on the master branch.

This release requires Python 3.7+ and NumPy 1.16.5 or greater.

For running on PyPy, PyPy3 6.0+ is required.


**************************
Highlights of this release
**************************

- A new submodule for quasi-Monte Carlo, `scipy.stats.qmc`, was added
- The documentation design was updated to use the same PyData-Sphinx theme as
  NumPy and other ecosystem libraries.
- We now vendor and leverage the Boost C++ library to enable numerous
  improvements for long-standing weaknesses in `scipy.stats`
- `scipy.stats` has six new distributions, eight new (or overhauled)
  hypothesis tests, a new function for bootstrapping, a class that enables
  fast random variate sampling and percentile point function evaluation,
  and many other enhancements.
- ``cdist`` and ``pdist`` distance calculations are faster for several metrics,
  especially weighted cases, thanks to a rewrite to a new C++ backend framework
- A new class for radial basis function interpolation, `RBFInterpolator`, was
  added to address issues with the `Rbf` class.

*We gratefully acknowledge the Chan-Zuckerberg Initiative Essential Open Source
Software for Science program for supporting many of the improvements to*
`scipy.stats`.

************
New features
************

`scipy.cluster` improvements
============================

An optional argument, ``seed``, has been added to ``kmeans`` and ``kmeans2`` to
set the random generator and random state.

`scipy.interpolate` improvements
================================

Improved input validation and error messages for ``fitpack.bispev`` and
``fitpack.parder`` for scenarios that previously caused substantial confusion
for users.

The class `RBFInterpolator` was added to supersede the `Rbf` class. The new
class has usage that more closely follows other interpolator classes, corrects
sign errors that caused unexpected smoothing behavior, includes polynomial
terms in the interpolant (which are necessary for some RBF choices), and
supports interpolation using only the k-nearest neighbors for memory
efficiency.

`scipy.linalg` improvements
===========================

An LAPACK wrapper was added for access to the ``tgexc`` subroutine.

`scipy.ndimage` improvements
============================

`scipy.ndimage.affine_transform` is now able to infer the ``output_shape`` from
the ``out`` array.

`scipy.optimize` improvements
=============================

The optional parameter ``bounds`` was added to
``_minimize_neldermead`` to support bounds constraints
for the Nelder-Mead solver.

``trustregion`` methods ``trust-krylov``, ``dogleg`` and ``trust-ncg`` can now
estimate ``hess`` by finite difference using one of
``["2-point", "3-point", "cs"]``.

``halton`` was added as a ``sampling_method`` in `scipy.optimize.shgo`.
``sobol`` was fixed and is now using `scipy.stats.qmc.Sobol`.

``halton`` and ``sobol`` were added as ``init`` methods in
`scipy.optimize.differential_evolution.`

``differential_evolution`` now accepts an ``x0`` parameter to provide an
initial guess for the minimization.

``least_squares`` has a modest performance improvement when SciPy is built
with Pythran transpiler enabled.

When ``linprog`` is used with ``method`` ``'highs'``, ``'highs-ipm'``, or
``'highs-ds'``, the result object now reports the marginals (AKA shadow
prices, dual values) and residuals associated with each constraint.

`scipy.signal` improvements
===========================

``get_window`` supports ``general_cosine`` and ``general_hamming`` window
functions.

`scipy.signal.medfilt2d` now releases the GIL where appropriate to enable
performance gains via multithreaded calculations.

`scipy.sparse` improvements
===========================

Addition of ``dia_matrix`` sparse matrices is now faster.


`scipy.spatial` improvements
============================

``distance.cdist`` and ``distance.pdist`` performance has greatly improved for
certain weighted metrics. Namely: ``minkowski``, ``euclidean``, ``chebyshev``,
``canberra``, and ``cityblock``.

Modest performance improvements for many of the unweighted ``cdist`` and
``pdist`` metrics noted above.

The parameter ``seed`` was added to `scipy.spatial.vq.kmeans` and
`scipy.spatial.vq.kmeans2`.

The parameters ``axis`` and ``keepdims`` where added to
`scipy.spatial.distance.jensenshannon`.

The ``rotation`` methods ``from_rotvec`` and ``as_rotvec`` now accept a
``degrees`` argument to specify usage of degrees instead of radians.

`scipy.special` improvements
============================

Wright's generalized Bessel function for positive arguments was added as
`scipy.special.wright_bessel`.

An implementation of the inverse of the Log CDF of the Normal Distribution is
now available via `scipy.special.ndtri_exp`.

`scipy.stats` improvements
==========================

Hypothesis Tests
----------------

The Mann-Whitney-Wilcoxon test, ``mannwhitneyu``, has been rewritten. It now
supports n-dimensional input, an exact test method when there are no ties,
and improved documentation. Please see "Other changes" for adjustments to
default behavior.

The new function `scipy.stats.binomtest` replaces `scipy.stats.binom_test`. The
new function returns an object that calculates a confidence intervals of the
proportion parameter. Also, performance was improved from O(n) to O(log(n)) by
using binary search.

The two-sample version of the Cramer-von Mises test is implemented in
`scipy.stats.cramervonmises_2samp`.

The Alexander-Govern test is implemented in the new function
`scipy.stats.alexandergovern`.

The new functions `scipy.stats.barnard_exact` and  `scipy.stats. boschloo_exact`
respectively perform Barnard's exact test and Boschloo's exact test
for 2x2 contingency tables.

The new function `scipy.stats.page_trend_test` performs Page's test for ordered
alternatives.

The new function `scipy.stats.somersd` performs Somers' D test for ordinal
association between two variables.

An option, ``permutations``, has been added in `scipy.stats.ttest_ind` to
perform permutation t-tests. A ``trim`` option was also added to perform
a trimmed (Yuen's) t-test.

The ``alternative`` parameter was added to the ``skewtest``, ``kurtosistest``,
``ranksums``, ``mood``, ``ansari``, ``linregress``, and ``spearmanr`` functions
to allow one-sided hypothesis testing.

Sample statistics
-----------------

The new function `scipy.stats.differential_entropy` estimates the differential
entropy of a continuous distribution from a sample.

The ``boxcox`` and ``boxcox_normmax`` now allow the user to control the
optimizer used to minimize the negative log-likelihood function.

A new function `scipy.stats.contingency.relative_risk` calculates the
relative risk, or risk ratio, of a 2x2 contingency table. The object
returned has a method to compute the confidence interval of the relative risk.

Performance improvements in the ``skew`` and ``kurtosis`` functions achieved
by removal of repeated/redundant calculations.

Substantial performance improvements in `scipy.stats.mstats.hdquantiles_sd`.

The new function `scipy.stats.contingency.association` computes several
measures of association for a contingency table: Pearsons contingency
coefficient, Cramer's V, and Tschuprow's T.

The parameter ``nan_policy`` was added to `scipy.stats.zmap` to provide options
for handling the occurrence of ``nan`` in the input data.

The parameter ``ddof`` was added to `scipy.stats.variation` and
`scipy.stats.mstats.variation`.

The parameter ``weights`` was added to `scipy.stats.gmean`.

Statistical Distributions
-------------------------

We now vendor and leverage the Boost C++ library to address a number of
previously reported issues in ``stats``. Notably, ``beta``, ``binom``,
``nbinom`` now have Boost backends, and it is straightforward to leverage
the backend for additional functions.

The skew Cauchy probability distribution has been implemented as
`scipy.stats.skewcauchy`.

The Zipfian probability distribution has been implemented as
`scipy.stats.zipfian`.

The new distributions ``nchypergeom_fisher`` and ``nchypergeom_wallenius``
implement the Fisher and Wallenius versions of the noncentral hypergeometric
distribution, respectively.

The generalized hyperbolic distribution was added in
`scipy.stats.genhyperbolic`.

The studentized range distribution was added in `scipy.stats.studentized_range`.

`scipy.stats.argus` now has improved handling for small parameter values.

Better argument handling/preparation has resulted in performance improvements
for many distributions.

The ``cosine`` distribution has added ufuncs for ``ppf``, ``cdf``, ``sf``, and
``isf`` methods including numerical precision improvements at the edges of the
support of the distribution.

An option to fit the distribution to data by the method of moments has been
added to the ``fit`` method of the univariate continuous distributions.

Other
-----
`scipy.stats.bootstrap` has been added to allow estimation of the confidence
interval and standard error of a statistic.

The new function `scipy.stats.contingency.crosstab` computes a contingency
table (i.e. a table of counts of unique entries) for the given data.

``scipy.stats.NumericalInverseHermite`` enables fast random variate sampling
and percentile point function evaluation of an arbitrary univariate statistical
distribution.

New `scipy.stats.qmc` module
----------------------------

This new module provides Quasi-Monte Carlo (QMC) generators and associated
helper functions.

It provides a generic class `scipy.stats.qmc.QMCEngine` which defines a QMC
engine/sampler. An engine is state aware: it can be continued, advanced and
reset. 3 base samplers are available:

- `scipy.stats.qmc.Sobol` the well known Sobol low discrepancy sequence.
  Several warnings have been added to guide the user into properly using this
  sampler. The sequence is scrambled by default.
- `scipy.stats.qmc.Halton`: Halton low discrepancy sequence. The sequence is
  scrambled by default.
- `scipy.stats.qmc.LatinHypercube`: plain LHS design.

And 2 special samplers are available:

- `scipy.stats.qmc.MultinomialQMC`: sampling from a multinomial distribution
  using any of the base `scipy.stats.qmc.QMCEngine`.
- `scipy.stats.qmc.MultivariateNormalQMC`: sampling from a multivariate Normal
  using any of the base `scipy.stats.qmc.QMCEngine`.

The module also provide the following helpers:

- `scipy.stats.qmc.discrepancy`: assess the quality of a set of points in terms
  of space coverage.
- `scipy.stats.qmc.update_discrepancy`: can be used in an optimization loop to
  construct a good set of points.
- `scipy.stats.qmc.scale`: easily scale a set of points from (to) the unit
  interval to (from) a given range.


*******************
Deprecated features
*******************

`scipy.linalg` deprecations
===========================

- `scipy.linalg.pinv2` is deprecated and its functionality is completely
  subsumed into `scipy.linalg.pinv`
- Both ``rcond``, ``cond`` keywords of `scipy.linalg.pinv` and
  `scipy.linalg.pinvh` were not working and now are deprecated. They are now
  replaced with functioning ``atol`` and ``rtol`` keywords with clear usage.

`scipy.spatial` deprecations
============================

- `scipy.spatial.distance` metrics expect 1d input vectors but will call
  ``np.squeeze`` on their inputs to accept any extra length-1 dimensions. That
  behaviour is now deprecated.


******************************
Backwards incompatible changes
******************************

*************
Other changes
*************

We now accept and leverage performance improvements from the ahead-of-time
Python-to-C++ transpiler, Pythran, which can be optionally disabled (via
``export SCIPY_USE_PYTHRAN=0``) but is enabled by default at build time.

There are two changes to the default behavior of `scipy.stats.mannwhitenyu`:

- For years, use of the default ``alternative=None`` was deprecated; explicit
  ``alternative`` specification was required. Use of the new default value of
  ``alternative``, "two-sided", is now permitted.
- Previously, all p-values were based on an asymptotic approximation. Now, for
  small samples without ties, the p-values returned are exact by default.

Support has been added for PEP 621 (project metadata in ``pyproject.toml``)

We now support a Gitpod environment to reduce the barrier to entry for SciPy
development; for more details see ``quickstart-gitpod``.


*******
Authors
*******

* @endolith
* Jelle Aalbers +
* Adam +
* Tania Allard +
* Sven Baars +
* Max Balandat +
* baumgarc +
* Christoph Baumgarten
* Peter Bell
* Lilian Besson
* Robinson Besson +
* Max Bolingbroke
* Blair Bonnett +
* Jordão Bragantini
* Harm Buisman +
* Evgeni Burovski
* Matthias Bussonnier
* Dominic C
* CJ Carey
* Ramón Casero +
* Chachay +
* charlotte12l +
* Benjamin Curtice Corbett +
* Falcon Dai +
* Ian Dall +
* Terry Davis
* droussea2001 +
* DWesl +
* dwight200 +
* Thomas J. Fan +
* Joseph Fox-Rabinovitz
* Max Frei +
* Laura Gutierrez Funderburk +
* gbonomib +
* Matthias Geier +
* Pradipta Ghosh +
* Ralf Gommers
* Evan H +
* h-vetinari
* Matt Haberland
* Anselm Hahn +
* Alex Henrie
* Piet Hessenius +
* Trever Hines +
* Elisha Hollander +
* Stephan Hoyer
* Tom Hu +
* Kei Ishikawa +
* Julien Jerphanion
* Robert Kern
* Shashank KS +
* Peter Mahler Larsen
* Eric Larson
* Cheng H. Lee +
* Gregory R. Lee
* Jean-Benoist Leger +
* lgfunderburk +
* liam-o-marsh +
* Xingyu Liu +
* Alex Loftus +
* Christian Lorentzen +
* Cong Ma
* Marc +
* MarkPundurs +
* Markus Löning +
* Liam Marsh +
* Nicholas McKibben
* melissawm +
* Jamie Morton
* Andrew Nelson
* Nikola Forró
* Tor Nordam +
* Olivier Gauthé +
* Rohit Pandey +
* Avanindra Kumar Pandeya +
* Tirth Patel
* paugier +
* Alex H. Wagner, PhD +
* Jeff Plourde +
* Ilhan Polat
* pranavrajpal +
* Vladyslav Rachek
* Bharat Raghunathan
* Recursing +
* Tyler Reddy
* Lucas Roberts
* Gregor Robinson +
* Pamphile Roy +
* Atsushi Sakai
* Benjamin Santos
* Martin K. Scherer +
* Thomas Schmelzer +
* Daniel Scott +
* Sebastian Wallkötter +
* serge-sans-paille +
* Namami Shanker +
* Masashi Shibata +
* Alexandre de Siqueira +
* Albert Steppi +
* Adam J. Stewart +
* Kai Striega
* Diana Sukhoverkhova
* Søren Fuglede Jørgensen
* Mike Taves
* Dan Temkin +
* Nicolas Tessore +
* tsubota20 +
* Robert Uhl
* christos val +
* Bas van Beek +
* Ashutosh Varma +
* Jose Vazquez +
* Sebastiano Vigna
* Aditya Vijaykumar
* VNMabus
* Arthur Volant +
* Samuel Wallan
* Stefan van der Walt
* Warren Weckesser
* Anreas Weh
* Josh Wilson
* Rory Yorke
* Egor Zemlyanoy
* Marc Zoeller +
* zoj613 +
* 秋纫 +

A total of 126 people contributed to this release.
People with a "+" by their names contributed a patch for the first time.
This list of names is automatically generated, and may not be fully complete.


***********************
Issues closed for 1.7.0
***********************

* `#636 <https://github.com/scipy/scipy/issues/636>`__: Statistics Review: mannwhitneyu (Trac #109)
* `#1346 <https://github.com/scipy/scipy/issues/1346>`__: signal.medfilt2d should fall back on signal.medfilt for types...
* `#2118 <https://github.com/scipy/scipy/issues/2118>`__: Mann-Whitney statistic returns incorrect results (Trac #1593)
* `#2158 <https://github.com/scipy/scipy/issues/2158>`__: special.chndtrix (ncx2.ppf) gives wrong results (Trac #1633)
* `#3284 <https://github.com/scipy/scipy/issues/3284>`__: build_sphinx weirdness
* `#3352 <https://github.com/scipy/scipy/issues/3352>`__: beta distribution sf
* `#4067 <https://github.com/scipy/scipy/issues/4067>`__: Mannwhitneyu with arrays full of nan still reports significance
* `#4080 <https://github.com/scipy/scipy/issues/4080>`__: entropy in Scipy
* `#4641 <https://github.com/scipy/scipy/issues/4641>`__: mstats.mannwhitneyu and stats.mannwhitneyu return inconsistent...
* `#5122 <https://github.com/scipy/scipy/issues/5122>`__: scipy.stats.binom.ppf Incorrect for p=0
* `#5180 <https://github.com/scipy/scipy/issues/5180>`__: Rbf interpolation - use only K nearest neighbors
* `#5258 <https://github.com/scipy/scipy/issues/5258>`__: affine_transform complains about output_shape when output array...
* `#5562 <https://github.com/scipy/scipy/issues/5562>`__: Wishart degrees of freedom should be $v > p-1$ instead of $v...
* `#5933 <https://github.com/scipy/scipy/issues/5933>`__: mstats_basic.py - mannwhitneyu [scipy/scipy/stats/mstats_basic.py]
* `#6409 <https://github.com/scipy/scipy/issues/6409>`__: _unequal_var_ttest_denom causes ZeroDivisionError in early samples
* `#6682 <https://github.com/scipy/scipy/issues/6682>`__: negative binomial survival function is imprecise
* `#6897 <https://github.com/scipy/scipy/issues/6897>`__: scipy.stats.mannwhitneyu of empty sets gives p=0.0 and does not...
* `#7303 <https://github.com/scipy/scipy/issues/7303>`__: stats.describe with nan_policy=omit returns matrix-wide minmax...
* `#7406 <https://github.com/scipy/scipy/issues/7406>`__: scipy.stats.binom.ppf returns nan for q between 0 and 1 if n...
* `#7437 <https://github.com/scipy/scipy/issues/7437>`__: ENH: add skewed Cauchy distribution to stats
* `#7542 <https://github.com/scipy/scipy/issues/7542>`__: DOC: stats tutorials: Questions on arcsine and Student t formulae
* `#7593 <https://github.com/scipy/scipy/issues/7593>`__: Meaning of \`tol\` argument in \`scipy.optimize.minimize\` is...
* `#8565 <https://github.com/scipy/scipy/issues/8565>`__: Error in SmoothSphereBivariateSpline(): "ValueError: Error code...
* `#8665 <https://github.com/scipy/scipy/issues/8665>`__: \`scipy.ncx2.sf\` should be monotone decreasing
* `#8836 <https://github.com/scipy/scipy/issues/8836>`__: scipy.optimize.linprog(method='simplex') needs to return duals
* `#9184 <https://github.com/scipy/scipy/issues/9184>`__: Mann-Whitney implementation wrong?
* `#9450 <https://github.com/scipy/scipy/issues/9450>`__: allow seeding of init methods in vq.kmeans2
* `#9704 <https://github.com/scipy/scipy/issues/9704>`__: RectSphereBivariateSpline fails for negative longitude
* `#9836 <https://github.com/scipy/scipy/issues/9836>`__: scipy.stats.rice gives incorrect results when s is very low compared...
* `#9904 <https://github.com/scipy/scipy/issues/9904>`__: Request/Proposal: Greatly improve scipy.interpolate.Rbf
* `#9981 <https://github.com/scipy/scipy/issues/9981>`__: stats.kruskal : add a warning for an input with 2 or more columns
* `#10358 <https://github.com/scipy/scipy/issues/10358>`__: DOC: linprog and linear_sum_assignment tutorials needed
* `#10908 <https://github.com/scipy/scipy/issues/10908>`__: Nakami fitting doesn't converge (scipy.stats)
* `#10933 <https://github.com/scipy/scipy/issues/10933>`__: Add scaled inverse chi2 distribution
* `#11014 <https://github.com/scipy/scipy/issues/11014>`__: Barnard's Test for More Powerful Hypothesis Testing of 2x2 Contingency...
* `#11050 <https://github.com/scipy/scipy/issues/11050>`__: Feature request: Nelder-Mead with bounds
* `#11086 <https://github.com/scipy/scipy/issues/11086>`__: scipy.stats.skew doesn't work correctly for float point numbers
* `#11113 <https://github.com/scipy/scipy/issues/11113>`__: inconsistent result from ttest_ind and mannwhitneyu when used...
* `#11134 <https://github.com/scipy/scipy/issues/11134>`__: Wrong confidence interval for binomial distribution with p=0
* `#11325 <https://github.com/scipy/scipy/issues/11325>`__: Add axis parameter for scipy.spatial.distance.jensenshannon
* `#11474 <https://github.com/scipy/scipy/issues/11474>`__: scipy.stats.skellam.cdf(0) returns 0 for large mu1 = mu2
* `#11523 <https://github.com/scipy/scipy/issues/11523>`__: scipy.stats.zipf doesn't implement zipf distribution
* `#11848 <https://github.com/scipy/scipy/issues/11848>`__: How to get Lagrange / lambda multipliers out of 'linprog' optimize...
* `#11909 <https://github.com/scipy/scipy/issues/11909>`__: Enable bounds for lambda in boxcox
* `#12118 <https://github.com/scipy/scipy/issues/12118>`__: Docstring missing defaults
* `#12132 <https://github.com/scipy/scipy/issues/12132>`__: Slow tests to be trimmed or moved to test('full')
* `#12230 <https://github.com/scipy/scipy/issues/12230>`__: Dendrogram: enable leaves labelling with 'labels' when using...
* `#12282 <https://github.com/scipy/scipy/issues/12282>`__: scipy.stats.chisquare test does not check that observed and expected...
* `#12298 <https://github.com/scipy/scipy/issues/12298>`__: BUG: fmin_powell missing squeeze in 1.5.0rc
* `#12403 <https://github.com/scipy/scipy/issues/12403>`__: Add nan_policy to stats.zmap
* `#12518 <https://github.com/scipy/scipy/issues/12518>`__: Null hypothesis of Kolmogorov Smirnov test is not correctly described
* `#12534 <https://github.com/scipy/scipy/issues/12534>`__: Feature request: scipy.linalg.norm to deal with 0-size array
* `#12622 <https://github.com/scipy/scipy/issues/12622>`__: scipy.interpolate.interpn docstring example
* `#12635 <https://github.com/scipy/scipy/issues/12635>`__: scipy.stats.beta.ppf gives unexpexted results
* `#12669 <https://github.com/scipy/scipy/issues/12669>`__: Median-averaging of complex CSDs
* `#12731 <https://github.com/scipy/scipy/issues/12731>`__: stats.ncx2.cdf fails for nc >> x >> 1
* `#12778 <https://github.com/scipy/scipy/issues/12778>`__: Confusing documentation of scipy.stats.weightedtau
* `#12794 <https://github.com/scipy/scipy/issues/12794>`__: [Bug] The result of stats.beta.isf is inconsistent with stats.beta.sf
* `#12837 <https://github.com/scipy/scipy/issues/12837>`__: stats.mannwhitneyu could support arrays
* `#12868 <https://github.com/scipy/scipy/issues/12868>`__: Vector-valued interpolation in \`interp2d\`
* `#12922 <https://github.com/scipy/scipy/issues/12922>`__: Minimize with trust-constr method leads to TypeError if option...
* `#12929 <https://github.com/scipy/scipy/issues/12929>`__: The use of starred expressions to create data detracts from understanding...
* `#12965 <https://github.com/scipy/scipy/issues/12965>`__: domain of argument of scipy.interpolate.RectSphereBivariateSpline(u,...
* `#13025 <https://github.com/scipy/scipy/issues/13025>`__: Generalized Hyperbolic Distribution
* `#13090 <https://github.com/scipy/scipy/issues/13090>`__: Broken link in doc for signal.max_len_seq
* `#13101 <https://github.com/scipy/scipy/issues/13101>`__: MAINT: Upgrade python version in docker file
* `#13158 <https://github.com/scipy/scipy/issues/13158>`__: \`signal.get_window()\` has a missing doc link and cannot get...
* `#13173 <https://github.com/scipy/scipy/issues/13173>`__: Uninformative error message from bisplev function
* `#13234 <https://github.com/scipy/scipy/issues/13234>`__: BUG: stats: Wrong shape of burr.moment() and fisk.moment() when...
* `#13242 <https://github.com/scipy/scipy/issues/13242>`__: Does kmeans "drop" clusters?
* `#13243 <https://github.com/scipy/scipy/issues/13243>`__: tgsen uses an output argument for computing a default argument
* `#13245 <https://github.com/scipy/scipy/issues/13245>`__: Kurtosis returning 1 for array of same elements
* `#13257 <https://github.com/scipy/scipy/issues/13257>`__: GitHub Actions test failures for MacOS
* `#13272 <https://github.com/scipy/scipy/issues/13272>`__: scipy.stats.yeojohnson_llf doc mistake
* `#13280 <https://github.com/scipy/scipy/issues/13280>`__: Wrong results with hypergeom cdf
* `#13285 <https://github.com/scipy/scipy/issues/13285>`__: description correction in scipy.stats.t
* `#13287 <https://github.com/scipy/scipy/issues/13287>`__: Generate binomial CDF with mu instead of prob
* `#13294 <https://github.com/scipy/scipy/issues/13294>`__: BUG: stats: wrong bounds returned by 'support' method for distributions...
* `#13299 <https://github.com/scipy/scipy/issues/13299>`__: Typing for scipy.spatial
* `#13300 <https://github.com/scipy/scipy/issues/13300>`__: Add a single individual to a latinhypercube initial population...
* `#13311 <https://github.com/scipy/scipy/issues/13311>`__: MAINT: pavement.py PYVER is outdated
* `#13339 <https://github.com/scipy/scipy/issues/13339>`__: savemat discards dimension information if any dimension is zero
* `#13341 <https://github.com/scipy/scipy/issues/13341>`__: add scipy.stats.variation with an ddof parameter
* `#13353 <https://github.com/scipy/scipy/issues/13353>`__: Documentation: in scipy.stats.johnsonsu, parameter \`a\` can...
* `#13405 <https://github.com/scipy/scipy/issues/13405>`__: TST: add a few tests for sparse BSR ctor
* `#13410 <https://github.com/scipy/scipy/issues/13410>`__: BUG: skew for empty array raises
* `#13417 <https://github.com/scipy/scipy/issues/13417>`__: 10,000 times speedup for generating random numbers from the cosine...
* `#13440 <https://github.com/scipy/scipy/issues/13440>`__: python runtest.py -t path-to-test.py failed
* `#13454 <https://github.com/scipy/scipy/issues/13454>`__: Scipy cosine distance can be greater than 2
* `#13459 <https://github.com/scipy/scipy/issues/13459>`__: Broken link in cramervonmises documentation
* `#13494 <https://github.com/scipy/scipy/issues/13494>`__: One-word typo in the documentation of optimize.linprog_simplex
* `#13501 <https://github.com/scipy/scipy/issues/13501>`__: minimize using Powell methods with Bounds leads to "TypeError:...
* `#13509 <https://github.com/scipy/scipy/issues/13509>`__: signal.medfilt2d vs ndimage.median_filter
* `#13511 <https://github.com/scipy/scipy/issues/13511>`__: DOC: error in description of "direc" parameter of "fmin_powell"
* `#13526 <https://github.com/scipy/scipy/issues/13526>`__: TST: stats: intermittent \`test_ttest_ind_randperm_alternative2...
* `#13536 <https://github.com/scipy/scipy/issues/13536>`__: \`_within_tolerance\` seems an unnecessary repetition of \`numpy.isclose\`
* `#13540 <https://github.com/scipy/scipy/issues/13540>`__: missing python 3.8 manylinux wheels on scipy-wheels-nightly
* `#13559 <https://github.com/scipy/scipy/issues/13559>`__: shape error in linprog with revised simplex
* `#13587 <https://github.com/scipy/scipy/issues/13587>`__: binned_statistic unreliable with single precision
* `#13589 <https://github.com/scipy/scipy/issues/13589>`__: Better argument preparation for distributions in stats package.
* `#13602 <https://github.com/scipy/scipy/issues/13602>`__: The crystallball distribution entropy is sometimes minus infinity
* `#13606 <https://github.com/scipy/scipy/issues/13606>`__: MAINT: mypy: some typing errors while running mypy + adding mypy...
* `#13608 <https://github.com/scipy/scipy/issues/13608>`__: Why does stats.binned_statistic_2d convert its values argument...
* `#13609 <https://github.com/scipy/scipy/issues/13609>`__: BUG: SciPy pip install -e gets unusable version spec
* `#13610 <https://github.com/scipy/scipy/issues/13610>`__: Highs solver did not provide a solution nor did it report a failure
* `#13614 <https://github.com/scipy/scipy/issues/13614>`__: BUG: invgauss.cdf should return the correct value when \`mu\`...
* `#13628 <https://github.com/scipy/scipy/issues/13628>`__: 1-letter typo in the definition of scipy.special.spence function...
* `#13634 <https://github.com/scipy/scipy/issues/13634>`__: mmwrite fails on dense, skew-symmetric array
* `#13646 <https://github.com/scipy/scipy/issues/13646>`__: Sparse matrix argmax() integer overflow on Windows 10
* `#13647 <https://github.com/scipy/scipy/issues/13647>`__: \`scipy.stats.qmc.LatinHypercube\` cannot sample single sample...
* `#13651 <https://github.com/scipy/scipy/issues/13651>`__: Documentation wrong in scipy.linalg.eigvalsh
* `#13664 <https://github.com/scipy/scipy/issues/13664>`__: BUG: gamma distribution's inverse survival function overflows...
* `#13693 <https://github.com/scipy/scipy/issues/13693>`__: BUG: sokalmichener appears to incorrectly apply weights
* `#13697 <https://github.com/scipy/scipy/issues/13697>`__: BUG: stats: Spurious warning generated by arcsine.pdf at the...
* `#13704 <https://github.com/scipy/scipy/issues/13704>`__: Make it possible to pass a rank cut-off value relatively to the...
* `#13707 <https://github.com/scipy/scipy/issues/13707>`__: Kullback Leibler Divergence broadcasting no longer works
* `#13740 <https://github.com/scipy/scipy/issues/13740>`__: Scipy.optimize x0 out of bounds when it is within bounds.
* `#13744 <https://github.com/scipy/scipy/issues/13744>`__: scipy.interpolate.interp1d has inconsistent behavior for non-unique...
* `#13754 <https://github.com/scipy/scipy/issues/13754>`__: optimize.minimize 'trust' methods and finite difference Hessian...
* `#13762 <https://github.com/scipy/scipy/issues/13762>`__: MAINT, TST: aarch64 stats test failures showing up in wheels...
* `#13769 <https://github.com/scipy/scipy/issues/13769>`__: probplot draws fit line even when fit=False
* `#13791 <https://github.com/scipy/scipy/issues/13791>`__: BUG: stats: wrapcauchy.cdf does not broadcast the shape parameter...
* `#13793 <https://github.com/scipy/scipy/issues/13793>`__: CI: CircleCI doc build failure
* `#13840 <https://github.com/scipy/scipy/issues/13840>`__: manylinux1 builds are failing because of C99 usage in \`special/_cosine.c\`
* `#13850 <https://github.com/scipy/scipy/issues/13850>`__: CI: Homebrew is failing due to bintray
* `#13875 <https://github.com/scipy/scipy/issues/13875>`__: BUG: chi2_contingency with Yates correction
* `#13878 <https://github.com/scipy/scipy/issues/13878>`__: BUG: \`signal.get_window\` argument handling issue
* `#13880 <https://github.com/scipy/scipy/issues/13880>`__: Remove all usages of numpy.compat
* `#13896 <https://github.com/scipy/scipy/issues/13896>`__: Boschloo's Test for More Powerful Hypothesis Testing of 2x2 Contingency...
* `#13923 <https://github.com/scipy/scipy/issues/13923>`__: Inverse of Log CDF of Normal Distribution
* `#13933 <https://github.com/scipy/scipy/issues/13933>`__: \`signal.get_window\` does not support \`general_cosine\` and...
* `#13950 <https://github.com/scipy/scipy/issues/13950>`__: DOC: scipy.spatial.KDTree.query
* `#13969 <https://github.com/scipy/scipy/issues/13969>`__: N=4 must not exceed M=3
* `#13970 <https://github.com/scipy/scipy/issues/13970>`__: Pearson's original paper on chi-square test could be referenced.
* `#13984 <https://github.com/scipy/scipy/issues/13984>`__: Faster addition of sparse diagonal matrices
* `#13988 <https://github.com/scipy/scipy/issues/13988>`__: An error occurred when using scipy.io.wavfile of scipy 1.6 version...
* `#13997 <https://github.com/scipy/scipy/issues/13997>`__: BUG: sparse: Incorrect result from \`dia_matrix.diagonal()\`
* `#14005 <https://github.com/scipy/scipy/issues/14005>`__: MAINT: optimize: \`curve_fit\` input error msg can be improved.
* `#14038 <https://github.com/scipy/scipy/issues/14038>`__: MAINT: add type annotations for _sobol.pyx
* `#14048 <https://github.com/scipy/scipy/issues/14048>`__: DOC: missing git submodule information
* `#14055 <https://github.com/scipy/scipy/issues/14055>`__: linalg.solve: Unclear error when using assume_a='her' with real...
* `#14093 <https://github.com/scipy/scipy/issues/14093>`__: DOC: Inconsistency in the definition of default values in the...
* `#14158 <https://github.com/scipy/scipy/issues/14158>`__: TST, BUG: test_rbfinterp.py -- test_interpolation_misfit_1d fails...
* `#14170 <https://github.com/scipy/scipy/issues/14170>`__: TST: signal submodule test_filtfilt_gust failing on 32-bit amd64...
* `#14194 <https://github.com/scipy/scipy/issues/14194>`__: MAINT: download-wheels.py missing import
* `#14199 <https://github.com/scipy/scipy/issues/14199>`__: Generated sources for biasedurn extension are broken in 1.7.0rc1


***********************
Pull requests for 1.7.0
***********************

* `#4824 <https://github.com/scipy/scipy/pull/4824>`__: Permutation Ttest (new PR)
* `#4933 <https://github.com/scipy/scipy/pull/4933>`__: ENH: Update the Mann-Whitney-Wilcoxon test
* `#7702 <https://github.com/scipy/scipy/pull/7702>`__: ENH: stats: Add Skewed Cauchy Distribution
* `#8306 <https://github.com/scipy/scipy/pull/8306>`__: Optional Pythran support for scipy.signal.max_len_seq_inner
* `#10170 <https://github.com/scipy/scipy/pull/10170>`__: MAINT: stats: Implement cdf and ppf as ufuncs for the cosine...
* `#10454 <https://github.com/scipy/scipy/pull/10454>`__: ENH: Extend find_peaks_cwt to take numbers and iterables for...
* `#10844 <https://github.com/scipy/scipy/pull/10844>`__: ENH: add stats.qmc module with quasi Monte Carlo functionality
* `#11313 <https://github.com/scipy/scipy/pull/11313>`__: ENH: add Wright's generalized Bessel function
* `#11352 <https://github.com/scipy/scipy/pull/11352>`__: ENH: stats: Add crosstab function.
* `#11477 <https://github.com/scipy/scipy/pull/11477>`__: FIX: bounded parameter in cdfchn.f gives bad results
* `#11695 <https://github.com/scipy/scipy/pull/11695>`__: ENH: stats: add method of moments to \`rv_continuous.fit\`
* `#11911 <https://github.com/scipy/scipy/pull/11911>`__: ENH: Added bounds to boxcox and boxcox_normmax
* `#12438 <https://github.com/scipy/scipy/pull/12438>`__: BUG: use ellipkm1 in elliptical filter design to prevent numerical...
* `#12531 <https://github.com/scipy/scipy/pull/12531>`__: ENH: stats: add Page's L test
* `#12603 <https://github.com/scipy/scipy/pull/12603>`__: ENH: stats: Add \`binomtest\` to replace \`binom_test\`.
* `#12653 <https://github.com/scipy/scipy/pull/12653>`__: ENH: stats: add Somers' D test
* `#12676 <https://github.com/scipy/scipy/pull/12676>`__: BUG: update median averaging in signal.csd
* `#12760 <https://github.com/scipy/scipy/pull/12760>`__: BUG: special: erfinv(x<<1) loses precision
* `#12801 <https://github.com/scipy/scipy/pull/12801>`__: ENH: Add single-sided p-values to remaining spearmanr and linregress
* `#12873 <https://github.com/scipy/scipy/pull/12873>`__: ENH: Stats: add Alexander Govern Test
* `#13008 <https://github.com/scipy/scipy/pull/13008>`__: ENH: Add 'alternative' to functions using normal CDF for p-value
* `#13040 <https://github.com/scipy/scipy/pull/13040>`__: BUG: Allow RectSphereBivariateSpline to accept negative longitude
* `#13048 <https://github.com/scipy/scipy/pull/13048>`__: ENH: stats: Add a function that computes the relative risk.
* `#13067 <https://github.com/scipy/scipy/pull/13067>`__: ENH: Add weights parameter to stats.gmean
* `#13084 <https://github.com/scipy/scipy/pull/13084>`__: ENH: fast Hankel transform
* `#13104 <https://github.com/scipy/scipy/pull/13104>`__: MAINT: upgrade python version (drop python 3.6) for docker dev...
* `#13153 <https://github.com/scipy/scipy/pull/13153>`__: ENH: added association measurements Pearsons Contingency Coefficient,...
* `#13166 <https://github.com/scipy/scipy/pull/13166>`__: ENH: stats: Add nan_policy to zmap.
* `#13175 <https://github.com/scipy/scipy/pull/13175>`__: MAINT: tests for tall cost matrices in \`linear_sum_assignment\`
* `#13177 <https://github.com/scipy/scipy/pull/13177>`__: BUG: raise NotImplementedError in fourier_ellipsoid when ndim...
* `#13184 <https://github.com/scipy/scipy/pull/13184>`__: BUG: stats: Fix min and max calculation of mstats.describe with...
* `#13188 <https://github.com/scipy/scipy/pull/13188>`__: DOC: stats: make null and alternative hypotheses of kstest more...
* `#13193 <https://github.com/scipy/scipy/pull/13193>`__: MAINT: stats: chisquare check sum of observed/expected frequencies
* `#13197 <https://github.com/scipy/scipy/pull/13197>`__: ENH/MAINT: HiGHS upstream enhancements and bug fixes
* `#13198 <https://github.com/scipy/scipy/pull/13198>`__: ENH: allow inference of output_shape from out array in affine_transform
* `#13204 <https://github.com/scipy/scipy/pull/13204>`__: ENH: stats: add Zipfian (different from Zipf/zeta) distribution
* `#13208 <https://github.com/scipy/scipy/pull/13208>`__: REL: set version to 1.7.0.dev0
* `#13216 <https://github.com/scipy/scipy/pull/13216>`__: TST: stats: break up and mark slow tests
* `#13224 <https://github.com/scipy/scipy/pull/13224>`__: Update docs for the weighted τ
* `#13230 <https://github.com/scipy/scipy/pull/13230>`__: ENH: linalg: Add LAPACK wrapper for tgexc.
* `#13232 <https://github.com/scipy/scipy/pull/13232>`__: MAINT: stats: raise error when input to kruskal has >1 dim
* `#13233 <https://github.com/scipy/scipy/pull/13233>`__: DOC: stats: fix MGF of arcsine and entropy of t in tutorial
* `#13236 <https://github.com/scipy/scipy/pull/13236>`__: MAINT: reorganize shared linear assignment tests
* `#13237 <https://github.com/scipy/scipy/pull/13237>`__: BENCH: Refactor stats.Distribution to easily add new distributions
* `#13238 <https://github.com/scipy/scipy/pull/13238>`__: BUG: stats: fix wrong shape output of burr and fisk distributions
* `#13240 <https://github.com/scipy/scipy/pull/13240>`__: MAINT: add tests of trivial cost matrices for linear sum assignment
* `#13252 <https://github.com/scipy/scipy/pull/13252>`__: DOC: optimize: add \`optimize.linear_sum_assignment\` tutorial.
* `#13254 <https://github.com/scipy/scipy/pull/13254>`__: BUG: Fix precision issues for constant input in skew and kurtosis
* `#13262 <https://github.com/scipy/scipy/pull/13262>`__: BUG: scipy.medfilt and .medfilt2d fixes
* `#13263 <https://github.com/scipy/scipy/pull/13263>`__: ENH: add Cramer-von Mises test for two samples
* `#13264 <https://github.com/scipy/scipy/pull/13264>`__: fix a minor typo in \`stats.anderson\` doc
* `#13268 <https://github.com/scipy/scipy/pull/13268>`__: ENH: stats: Add implementation of _entropy for the t distr.
* `#13273 <https://github.com/scipy/scipy/pull/13273>`__: DOC: stats: fix typo in Yeo-Johnson LL function documentation
* `#13275 <https://github.com/scipy/scipy/pull/13275>`__: MAINT: stats: Correct a comment in the _fitstart method of gamma.
* `#13283 <https://github.com/scipy/scipy/pull/13283>`__: BUG: stats: fix the cdf method of rv_discrete class
* `#13286 <https://github.com/scipy/scipy/pull/13286>`__: DOC: stats: clairify rv_continuous/discrete.stats example
* `#13288 <https://github.com/scipy/scipy/pull/13288>`__: DOC: stats: discrete distribution shape parameter restrictions
* `#13289 <https://github.com/scipy/scipy/pull/13289>`__: MAINT: fix a build warning in sigtoolsmodule.c
* `#13290 <https://github.com/scipy/scipy/pull/13290>`__: DOC: Expand the discussion of the nan_policy API.
* `#13291 <https://github.com/scipy/scipy/pull/13291>`__: MAINT: signal, stats: Use keepdims where appropriate.
* `#13292 <https://github.com/scipy/scipy/pull/13292>`__: DOC: stats: note another common parameterization of nbinom
* `#13293 <https://github.com/scipy/scipy/pull/13293>`__: DOC: Change broken link for default values to archived link
* `#13295 <https://github.com/scipy/scipy/pull/13295>`__: BUG: stats: fix the support method to return correct bounds
* `#13296 <https://github.com/scipy/scipy/pull/13296>`__: DOC: stats: Fix latex markup in the kstwo docstring.
* `#13297 <https://github.com/scipy/scipy/pull/13297>`__: TST: mark kde.logpdf overflow test as xslow
* `#13298 <https://github.com/scipy/scipy/pull/13298>`__: Generalized Hyperbolic Distribution
* `#13301 <https://github.com/scipy/scipy/pull/13301>`__: DOC: cluster: Add cluster number note to the docstring of cluster.vq.kmeans
* `#13302 <https://github.com/scipy/scipy/pull/13302>`__: BUG: Fix ndimage.morphology.distance_transform\_\* argument handling
* `#13303 <https://github.com/scipy/scipy/pull/13303>`__: CI: prevent Codecov giving false CI failures and wrong PR annotations
* `#13313 <https://github.com/scipy/scipy/pull/13313>`__: ENH: static typing for qhull
* `#13316 <https://github.com/scipy/scipy/pull/13316>`__: Pythran implementation of scipy.signal._spectral
* `#13317 <https://github.com/scipy/scipy/pull/13317>`__: DOC: forward port 1.6.0 relnotes
* `#13319 <https://github.com/scipy/scipy/pull/13319>`__: ENH: stats: add fast numerical inversion of distribution CDF
* `#13320 <https://github.com/scipy/scipy/pull/13320>`__: ENH: x0 for differential_evolution
* `#13324 <https://github.com/scipy/scipy/pull/13324>`__: DOC correct linprog highs versionadded to 1.6
* `#13326 <https://github.com/scipy/scipy/pull/13326>`__: MAINT: update numpydoc to v1.1.0
* `#13327 <https://github.com/scipy/scipy/pull/13327>`__: DOC: interpolate: improved docstring examples of \`interpolate.interpn()\`...
* `#13328 <https://github.com/scipy/scipy/pull/13328>`__: ENH: Boost stats distributions
* `#13330 <https://github.com/scipy/scipy/pull/13330>`__: ENH: stats: add noncentral hypergeometric distributions (Fisher's...
* `#13331 <https://github.com/scipy/scipy/pull/13331>`__: MAINT/ENH: resolve mypy warnings/errors
* `#13332 <https://github.com/scipy/scipy/pull/13332>`__: DOC: interpolate: improved docstring of \`interpolate.interp2d\`...
* `#13333 <https://github.com/scipy/scipy/pull/13333>`__: ENH: stats: Some more _sf and _isf implementations.
* `#13334 <https://github.com/scipy/scipy/pull/13334>`__: MAINT: stats: Clean up a few defunct comments in _continuous_distns.py
* `#13336 <https://github.com/scipy/scipy/pull/13336>`__: Pythran version of scipy.optimize._group_columns
* `#13337 <https://github.com/scipy/scipy/pull/13337>`__: DOC|ENH: type hinting in scipy.integrate.simpson
* `#13346 <https://github.com/scipy/scipy/pull/13346>`__: ENH: stats: add 'ddof' parameter to the 'variation' function
* `#13355 <https://github.com/scipy/scipy/pull/13355>`__: ENH: stats: implement _logpdf, _sf and _isf for loggamma.
* `#13360 <https://github.com/scipy/scipy/pull/13360>`__: ENH|DOC: fix docstring and input validation in interpolate.RectSphereBivariateSpline
* `#13366 <https://github.com/scipy/scipy/pull/13366>`__: BUG: stats: Don't raise ZeroDivisionError in _unequal_var_ttest_denom
* `#13370 <https://github.com/scipy/scipy/pull/13370>`__: ENH: fix ARGUS distribution for small parameters in stats
* `#13371 <https://github.com/scipy/scipy/pull/13371>`__: ENH: stats: add \`bootstrap\` for estimating confidence interval...
* `#13373 <https://github.com/scipy/scipy/pull/13373>`__: BUG: io/matlab: preserve dimensions of empty >=2D arrays
* `#13374 <https://github.com/scipy/scipy/pull/13374>`__: ENH: stats: add skewed Cauchy distribution
* `#13379 <https://github.com/scipy/scipy/pull/13379>`__: BUG: sparse: fix verbosity in sparse lsqr
* `#13383 <https://github.com/scipy/scipy/pull/13383>`__: TST: stats: mark many dimension permutation t-test slow
* `#13384 <https://github.com/scipy/scipy/pull/13384>`__: MAINT: Make keywords array static
* `#13388 <https://github.com/scipy/scipy/pull/13388>`__: PERF: Avoid duplicate mean calculations in skew and kurtosis
* `#13389 <https://github.com/scipy/scipy/pull/13389>`__: DOC: Fix deprecated directive syntax
* `#13390 <https://github.com/scipy/scipy/pull/13390>`__: DOC: Correct line length for Parameter Section underline
* `#13393 <https://github.com/scipy/scipy/pull/13393>`__: MAINT: stats: allow wishart dim - 1 < df < dim
* `#13395 <https://github.com/scipy/scipy/pull/13395>`__: DOC: fix typo in setup.py warning message
* `#13396 <https://github.com/scipy/scipy/pull/13396>`__: BUG: Fix MLE for Nakagami \`nakagami_gen.fit\`
* `#13397 <https://github.com/scipy/scipy/pull/13397>`__: MAINT:linalg: Fix tgsen family wrapper and ordqz
* `#13406 <https://github.com/scipy/scipy/pull/13406>`__: TST: add error handling tests for sparse BSR ctor
* `#13413 <https://github.com/scipy/scipy/pull/13413>`__: DOC: ultra-quickstart guide
* `#13418 <https://github.com/scipy/scipy/pull/13418>`__: BUG: Fix moment returning inconsistent types and shapes
* `#13423 <https://github.com/scipy/scipy/pull/13423>`__: DOC: Update example for leaf_label_func/dendrogram
* `#13431 <https://github.com/scipy/scipy/pull/13431>`__: ENH: stats: override _rvs for nhypergeom
* `#13432 <https://github.com/scipy/scipy/pull/13432>`__: Add indicator in NDInterpolator docstring that N must be > 1
* `#13434 <https://github.com/scipy/scipy/pull/13434>`__: DOC: stats: note relationship between scaled-inv-chi2 and invgamma
* `#13436 <https://github.com/scipy/scipy/pull/13436>`__: ENH: interpolate: add input validation to check input x-y is...
* `#13441 <https://github.com/scipy/scipy/pull/13441>`__: ENH: add functionality \`barnard_exact\` test to scipy.stats.
* `#13443 <https://github.com/scipy/scipy/pull/13443>`__: MAINT: stats: Updates for skewcauchy
* `#13444 <https://github.com/scipy/scipy/pull/13444>`__: DOC: clarify range of \`a\` parameter fpr johnsonsu/johnsonsb
* `#13445 <https://github.com/scipy/scipy/pull/13445>`__: DOC: fix runtests guidelines.
* `#13446 <https://github.com/scipy/scipy/pull/13446>`__: MAINT: stats: Add _fitstart method to wrapcauchy.
* `#13447 <https://github.com/scipy/scipy/pull/13447>`__: DEV: Update development Docker image
* `#13448 <https://github.com/scipy/scipy/pull/13448>`__: ENH: Add annotations for \`scipy.spatial.distance\`
* `#13451 <https://github.com/scipy/scipy/pull/13451>`__: DOC: minor formatting.
* `#13458 <https://github.com/scipy/scipy/pull/13458>`__: DOC: indent see also.
* `#13460 <https://github.com/scipy/scipy/pull/13460>`__: DOC: stats: Fix link to Cramer-von Mises wikipedia article.
* `#13461 <https://github.com/scipy/scipy/pull/13461>`__: DOC: reorganize scipy.stats overview docs page
* `#13463 <https://github.com/scipy/scipy/pull/13463>`__: DOC: misc formatting fixes
* `#13466 <https://github.com/scipy/scipy/pull/13466>`__: DOC: Typo in see also s/SmoothUni/SmoothBi/g
* `#13467 <https://github.com/scipy/scipy/pull/13467>`__: DOC: optimize: add description about \`tol\` argument for \`minimize\`.
* `#13469 <https://github.com/scipy/scipy/pull/13469>`__: MAINT: Refactor optimization methods to use scipy.stats.qmc
* `#13477 <https://github.com/scipy/scipy/pull/13477>`__: CI: pin numpy to 1.19.5 for the three macOS CI jobs
* `#13478 <https://github.com/scipy/scipy/pull/13478>`__: DOC: fix typos where double :: for Sphinx directives were missing
* `#13481 <https://github.com/scipy/scipy/pull/13481>`__: CI: pin numpy to 1.19.5 in the 4 parallel Windows builds on Azure
* `#13482 <https://github.com/scipy/scipy/pull/13482>`__: CI: use numpy 1.20.0 again in macOS CI
* `#13483 <https://github.com/scipy/scipy/pull/13483>`__: DOC: Multiple documentation syntax fixes.
* `#13484 <https://github.com/scipy/scipy/pull/13484>`__: Move some pythran config from CI to setup
* `#13487 <https://github.com/scipy/scipy/pull/13487>`__: DOC: add a tutorial about scipy.stats.qmc
* `#13492 <https://github.com/scipy/scipy/pull/13492>`__: ENH: GH actions should not run on forks
* `#13493 <https://github.com/scipy/scipy/pull/13493>`__: DEV: Enable gitpod for SciPy
* `#13495 <https://github.com/scipy/scipy/pull/13495>`__: DOC One-word typo in the documentation of optimize.linprog_simplex
* `#13499 <https://github.com/scipy/scipy/pull/13499>`__: DOC: describe LSAP implementation
* `#13502 <https://github.com/scipy/scipy/pull/13502>`__: BUG: Bounds created with lists weren't working for Powell
* `#13507 <https://github.com/scipy/scipy/pull/13507>`__: MAINT, TST: stats: centralize invalid parameters list for all...
* `#13510 <https://github.com/scipy/scipy/pull/13510>`__: DOC: stats: fix small doc errors in 'multivariate_hypergeom'
* `#13513 <https://github.com/scipy/scipy/pull/13513>`__: DOC: Added math notation in examples in ltisys.py
* `#13514 <https://github.com/scipy/scipy/pull/13514>`__: ENH: simplify low_0_bit function for Sobol
* `#13515 <https://github.com/scipy/scipy/pull/13515>`__: ENH: optimize: add bound constraint support for nelder-mead solver
* `#13516 <https://github.com/scipy/scipy/pull/13516>`__: DOC: reduce LaTeX usage for johnsonb docstring
* `#13519 <https://github.com/scipy/scipy/pull/13519>`__: BLD: remove build_sphinx support from setup.py
* `#13527 <https://github.com/scipy/scipy/pull/13527>`__: TST: stats: xfail ttest_ind_randperm_alternative2 on 32 bit
* `#13530 <https://github.com/scipy/scipy/pull/13530>`__: DOC: correct comparisons between median filter functions
* `#13532 <https://github.com/scipy/scipy/pull/13532>`__: ENH: release the GIL inside medfilt2d
* `#13538 <https://github.com/scipy/scipy/pull/13538>`__: DOC: optimize: fix minor doc error in 'fmin_powell' (#13511)
* `#13546 <https://github.com/scipy/scipy/pull/13546>`__: DOC: fix list of "mode" options for ndimage
* `#13549 <https://github.com/scipy/scipy/pull/13549>`__: ENH: stats: add 'alternative' keyword to some normality tests.
* `#13551 <https://github.com/scipy/scipy/pull/13551>`__: MAINT: add git to docker env
* `#13552 <https://github.com/scipy/scipy/pull/13552>`__: MAINT: stats: remove float_power shim
* `#13553 <https://github.com/scipy/scipy/pull/13553>`__: DOC: use support rather than a/b in stats tutorial
* `#13560 <https://github.com/scipy/scipy/pull/13560>`__: MAINT: optimize: improve linprog error message for sparse input...
* `#13562 <https://github.com/scipy/scipy/pull/13562>`__: MAINT: optimize: using np.isclose instead of _within_tolerance.
* `#13566 <https://github.com/scipy/scipy/pull/13566>`__: ENH: Speed up hdquantiles_sd()
* `#13569 <https://github.com/scipy/scipy/pull/13569>`__: BENCH: optimize: benchmark only HiGHS methods; add bigger linprog...
* `#13574 <https://github.com/scipy/scipy/pull/13574>`__: DOC: In description of cluster.hierarchy.dendrogram 'level' parameter,...
* `#13576 <https://github.com/scipy/scipy/pull/13576>`__: ENH: improve discrepancy performance
* `#13579 <https://github.com/scipy/scipy/pull/13579>`__: TST: Add pybind11 to tox environments
* `#13583 <https://github.com/scipy/scipy/pull/13583>`__: BUG: Fix Dockerfile apt-get installs
* `#13588 <https://github.com/scipy/scipy/pull/13588>`__: MAINT: forward port 1.6.1 relnotes.
* `#13593 <https://github.com/scipy/scipy/pull/13593>`__: BUG: stats: preserve sample dtype for bin edges
* `#13595 <https://github.com/scipy/scipy/pull/13595>`__: ENH: interpolate: add RBFInterpolator
* `#13596 <https://github.com/scipy/scipy/pull/13596>`__: DOC: Fix indentation in new_stats_distribution.rst.inc
* `#13601 <https://github.com/scipy/scipy/pull/13601>`__: Add dpss for get_window function
* `#13604 <https://github.com/scipy/scipy/pull/13604>`__: DOC: Correct dual annealing visiting param range.
* `#13605 <https://github.com/scipy/scipy/pull/13605>`__: Add Codecov badge to README
* `#13607 <https://github.com/scipy/scipy/pull/13607>`__: MAINT: stats: fix crystalball entropy
* `#13611 <https://github.com/scipy/scipy/pull/13611>`__: Better argument preparation for distributions in stats package.
* `#13612 <https://github.com/scipy/scipy/pull/13612>`__: Add docker run command for Windows cmd
* `#13613 <https://github.com/scipy/scipy/pull/13613>`__: MAINT, CI: mypy: fix typing errors + add mypy to CI
* `#13616 <https://github.com/scipy/scipy/pull/13616>`__: FIX: Return correct output for invgauss.cdf when mu is very small
* `#13617 <https://github.com/scipy/scipy/pull/13617>`__: MAINT: accept numbers and iterables for width in find_peaks_cwt
* `#13620 <https://github.com/scipy/scipy/pull/13620>`__: CI: disable the mypy CI job (partial revert of gh-13613)
* `#13621 <https://github.com/scipy/scipy/pull/13621>`__: DOC: signal: use array_like for input types
* `#13622 <https://github.com/scipy/scipy/pull/13622>`__: MAINT: clean up some unused files, make \`mypy scipy\` pass
* `#13623 <https://github.com/scipy/scipy/pull/13623>`__: CI: enable Mypy CI job again
* `#13624 <https://github.com/scipy/scipy/pull/13624>`__: TST: test more values for \`visiting_param\` input to \`dual_annealing\`
* `#13625 <https://github.com/scipy/scipy/pull/13625>`__: Rename integrate.simps to integrate.simpsons in documentation...
* `#13631 <https://github.com/scipy/scipy/pull/13631>`__: ENH: add a \`stats.differential_entropy\` function
* `#13633 <https://github.com/scipy/scipy/pull/13633>`__: BUG: stats.binned_statistic_2d user function expecting arrays
* `#13641 <https://github.com/scipy/scipy/pull/13641>`__: ENH: Added degrees parameter to rotvec
* `#13645 <https://github.com/scipy/scipy/pull/13645>`__: MAINT: mypy: don't install numpy-stubs
* `#13649 <https://github.com/scipy/scipy/pull/13649>`__: BUG: sparse: csc_matrix.argmax() integer overflow
* `#13650 <https://github.com/scipy/scipy/pull/13650>`__: ENH: stats: add 'alternative' parameter to ansari
* `#13652 <https://github.com/scipy/scipy/pull/13652>`__: DOC: fix eigvalsh documentation (#13651)
* `#13654 <https://github.com/scipy/scipy/pull/13654>`__: BUG: Fix LatinHypercubes
* `#13656 <https://github.com/scipy/scipy/pull/13656>`__: DOC: Fix PCHIP references
* `#13657 <https://github.com/scipy/scipy/pull/13657>`__: TST: remove IPython warning in debug session
* `#13658 <https://github.com/scipy/scipy/pull/13658>`__: Remove spurious quotes in docstring
* `#13661 <https://github.com/scipy/scipy/pull/13661>`__: ENH: stats: improve efficiency of / fix bug in exact permutation...
* `#13667 <https://github.com/scipy/scipy/pull/13667>`__: MAINT: Make latest Docker image default
* `#13668 <https://github.com/scipy/scipy/pull/13668>`__: MAINT: add .theia/ to .gitignore
* `#13669 <https://github.com/scipy/scipy/pull/13669>`__: BLD: change SCIPY_USE_PYTHRAN default to \`1\`
* `#13676 <https://github.com/scipy/scipy/pull/13676>`__: ENH Small improvements for LSQR with damp
* `#13678 <https://github.com/scipy/scipy/pull/13678>`__: MAINT: add Pythran-generated files to .gitignore
* `#13679 <https://github.com/scipy/scipy/pull/13679>`__: MAINT: move the \`conda develop .\` in the Gitpod config
* `#13680 <https://github.com/scipy/scipy/pull/13680>`__: DOC: Add cKDTree note comparing it with KDTree
* `#13681 <https://github.com/scipy/scipy/pull/13681>`__: DOC: build doc updates on Pythran, compiled code, and cleanups
* `#13683 <https://github.com/scipy/scipy/pull/13683>`__: BUG: mmwrite correctly serializes non skew-symmetric arrays
* `#13684 <https://github.com/scipy/scipy/pull/13684>`__: FIX: fix numerical overflow in gamma.isf method
* `#13685 <https://github.com/scipy/scipy/pull/13685>`__: BUG: fix cosine distance range to 0-2
* `#13694 <https://github.com/scipy/scipy/pull/13694>`__: MAINT: fix warning emitted when NumPy version is incorrect
* `#13696 <https://github.com/scipy/scipy/pull/13696>`__: ENH: support trimming in ttest_ind
* `#13698 <https://github.com/scipy/scipy/pull/13698>`__: BUG: stats: Fix spurious warnings generated by arcsine.pdf
* `#13701 <https://github.com/scipy/scipy/pull/13701>`__: DEV: scipy.interpolate b-splines (periodic case)
* `#13702 <https://github.com/scipy/scipy/pull/13702>`__: DEP: Clean up spent deprecations in spatial.distance
* `#13703 <https://github.com/scipy/scipy/pull/13703>`__: MAINT: fix issues found by static code analysis
* `#13706 <https://github.com/scipy/scipy/pull/13706>`__: ENH: stats: Implement sf and isf for the laplace distribution.
* `#13711 <https://github.com/scipy/scipy/pull/13711>`__: MAINT: stats: fix broadcasting for scipy.stats.entropy
* `#13712 <https://github.com/scipy/scipy/pull/13712>`__: BUG: stats: Override _fitstart for the invweibull distribution.
* `#13713 <https://github.com/scipy/scipy/pull/13713>`__: DOC: update toolchain.rst to reflect windows universal C runtime
* `#13714 <https://github.com/scipy/scipy/pull/13714>`__: MAINT: stats: Remove an unused list from test_continuous_basic.py.
* `#13715 <https://github.com/scipy/scipy/pull/13715>`__: MAINT: stats: No need to suppress frechet deprecation warnings.
* `#13716 <https://github.com/scipy/scipy/pull/13716>`__: MAINT: use super() as described by PEP 3135
* `#13718 <https://github.com/scipy/scipy/pull/13718>`__: MAINT: new-style class, removing inheritance to object
* `#13721 <https://github.com/scipy/scipy/pull/13721>`__: MAINT: add a type-ignore for mpmath (#13721)
* `#13723 <https://github.com/scipy/scipy/pull/13723>`__: MAINT: mypy: ignore mpmath imports in mypy.ini
* `#13724 <https://github.com/scipy/scipy/pull/13724>`__: DOC: pydata sphinx theme
* `#13725 <https://github.com/scipy/scipy/pull/13725>`__: BENCH: add benchmark for Kendalltau
* `#13727 <https://github.com/scipy/scipy/pull/13727>`__: CI: simplify Pythran configuration setup for Azure
* `#13731 <https://github.com/scipy/scipy/pull/13731>`__: MAINT: stats: Some flake8-driven clean up.
* `#13732 <https://github.com/scipy/scipy/pull/13732>`__: ENH: stats: Studentized Range Distribution
* `#13735 <https://github.com/scipy/scipy/pull/13735>`__: DOC: correct Voronoi docstring
* `#13738 <https://github.com/scipy/scipy/pull/13738>`__: DOC: add example to wright_bessel
* `#13739 <https://github.com/scipy/scipy/pull/13739>`__: ENH: stats: Implement _sf and _isf for the chi distribution.
* `#13741 <https://github.com/scipy/scipy/pull/13741>`__: MAINT: prevent overwriting of x in minimize
* `#13747 <https://github.com/scipy/scipy/pull/13747>`__: DOC: Add note for interp1d for non-unique x-values
* `#13749 <https://github.com/scipy/scipy/pull/13749>`__: MAINT: forward port 1.6.2 relnotes
* `#13759 <https://github.com/scipy/scipy/pull/13759>`__: MAINT: simpson small performance speedups
* `#13765 <https://github.com/scipy/scipy/pull/13765>`__: FIX: npymath missing causing npy_log1p to be unknown
* `#13768 <https://github.com/scipy/scipy/pull/13768>`__: BENCH: Add missing pythran dependency
* `#13770 <https://github.com/scipy/scipy/pull/13770>`__: ENH: stats.contingency: Add the sparse option to crosstab.
* `#13774 <https://github.com/scipy/scipy/pull/13774>`__: DEP: Deprecate squeezing input vectors in spatial.distance
* `#13775 <https://github.com/scipy/scipy/pull/13775>`__: Enable trust region methods to use a finite difference Hessian...
* `#13777 <https://github.com/scipy/scipy/pull/13777>`__: DOC: Fix Ubuntu/Debian installation instructions
* `#13778 <https://github.com/scipy/scipy/pull/13778>`__: DOC: remove references to RandomState
* `#13782 <https://github.com/scipy/scipy/pull/13782>`__: MAINT: LBFGSB err msg on MAXLS changed closes #11718
* `#13785 <https://github.com/scipy/scipy/pull/13785>`__: BENCH: Add benchmark for cdist/pdist with weights
* `#13786 <https://github.com/scipy/scipy/pull/13786>`__: MAINT: Prepare cdist/pdist for C++ rework
* `#13787 <https://github.com/scipy/scipy/pull/13787>`__: MAINT: stats: move entropy and differential_entropy functions...
* `#13790 <https://github.com/scipy/scipy/pull/13790>`__: DOC: Add some dependencies for Dockerfile doc of scipy development.
* `#13792 <https://github.com/scipy/scipy/pull/13792>`__: BUG: stats: Fix broadcasting in wrapcauchy.cdf
* `#13795 <https://github.com/scipy/scipy/pull/13795>`__: MAINT: stats: add hypotests to __all__ in init.py, not stats.py
* `#13797 <https://github.com/scipy/scipy/pull/13797>`__: MAINT: stats: probplot: don't plot least-squares fit line unless...
* `#13798 <https://github.com/scipy/scipy/pull/13798>`__: MAINT: fix incorrect code comment in \`hierarchy.to_tree\`
* `#13802 <https://github.com/scipy/scipy/pull/13802>`__: DEV: add environment.yml file for development with conda/mamba
* `#13803 <https://github.com/scipy/scipy/pull/13803>`__: DOC: fix doc build warning about arxiv role already being registered
* `#13804 <https://github.com/scipy/scipy/pull/13804>`__: DOC+MAINT: optimize: lb and ub in the Bounds constructor are...
* `#13807 <https://github.com/scipy/scipy/pull/13807>`__: MAINT: Dont use parallel Sphinx
* `#13808 <https://github.com/scipy/scipy/pull/13808>`__: MAINT: cluster.to_tree: more idiomatic looping over rows of matrix...
* `#13810 <https://github.com/scipy/scipy/pull/13810>`__: MAINT: add a CODEOWNERS file
* `#13811 <https://github.com/scipy/scipy/pull/13811>`__: MAINT: Add ci skip to azp
* `#13814 <https://github.com/scipy/scipy/pull/13814>`__: ENH/DOC: pydata sphinx theme polishing
* `#13817 <https://github.com/scipy/scipy/pull/13817>`__: DOC: Misc parameter typo and casing in scipy/linalg/_decomp_ldl.py
* `#13818 <https://github.com/scipy/scipy/pull/13818>`__: MAINT: stats: keep \`entropy\` importable from \`scipy.stats.distributions\`
* `#13820 <https://github.com/scipy/scipy/pull/13820>`__: BUG: update _kendall_p_exact ValueError to f-string
* `#13831 <https://github.com/scipy/scipy/pull/13831>`__: FIX:DEP: Allow better tolerance control for pinv and pinvh and...
* `#13832 <https://github.com/scipy/scipy/pull/13832>`__: BUG: stats: Fix rvs for levy_stable when alpha=1
* `#13833 <https://github.com/scipy/scipy/pull/13833>`__: MAINT: Add inline type hintings for stats.qmc
* `#13836 <https://github.com/scipy/scipy/pull/13836>`__: MAINT: Fix a couple compiler warnings.
* `#13838 <https://github.com/scipy/scipy/pull/13838>`__: TST: relax test tolerances for BinomTest
* `#13841 <https://github.com/scipy/scipy/pull/13841>`__: BLD: add \`-std=c99\` flag to scipy.special extensions using...
* `#13845 <https://github.com/scipy/scipy/pull/13845>`__: ENH: stats: add \`method\` parameter to \`differential_entropy\`...
* `#13847 <https://github.com/scipy/scipy/pull/13847>`__: TST: skip on optimize failure on macOS, mark one as xfail
* `#13848 <https://github.com/scipy/scipy/pull/13848>`__: DOC: optimize: move Nelder Mead doc from Unconstrained minimization...
* `#13849 <https://github.com/scipy/scipy/pull/13849>`__: DOC: Roadmap update
* `#13852 <https://github.com/scipy/scipy/pull/13852>`__: CI: fix temporary wrong brew version from GitHub
* `#13854 <https://github.com/scipy/scipy/pull/13854>`__: ENH: Update Scipy Gitpod
* `#13859 <https://github.com/scipy/scipy/pull/13859>`__: TST: fix ultra-slow ttest permutations test
* `#13860 <https://github.com/scipy/scipy/pull/13860>`__: MAINT: clean up LSAP error checking
* `#13863 <https://github.com/scipy/scipy/pull/13863>`__: DOC: remove seed in examples
* `#13865 <https://github.com/scipy/scipy/pull/13865>`__: DOC: optimize: The bounds param of differential_evolution is...
* `#13866 <https://github.com/scipy/scipy/pull/13866>`__: MAINT: special: Remove an unused variable from _poly_approx in...
* `#13867 <https://github.com/scipy/scipy/pull/13867>`__: DOC: stats: Explain meaning of alternatives for fisher_exact.
* `#13868 <https://github.com/scipy/scipy/pull/13868>`__: CI: fix the failing job on linux.
* `#13870 <https://github.com/scipy/scipy/pull/13870>`__: MAINT: move LSAP rectangular matrix handling into solver code
* `#13871 <https://github.com/scipy/scipy/pull/13871>`__: DOC: Add Gitpod documentation
* `#13876 <https://github.com/scipy/scipy/pull/13876>`__: Workflow : Add nightly release of NumPy in linux workflows
* `#13877 <https://github.com/scipy/scipy/pull/13877>`__: DOC: Conform to numpydoc + uniformity.
* `#13879 <https://github.com/scipy/scipy/pull/13879>`__: BUG: signal: fix get_window argument handling and add tests.
* `#13881 <https://github.com/scipy/scipy/pull/13881>`__: CI: remove .travis.yml, remove codecov from CircleCI
* `#13882 <https://github.com/scipy/scipy/pull/13882>`__: BLD: ensure incrementing dev version strings
* `#13886 <https://github.com/scipy/scipy/pull/13886>`__: TST: optimize: skip test_network_flow_limited_capacity w/ UMFPACK...
* `#13888 <https://github.com/scipy/scipy/pull/13888>`__: MAINT: Fix issues involving elif conditions
* `#13891 <https://github.com/scipy/scipy/pull/13891>`__: Rename InivariateSpline to UnivariateSpline
* `#13893 <https://github.com/scipy/scipy/pull/13893>`__: ENH: linprog HiGHS marginals/sensitivy analysis
* `#13894 <https://github.com/scipy/scipy/pull/13894>`__: DOC: Add blank line before \`Return\` section.
* `#13897 <https://github.com/scipy/scipy/pull/13897>`__: DOC: BLD: fix doc build version check, and improve build time
* `#13903 <https://github.com/scipy/scipy/pull/13903>`__: MAINT: Gitpod fixes
* `#13907 <https://github.com/scipy/scipy/pull/13907>`__: ENH: Rewrite minkowski metric in C++ with pybind11
* `#13909 <https://github.com/scipy/scipy/pull/13909>`__: Revert "Workflow : Add nightly release of NumPy in linux workflows"
* `#13910 <https://github.com/scipy/scipy/pull/13910>`__: DOC: update Readme
* `#13911 <https://github.com/scipy/scipy/pull/13911>`__: MAINT: use dict built-in rather than OrderedDict
* `#13920 <https://github.com/scipy/scipy/pull/13920>`__: BUG: Reactivate conda environment in init
* `#13925 <https://github.com/scipy/scipy/pull/13925>`__: BUG: stats: magnitude of Yates' correction <= abs(observed-expected)...
* `#13926 <https://github.com/scipy/scipy/pull/13926>`__: DOC: correct return type in disjoint_set.subsets docstring
* `#13927 <https://github.com/scipy/scipy/pull/13927>`__: DOC/MAINT: Add copyright notice to qmc.primes_from_2_to
* `#13928 <https://github.com/scipy/scipy/pull/13928>`__: BUG: DOC: signal: fix need argument config and add missing doc...
* `#13929 <https://github.com/scipy/scipy/pull/13929>`__: REL: add PEP 621 (project metadata in pyproject.toml) support
* `#13931 <https://github.com/scipy/scipy/pull/13931>`__: MAINT: special: get rid of _logit.c.src
* `#13934 <https://github.com/scipy/scipy/pull/13934>`__: ENH: signal: make \`get_window\` supports \`general_cosine\`...
* `#13940 <https://github.com/scipy/scipy/pull/13940>`__: MAINT: QMCEngine d input validation
* `#13941 <https://github.com/scipy/scipy/pull/13941>`__: MAINT: forward port 1.6.3 relnotes
* `#13944 <https://github.com/scipy/scipy/pull/13944>`__: BUG: spatial: fix weight handling of \`distance.sokalmichener\`.
* `#13947 <https://github.com/scipy/scipy/pull/13947>`__: MAINT: Remove duplicate calculations in sokalmichener
* `#13949 <https://github.com/scipy/scipy/pull/13949>`__: DOC: minor grammar fixes in minimize and KDTree.query
* `#13951 <https://github.com/scipy/scipy/pull/13951>`__: ENH: Add Boschloo exact test to stats
* `#13956 <https://github.com/scipy/scipy/pull/13956>`__: ENH: spatial: add \`axis\` and \`keepdims\` optional argument...
* `#13963 <https://github.com/scipy/scipy/pull/13963>`__: MAINT: stats: Fix unused imports and a few other issues related...
* `#13971 <https://github.com/scipy/scipy/pull/13971>`__: DOC: Add Karl Pearson's reference to chi-square test
* `#13972 <https://github.com/scipy/scipy/pull/13972>`__: ENH: cluster: add an optional argument \`seed\` for \`kmeans\`...
* `#13973 <https://github.com/scipy/scipy/pull/13973>`__: BLD: fix build warnings for causal/anticausal pointers in ndimage
* `#13975 <https://github.com/scipy/scipy/pull/13975>`__: ENH: set empty array norm to zero.
* `#13977 <https://github.com/scipy/scipy/pull/13977>`__: MAINT: signal: replace distutils templating with tempita
* `#13978 <https://github.com/scipy/scipy/pull/13978>`__: MAINT: improve validations and keyword only arguments for some...
* `#13979 <https://github.com/scipy/scipy/pull/13979>`__: ENH: Add Inverse of Log CDF of Normal Distribution
* `#13983 <https://github.com/scipy/scipy/pull/13983>`__: Fixing \`ndimage.watershed_ift\` tutorial's documentation
* `#13987 <https://github.com/scipy/scipy/pull/13987>`__: DOC: Adding examples to docstrings in morphology: white_tophat,...
* `#13989 <https://github.com/scipy/scipy/pull/13989>`__: DOC: interpolate: improve examples of \`RegularGridInterpolator\`...
* `#13990 <https://github.com/scipy/scipy/pull/13990>`__: MAINT, DOC: optimize: Make the input validation explanation clear...
* `#13992 <https://github.com/scipy/scipy/pull/13992>`__: Workflow : Add nightly release of NumPy in linux workflows
* `#13995 <https://github.com/scipy/scipy/pull/13995>`__: Doc: Continuous integration information
* `#14000 <https://github.com/scipy/scipy/pull/14000>`__: BUG: sparse: Fix DIA.diagonal bug and add a regression test
* `#14004 <https://github.com/scipy/scipy/pull/14004>`__: ENH: Fast addition dia matrix
* `#14006 <https://github.com/scipy/scipy/pull/14006>`__: MAINT: optimize: add validation to check func parameter number...
* `#14008 <https://github.com/scipy/scipy/pull/14008>`__: BUG: Raise exception for inconsistent WAV header
* `#14009 <https://github.com/scipy/scipy/pull/14009>`__: DEP: Remove usage of numpy.compat
* `#14010 <https://github.com/scipy/scipy/pull/14010>`__: MAINT: add support for wheel DL proxy
* `#14012 <https://github.com/scipy/scipy/pull/14012>`__: DOC: Broaden Exact Test Reference
* `#14015 <https://github.com/scipy/scipy/pull/14015>`__: MAINT: remove brew update
* `#14017 <https://github.com/scipy/scipy/pull/14017>`__: BENCH: Add more formats for sparse arithmetic
* `#14018 <https://github.com/scipy/scipy/pull/14018>`__: BENCH: add benchmark for f_oneway
* `#14020 <https://github.com/scipy/scipy/pull/14020>`__: MAINT: modify np.int\_ to np.int32 to make it the same for 32/64...
* `#14023 <https://github.com/scipy/scipy/pull/14023>`__: MAINT: Fix clang build and remove some unicode characters
* `#14025 <https://github.com/scipy/scipy/pull/14025>`__: BUG: sparse: fix DIA.setdiag issue
* `#14026 <https://github.com/scipy/scipy/pull/14026>`__: TST: optimize: xfail part of test_powell
* `#14029 <https://github.com/scipy/scipy/pull/14029>`__: CI: github macos fix
* `#14030 <https://github.com/scipy/scipy/pull/14030>`__: MAINT: use 'yield from <expr>' (PEP 380)
* `#14031 <https://github.com/scipy/scipy/pull/14031>`__: MAINT: new-style class, removing inheritance to object
* `#14032 <https://github.com/scipy/scipy/pull/14032>`__: MAINT: CXXFLAGS for Pythran
* `#14033 <https://github.com/scipy/scipy/pull/14033>`__: ENH: Port sqeuclidean and braycurtis to _distance_pybind
* `#14034 <https://github.com/scipy/scipy/pull/14034>`__: MAINT: Clean-up 'next = __next__'
* `#14045 <https://github.com/scipy/scipy/pull/14045>`__: MAINT: bump PYVER pavement.py
* `#14047 <https://github.com/scipy/scipy/pull/14047>`__: DEV: initialize boost submodule in Gitpod Dockerfile
* `#14051 <https://github.com/scipy/scipy/pull/14051>`__: BLD: if boost submodule content is missing, error out early
* `#14052 <https://github.com/scipy/scipy/pull/14052>`__: DOC: missing submodule init information
* `#14057 <https://github.com/scipy/scipy/pull/14057>`__: DOC: special: Add Examples to \`psi\` docstring
* `#14058 <https://github.com/scipy/scipy/pull/14058>`__: BUG: fixed a dtype bug in linalg.solve.
* `#14060 <https://github.com/scipy/scipy/pull/14060>`__: Doc: Fix typo in documentation of spence function.
* `#14061 <https://github.com/scipy/scipy/pull/14061>`__: MAINT:stats: Type annotations for _sobol.pyx
* `#14062 <https://github.com/scipy/scipy/pull/14062>`__: DOC: A few small fixes in quickstart_gitpod.rst
* `#14063 <https://github.com/scipy/scipy/pull/14063>`__: DOC: signal: add Add Examples to \`cont2discrete\` docstring
* `#14064 <https://github.com/scipy/scipy/pull/14064>`__: DOC: optimize: Add Examples to fmin_bfgs docstring
* `#14065 <https://github.com/scipy/scipy/pull/14065>`__: Add example for scipy stats.trim1 under docstring
* `#14066 <https://github.com/scipy/scipy/pull/14066>`__: DOC add example to scipy.special.hermite
* `#14067 <https://github.com/scipy/scipy/pull/14067>`__: DOC add alpha docstring description, add example to docstring
* `#14070 <https://github.com/scipy/scipy/pull/14070>`__: DOC add parameters, return, and example to docstring
* `#14072 <https://github.com/scipy/scipy/pull/14072>`__: MAINT/TST: Fix tests failing with the nightly build of numpy.
* `#14075 <https://github.com/scipy/scipy/pull/14075>`__: DOC Improve the code snippet in signal.hilbert docstring.
* `#14076 <https://github.com/scipy/scipy/pull/14076>`__: DOC: Document Jensen-Shannon distance being accepted by cdist/pdist
* `#14079 <https://github.com/scipy/scipy/pull/14079>`__: BLD: Avoid importing scipy.stats during cythonize stage
* `#14082 <https://github.com/scipy/scipy/pull/14082>`__: MAINT: Remove old, commented extract_diagonal
* `#14083 <https://github.com/scipy/scipy/pull/14083>`__: MAINT: sparse: Remove defunct function extract_diagonal
* `#14085 <https://github.com/scipy/scipy/pull/14085>`__: ENH: Implement canberra distance in _distance_pybind
* `#14086 <https://github.com/scipy/scipy/pull/14086>`__: MAINT: Clear scipy namespace of entries better imported from...
* `#14088 <https://github.com/scipy/scipy/pull/14088>`__: Install Pythran from sources for python 3.10
* `#14092 <https://github.com/scipy/scipy/pull/14092>`__: BUG: Fixes issue with clang.
* `#14094 <https://github.com/scipy/scipy/pull/14094>`__: DOC: Correct the inconsistence definition of Default in class...
* `#14105 <https://github.com/scipy/scipy/pull/14105>`__: TST: stats: mannwhitneyu: check that mstats and stats mannwhitneyu...
* `#14106 <https://github.com/scipy/scipy/pull/14106>`__: DOC: stats.mstats: mannwhitneyu: the returned statistic is the...
* `#14107 <https://github.com/scipy/scipy/pull/14107>`__: ENH: stats: bootstrap: add \`vectorized\` parameter; automatically...
* `#14109 <https://github.com/scipy/scipy/pull/14109>`__: BUG: fix two issues in the fblas signature files
* `#14110 <https://github.com/scipy/scipy/pull/14110>`__: DOC: mailmap update
* `#14113 <https://github.com/scipy/scipy/pull/14113>`__: ENH: stats: bootstrap: add \`paired\` parameter
* `#14116 <https://github.com/scipy/scipy/pull/14116>`__: MAINT: fix deprecated Python C API usage in odr
* `#14118 <https://github.com/scipy/scipy/pull/14118>`__: DOC: 1.7.0 release notes
* `#14125 <https://github.com/scipy/scipy/pull/14125>`__: DOC: fix typo
* `#14126 <https://github.com/scipy/scipy/pull/14126>`__: ENH: stats: bootstrap: add \`batch\` parameter to control batch...
* `#14127 <https://github.com/scipy/scipy/pull/14127>`__: CI: upgrade pip in benchmarks CI run
* `#14130 <https://github.com/scipy/scipy/pull/14130>`__: BUG: Fix trust-constr report TypeError if verbose is set to 2...
* `#14133 <https://github.com/scipy/scipy/pull/14133>`__: MAINT: interpolate: raise NotImplementedError not ValueError
* `#14139 <https://github.com/scipy/scipy/pull/14139>`__: FIX/DOC: lsqr doctests print failure
* `#14145 <https://github.com/scipy/scipy/pull/14145>`__: MAINT: 1.7.x version pins ("backport")
* `#14146 <https://github.com/scipy/scipy/pull/14146>`__: MAINT: commit count if no tag
* `#14164 <https://github.com/scipy/scipy/pull/14164>`__: TST, BUG: fix rbf matrix value
* `#14166 <https://github.com/scipy/scipy/pull/14166>`__: CI, MAINT: restrictions on pre-release CI
* `#14171 <https://github.com/scipy/scipy/pull/14171>`__: TST: signal: Bump tolerances for a test of Gustafsson's...
* `#14175 <https://github.com/scipy/scipy/pull/14175>`__: TST: stats: Loosen tolerance in some binomtest tests.
* `#14182 <https://github.com/scipy/scipy/pull/14182>`__: MAINT: stats: Update ppcc_plot and ppcc_max docstring.
* `#14195 <https://github.com/scipy/scipy/pull/14195>`__: MAINT: download-wheels missing import
* `#14230 <https://github.com/scipy/scipy/pull/14230>`__: REL: stop shipping generated Cython sources in sdist

# ===== SOURCE: https://raw.githubusercontent.com/scipy/scipy/main/doc/source/release/1.8.0-notes.rst =====

=========================
SciPy 1.8.0 Release Notes
=========================

.. contents::

SciPy 1.8.0 is the culmination of 6 months of hard work. It contains
many new features, numerous bug-fixes, improved test coverage and better
documentation. There have been a number of deprecations and API changes
in this release, which are documented below. All users are encouraged to
upgrade to this release, as there are a large number of bug-fixes and
optimizations. Before upgrading, we recommend that users check that
their own code does not use deprecated SciPy functionality (to do so,
run your code with ``python -Wd`` and check for ``DeprecationWarning`` s).
Our development attention will now shift to bug-fix releases on the
1.8.x branch, and on adding new features on the master branch.

This release requires Python 3.8+ and NumPy 1.17.3 or greater.

For running on PyPy, PyPy3 6.0+ is required.


**************************
Highlights of this release
**************************

- A sparse array API has been added for early testing and feedback; this
  work is ongoing, and users should expect minor API refinements over
  the next few releases.
- The sparse SVD library PROPACK is now vendored with SciPy, and an interface
  is exposed via `scipy.sparse.svds` with ``solver='PROPACK'``. It is currently
  default-off due to potential issues on Windows that we aim to
  resolve in the next release, but can be optionally enabled at runtime for
  friendly testing with an environment variable setting of ``USE_PROPACK=1``.
- A new `scipy.stats.sampling` submodule that leverages the ``UNU.RAN`` C
  library to sample from arbitrary univariate non-uniform continuous and
  discrete distributions
- All namespaces that were private but happened to miss underscores in
  their names have been deprecated.


************
New features
************

`scipy.fft` improvements
========================

Added an ``orthogonalize=None`` parameter to the real transforms in `scipy.fft`
which controls whether the modified definition of DCT/DST is used without
changing the overall scaling.

`scipy.fft` backend registration is now smoother, operating with a single
registration call and no longer requiring a context manager.

`scipy.integrate` improvements
==============================

`scipy.integrate.quad_vec` introduces a new optional keyword-only argument,
``args``. ``args`` takes in a tuple of extra arguments if any (default is
``args=()``), which is then internally used to pass into the callable function
(needing these extra arguments) which we wish to integrate.

`scipy.interpolate` improvements
================================

`scipy.interpolate.BSpline` has a new method, ``design_matrix``, which
constructs a design matrix of b-splines in the sparse CSR format.

A new method ``from_cubic`` in ``BSpline`` class allows to convert a
``CubicSpline`` object to ``BSpline`` object.

`scipy.linalg` improvements
===========================

`scipy.linalg` gained three new public array structure investigation functions.
`scipy.linalg.bandwidth` returns information about the bandedness of an array
and can be used to test for triangular structure discovery, while
`scipy.linalg.issymmetric` and `scipy.linalg.ishermitian` test the array for
exact and approximate symmetric/Hermitian structure.

`scipy.optimize` improvements
=============================

`scipy.optimize.check_grad` introduces two new optional keyword only arguments,
``direction`` and ``seed``. ``direction`` can take values, ``'all'`` (default),
in which case all the one hot direction vectors will be used for verifying
the input analytical gradient function and ``'random'``, in which case a
random direction vector will be used for the same purpose. ``seed``
(default is ``None``) can be used for reproducing the return value of
``check_grad`` function. It will be used only when ``direction='random'``.

The `scipy.optimize.minimize` ``TNC`` method has been rewritten to use Cython
bindings. This also fixes an issue with the callback altering the state of the
optimization.

Added optional parameters ``target_accept_rate`` and ``stepwise_factor`` for
adapative step size adjustment in ``basinhopping``.

The ``epsilon`` argument to ``approx_fprime`` is now optional so that it may
have a default value consistent with most other functions in `scipy.optimize`.

`scipy.signal` improvements
===========================

Add ``analog`` argument, default ``False``, to ``zpk2sos``, and add new pairing
option ``'minimal'`` to construct analog and minimal discrete SOS arrays.
``tf2sos`` uses zpk2sos; add ``analog`` argument here as well, and pass it on
to ``zpk2sos``.

``savgol_coeffs`` and ``savgol_filter`` now work for even window lengths.

Added the Chirp Z-transform and Zoom FFT available as `scipy.signal.CZT` and
`scipy.signal.ZoomFFT`.

`scipy.sparse` improvements
===========================

An array API has been added for early testing and feedback; this
work is ongoing, and users should expect minor API refinements over
the next few releases. Please refer to the `scipy.sparse`
docstring for more information.

``maximum_flow`` introduces optional keyword only argument, ``method``
which accepts either, ``'edmonds-karp'`` (Edmonds Karp algorithm) or
``'dinic'`` (Dinic's algorithm). Moreover, ``'dinic'`` is used as default
value for ``method`` which means that Dinic's algorithm is used for computing
maximum flow unless specified. See, the comparison between the supported
algorithms in
`this comment <https://github.com/scipy/scipy/pull/14358#issue-684212523>`_.

Parameters ``atol``, ``btol`` now default to 1e-6 in
`scipy.sparse.linalg.lsmr` to match with default values in
`scipy.sparse.linalg.lsqr`.

Add the Transpose-Free Quasi-Minimal Residual algorithm (TFQMR) for general
nonsingular non-Hermitian linear systems in `scipy.sparse.linalg.tfqmr`.

The sparse SVD library PROPACK is now vendored with SciPy, and an interface is
exposed via `scipy.sparse.svds` with ``solver='PROPACK'``. For some problems,
this may be faster and/or more accurate than the default, ARPACK. PROPACK
functionality is currently opt-in--you must specify ``USE_PROPACK=1`` at
runtime to use it due to potential issues on Windows
that we aim to resolve in the next release.

``sparse.linalg`` iterative solvers now have a nonzero initial guess option,
which may be specified as ``x0 = 'Mb'``.

The ``trace`` method has been added for sparse matrices.

`scipy.spatial` improvements
============================

`scipy.spatial.transform.Rotation` now supports item assignment and has a new
``concatenate`` method.

Add `scipy.spatial.distance.kulczynski1` in favour of
``scipy.spatial.distance.kulsinski`` which will be deprecated in the next
release.

`scipy.spatial.distance.minkowski` now also supports ``0<p<1``.

`scipy.special` improvements
============================

The new function `scipy.special.log_expit` computes the logarithm of the
logistic sigmoid function. The function is formulated to provide accurate
results for large positive and negative inputs, so it avoids the problems
that would occur in the naive implementation ``log(expit(x))``.

A suite of five new functions for elliptic integrals:
``scipy.special.ellipr{c,d,f,g,j}``. These are the
`Carlson symmetric elliptic integrals <https://dlmf.nist.gov/19.16>`_, which
have computational advantages over the classical Legendre integrals. Previous
versions included some elliptic integrals from the Cephes library
(``scipy.special.ellip{k,km1,kinc,e,einc}``) but was missing the integral of
third kind (Legendre's Pi), which can be evaluated using the new Carlson
functions. The new Carlson elliptic integral functions can be evaluated in the
complex plane, whereas the Cephes library's functions are only defined for
real inputs.

Several defects in `scipy.special.hyp2f1` have been corrected. Approximately
correct values are now returned for ``z`` near ``exp(+-i*pi/3)``, fixing
`#8054 <https://github.com/scipy/scipy/issues/8054>`_. Evaluation for such ``z``
is now calculated through a series derived by
`López and Temme (2013) <https://arxiv.org/abs/1306.2046>`_ that converges in
these regions. In addition, degenerate cases with one or more of ``a``, ``b``,
and/or ``c`` a non-positive integer are now handled in a manner consistent with
`mpmath's hyp2f1 implementation <https://mpmath.org/doc/current/functions/hypergeometric.html>`_,
which fixes `#7340 <https://github.com/scipy/scipy/issues/7340>`_. These fixes
were made as part of an effort to rewrite the Fortran 77 implementation of
hyp2f1 in Cython piece by piece. This rewriting is now roughly 50% complete.

`scipy.stats` improvements
==========================

`scipy.stats.qmc.LatinHypercube` introduces two new optional keyword-only
arguments, ``optimization`` and ``strength``. ``optimization`` is either
``None`` or ``random-cd``. In the latter, random permutations are performed to
improve the centered discrepancy. ``strength`` is either 1 or 2. 1 corresponds
to the classical LHS while 2 has better sub-projection properties. This
construction is referred to as an orthogonal array based LHS of strength 2.
In both cases, the output is still a LHS.

`scipy.stats.qmc.Halton` is faster as the underlying Van der Corput sequence
was ported to Cython.

The ``alternative`` parameter was added to the ``kendalltau`` and ``somersd``
functions to allow one-sided hypothesis testing. Similarly, the masked
versions of ``skewtest``, ``kurtosistest``, ``ttest_1samp``, ``ttest_ind``,
and ``ttest_rel`` now also have an ``alternative`` parameter.

Add `scipy.stats.gzscore` to calculate the geometrical z score.

Random variate generators to sample from arbitrary univariate non-uniform
continuous and discrete distributions have been added to the new
`scipy.stats.sampling` submodule. Implementations of a C library
`UNU.RAN <http://statmath.wu.ac.at/software/unuran/>`_ are used for
performance. The generators added are:

- TransformedDensityRejection
- DiscreteAliasUrn
- NumericalInversePolynomial
- DiscreteGuideTable
- SimpleRatioUniforms

The ``binned_statistic`` set of functions now have improved performance for
the ``std``, ``min``, ``max``, and ``median`` statistic calculations.

``somersd`` and ``_tau_b`` now have faster Pythran-based implementations.

Some general efficiency improvements to handling of ``nan`` values in
several ``stats`` functions.

Added the Tukey-Kramer test as `scipy.stats.tukey_hsd`.

Improved performance of `scipy.stats.argus` ``rvs`` method.

Added the parameter ``keepdims`` to `scipy.stats.variation` and prevent the
undesirable return of a masked array from the function in some cases.

``permutation_test`` performs an exact or randomized permutation test of a
given statistic on provided data.

*******************
Deprecated features
*******************

Clear split between public and private API
==========================================

SciPy has always documented what its public API consisted of in
:ref:`its API reference docs <scipy-api>`,
however there never was a clear split between public and
private namespaces in the code base. In this release, all namespaces that were
private but happened to miss underscores in their names have been deprecated.
These include (as examples, there are many more):

- ``scipy.signal.spline``
- ``scipy.ndimage.filters``
- ``scipy.ndimage.fourier``
- ``scipy.ndimage.measurements``
- ``scipy.ndimage.morphology``
- ``scipy.ndimage.interpolation``
- ``scipy.sparse.linalg.solve``
- ``scipy.sparse.linalg.eigen``
- ``scipy.sparse.linalg.isolve``

All functions and other objects in these namespaces that were meant to be
public are accessible from their respective public namespace (e.g.
`scipy.signal`). The design principle is that any public object must be
accessible from a single namespace only; there are a few exceptions, mostly for
historical reasons (e.g., ``stats`` and ``stats.distributions`` overlap).
For other libraries aiming to provide a SciPy-compatible API, it is now
unambiguous what namespace structure to follow.  See
`gh-14360 <https://github.com/scipy/scipy/issues/14360>`_ for more details.

Other deprecations
==================

``NumericalInverseHermite`` has been deprecated from `scipy.stats` and moved
to the `scipy.stats.sampling` submodule. It now uses the C implementation of
the UNU.RAN library so the result of methods like ``ppf`` may vary slightly.
Parameter ``tol`` has been deprecated and renamed to ``u_resolution``. The
parameter ``max_intervals`` has also been deprecated and will be removed in a
future release of SciPy.


******************************
Backwards incompatible changes
******************************

- SciPy has raised the minimum compiler versions to GCC 6.3 on linux and
  VS2019 on windows. In particular, this means that SciPy may now use C99 and
  C++14 features. For more details see
  `here <https://docs.scipy.org/doc/scipy/reference/dev/toolchain.html>`_.
- The result for empty bins for `scipy.stats.binned_statistic` with the builtin
  ``'std'`` metric is now ``nan``, for consistency with ``np.std``.
- The function `scipy.spatial.distance.wminkowski` has been removed. To achieve
  the same results as before, please use the ``minkowski`` distance function
  with the (optional) ``w=`` keyword-argument for the given weight.

*************
Other changes
*************

Some Fortran 77 code was modernized to be compatible with NAG's nagfor Fortran
compiler (see, e.g., `PR 13229 <https://github.com/scipy/scipy/pull/13229>`_).

``threadpoolctl`` may now be used by our test suite to substantially improve
the efficiency of parallel test suite runs.

*******
Authors
*******

* @endolith
* adamadanandy +
* akeemlh +
* Anton Akhmerov
* Marvin Albert +
* alegresor +
* Andrew Annex +
* Pantelis Antonoudiou +
* Ross Barnowski +
* Christoph Baumgarten
* Stephen Becker +
* Nickolai Belakovski
* Peter Bell
* berberto +
* Georgii Bocharov +
* Evgeni Burovski
* Matthias Bussonnier
* CJ Carey
* Justin Charlong +
* Hood Chatham +
* Dennis Collaris +
* David Cottrell +
* cruyffturn +
* da-woods +
* Anirudh Dagar
* Tiger Du +
* Thomas Duvernay
* Dani El-Ayyass +
* Castedo Ellerman +
* Donnie Erb +
* Andreas Esders-Kopecky +
* Livio F +
* Isuru Fernando
* Evelyn Fitzgerald +
* Sara Fridovich-Keil +
* Mark E Fuller +
* Ralf Gommers
* Kevin Richard Green +
* guiweber +
* Nitish Gupta +
* h-vetinari
* Matt Haberland
* J. Hariharan +
* Charles Harris
* Jonathan Helgert +
* Trever Hines
* Nadav Horesh
* Ian Hunt-Isaak +
* ich +
* Itrimel +
* Jan-Hendrik Müller +
* Jebby993 +
* Yikun Jiang +
* Evan W Jones +
* Nathaniel Jones +
* Jeffrey Kelling +
* Malik Idrees Hasan Khan +
* Paul Kienzle 
* Sergey B Kirpichev
* Kadatatlu Kishore +
* Andrew Knyazev
* Ravin Kumar +
* Peter Mahler Larsen
* Eric Larson
* Antony Lee
* Gregory R. Lee
* Tim Leslie
* lezcano +
* Xingyu Liu
* Christian Lorentzen
* Lorenzo +
* Smit Lunagariya +
* Lv101Magikarp +
* Yair M +
* Cong Ma
* Lorenzo Maffioli +
* majiang +
* Brian McFee +
* Nicholas McKibben
* John Speed Meyers +
* millivolt9 +
* Jarrod Millman
* Harsh Mishra +
* Boaz Mohar +
* naelsondouglas +
* Andrew Nelson
* Nico Schlömer
* Thomas Nowotny +
* nullptr +
* Teddy Ort +
* Nick Papior
* ParticularMiner +
* Dima Pasechnik
* Tirth Patel
* Matti Picus
* Ilhan Polat
* Adrian Price-Whelan +
* Quentin Barthélemy +
* Sundar R +
* Judah Rand +
* Tyler Reddy
* Renal-Of-Loon +
* Frederic Renner +
* Pamphile Roy
* Bharath Saiguhan +
* Atsushi Sakai
* Eric Schanet +
* Sebastian Wallkötter
* serge-sans-paille
* Reshama Shaikh +
* Namami Shanker
* siddhantwahal +
* Walter Simson +
* Gagandeep Singh +
* Leo C. Stein +
* Albert Steppi
* Kai Striega
* Diana Sukhoverkhova
* Søren Fuglede Jørgensen
* Masayuki Takagi +
* Mike Taves
* Ben Thompson +
* Bas van Beek
* Jacob Vanderplas
* Dhruv Vats +
* H. Vetinari +
* Thomas Viehmann +
* Pauli Virtanen
* Vlad +
* Arthur Volant
* Samuel Wallan
* Stefan van der Walt
* Warren Weckesser
* Josh Wilson
* Haoyin Xu +
* Rory Yorke
* Egor Zemlyanoy
* Gang Zhao +
* 赵丰 (Zhao Feng) +

A total of 139 people contributed to this release.
People with a "+" by their names contributed a patch for the first time.
This list of names is automatically generated, and may not be fully complete.


***********************
Issues closed for 1.8.0
***********************

* `#592 <https://github.com/scipy/scipy/issues/592>`__: Statistics Review: variation (Trac #65)
* `#857 <https://github.com/scipy/scipy/issues/857>`__: A Wrapper for PROPACK (Trac #330)
* `#2009 <https://github.com/scipy/scipy/issues/2009>`__: "Kulsinski" dissimilarity seems wrong (Trac #1484)
* `#2063 <https://github.com/scipy/scipy/issues/2063>`__: callback functions for COBYLA and TNC (Trac #1538)
* `#2358 <https://github.com/scipy/scipy/issues/2358>`__: ndimage.center_of_mass doesnt return all for all labelled objects...
* `#5668 <https://github.com/scipy/scipy/issues/5668>`__: Need zpk2sos for analog filters
* `#7340 <https://github.com/scipy/scipy/issues/7340>`__: SciPy Hypergeometric function hyp2f1 producing infinities
* `#8774 <https://github.com/scipy/scipy/issues/8774>`__: In \`optimize.basinhopping\`, the target acceptance rate should...
* `#10497 <https://github.com/scipy/scipy/issues/10497>`__: scipy.sparse.csc_matrix.toarray docstring is wrong
* `#10888 <https://github.com/scipy/scipy/issues/10888>`__: Check finite difference gradient approximation in a random direction
* `#10974 <https://github.com/scipy/scipy/issues/10974>`__: Non explicit error message in lobpcg
* `#11452 <https://github.com/scipy/scipy/issues/11452>`__: Normalisation requirement for \`Wn\` unclear in \`scipy.signal.butter\`
* `#11700 <https://github.com/scipy/scipy/issues/11700>`__: solve_ivp errors out instead of simply quitting after the solve...
* `#12006 <https://github.com/scipy/scipy/issues/12006>`__: newton: Shouldn't it take a Jacobian for multivariate problems...
* `#12100 <https://github.com/scipy/scipy/issues/12100>`__: solve_ivp: custom t_eval list and the terminating event
* `#12106 <https://github.com/scipy/scipy/issues/12106>`__: \`axis\` option for \`stats.tmean\` do not appear to be working...
* `#12192 <https://github.com/scipy/scipy/issues/12192>`__: \`scipy.stats.rv_continuous.moment\` does not accept array input
* `#12502 <https://github.com/scipy/scipy/issues/12502>`__: Divide by zero in Jacobian numerical differentiation when equality...
* `#12981 <https://github.com/scipy/scipy/issues/12981>`__: SLSQP constrained minimization error in 1.5.2
* `#12999 <https://github.com/scipy/scipy/issues/12999>`__: Bug in scipy.stats.ks_2samp for two-sided auto and exact modes...
* `#13402 <https://github.com/scipy/scipy/issues/13402>`__: ENH: Faster Max Flow algorithm in scipy.sparse.csgraph
* `#13580 <https://github.com/scipy/scipy/issues/13580>`__: truncnorm gives incorrect means and variances
* `#13642 <https://github.com/scipy/scipy/issues/13642>`__: stats.truncnorm variance works incorrectly when input is an array.
* `#13659 <https://github.com/scipy/scipy/issues/13659>`__: Orthogonal Array for Latin hypercube in \`scipy.stats.qmc\`
* `#13737 <https://github.com/scipy/scipy/issues/13737>`__: brentq can overflow / underflow
* `#13745 <https://github.com/scipy/scipy/issues/13745>`__: different default atol, btol for lsqr, lsmr
* `#13898 <https://github.com/scipy/scipy/issues/13898>`__: Savitzky-Golay filter for even number data
* `#13902 <https://github.com/scipy/scipy/issues/13902>`__: Different solvers of \`svds\` return quite different results
* `#13922 <https://github.com/scipy/scipy/issues/13922>`__: Need Exception / Error for Incorrect and/or misleading analog...
* `#14122 <https://github.com/scipy/scipy/issues/14122>`__: Item assignement for spatial.transform.Rotation objects
* `#14140 <https://github.com/scipy/scipy/issues/14140>`__: Likely unnecessary invalid value warning from PchipInterpolator
* `#14152 <https://github.com/scipy/scipy/issues/14152>`__: zpk2sos not working correctly when butterworth band-pass filter...
* `#14165 <https://github.com/scipy/scipy/issues/14165>`__: scipy.optimize.minimize method='Nelder-Mead': 'maxfev' is not...
* `#14168 <https://github.com/scipy/scipy/issues/14168>`__: Missing "inverse" word in the multidimensional Discrete Cosine/Sine...
* `#14189 <https://github.com/scipy/scipy/issues/14189>`__: Incorrect shape handling in \`scipy.stat.multivariate_t.rvs\`...
* `#14190 <https://github.com/scipy/scipy/issues/14190>`__: Links in documentation of Dirichlet distribution are a mess
* `#14193 <https://github.com/scipy/scipy/issues/14193>`__: Implementation of scrambled Van der Corput sequence differs from...
* `#14217 <https://github.com/scipy/scipy/issues/14217>`__: Error in documentation for \`scipy.stats.gaussian_kde.factor\`
* `#14235 <https://github.com/scipy/scipy/issues/14235>`__: Should this be $y$ only, instead of $m_y$?
* `#14236 <https://github.com/scipy/scipy/issues/14236>`__: BUG: discrete isf is wrong at boundary if loc != 0
* `#14277 <https://github.com/scipy/scipy/issues/14277>`__: Broken reference in docstring of scipy.stats.power_divergence
* `#14324 <https://github.com/scipy/scipy/issues/14324>`__: BUG: scipy.stats.theilslopes intercept calculation can produce...
* `#14332 <https://github.com/scipy/scipy/issues/14332>`__: Strange output of \`binned_statistic_dd\` with \`statistic=sum\`
* `#14340 <https://github.com/scipy/scipy/issues/14340>`__: Initialize Rotation using list or array of Rotations
* `#14346 <https://github.com/scipy/scipy/issues/14346>`__: scipy.stats.rv_continuous.fit returns wrapper instead of fit...
* `#14360 <https://github.com/scipy/scipy/issues/14360>`__: Making clearer what namespaces are public by use of underscores
* `#14385 <https://github.com/scipy/scipy/issues/14385>`__: csgraph.maximum_flow can cause Python crash for large but very...
* `#14409 <https://github.com/scipy/scipy/issues/14409>`__: Lagrange polynomials and numpy Polynomials
* `#14412 <https://github.com/scipy/scipy/issues/14412>`__: Extra function arguments to \`scipy.integrate.quad_vec\`
* `#14416 <https://github.com/scipy/scipy/issues/14416>`__: Is the r-value outputted by scipy.stats.linregress always the...
* `#14420 <https://github.com/scipy/scipy/issues/14420>`__: BUG: RBFInterpolator fails when calling it with a slice of a...
* `#14425 <https://github.com/scipy/scipy/issues/14425>`__: Running tests in parallel is not any faster than without pytest-xdist...
* `#14445 <https://github.com/scipy/scipy/issues/14445>`__: BUG: out of bounds indexing issue in \`prini.f\`
* `#14482 <https://github.com/scipy/scipy/issues/14482>`__: Azure CI jobs do not set exit status for build stage correctly
* `#14491 <https://github.com/scipy/scipy/issues/14491>`__: MAINT: Replace np.rollaxis with np.moveaxis
* `#14501 <https://github.com/scipy/scipy/issues/14501>`__: runtests.py overrides \`$PYTHONPATH\`
* `#14514 <https://github.com/scipy/scipy/issues/14514>`__: linprog kwargs not recognised
* `#14529 <https://github.com/scipy/scipy/issues/14529>`__: CI: Azure pipelines don't appear to be running
* `#14535 <https://github.com/scipy/scipy/issues/14535>`__: hess option does not work in minimize function
* `#14551 <https://github.com/scipy/scipy/issues/14551>`__: Cannot create Compressed sparse column matrix of shape N x N-2
* `#14568 <https://github.com/scipy/scipy/issues/14568>`__: \`stats.norminvgauss\` incorrect implementation?
* `#14585 <https://github.com/scipy/scipy/issues/14585>`__: DOC: toolchain updates and max Python
* `#14607 <https://github.com/scipy/scipy/issues/14607>`__: scipy.sparse.linalg.inv cannot take ndarray as argument despite...
* `#14608 <https://github.com/scipy/scipy/issues/14608>`__: BUG: scipy.stats.multivariate_t distribution math documentation
* `#14623 <https://github.com/scipy/scipy/issues/14623>`__: BUG: Error constructing sparse matrix with indices larger than...
* `#14654 <https://github.com/scipy/scipy/issues/14654>`__: DOC: Linux Devdocs workflow requires installing packages that...
* `#14680 <https://github.com/scipy/scipy/issues/14680>`__: BUG: misleading documentation in scipy.stats.entropy
* `#14683 <https://github.com/scipy/scipy/issues/14683>`__: DOC: OptimizeResult Notes are placed before attribute section,...
* `#14733 <https://github.com/scipy/scipy/issues/14733>`__: BUG: resample_poly does not preserve dtype
* `#14746 <https://github.com/scipy/scipy/issues/14746>`__: site.cfg: [ALL] or [DEFAULT]?
* `#14770 <https://github.com/scipy/scipy/issues/14770>`__: BUG: lpmn ref broken link
* `#14807 <https://github.com/scipy/scipy/issues/14807>`__: BUG: wrong weights of the 7-point gauss rule in QUADPACK: dqk15w.f
* `#14830 <https://github.com/scipy/scipy/issues/14830>`__: do CDF inversion methods have to be public?
* `#14859 <https://github.com/scipy/scipy/issues/14859>`__: BUG: constraint function is overwritten when equal bounds are...
* `#14873 <https://github.com/scipy/scipy/issues/14873>`__: ENH: get the driver used in scipy.linalg.eigh
* `#14879 <https://github.com/scipy/scipy/issues/14879>`__: BUG: TNC output is different if a callback is used.
* `#14891 <https://github.com/scipy/scipy/issues/14891>`__: DOC: \`directed_hausdorff\` expects 2D array despite docs stating...
* `#14910 <https://github.com/scipy/scipy/issues/14910>`__: \`stats.contingency\` not listed as public API
* `#14911 <https://github.com/scipy/scipy/issues/14911>`__: MAINT, DOC: CI failure for doc building
* `#14942 <https://github.com/scipy/scipy/issues/14942>`__: DOC: Ambiguous command instruction for running tests in Mac docs
* `#14968 <https://github.com/scipy/scipy/issues/14968>`__: Debug build CI job crashes on \`stats._unuran\` threading test
* `#14984 <https://github.com/scipy/scipy/issues/14984>`__: BUG: scipy.sparse.linalg.spsolve: runtime memory error caused...
* `#14987 <https://github.com/scipy/scipy/issues/14987>`__: ENH: The knot interval lookup for BSpline.design_matrix is inefficient
* `#15025 <https://github.com/scipy/scipy/issues/15025>`__: Might be j<=i+k?
* `#15033 <https://github.com/scipy/scipy/issues/15033>`__: BUG: scipy.fft.dct type I with norm = "ortho" leads to wrong...
* `#15051 <https://github.com/scipy/scipy/issues/15051>`__: BUG: test failures on aarch in wheel builder repo
* `#15064 <https://github.com/scipy/scipy/issues/15064>`__: MAINT: \`interpolation\` keyword is renamed to \`method\` in...
* `#15103 <https://github.com/scipy/scipy/issues/15103>`__: BUG: scipy.stats.chi.mean returns nan for large df due to use...
* `#15186 <https://github.com/scipy/scipy/issues/15186>`__: Fix use of \`pytest.warns(None)\` for pytest 7.0.0
* `#15206 <https://github.com/scipy/scipy/issues/15206>`__: BUG: Minor issue with suggestions in scipy.sparse DeprecationWarnings...
* `#15224 <https://github.com/scipy/scipy/issues/15224>`__: BUG: 0th power of sparse array/matrix always returns the identity...
* `#15228 <https://github.com/scipy/scipy/issues/15228>`__: BUG: bounded L-BFGS-B doesn't work with a scalar.
* `#15254 <https://github.com/scipy/scipy/issues/15254>`__: BUG: \`DeprecationWarning: distutils Version classes are deprecated\`
* `#15267 <https://github.com/scipy/scipy/issues/15267>`__: Windows CI jobs have a build issue with Pythran 0.11
* `#15276 <https://github.com/scipy/scipy/issues/15276>`__: Boost and PROPACK git submodules are too easy to commit changes...
* `#15316 <https://github.com/scipy/scipy/issues/15316>`__: BUG: Failed to install scipy 1.7.x with pypy 3.7 in aarch64
* `#15339 <https://github.com/scipy/scipy/issues/15339>`__: BUG: \`highs-ds\` returns memoryviews instead of np.arrays for...
* `#15375 <https://github.com/scipy/scipy/issues/15375>`__: BUG: axis argument to scipy.stats.mode does not accept negative...
* `#15517 <https://github.com/scipy/scipy/issues/15517>`__: BUG: Link to mailing list seems broken

***********************
Pull requests for 1.8.0
***********************

* `#4607 <https://github.com/scipy/scipy/pull/4607>`__: Add Chirp Z-transform, zoom FFT
* `#10504 <https://github.com/scipy/scipy/pull/10504>`__: ENH: Carlson symmetric elliptic integrals.
* `#11263 <https://github.com/scipy/scipy/pull/11263>`__: MAINT:optimize: Comply with user-specified rel_step
* `#11754 <https://github.com/scipy/scipy/pull/11754>`__: ENH: stats: Updates to \`variation\`.
* `#11954 <https://github.com/scipy/scipy/pull/11954>`__: ENH: improve ARGUS rv generation in scipy.stats
* `#12143 <https://github.com/scipy/scipy/pull/12143>`__: BUG: Correctly use \`axis\` in \`scipy.stats.tmean\`
* `#12146 <https://github.com/scipy/scipy/pull/12146>`__: DOC: add docs to explain behaviour of newton's mehod on arrays
* `#12197 <https://github.com/scipy/scipy/pull/12197>`__: BUG: fix moments method to support arrays and list
* `#12889 <https://github.com/scipy/scipy/pull/12889>`__: MAINT: deal with cases in \`minimize\` for \`(bounds.lb == bounds.ub).any()
* `#13002 <https://github.com/scipy/scipy/pull/13002>`__: ENH: stats: Tukey's honestly significant difference test
* `#13096 <https://github.com/scipy/scipy/pull/13096>`__: BUG: optimize: alternative fix for minimize issues with lb==ub
* `#13143 <https://github.com/scipy/scipy/pull/13143>`__: MAINT: deal with cases in \`minimize\` for \`(bounds.lb == bounds.ub).any()...
* `#13229 <https://github.com/scipy/scipy/pull/13229>`__: ENH: modernise some Fortran code, needed for nagfor compiler
* `#13312 <https://github.com/scipy/scipy/pull/13312>`__: ENH: stats: add \`axis\` and \`nan_policy\` parameters to functions...
* `#13347 <https://github.com/scipy/scipy/pull/13347>`__: CI: bump gcc from 4.8 to 5.x
* `#13392 <https://github.com/scipy/scipy/pull/13392>`__: MAINT: streamlined kwargs for minimizer in dual_annealing
* `#13419 <https://github.com/scipy/scipy/pull/13419>`__: BUG: Fix group delay singularity check
* `#13471 <https://github.com/scipy/scipy/pull/13471>`__: ENH: LHS based OptimalDesign (scipy.stats.qmc)
* `#13581 <https://github.com/scipy/scipy/pull/13581>`__: MAINT: stats: fix truncnorm stats with array shapes
* `#13839 <https://github.com/scipy/scipy/pull/13839>`__: MAINT: set same tolerance between LSMR and LSQR
* `#13864 <https://github.com/scipy/scipy/pull/13864>`__: Array scalar conversion deprecation
* `#13883 <https://github.com/scipy/scipy/pull/13883>`__: MAINT: move LSAP maximization handling into solver code
* `#13899 <https://github.com/scipy/scipy/pull/13899>`__: ENH: stats: add general permutation hypothesis test
* `#13921 <https://github.com/scipy/scipy/pull/13921>`__: BUG: optimize: fix max function call validation for \`minimize\`...
* `#13958 <https://github.com/scipy/scipy/pull/13958>`__: ENH: stats: add \`alternative\` to masked version of T-Tests
* `#13960 <https://github.com/scipy/scipy/pull/13960>`__: ENH: stats: add \`alternative\` to masked normality tests
* `#14007 <https://github.com/scipy/scipy/pull/14007>`__: BUG: Fix root bracketing logic in Brent's method (issue #13737)
* `#14024 <https://github.com/scipy/scipy/pull/14024>`__: ENH: Add annotations for \`scipy.spatial.cKDTree\`
* `#14049 <https://github.com/scipy/scipy/pull/14049>`__: MAINT: Change special.orthogonal.orthopoly1d type hints to ArrayLike
* `#14132 <https://github.com/scipy/scipy/pull/14132>`__: DOC: badge with version of the doc in the navbar
* `#14144 <https://github.com/scipy/scipy/pull/14144>`__: REL: set version to 1.8.0.dev0
* `#14151 <https://github.com/scipy/scipy/pull/14151>`__: BLD: update pyproject.toml - add macOS M1, drop py36
* `#14153 <https://github.com/scipy/scipy/pull/14153>`__: BUG: stats: Implementing boost's hypergeometric distribution...
* `#14160 <https://github.com/scipy/scipy/pull/14160>`__: ENH: sparse.linalg: Add TFQMR algorithm for non-Hermitian sparse...
* `#14163 <https://github.com/scipy/scipy/pull/14163>`__: BENCH: add benchmark for energy_distance and wasserstein_distance
* `#14173 <https://github.com/scipy/scipy/pull/14173>`__: BUG: Fixed an issue wherein \`geometric_slerp\` would return...
* `#14174 <https://github.com/scipy/scipy/pull/14174>`__: ENH: Add annotations to \`scipy.spatial.geometric_slerp\`
* `#14183 <https://github.com/scipy/scipy/pull/14183>`__: DOC: add examples/ update mstats doc of pearsonr in scipy.stats
* `#14186 <https://github.com/scipy/scipy/pull/14186>`__: TST, MAINT: hausdorff test cleanups
* `#14187 <https://github.com/scipy/scipy/pull/14187>`__: DOC: interpolate: rbf has kwargs too.
* `#14191 <https://github.com/scipy/scipy/pull/14191>`__: MAINT:TST:linalg modernize the test assertions
* `#14192 <https://github.com/scipy/scipy/pull/14192>`__: BUG: stats: fix shape handing in multivariate_t.rvs
* `#14197 <https://github.com/scipy/scipy/pull/14197>`__: CI: azure: Fix handling of 'skip azp'.
* `#14200 <https://github.com/scipy/scipy/pull/14200>`__: DOC: Remove link to alpha in scipy.stats.dirichlet
* `#14201 <https://github.com/scipy/scipy/pull/14201>`__: TST: cleanup in lsqr and lsmr tests
* `#14204 <https://github.com/scipy/scipy/pull/14204>`__: Improve error message for index dimension
* `#14208 <https://github.com/scipy/scipy/pull/14208>`__: MAINT: add invalid='ignore' to np.errstate block in PchipInterpolator
* `#14209 <https://github.com/scipy/scipy/pull/14209>`__: ENH: stats: kendalltau: add alternative parameter
* `#14210 <https://github.com/scipy/scipy/pull/14210>`__: BUG: Fix Nelder-Mead logic when using a non-1D x0 and adapative
* `#14211 <https://github.com/scipy/scipy/pull/14211>`__: Fixed doc for gaussian_kde (kde.factor description)
* `#14213 <https://github.com/scipy/scipy/pull/14213>`__: ENH: stats: somersd: add alternative parameter
* `#14214 <https://github.com/scipy/scipy/pull/14214>`__: ENH: Improve the \`scipy.spatial.qhull\` annotations
* `#14215 <https://github.com/scipy/scipy/pull/14215>`__: ENH: stats: Integrate library UNU.RAN in \`scipy.stats\` [GSoC...
* `#14218 <https://github.com/scipy/scipy/pull/14218>`__: DOC: clarify \`ndimage.center_of_mass\` docstring
* `#14219 <https://github.com/scipy/scipy/pull/14219>`__: ENH: sparse.linalg: Use the faster "sqrt" from "math" and be...
* `#14222 <https://github.com/scipy/scipy/pull/14222>`__: MAINT: stats: remove unused 'type: ignore' comment
* `#14224 <https://github.com/scipy/scipy/pull/14224>`__: MAINT: Modify to use new random API in benchmarks
* `#14225 <https://github.com/scipy/scipy/pull/14225>`__: MAINT: fix missing LowLevelCallable in \`dir(scipy)\`
* `#14226 <https://github.com/scipy/scipy/pull/14226>`__: BLD: fix warning for missing dependency, and dev version number
* `#14227 <https://github.com/scipy/scipy/pull/14227>`__: MAINT: fix maybe-uninitialized warnings in lbfgbf.f
* `#14228 <https://github.com/scipy/scipy/pull/14228>`__: BENCH: add more benchmarks for inferential statistics tests
* `#14237 <https://github.com/scipy/scipy/pull/14237>`__: Removes unused variable
* `#14240 <https://github.com/scipy/scipy/pull/14240>`__: ENH: sparse.linalg: Normalize type descriptions
* `#14242 <https://github.com/scipy/scipy/pull/14242>`__: BUG: stats: fix discrete \`.isf\` to work at boundaries when...
* `#14250 <https://github.com/scipy/scipy/pull/14250>`__: Error in parameter checking in cdfbin.f
* `#14254 <https://github.com/scipy/scipy/pull/14254>`__: BUG: Fixed an issue wherein \`SphericalVoronoi\` could raise...
* `#14255 <https://github.com/scipy/scipy/pull/14255>`__: BUG: Numerical stability for large N BarycentricInterpolator
* `#14257 <https://github.com/scipy/scipy/pull/14257>`__: MAINT: Fixed deprecated API calls in scipy.optimize
* `#14258 <https://github.com/scipy/scipy/pull/14258>`__: DOC: fix stats.pearsonr example that was failing in CI
* `#14259 <https://github.com/scipy/scipy/pull/14259>`__: CI: pin mypy to 0.902 and fix one CI failure
* `#14260 <https://github.com/scipy/scipy/pull/14260>`__: BLD: optimize: fix some warnings in moduleTNC and minpack.h
* `#14261 <https://github.com/scipy/scipy/pull/14261>`__: BLD: fix include order and build warnings for \`optimize/_trlib\`
* `#14263 <https://github.com/scipy/scipy/pull/14263>`__: DOC: forward port 1.7.0 relnotes
* `#14268 <https://github.com/scipy/scipy/pull/14268>`__: MAINT: Replaced direct field access in PyArrayObject\* with wrapper...
* `#14274 <https://github.com/scipy/scipy/pull/14274>`__: MAINT: more scalar array conversion fixes for optimize
* `#14275 <https://github.com/scipy/scipy/pull/14275>`__: MAINT: Update vendored uarray, required for auto-dispatching
* `#14278 <https://github.com/scipy/scipy/pull/14278>`__: MAINT: two small fixes for implicit scalar-array-conversions
* `#14281 <https://github.com/scipy/scipy/pull/14281>`__: ENH: Annotate the array dtypes of \`scipy.spatial.qhull\`
* `#14285 <https://github.com/scipy/scipy/pull/14285>`__: DEV: remove scikit-umfpack from environment.yml
* `#14287 <https://github.com/scipy/scipy/pull/14287>`__: TST: Add testing for hyp2f1 for complex values in anticipation...
* `#14291 <https://github.com/scipy/scipy/pull/14291>`__: TST: split combined LSAP input validation tests up
* `#14293 <https://github.com/scipy/scipy/pull/14293>`__: MAINT: remove the last deprecated \`PyEval_\*\` usages
* `#14294 <https://github.com/scipy/scipy/pull/14294>`__: ENH: Annotate array dtypes in \`scipy.spatial.ckdtree\` and \`distance\`
* `#14295 <https://github.com/scipy/scipy/pull/14295>`__: MAINT: move LSAP input validation into lsap_module
* `#14297 <https://github.com/scipy/scipy/pull/14297>`__: DOC: Make code block an Item List
* `#14301 <https://github.com/scipy/scipy/pull/14301>`__: MAINT: fix the last build warning in \`optimize/_trlib/\`
* `#14302 <https://github.com/scipy/scipy/pull/14302>`__: BLD: fix build warnings for \`stats/biasedurn\`
* `#14305 <https://github.com/scipy/scipy/pull/14305>`__: MAINT: silence warning in odepackmodule.c
* `#14308 <https://github.com/scipy/scipy/pull/14308>`__: ENH: use Pythran to speedup somersd and _tau_b
* `#14309 <https://github.com/scipy/scipy/pull/14309>`__: BLD: fix build warnings for scipy.special
* `#14310 <https://github.com/scipy/scipy/pull/14310>`__: ENH: make epsilon optional in optimize.approx_fprime.
* `#14311 <https://github.com/scipy/scipy/pull/14311>`__: MAINT: Corrected NumPy API usage in scipy.spatial
* `#14312 <https://github.com/scipy/scipy/pull/14312>`__: ENH: Using random directional derivative to check grad
* `#14326 <https://github.com/scipy/scipy/pull/14326>`__: MAINT: Removed redifinition of trace1 in spatial/qhull
* `#14328 <https://github.com/scipy/scipy/pull/14328>`__: MAINT: _lib: add __dealloc__ to MessageStream
* `#14331 <https://github.com/scipy/scipy/pull/14331>`__: ENH: Complement \`trace\` method of sparse matrices like \`csr_matrix/csc_matrix/coo_matrix\`
* `#14338 <https://github.com/scipy/scipy/pull/14338>`__: BUG: fix \`stats.binned_statistic_dd\` issue with values close...
* `#14339 <https://github.com/scipy/scipy/pull/14339>`__: TST: fix \`sparse.linalg.spsolve\` test with singular input
* `#14341 <https://github.com/scipy/scipy/pull/14341>`__: MAINT: Add missing parenthesis in _nnls.py
* `#14342 <https://github.com/scipy/scipy/pull/14342>`__: ENH: make \`savgol_coeffs\`, \`savgol_filter\` work for even...
* `#14344 <https://github.com/scipy/scipy/pull/14344>`__: ENH: scipy.interpolate b-splines (design_matrix)
* `#14350 <https://github.com/scipy/scipy/pull/14350>`__: MAINT: make fit method of rv_continuous pickleable
* `#14358 <https://github.com/scipy/scipy/pull/14358>`__: ENH: Dinic's algorithm for maximum_flow
* `#14359 <https://github.com/scipy/scipy/pull/14359>`__: ENH: Set fft backend with try_last=True
* `#14362 <https://github.com/scipy/scipy/pull/14362>`__: Use list comprehension
* `#14367 <https://github.com/scipy/scipy/pull/14367>`__: BUG: Check for NULL pointer in \`memmove\`
* `#14377 <https://github.com/scipy/scipy/pull/14377>`__: Fix behavior of binary morphology with output=input when iterations=1
* `#14378 <https://github.com/scipy/scipy/pull/14378>`__: MAINT: Removing deprecated NumPy C API from \`interpolate\`
* `#14380 <https://github.com/scipy/scipy/pull/14380>`__: ENH: Fixed intercept computation in theilslopes
* `#14381 <https://github.com/scipy/scipy/pull/14381>`__: BENCH: add benchmark for somersd
* `#14387 <https://github.com/scipy/scipy/pull/14387>`__: MAINT: Removed deprecated NumPy C api from \`sparse\`
* `#14392 <https://github.com/scipy/scipy/pull/14392>`__: BUG/ENH: rework maximum flow preprocessing
* `#14393 <https://github.com/scipy/scipy/pull/14393>`__: CI: Lint checks failures are reporting success
* `#14403 <https://github.com/scipy/scipy/pull/14403>`__: Fix off by one error in doc string.
* `#14404 <https://github.com/scipy/scipy/pull/14404>`__: DOC: docstring fix for default of n param of interpolate.pade
* `#14406 <https://github.com/scipy/scipy/pull/14406>`__: MAINT: Use numpy_nodepr_api in \`spatial\`
* `#14411 <https://github.com/scipy/scipy/pull/14411>`__: MAINT: minor cleanups in usage of \`compute_uv\` keyword of \`svd\`
* `#14413 <https://github.com/scipy/scipy/pull/14413>`__: DOC:interpolate: Fix the docstring example of "lagrange"
* `#14419 <https://github.com/scipy/scipy/pull/14419>`__: DEP: deprecate private but non-underscored \`signal.spline\`...
* `#14422 <https://github.com/scipy/scipy/pull/14422>`__: MAINT: csgraph: change Dinic algorithm to iterative implementation
* `#14423 <https://github.com/scipy/scipy/pull/14423>`__: CI: remove printing of skipped and xfailed tests from Azure test...
* `#14426 <https://github.com/scipy/scipy/pull/14426>`__: ENH: Add args argument for callable in quad_vec
* `#14427 <https://github.com/scipy/scipy/pull/14427>`__: MAINT: extra pythran annotation for i686 support
* `#14432 <https://github.com/scipy/scipy/pull/14432>`__: BUG/ENH: more stable recursion for 2-sample ks test exact p-values
* `#14433 <https://github.com/scipy/scipy/pull/14433>`__: ENH: add PROPACK wrapper for improved sparse SVD
* `#14440 <https://github.com/scipy/scipy/pull/14440>`__: MAINT: stats: silence mypy complaints
* `#14441 <https://github.com/scipy/scipy/pull/14441>`__: ENH: TST: add a threadpoolctl hook to limit OpenBLAS parallelism
* `#14442 <https://github.com/scipy/scipy/pull/14442>`__: MAINT: Fix uninitialized warnings in \`sparse/linalg/dsolve\`
* `#14447 <https://github.com/scipy/scipy/pull/14447>`__: MAINT: rename scipy.ndimage modules
* `#14449 <https://github.com/scipy/scipy/pull/14449>`__: ENH: Cythonize van der corput
* `#14454 <https://github.com/scipy/scipy/pull/14454>`__: MAINT: Begin translation of hyp2f1 for complex numbers into Cython
* `#14456 <https://github.com/scipy/scipy/pull/14456>`__: CI: Lint with flake8 instead of pyflakes + pycodestyle
* `#14458 <https://github.com/scipy/scipy/pull/14458>`__: DOC: clarify meaning of rvalue in stats.linregress
* `#14459 <https://github.com/scipy/scipy/pull/14459>`__: MAINT: Fix uninitialized warnings in \`interpolate\` and \`cluster\`
* `#14463 <https://github.com/scipy/scipy/pull/14463>`__: Fix typo in doc overview: "pandas" to "SciPy"
* `#14474 <https://github.com/scipy/scipy/pull/14474>`__: DEP: Deprecate private but non-underscored ndimage.<module> namespace
* `#14477 <https://github.com/scipy/scipy/pull/14477>`__: MAINT: Using Tempita file for bspline (signal)
* `#14479 <https://github.com/scipy/scipy/pull/14479>`__: Added \`Inverse\` word in \`idstn\` and \`idctn\` docstrings
* `#14487 <https://github.com/scipy/scipy/pull/14487>`__: TST: modify flaky test for constrained minimization
* `#14489 <https://github.com/scipy/scipy/pull/14489>`__: MAINT: cleanup of some line_search code
* `#14492 <https://github.com/scipy/scipy/pull/14492>`__: CI: make sure Azure job step fails when building a SciPy wheel...
* `#14496 <https://github.com/scipy/scipy/pull/14496>`__: MAINT: switch to using spmatrix.toarray instead of .todense
* `#14499 <https://github.com/scipy/scipy/pull/14499>`__: DOC: fix toarray/todense docstring
* `#14507 <https://github.com/scipy/scipy/pull/14507>`__: CI: Add lint_diff docs & option to run only on specified files/dirs
* `#14513 <https://github.com/scipy/scipy/pull/14513>`__: DOC: added reference and example in jacobi docstring
* `#14520 <https://github.com/scipy/scipy/pull/14520>`__: BUG: diffev maxfun can be reached partway through population
* `#14524 <https://github.com/scipy/scipy/pull/14524>`__: ENH: Rotation.concatenate
* `#14532 <https://github.com/scipy/scipy/pull/14532>`__: ENH: sparse.linalg: The solution is zero when R.H.S. is zero
* `#14538 <https://github.com/scipy/scipy/pull/14538>`__: CI: Revert "CI: make sure Azure job step fails when building...
* `#14539 <https://github.com/scipy/scipy/pull/14539>`__: DOC: added chebyt and chebyu docstring examples in scipy.special
* `#14546 <https://github.com/scipy/scipy/pull/14546>`__: ENH: Orthogonal Latin Hypercube Sampling to QMC
* `#14547 <https://github.com/scipy/scipy/pull/14547>`__: ENH: __setitem__ method for Rotation class
* `#14549 <https://github.com/scipy/scipy/pull/14549>`__: Small test fixes for pypy + win + mmap
* `#14554 <https://github.com/scipy/scipy/pull/14554>`__: ENH: scipy.interpolate.BSpline from_power_basis
* `#14555 <https://github.com/scipy/scipy/pull/14555>`__: BUG: sparse: fix a DIA.tocsc bug
* `#14556 <https://github.com/scipy/scipy/pull/14556>`__: Fix the link to details of the strongly connected components...
* `#14559 <https://github.com/scipy/scipy/pull/14559>`__: WIP: TST: add tests for Pythran somersd
* `#14561 <https://github.com/scipy/scipy/pull/14561>`__: DOC: added reference and examples in (gen)laguerre docstring...
* `#14564 <https://github.com/scipy/scipy/pull/14564>`__: ENH: Add threaded Van Der Corput
* `#14571 <https://github.com/scipy/scipy/pull/14571>`__: Fix repeated word in _mannwhitneyu.py example
* `#14572 <https://github.com/scipy/scipy/pull/14572>`__: Set min length of the knot array for BSpline.design_matrix
* `#14578 <https://github.com/scipy/scipy/pull/14578>`__: DOC: added examples in spherical Bessel docstrings
* `#14581 <https://github.com/scipy/scipy/pull/14581>`__: MAINT: Refactor \`linalg.tests.test_interpolative::TestInterpolativeDecomposition::test_id\`
* `#14588 <https://github.com/scipy/scipy/pull/14588>`__: ENH: Added \`\`kulczynski1\`\` to \`\`scipy.spatial.distance\`\`
* `#14592 <https://github.com/scipy/scipy/pull/14592>`__: DOC: clarify parameters of norminvgauss in scipy.stats
* `#14595 <https://github.com/scipy/scipy/pull/14595>`__: Removing unused subroutines in \`\`scipy/linalg/src/id_dist/src/prini.f\`\`
* `#14601 <https://github.com/scipy/scipy/pull/14601>`__: Fixed inconsistencies between numpy and scipy interp
* `#14602 <https://github.com/scipy/scipy/pull/14602>`__: MAINT: Fix \`-Wunused-result\` warnings in \`sparse/linalg/dsolve\`
* `#14603 <https://github.com/scipy/scipy/pull/14603>`__: DEV: initialize all submodules in Gitpod Dockerfile
* `#14609 <https://github.com/scipy/scipy/pull/14609>`__: MAINT: Fix \`-Wmaybe-uninitialized\` warnings in \`optimize/_highs\`
* `#14610 <https://github.com/scipy/scipy/pull/14610>`__: MAINT: Ignored \`\`scipy/signal/bspline_util.c\`\`
* `#14613 <https://github.com/scipy/scipy/pull/14613>`__: MAINT: interpolate: Declare type for a Cython indexing variable.
* `#14619 <https://github.com/scipy/scipy/pull/14619>`__: ENH: stats.unuran: add Polynomial interpolation based numerical...
* `#14620 <https://github.com/scipy/scipy/pull/14620>`__: CI: fix Azure job which uses pre-release wheels + Python 3.7
* `#14625 <https://github.com/scipy/scipy/pull/14625>`__: ENH: optimize min max and median scipy.stats.binned_statistic
* `#14626 <https://github.com/scipy/scipy/pull/14626>`__: MAINT: fix type-narrowing addition in sparse.construct.bmat
* `#14627 <https://github.com/scipy/scipy/pull/14627>`__: MAINT: Bumped tolerances to pass \`\`special.tests\`\` on Apple...
* `#14628 <https://github.com/scipy/scipy/pull/14628>`__: DOC: clarify usage of options param in scipy.optimize.linprog
* `#14629 <https://github.com/scipy/scipy/pull/14629>`__: ENH: optimize std in scipy.stats.binned_statistic
* `#14630 <https://github.com/scipy/scipy/pull/14630>`__: DOC: add citation file
* `#14631 <https://github.com/scipy/scipy/pull/14631>`__: Fix unuran builds for older compilers
* `#14633 <https://github.com/scipy/scipy/pull/14633>`__: BUG: scipy.stats._unran: send only strings to include_dirs
* `#14634 <https://github.com/scipy/scipy/pull/14634>`__: DOC: Fix Wikipedia bootstrap link
* `#14635 <https://github.com/scipy/scipy/pull/14635>`__: DOC: stats: fix multivariate_t docs pdf eqn
* `#14637 <https://github.com/scipy/scipy/pull/14637>`__: MAINT: copy discrete dist dict
* `#14643 <https://github.com/scipy/scipy/pull/14643>`__: MAINT: address gh6019, disp for minimize_scalar
* `#14644 <https://github.com/scipy/scipy/pull/14644>`__: DOC: stats: add UNU.RAN references in the tutorial
* `#14649 <https://github.com/scipy/scipy/pull/14649>`__: DOC: clarify SciPy compatibility with Python and NumPy.
* `#14655 <https://github.com/scipy/scipy/pull/14655>`__: MAINT: remove support for Python 3.7 (hence NumPy 1.16)
* `#14656 <https://github.com/scipy/scipy/pull/14656>`__: MAINT: replacing ``assert_`` with assert
* `#14658 <https://github.com/scipy/scipy/pull/14658>`__: DOC: use conda-forge in Ubuntu quickstart
* `#14660 <https://github.com/scipy/scipy/pull/14660>`__: MAINT: refactor "for ... in range(len(" statements
* `#14663 <https://github.com/scipy/scipy/pull/14663>`__: MAINT: update leftover Python and NumPy version from pyproject.toml
* `#14665 <https://github.com/scipy/scipy/pull/14665>`__: BLD: fix confusing "import pip" failure that should be caught
* `#14666 <https://github.com/scipy/scipy/pull/14666>`__: MAINT: remove unnecessary seeding and update \`check_random_state\`
* `#14669 <https://github.com/scipy/scipy/pull/14669>`__: ENH: Refactor GitHub Issue form templates
* `#14673 <https://github.com/scipy/scipy/pull/14673>`__: BLD: fix include order, Python.h before standard headers
* `#14676 <https://github.com/scipy/scipy/pull/14676>`__: BUG: Fixes failing benchmark tests optimize_qap.QuadraticAssignment.track_score
* `#14677 <https://github.com/scipy/scipy/pull/14677>`__: MAINT: github labeler on file paths
* `#14682 <https://github.com/scipy/scipy/pull/14682>`__: DOC: Fix typo in mannwhitneyu docstring
* `#14684 <https://github.com/scipy/scipy/pull/14684>`__: DOC: optimize: fix sporadic linprog doctest failure
* `#14685 <https://github.com/scipy/scipy/pull/14685>`__: MAINT: static typing of entropy
* `#14686 <https://github.com/scipy/scipy/pull/14686>`__: BUG: fix issue in lsqr.py introduced in a recent commit
* `#14689 <https://github.com/scipy/scipy/pull/14689>`__: MAINT: replace IOError alias with OSError or other appropriate...
* `#14692 <https://github.com/scipy/scipy/pull/14692>`__: MAINT: Translation of hyp2f1 for complex numbers into Cython,...
* `#14693 <https://github.com/scipy/scipy/pull/14693>`__: DOC: update OptimizeResult notes
* `#14694 <https://github.com/scipy/scipy/pull/14694>`__: Simplify PythranBuildExt usage
* `#14695 <https://github.com/scipy/scipy/pull/14695>`__: BLD: bump Pythran version to 0.9.12
* `#14697 <https://github.com/scipy/scipy/pull/14697>`__: CI: add \`cffi\` in the benchmark CI job, and in environment.yml
* `#14699 <https://github.com/scipy/scipy/pull/14699>`__: BUG: Fix TypeError in \`stats._discrete_distns\`
* `#14700 <https://github.com/scipy/scipy/pull/14700>`__: DOC: update detailed roadmap
* `#14701 <https://github.com/scipy/scipy/pull/14701>`__: ENH:linalg: Add Cythonized get_array_bandwidth, issymmetric,...
* `#14706 <https://github.com/scipy/scipy/pull/14706>`__: BUG: Fix hyp2f1 to return correct values in regions near exp(±iπ/3).
* `#14707 <https://github.com/scipy/scipy/pull/14707>`__: Update constants.py
* `#14708 <https://github.com/scipy/scipy/pull/14708>`__: BENCH: shorten svds benchmark that is timing out in CI
* `#14709 <https://github.com/scipy/scipy/pull/14709>`__: CI: remove labeler sync
* `#14712 <https://github.com/scipy/scipy/pull/14712>`__: MAINT: special: Updates for _cosine.c.
* `#14720 <https://github.com/scipy/scipy/pull/14720>`__: DOC: optimize hess and consistency
* `#14721 <https://github.com/scipy/scipy/pull/14721>`__: MAINT: correct PR template link
* `#14723 <https://github.com/scipy/scipy/pull/14723>`__: DOC: add note on padding to \`stats.binned_statistic_2d\` docs
* `#14727 <https://github.com/scipy/scipy/pull/14727>`__: ENH: sparse.linalg: Add an useful nonzero initial guess option
* `#14729 <https://github.com/scipy/scipy/pull/14729>`__: DOC: fix documentation for scipy.optimize.brenth
* `#14737 <https://github.com/scipy/scipy/pull/14737>`__: BUG:signal: matching window dtype to input
* `#14739 <https://github.com/scipy/scipy/pull/14739>`__: TST: sparse.linalg: Add test case with 2-D Poisson equations
* `#14743 <https://github.com/scipy/scipy/pull/14743>`__: TST:sparse.linalg: Use the more convenient "assert_normclose"...
* `#14748 <https://github.com/scipy/scipy/pull/14748>`__: DOC: fix matrix representation in scipy.sparse.csgraph
* `#14751 <https://github.com/scipy/scipy/pull/14751>`__: ENH: numpy masked_arrays in refguide-check
* `#14755 <https://github.com/scipy/scipy/pull/14755>`__: BUG: Avoid \`solve_ivp\` failure when \`ts\` is empty
* `#14756 <https://github.com/scipy/scipy/pull/14756>`__: MAINT: LinAlgError from public numpy.linalg
* `#14759 <https://github.com/scipy/scipy/pull/14759>`__: BLD: change section name in site.cfg.example from ALL to DEFAULT
* `#14760 <https://github.com/scipy/scipy/pull/14760>`__: TST: suppress jinja2 deprecation warning
* `#14761 <https://github.com/scipy/scipy/pull/14761>`__: CI: remove \`pre_release_deps_source_dist\` job from Azure CI...
* `#14762 <https://github.com/scipy/scipy/pull/14762>`__: TST: add a seed to the pickling test of RBFInterpolator
* `#14763 <https://github.com/scipy/scipy/pull/14763>`__: MAINT: Make solve_ivp slightly more strict wrt. t_span.
* `#14772 <https://github.com/scipy/scipy/pull/14772>`__: DOC:special: Fix broken links to jburkardt
* `#14787 <https://github.com/scipy/scipy/pull/14787>`__: MAINT: Increase tolerance values to avoid test failures
* `#14789 <https://github.com/scipy/scipy/pull/14789>`__: MAINT: fix a tiny typo in signal/spectral.py
* `#14790 <https://github.com/scipy/scipy/pull/14790>`__: [MRG] BUG: Avoid lobpcg failure when iterations can't continue
* `#14794 <https://github.com/scipy/scipy/pull/14794>`__: Fix typos in bspline docs (and comments)
* `#14796 <https://github.com/scipy/scipy/pull/14796>`__: MAINT: Allow F401 and F403 in module init files
* `#14798 <https://github.com/scipy/scipy/pull/14798>`__: BUG: correct the test loop in test_arpack.eval_evec
* `#14801 <https://github.com/scipy/scipy/pull/14801>`__: CI, MAINT: pin Cython for azure pre-rel
* `#14805 <https://github.com/scipy/scipy/pull/14805>`__: BUG: optimize: fix max function call validation for minimize...
* `#14808 <https://github.com/scipy/scipy/pull/14808>`__: Fix Bug #14807
* `#14814 <https://github.com/scipy/scipy/pull/14814>`__: MAINT:integrate: add upstream quadpack changes
* `#14817 <https://github.com/scipy/scipy/pull/14817>`__: ENH: stats: add geometric zscore
* `#14820 <https://github.com/scipy/scipy/pull/14820>`__: MAINT: Remove \`np.rollaxis\` usage with \`np.moveaxis\` and...
* `#14821 <https://github.com/scipy/scipy/pull/14821>`__: DOC: Updated documentation for interp1d
* `#14822 <https://github.com/scipy/scipy/pull/14822>`__: Add an array API to scipy.sparse
* `#14832 <https://github.com/scipy/scipy/pull/14832>`__: MAINT: py3.10 in more jobs and bump some 3.8 to 3.9
* `#14833 <https://github.com/scipy/scipy/pull/14833>`__: FIX: raise Python OverflowError exception on Boost.Math error
* `#14836 <https://github.com/scipy/scipy/pull/14836>`__: Bug fix: dqc25f.f
* `#14837 <https://github.com/scipy/scipy/pull/14837>`__: DOC: sparse.linalg: Fixed incorrect comments when the initial...
* `#14838 <https://github.com/scipy/scipy/pull/14838>`__: TST: seed a stats test
* `#14841 <https://github.com/scipy/scipy/pull/14841>`__: MAINT: Increase tolerances in tests to avoid Nightly CPython3.10...
* `#14844 <https://github.com/scipy/scipy/pull/14844>`__: DOC: Add refguide_check option details to runtests.rst
* `#14845 <https://github.com/scipy/scipy/pull/14845>`__: DOC: update a type specifier in a docstring in \`radau.py\`
* `#14848 <https://github.com/scipy/scipy/pull/14848>`__: Typo "copmlex"
* `#14852 <https://github.com/scipy/scipy/pull/14852>`__: DOC: Fix documentation bugs in \`lstsq\`
* `#14860 <https://github.com/scipy/scipy/pull/14860>`__: minimize: copy user constraints if parameter is factored out....
* `#14865 <https://github.com/scipy/scipy/pull/14865>`__: BUG: stats: Fix a crash in stats.skew
* `#14868 <https://github.com/scipy/scipy/pull/14868>`__: [MRG] BUG: Update lobpcg.py to validate the accuracy and issue...
* `#14871 <https://github.com/scipy/scipy/pull/14871>`__: MAINT: removed a pitfall where a built-in name was being shadowed
* `#14872 <https://github.com/scipy/scipy/pull/14872>`__: DEP: Deprecate private namespaces in \`scipy.linalg\`
* `#14878 <https://github.com/scipy/scipy/pull/14878>`__: TST: bump rtol for equal_bounds
* `#14881 <https://github.com/scipy/scipy/pull/14881>`__: DEP: Deprecate private namespaces in \`scipy.special\`
* `#14882 <https://github.com/scipy/scipy/pull/14882>`__: BUG: Convert TNC C module to cython
* `#14883 <https://github.com/scipy/scipy/pull/14883>`__: DOC:linalg: Clarify driver defaults in eigh
* `#14884 <https://github.com/scipy/scipy/pull/14884>`__: BUG: optimize: add missing attributes of \`OptimizeResult\` for...
* `#14892 <https://github.com/scipy/scipy/pull/14892>`__: DOC: Correct docs for Hausdorff distance
* `#14898 <https://github.com/scipy/scipy/pull/14898>`__: DEP: Deprecate private namespace in \`scipy.stats\`
* `#14902 <https://github.com/scipy/scipy/pull/14902>`__: MAINT:linalg: Rename func to "bandwidth"
* `#14906 <https://github.com/scipy/scipy/pull/14906>`__: DEP: Deprecate private namespace in \`scipy.constants\`
* `#14913 <https://github.com/scipy/scipy/pull/14913>`__: DEP: Deprecate private namespace in \`scipy.fftpack\`
* `#14916 <https://github.com/scipy/scipy/pull/14916>`__: DEP: Deprecate \`stats.biasedurn\` and make it private
* `#14918 <https://github.com/scipy/scipy/pull/14918>`__: DEP: Deprecate private namespaces in \`\`scipy.interpolate\`\`
* `#14919 <https://github.com/scipy/scipy/pull/14919>`__: DEP: Deprecate private namespaces in \`scipy.integrate\`
* `#14920 <https://github.com/scipy/scipy/pull/14920>`__: Fix for complex Fresnel
* `#14923 <https://github.com/scipy/scipy/pull/14923>`__: DEP: Deprecate private namespaces in \`\`scipy.spatial\`\`
* `#14924 <https://github.com/scipy/scipy/pull/14924>`__: Fix extent for scipy.signal.cwt example
* `#14925 <https://github.com/scipy/scipy/pull/14925>`__: MAINT: Ignore build generated files in \`\`scipy.stats\`\`
* `#14927 <https://github.com/scipy/scipy/pull/14927>`__: DEP: Deprecate private namespaces in \`scipy.misc\`
* `#14928 <https://github.com/scipy/scipy/pull/14928>`__: MAINT: fix runtest.py overriding \`$PYTHONPATH\`: prepend instead
* `#14934 <https://github.com/scipy/scipy/pull/14934>`__: BUG: optimize: add a missing attribute of OptimizeResult in \`basinhopping\`
* `#14939 <https://github.com/scipy/scipy/pull/14939>`__: DEP: Deprecate private namespaces in \`\`scipy.sparse\`\`
* `#14941 <https://github.com/scipy/scipy/pull/14941>`__: ENH: optimize: add optional parameters of adaptive step size...
* `#14943 <https://github.com/scipy/scipy/pull/14943>`__: DOC: clarify mac pytest; add blank line
* `#14944 <https://github.com/scipy/scipy/pull/14944>`__: BUG: MultivariateNormalQMC with specific QMCEngine remove unneeded...
* `#14947 <https://github.com/scipy/scipy/pull/14947>`__: DOC: adding example to decimate function
* `#14950 <https://github.com/scipy/scipy/pull/14950>`__: MAINT: Use matmul binary operator in scipy.sparse.linalg
* `#14954 <https://github.com/scipy/scipy/pull/14954>`__: DOC: Add missing params to minres docstring.
* `#14955 <https://github.com/scipy/scipy/pull/14955>`__: BUG: stats: fix broadcasting behavior of argsreduce
* `#14960 <https://github.com/scipy/scipy/pull/14960>`__: Update links for new site
* `#14961 <https://github.com/scipy/scipy/pull/14961>`__: CI: use https protocol for git in CircleCI
* `#14962 <https://github.com/scipy/scipy/pull/14962>`__: DEP: Deprecate private namespaces in \`scipy.signal\`
* `#14963 <https://github.com/scipy/scipy/pull/14963>`__: MAINT: \`integrate.lsoda\` missing in .gitignore
* `#14965 <https://github.com/scipy/scipy/pull/14965>`__: DOC: update logo and add favicon.
* `#14966 <https://github.com/scipy/scipy/pull/14966>`__: DEP: Deprecate private namespaces in \`\`scipy.optimize\`\`
* `#14969 <https://github.com/scipy/scipy/pull/14969>`__: CI: Fixes pyparsing version in doc build
* `#14972 <https://github.com/scipy/scipy/pull/14972>`__: Don't put space after directive name.
* `#14979 <https://github.com/scipy/scipy/pull/14979>`__: BUG: scipy.sparse.linalg.spsolve: fix memory error caused from...
* `#14988 <https://github.com/scipy/scipy/pull/14988>`__: BLD: update pyproject.toml for Python 3.10
* `#14989 <https://github.com/scipy/scipy/pull/14989>`__: ENH: Speed up knot interval lookup for BSpline.design_matrix
* `#14992 <https://github.com/scipy/scipy/pull/14992>`__: Pythranized version of _matfuncs_sqrtm
* `#14993 <https://github.com/scipy/scipy/pull/14993>`__: MAINT: forward port 1.7.2 relnotes
* `#15004 <https://github.com/scipy/scipy/pull/15004>`__: ENH: Make \`get_matfile_version\` and other \`io.matlab\` objects...
* `#15007 <https://github.com/scipy/scipy/pull/15007>`__: DOC: add missing "regularized" to \`gammainccinv\` documentation
* `#15008 <https://github.com/scipy/scipy/pull/15008>`__: MAINT: restore access to deprecated private namespaces
* `#15010 <https://github.com/scipy/scipy/pull/15010>`__: TST: remove fragile test which checks if g77 is linked
* `#15013 <https://github.com/scipy/scipy/pull/15013>`__: MAINT: Fix use-after-free bug in Py_FindObjects
* `#15018 <https://github.com/scipy/scipy/pull/15018>`__: CI: Work around Sphinx bug
* `#15019 <https://github.com/scipy/scipy/pull/15019>`__: Finite Difference Hessian in Scipy Optimize Solvers (Newton-CG)
* `#15020 <https://github.com/scipy/scipy/pull/15020>`__: ENH: sparse.linalg: Fixed the issue that the initial guess "x0"...
* `#15022 <https://github.com/scipy/scipy/pull/15022>`__: DOC: mitigate newton optimization not converging.
* `#15023 <https://github.com/scipy/scipy/pull/15023>`__: CI: Unpin Sphinx
* `#15027 <https://github.com/scipy/scipy/pull/15027>`__: DOC: linalg: Fix a small condition doc error
* `#15029 <https://github.com/scipy/scipy/pull/15029>`__: DEP: Deprecate private namespaces in \`scipy.sparse.linalg\`
* `#15034 <https://github.com/scipy/scipy/pull/15034>`__: DOC: use numpydoc format for C function in \`_superlumodule.c\`
* `#15035 <https://github.com/scipy/scipy/pull/15035>`__: MAINT: simplify UNU.RAN api in stats
* `#15037 <https://github.com/scipy/scipy/pull/15037>`__: New example for gaussian_filter
* `#15040 <https://github.com/scipy/scipy/pull/15040>`__: MAINT: Add test for public API
* `#15041 <https://github.com/scipy/scipy/pull/15041>`__: DOC: Add warning to dct documentation about norm='ortho'
* `#15045 <https://github.com/scipy/scipy/pull/15045>`__: DOC: update toolchain.rst
* `#15053 <https://github.com/scipy/scipy/pull/15053>`__: TST: Add some test skips to get wheel builder CI green again
* `#15054 <https://github.com/scipy/scipy/pull/15054>`__: MAINT: Remove wminkowski
* `#15055 <https://github.com/scipy/scipy/pull/15055>`__: ENH: allow p>0 for Minkowski distance
* `#15061 <https://github.com/scipy/scipy/pull/15061>`__: MAINT:sparse: expm() fix redundant imports
* `#15062 <https://github.com/scipy/scipy/pull/15062>`__: MAINT:BLD: Open file in text mode for tempita
* `#15066 <https://github.com/scipy/scipy/pull/15066>`__: CI: bump gcc from 4.8 to 6
* `#15067 <https://github.com/scipy/scipy/pull/15067>`__: DOC: Update broken link to SuperLU library.
* `#15078 <https://github.com/scipy/scipy/pull/15078>`__: MAINT: update \`stats.iqr\` for deprecated \`np.percentile\`...
* `#15083 <https://github.com/scipy/scipy/pull/15083>`__: MAINT: stats: separate UNU.RAN functionality to its own submodule
* `#15084 <https://github.com/scipy/scipy/pull/15084>`__: MAINT: Include \`scipy.io.matlab\` in public API
* `#15085 <https://github.com/scipy/scipy/pull/15085>`__: ENH: support creation of analog SOS outputs
* `#15087 <https://github.com/scipy/scipy/pull/15087>`__: TST: Review \`\`_assert_within_tol\`\` positional arguments
* `#15095 <https://github.com/scipy/scipy/pull/15095>`__: MAINT: update gitignore to ignore private directories
* `#15099 <https://github.com/scipy/scipy/pull/15099>`__: MAINT: ScalarFunction remember best_x
* `#15100 <https://github.com/scipy/scipy/pull/15100>`__: MAINT: Include \`stats.contingency\` in public API
* `#15102 <https://github.com/scipy/scipy/pull/15102>`__: ENH: Add orthogonalize argument to DCT/DST
* `#15105 <https://github.com/scipy/scipy/pull/15105>`__: MAINT: Add missing imports in deprecated modules
* `#15107 <https://github.com/scipy/scipy/pull/15107>`__: BUG: Update chi_gen to use scipy.special.gammaln
* `#15109 <https://github.com/scipy/scipy/pull/15109>`__: MAINT: remove NaiveRatioUniforms from scipy.stats
* `#15111 <https://github.com/scipy/scipy/pull/15111>`__: ENH: Add special.log_expit and use it in stats.logistic
* `#15112 <https://github.com/scipy/scipy/pull/15112>`__: DOC: update 'Wn' definition in signal.butter
* `#15114 <https://github.com/scipy/scipy/pull/15114>`__: DOC: added Fermi-Dirac distribution by name
* `#15119 <https://github.com/scipy/scipy/pull/15119>`__: DOC: fix symlink to \`logistic.sf\` in \`stats.logistic\`
* `#15120 <https://github.com/scipy/scipy/pull/15120>`__: MAINT: Install \`sparse.linalg._eigen\` tests and fix test failures
* `#15123 <https://github.com/scipy/scipy/pull/15123>`__: MAINT: interpolate: move the \`sparse\` dependency from cython...
* `#15127 <https://github.com/scipy/scipy/pull/15127>`__: DOC: update linux build instructions to mention C++
* `#15134 <https://github.com/scipy/scipy/pull/15134>`__: DOC: Improve Lomb-Scargle example
* `#15135 <https://github.com/scipy/scipy/pull/15135>`__: ENH: Carlson symmetric elliptic integrals.
* `#15137 <https://github.com/scipy/scipy/pull/15137>`__: DOC: special: Add 'Examples' to multigammaln and roots_legendre...
* `#15139 <https://github.com/scipy/scipy/pull/15139>`__: Use constrained_layout in Lomb-Scargle example
* `#15142 <https://github.com/scipy/scipy/pull/15142>`__: ENH: stats.sampling: add SROU method
* `#15143 <https://github.com/scipy/scipy/pull/15143>`__: MAINT: Remove some unused imports.
* `#15144 <https://github.com/scipy/scipy/pull/15144>`__: BUG: Add missing import of 'errno' to runtests.py
* `#15157 <https://github.com/scipy/scipy/pull/15157>`__: ENH: rebased version of gh-14279
* `#15159 <https://github.com/scipy/scipy/pull/15159>`__: DOC: stats: fix a header in \`stats.sampling\` tutorial
* `#15161 <https://github.com/scipy/scipy/pull/15161>`__: DOC: 1.8.0 relnotes update
* `#15175 <https://github.com/scipy/scipy/pull/15175>`__: MAINT: 1.8.0 backports for relnotes and .gitignore
* `#15181 <https://github.com/scipy/scipy/pull/15181>`__: BUG: The pytest decorator for conditional skipping is 'skipif'
* `#15191 <https://github.com/scipy/scipy/pull/15191>`__: MAINT: version bounds before 1.8.0rc1
* `#15192 <https://github.com/scipy/scipy/pull/15192>`__: MAINT: Replace use of \`pytest.warns(None)\` with \`warnings.catch_warnings\`
* `#15194 <https://github.com/scipy/scipy/pull/15194>`__: BUG: stats: Fix numerical issues of recipinvgauss
* `#15214 <https://github.com/scipy/scipy/pull/15214>`__: TST: sparse.linalg: store only PROPACK test matrices; generate...
* `#15220 <https://github.com/scipy/scipy/pull/15220>`__: BUG: sparse.linalg: Fix deprecation warnings.
* `#15225 <https://github.com/scipy/scipy/pull/15225>`__: Make 0th power of a sparse array/matrix return the identity with...
* `#15229 <https://github.com/scipy/scipy/pull/15229>`__: BUG: minimize should work with a scalar closes #15228
* `#15232 <https://github.com/scipy/scipy/pull/15232>`__: BUG: Add rmul for sparse arrays
* `#15236 <https://github.com/scipy/scipy/pull/15236>`__: BLD: update setup.py for Python 3.10
* `#15248 <https://github.com/scipy/scipy/pull/15248>`__: MAINT: 1.8.0rc2 backports
* `#15249 <https://github.com/scipy/scipy/pull/15249>`__: FIX: PROPACK MKL compatibility
* `#15253 <https://github.com/scipy/scipy/pull/15253>`__: BUG: special: fix \`stdtr\` and \`stdtrit\` for infinite df
* `#15256 <https://github.com/scipy/scipy/pull/15256>`__: MAINT: use PEP440 vs. distutils
* `#15268 <https://github.com/scipy/scipy/pull/15268>`__: CI: pin setuptools to 59.6.0 and Pythran to 0.10.0 for Windows...
* `#15270 <https://github.com/scipy/scipy/pull/15270>`__: MAINT: rename \`moduleTNC\` extension back to \`_moduleTNC\`
* `#15271 <https://github.com/scipy/scipy/pull/15271>`__: TST: slightly bump test tolerance for a new lobpcg test
* `#15275 <https://github.com/scipy/scipy/pull/15275>`__: MAINT: Fix imports in \`signal._signaltools\`
* `#15278 <https://github.com/scipy/scipy/pull/15278>`__: MAINT: remove non-default settings (except \`shallow\`) in \`.gitmodules\`
* `#15288 <https://github.com/scipy/scipy/pull/15288>`__: BLD Respect the --skip-build flag in setup.py
* `#15293 <https://github.com/scipy/scipy/pull/15293>`__: BUG: fix Hausdorff int overflow
* `#15301 <https://github.com/scipy/scipy/pull/15301>`__: TST: update \`sparse.linalg\` tests for failures due to tolerances
* `#15318 <https://github.com/scipy/scipy/pull/15318>`__: BLD: update pyproject.toml to not pin numpy for aarch64 + PyPy
* `#15322 <https://github.com/scipy/scipy/pull/15322>`__: BLD: update minimum Pythran version to 0.10.0 for SciPy 1.8.0
* `#15323 <https://github.com/scipy/scipy/pull/15323>`__: MAINT: filter RuntimeWarnings in stats functions
* `#15328 <https://github.com/scipy/scipy/pull/15328>`__: MAINT: interpolate: csr_matrix -> csr_array
* `#15331 <https://github.com/scipy/scipy/pull/15331>`__: BUG: stats._unuran: fix invalid attribute lookups
* `#15332 <https://github.com/scipy/scipy/pull/15332>`__: CI: pin numpy to 1.21.5 for the doc build on CircleCI
* `#15334 <https://github.com/scipy/scipy/pull/15334>`__: BUG: stats._unuran: fix remaining attribute lookup errors
* `#15335 <https://github.com/scipy/scipy/pull/15335>`__: CI: pin numpy to 1.21.5 in the Azure refguide check job
* `#15341 <https://github.com/scipy/scipy/pull/15341>`__: BUG: \`highs-ds\` returns memoryviews instead of np.arrays for...
* `#15397 <https://github.com/scipy/scipy/pull/15397>`__: BUG: ensured vendored pep440 is imported
* `#15416 <https://github.com/scipy/scipy/pull/15416>`__: BUG: Fix PyUFunc for wasm targets
* `#15418 <https://github.com/scipy/scipy/pull/15418>`__: MAINT: 1.8.0 rc3 backports round 1
* `#15421 <https://github.com/scipy/scipy/pull/15421>`__: BUG: stats: mode: fix negative axis issue with np.moveaxis instead...
* `#15432 <https://github.com/scipy/scipy/pull/15432>`__: MAINT: release branch PROPACK switch (default off)
* `#15515 <https://github.com/scipy/scipy/pull/15515>`__: MAINT: fix broken link and remove CI badges


# ===== SOURCE: https://raw.githubusercontent.com/scipy/scipy/main/doc/source/release/1.9.0-notes.rst =====

==========================
SciPy 1.9.0 Release Notes
==========================

.. contents::

SciPy 1.9.0 is the culmination of 6 months of hard work. It contains
many new features, numerous bug-fixes, improved test coverage and better
documentation. There have been a number of deprecations and API changes
in this release, which are documented below. All users are encouraged to
upgrade to this release, as there are a large number of bug-fixes and
optimizations. Before upgrading, we recommend that users check that
their own code does not use deprecated SciPy functionality (to do so,
run your code with ``python -Wd`` and check for ``DeprecationWarning`` s).
Our development attention will now shift to bug-fix releases on the
1.9.x branch, and on adding new features on the main branch.

This release requires Python 3.8-3.11 and NumPy 1.18.5 or greater.

For running on PyPy, PyPy3 6.0+ is required.


**************************
Highlights of this release
**************************

- We have modernized our build system to use ``meson``, substantially improving
  our build performance, and providing better build-time configuration and
  cross-compilation support,
- Added `scipy.optimize.milp`, new function for mixed-integer linear
  programming,
- Added `scipy.stats.fit` for fitting discrete and continuous distributions
  to data,
- Tensor-product spline interpolation modes were added to
  `scipy.interpolate.RegularGridInterpolator`,
- A new global optimizer (DIviding RECTangles algorithm)
  `scipy.optimize.direct`.


************
New features
************


`scipy.interpolate` improvements
================================
- Speed up the ``RBFInterpolator`` evaluation with high dimensional
  interpolants.
- Added new spline based interpolation methods for
  `scipy.interpolate.RegularGridInterpolator` and its tutorial.
- `scipy.interpolate.RegularGridInterpolator` and `scipy.interpolate.interpn`
  now accept descending ordered points.
- ``RegularGridInterpolator`` now handles length-1 grid axes.
- The ``BivariateSpline`` subclasses have a new method ``partial_derivative``
  which constructs a new spline object representing a derivative of an
  original spline. This mirrors the corresponding functionality for univariate
  splines, ``splder`` and ``BSpline.derivative``, and can substantially speed
  up repeated evaluation of derivatives.

`scipy.linalg` improvements
===========================
- `scipy.linalg.expm` now accepts nD arrays. Its speed is also improved.
- Minimum required LAPACK version is bumped to ``3.7.1``.


`scipy.fft` improvements
========================
- Added ``uarray`` multimethods for `scipy.fft.fht` and `scipy.fft.ifht`
  to allow provision of third party backend implementations such as those
  recently added to CuPy.

`scipy.optimize` improvements
=============================
- A new global optimizer, `scipy.optimize.direct` (DIviding RECTangles algorithm)
  was added. For problems with inexpensive function evaluations, like the ones
  in the SciPy benchmark suite, ``direct`` is competitive with the best other
  solvers in SciPy (``dual_annealing`` and ``differential_evolution``) in terms
  of execution time. See
  `gh-14300 <https://github.com/scipy/scipy/pull/14300>`__ for more details.

- Add a ``full_output`` parameter to `scipy.optimize.curve_fit` to output
  additional solution information.
- Add a ``integrality`` parameter to `scipy.optimize.differential_evolution`,
  enabling integer constraints on parameters.
- Add a ``vectorized`` parameter to call a vectorized objective function only
  once per iteration. This can improve minimization speed by reducing
  interpreter overhead from the multiple objective function calls.
- The default method of `scipy.optimize.linprog` is now ``'highs'``.
- Added `scipy.optimize.milp`, new function for mixed-integer linear
  programming.
- Added Newton-TFQMR method to ``newton_krylov``.
- Added support for the ``Bounds`` class in ``shgo`` and ``dual_annealing`` for
  a more uniform API across `scipy.optimize`.
- Added the ``vectorized`` keyword to ``differential_evolution``.
- ``approx_fprime`` now works with vector-valued functions.

`scipy.signal` improvements
===========================
- The new window function `scipy.signal.windows.kaiser_bessel_derived` was
  added to compute the Kaiser-Bessel derived window.
- Single-precision ``hilbert`` operations are now faster as a result of more
  consistent ``dtype`` handling.

`scipy.sparse` improvements
===========================
- Add a ``copy`` parameter to `scipy.sparse.csgraph.laplacian`. Using inplace
  computation with ``copy=False`` reduces the memory footprint.
- Add a ``dtype`` parameter to `scipy.sparse.csgraph.laplacian` for type casting.
- Add a ``symmetrized`` parameter to `scipy.sparse.csgraph.laplacian` to produce
  symmetric Laplacian for directed graphs.
- Add a ``form`` parameter to `scipy.sparse.csgraph.laplacian` taking one of the
  three values: ``array``, or ``function``, or ``lo`` determining the format of
  the output Laplacian:
  * ``array`` is a numpy array (backward compatible default);
  * ``function`` is a pointer to a lambda-function evaluating the
  Laplacian-vector or Laplacian-matrix product;
  * ``lo`` results in the format of the ``LinearOperator``.

`scipy.sparse.linalg` improvements
==================================
- ``lobpcg`` performance improvements for small input cases.

`scipy.spatial` improvements
============================
- Add an ``order`` parameter to `scipy.spatial.transform.Rotation.from_quat`
  and `scipy.spatial.transform.Rotation.as_quat` to specify quaternion format.


`scipy.stats` improvements
==========================
- `scipy.stats.monte_carlo_test` performs one-sample Monte Carlo hypothesis
  tests to assess whether a sample was drawn from a given distribution. Besides
  reproducing the results of hypothesis tests like `scipy.stats.ks_1samp`,
  `scipy.stats.normaltest`, and `scipy.stats.cramervonmises` without small sample
  size limitations, it makes it possible to perform similar tests using arbitrary
  statistics and distributions.

- Several `scipy.stats` functions support new ``axis`` (integer or tuple of
  integers) and ``nan_policy`` ('raise', 'omit', or 'propagate'), and
  ``keepdims`` arguments.
  These functions also support masked arrays as inputs, even if they do not have
  a `scipy.stats.mstats` counterpart. Edge cases for multidimensional arrays,
  such as when axis-slices have no unmasked elements or entire inputs are of
  size zero, are handled consistently.

- Add a ``weights`` parameter to `scipy.stats.hmean`.

- Several improvements have been made to `scipy.stats.levy_stable`. Substantial
  improvement has been made for numerical evaluation of the pdf and cdf,
  resolving [#12658](https://github.com/scipy/scipy/issues/12658) and
  [#14944](https://github.com/scipy/scipy/issues/14994). The improvement is
  particularly dramatic for stability parameter ``alpha`` close to or equal to 1
  and for ``alpha`` below but approaching its maximum value of 2. The alternative
  fast Fourier transform based method for pdf calculation has also been updated
  to use the approach of Wang and Zhang from their 2008 conference paper
  *Simpson’s rule based FFT method to compute densities of stable distribution*,
  making this method more competitive with the default method. In addition,
  users now have the option to change the parametrization of the Levy Stable
  distribution to Nolan's "S0" parametrization which is used internally by
  SciPy's pdf and cdf implementations. The "S0"  parametrization is described in
  Nolan's paper [*Numerical calculation of stable densities and distribution
  functions*](https://doi.org/10.1080/15326349708807450) upon which SciPy's
  implementation is based. "S0" has the advantage that ``delta`` and ``gamma``
  are proper location and scale parameters. With ``delta`` and ``gamma`` fixed,
  the location and scale of the resulting distribution remain unchanged as
  ``alpha`` and ``beta`` change. This is not the case for the default "S1"
  parametrization. Finally, more options have been exposed to allow users to
  trade off between runtime and accuracy for both the default and FFT methods of
  pdf and cdf calculation. More information can be found in the documentation
  here (to be linked).

- Added `scipy.stats.fit` for fitting discrete and continuous distributions to
  data.

- The methods ``"pearson"`` and ``"tippet"`` from `scipy.stats.combine_pvalues`
  have been fixed to return the correct p-values, resolving
  [#15373](https://github.com/scipy/scipy/issues/15373). In addition, the
  documentation for `scipy.stats.combine_pvalues` has been expanded and improved.

- Unlike other reduction functions, ``stats.mode`` didn't consume the axis
  being operated on and failed for negative axis inputs. Both the bugs have been
  fixed. Note that ``stats.mode`` will now consume the input axis and return an
  ndarray with the ``axis`` dimension removed.

- Replaced implementation of `scipy.stats.ncf` with the implementation from
  Boost for improved reliability.

- Add a `bits` parameter to `scipy.stats.qmc.Sobol`. It allows to use from 0
  to 64 bits to compute the sequence. Default is ``None`` which corresponds to
  30 for backward compatibility. Using a higher value allow to sample more
  points. Note: ``bits`` does not affect the output dtype.

- Add a `integers` method to `scipy.stats.qmc.QMCEngine`. It allows sampling
  integers using any QMC sampler.

- Improved the fit speed and accuracy of ``stats.pareto``.

- Added ``qrvs`` method to ``NumericalInversePolynomial`` to match the
  situation for ``NumericalInverseHermite``.

- Faster random variate generation for ``gennorm`` and ``nakagami``.

- ``lloyd_centroidal_voronoi_tessellation`` has been added to allow improved
  sample distributions via iterative application of Voronoi diagrams and
  centering operations

- Add `scipy.stats.qmc.PoissonDisk` to sample using the Poisson disk sampling
  method. It guarantees that samples are separated from each other by a
  given ``radius``.

- Add `scipy.stats.pmean` to calculate the weighted power mean also called
  generalized mean.


*******************
Deprecated features
*******************

- Due to collision with the shape parameter ``n`` of several distributions,
  use of the distribution ``moment`` method with keyword argument ``n`` is
  deprecated. Keyword ``n`` is replaced with keyword ``order``.
- Similarly, use of the distribution ``interval`` method with keyword arguments
  ``alpha`` is deprecated. Keyword ``alpha`` is replaced with keyword
  ``confidence``.
- The ``'simplex'``, ``'revised simplex'``, and ``'interior-point'`` methods
  of `scipy.optimize.linprog` are deprecated. Methods ``highs``, ``highs-ds``,
  or ``highs-ipm`` should be used in new code.
- Support for non-numeric arrays has been deprecated from ``stats.mode``.
  ``pandas.DataFrame.mode`` can be used instead.
- The function `spatial.distance.kulsinski` has been deprecated in favor
  of `spatial.distance.kulczynski1`.
- The ``maxiter`` keyword of the truncated Newton (TNC) algorithm has been
  deprecated in favour of ``maxfun``.
- The ``vertices`` keyword of ``Delauney.qhull`` now raises a
  DeprecationWarning, after having been deprecated in documentation only
  for a long time.
- The ``extradoc`` keyword of ``rv_continuous``, ``rv_discrete`` and
  ``rv_sample`` now raises a DeprecationWarning, after having been deprecated in
  documentation only for a long time.

********************
Expired Deprecations
********************
There is an ongoing effort to follow through on long-standing deprecations.
The following previously deprecated features are affected:

- Object arrays in sparse matrices now raise an error.
- Inexact indices into sparse matrices now raise an error.
- Passing ``radius=None`` to `scipy.spatial.SphericalVoronoi` now raises an
  error (not adding ``radius`` defaults to 1, as before).
- Several BSpline methods now raise an error if inputs have ``ndim > 1``.
- The ``_rvs`` method of statistical distributions now requires a ``size``
  parameter.
- Passing a ``fillvalue`` that cannot be cast to the output type in
  `scipy.signal.convolve2d` now raises an error.
- `scipy.spatial.distance` now enforces that the input vectors are
  one-dimensional.
- Removed ``stats.itemfreq``.
- Removed ``stats.median_absolute_deviation``.
- Removed ``n_jobs`` keyword argument and use of ``k=None`` from
  ``kdtree.query``.
- Removed ``right`` keyword from ``interpolate.PPoly.extend``.
- Removed ``debug`` keyword from ``scipy.linalg.solve_*``.
- Removed class ``_ppform`` ``scipy.interpolate``.
- Removed BSR methods ``matvec`` and ``matmat``.
- Removed ``mlab`` truncation mode from ``cluster.dendrogram``.
- Removed ``cluster.vq.py_vq2``.
- Removed keyword arguments ``ftol`` and ``xtol`` from
  ``optimize.minimize(method='Nelder-Mead')``.
- Removed ``signal.windows.hanning``.
- Removed LAPACK ``gegv`` functions from ``linalg``; this raises the minimally
  required LAPACK version to 3.7.1.
- Removed ``spatial.distance.matching``.
- Removed the alias ``scipy.random`` for ``numpy.random``.
- Removed docstring related functions from ``scipy.misc`` (``docformat``,
  ``inherit_docstring_from``, ``extend_notes_in_docstring``,
  ``replace_notes_in_docstring``, ``indentcount_lines``, ``filldoc``,
  ``unindent_dict``, ``unindent_string``).
- Removed ``linalg.pinv2``.

******************************
Backwards incompatible changes
******************************

- Several `scipy.stats` functions now convert ``np.matrix`` to ``np.ndarray``s
  before the calculation is performed. In this case, the output will be a scalar
  or ``np.ndarray`` of appropriate shape rather than a 2D ``np.matrix``.
  Similarly, while masked elements of masked arrays are still ignored, the
  output will be a scalar or ``np.ndarray`` rather than a masked array with
  ``mask=False``.
- The default method of `scipy.optimize.linprog` is now ``'highs'``, not
  ``'interior-point'`` (which is now deprecated), so callback functions and
  some options are no longer supported with the default method. With the
  default method, the ``x`` attribute of the returned ``OptimizeResult`` is
  now ``None`` (instead of a non-optimal array) when an optimal solution
  cannot be found (e.g. infeasible problem).
- For `scipy.stats.combine_pvalues`, the sign of the test statistic returned
  for the method ``"pearson"`` has been flipped so that higher values of the
  statistic now correspond to lower p-values, making the statistic more
  consistent with those of the other methods and with the majority of the
  literature.
- `scipy.linalg.expm` due to historical reasons was using the sparse
  implementation and thus was accepting sparse arrays. Now it only works with
  nDarrays. For sparse usage, `scipy.sparse.linalg.expm` needs to be used
  explicitly.
- The definition of `scipy.stats.circvar` has reverted to the one that is
  standard in the literature; note that this is not the same as the square of
  `scipy.stats.circstd`.
- Remove inheritance to `QMCEngine` in `MultinomialQMC` and
  `MultivariateNormalQMC`. It removes the methods `fast_forward` and `reset`.
- Init of `MultinomialQMC` now require the number of trials with `n_trials`.
  Hence, `MultinomialQMC.random` output has now the correct shape ``(n, pvals)``.
- Several function-specific warnings (``F_onewayConstantInputWarning``,
  ``F_onewayBadInputSizesWarning``, ``PearsonRConstantInputWarning``,
  ``PearsonRNearConstantInputWarning``, ``SpearmanRConstantInputWarning``, and
  ``BootstrapDegenerateDistributionWarning``) have been replaced with more
  general warnings.


*************
Other changes
*************

- A draft developer CLI is available for SciPy, leveraging the ``doit``,
  ``click`` and ``rich-click`` tools. For more details, see
  [gh-15959](https://github.com/scipy/scipy/pull/15959).

- The SciPy contributor guide has been reorganized and updated
  (see [#15947](https://github.com/scipy/scipy/pull/15947) for details).

- QUADPACK Fortran routines in `scipy.integrate`, which power
  `scipy.integrate.quad`, have been marked as `recursive`. This should fix rare
  issues in multivariate integration (`nquad` and friends) and obviate the need
  for compiler-specific compile flags (`/recursive` for ifort etc). Please file
  an issue if this change turns out problematic for you. This is also true for
  ``FITPACK`` routines in `scipy.interpolate`, which power ``splrep``,
  ``splev`` etc., and ``*UnivariateSpline`` and ``*BivariateSpline`` classes.

- the ``USE_PROPACK`` environment variable has been renamed to
  ``SCIPY_USE_PROPACK``; setting to a non-zero value will enable
  the usage of the ``PROPACK`` library as before

- Building SciPy on windows with MSVC now requires at least the vc142
  toolset (available in Visual Studio 2019 and higher).

Lazy access to subpackages
==========================

Before this release, all subpackages of SciPy (`cluster`, `fft`, `ndimage`,
etc.) had to be explicitly imported. Now, these subpackages are lazily loaded
as soon as they are accessed, so that the following is possible (if desired
for interactive use, it's not actually recommended for code,
see :ref:`scipy-api`):
``import scipy as sp; sp.fft.dct([1, 2, 3])``. Advantages include: making it
easier to navigate SciPy in interactive terminals, reducing subpackage import
conflicts (which before required
``import networkx.linalg as nla; import scipy.linalg as sla``),
and avoiding repeatedly having to update imports during teaching &
experimentation. Also see
[the related community specification document](https://scientific-python.org/specs/spec-0001/).

SciPy switched to Meson as its build system
===========================================

This is the first release that ships with [Meson](https://mesonbuild.com) as
the build system. When installing with ``pip`` or ``pypa/build``, Meson will be
used (invoked via the ``meson-python`` build hook). This change brings
significant benefits - most importantly much faster build times, but also
better support for cross-compilation and cleaner build logs.

.. note::

   This release still ships with support for ``numpy.distutils``-based builds
   as well. Those can be invoked through the ``setup.py`` command-line
   interface (e.g., ``python setup.py install``). It is planned to remove
   ``numpy.distutils`` support before the 1.10.0 release.

When building from source, a number of things have changed compared to building
with ``numpy.distutils``:

- New build dependencies: ``meson``, ``ninja``, and ``pkg-config``.
  ``setuptools`` and ``wheel`` are no longer needed.
- BLAS and LAPACK libraries that are supported haven't changed, however the
  discovery mechanism has: that is now using ``pkg-config`` instead of hardcoded
  paths or a ``site.cfg`` file.
- The build defaults to using OpenBLAS. See :ref:`blas-lapack-selection` for
  details.

The two CLIs that can be used to build wheels are ``pip`` and ``build``. In
addition, the SciPy repo contains a ``python dev.py`` CLI for any kind of
development task (see its ``--help`` for details). For a comparison between old
(``distutils``) and new (``meson``) build commands, see :ref:`distutils-meson-equivalents`.

For more information on the introduction of Meson support in SciPy, see
`gh-13615 <https://github.com/scipy/scipy/issues/13615>`__ and
`this blog post <https://labs.quansight.org/blog/2021/07/moving-scipy-to-meson/>`__.


*******
Authors
*******

* endolith (12)
* h-vetinari (11)
* Caio Agiani (2) +
* Emmy Albert (1) +
* Joseph Albert (1)
* Tania Allard (3)
* Carsten Allefeld (1) +
* Kartik Anand (1) +
* Virgile Andreani (2) +
* Weh Andreas (1) +
* Francesco Andreuzzi (5) +
* Kian-Meng Ang (2) +
* Gerrit Ansmann (1)
* Ar-Kareem (1) +
* Shehan Atukorala (1) +
* avishai231 (1) +
* Blair Azzopardi (1)
* Sayantika Banik (2) +
* Ross Barnowski (9)
* Christoph Baumgarten (3)
* Nickolai Belakovski (1)
* Peter Bell (9)
* Sebastian Berg (3)
* Bharath (1) +
* bobcatCA (2) +
* boussoffara (2) +
* Islem BOUZENIA (1) +
* Jake Bowhay (41) +
* Matthew Brett (11)
* Dietrich Brunn (2) +
* Michael Burkhart (2) +
* Evgeni Burovski (96)
* Matthias Bussonnier (20)
* Dominic C (1)
* Cameron (1) +
* CJ Carey (3)
* Thomas A Caswell (2)
* Ali Cetin (2) +
* Hood Chatham (5) +
* Klesk Chonkin (1)
* Craig Citro (1) +
* Dan Cogswell (1) +
* Luigi Cruz (1) +
* Anirudh Dagar (5)
* Brandon David (1)
* deepakdinesh1123 (1) +
* Denton DeLoss (1) +
* derbuihan (2) +
* Sameer Deshmukh (13) +
* Niels Doucet (1) +
* DWesl (8)
* eytanadler (30) +
* Thomas J. Fan (5)
* Isuru Fernando (3)
* Joseph Fox-Rabinovitz (1)
* Ryan Gibson (4) +
* Ralf Gommers (327)
* Srinivas Gorur-Shandilya (1) +
* Alex Griffing (2)
* Matt Haberland (461)
* Tristan Hearn (1) +
* Jonathan Helgert (1) +
* Samuel Hinton (1) +
* Jake (1) +
* Stewart Jamieson (1) +
* Jan-Hendrik Müller (1)
* Yikun Jiang (1) +
* JuliaMelle01 (1) +
* jyuv (12) +
* Toshiki Kataoka (1)
* Chris Keefe (1) +
* Robert Kern (4)
* Andrew Knyazev (11)
* Matthias Koeppe (4) +
* Sergey Koposov (1)
* Volodymyr Kozachynskyi (1) +
* Yotaro Kubo (2) +
* Jacob Lapenna (1) +
* Peter Mahler Larsen (8)
* Eric Larson (4)
* Laurynas Mikšys (1) +
* Antony Lee (1)
* Gregory R. Lee (2)
* lerichi (1) +
* Tim Leslie (2)
* P. L. Lim (1)
* Smit Lunagariya (43)
* lutefiskhotdish (1) +
* Cong Ma (12)
* Syrtis Major (1)
* Nicholas McKibben (18)
* Melissa Weber Mendonça (10)
* Mark Mikofski (1)
* Jarrod Millman (13)
* Harsh Mishra (6)
* ML-Nielsen (3) +
* Matthew Murray (1) +
* Andrew Nelson (50)
* Dimitri Papadopoulos Orfanos (1) +
* Evgueni Ovtchinnikov (2) +
* Sambit Panda (1)
* Nick Papior (2)
* Tirth Patel (43)
* Petar Mlinarić (1)
* petroselo (1) +
* Ilhan Polat (64)
* Anthony Polloreno (1)
* Amit Portnoy (1) +
* Quentin Barthélemy (9)
* Patrick N. Raanes (1) +
* Tyler Reddy (185)
* Pamphile Roy (199)
* Vivek Roy (2) +
* sabonerune (1) +
* Niyas Sait (2) +
* Atsushi Sakai (25)
* Mazen Sayed (1) +
* Eduardo Schettino (5) +
* Daniel Schmitz (6) +
* Eli Schwartz (4) +
* SELEE (2) +
* Namami Shanker (4)
* siddhantwahal (1) +
* Gagandeep Singh (8)
* Soph (1) +
* Shivnaren Srinivasan (1) +
* Scott Staniewicz (1) +
* Leo C. Stein (4)
* Albert Steppi (7)
* Christopher Strickland (1) +
* Kai Striega (4)
* Søren Fuglede Jørgensen (1)
* Aleksandr Tagilov (1) +
* Masayuki Takagi (1) +
* Sai Teja (1) +
* Ewout ter Hoeven (2) +
* Will Tirone (2)
* Bas van Beek (7)
* Dhruv Vats (1)
* Arthur Volant (1)
* Samuel Wallan (5)
* Stefan van der Walt (8)
* Warren Weckesser (84)
* Anreas Weh (1)
* Nils Werner (1)
* Aviv Yaish (1) +
* Dowon Yi (1)
* Rory Yorke (1)
* Yosshi999 (1) +
* yuanx749 (2) +
* Gang Zhao (23)
* ZhihuiChen0903 (1)
* Pavel Zun (1) +
* David Zwicker (1) +

A total of 154 people contributed to this release.
People with a "+" by their names contributed a patch for the first time.
This list of names is automatically generated, and may not be fully complete.


***********************
Issues closed for 1.9.0
***********************

* `#1884 <https://github.com/scipy/scipy/issues/1884>`__: stats distributions fit problems (Trac #1359)
* `#2047 <https://github.com/scipy/scipy/issues/2047>`__: derivatives() method is missing in BivariateSpline (Trac #1522)
* `#2071 <https://github.com/scipy/scipy/issues/2071>`__: TST: stats: \`check_sample_var\` should be two-sided (Trac #1546)
* `#2414 <https://github.com/scipy/scipy/issues/2414>`__: stats binom at non-integer n (Trac #1895)
* `#2623 <https://github.com/scipy/scipy/issues/2623>`__: stats.distributions statistical power of test suite
* `#2625 <https://github.com/scipy/scipy/issues/2625>`__: wilcoxon() function does not return z-statistic
* `#2650 <https://github.com/scipy/scipy/issues/2650>`__: (2D) Interpolation functions should work with complex numbers
* `#2834 <https://github.com/scipy/scipy/issues/2834>`__: ksone fitting
* `#2868 <https://github.com/scipy/scipy/issues/2868>`__: nan and stats.percentileofscore
* `#2877 <https://github.com/scipy/scipy/issues/2877>`__: distributions.ncf numerical issues
* `#2993 <https://github.com/scipy/scipy/issues/2993>`__: optimize.approx_fprime & jacobians
* `#3214 <https://github.com/scipy/scipy/issues/3214>`__: stats distributions ppf-cdf roundtrip
* `#3758 <https://github.com/scipy/scipy/issues/3758>`__: discrete distribution defined by \`values\` with non-integer...
* `#4130 <https://github.com/scipy/scipy/issues/4130>`__: BUG: stats: fisher_exact returns incorrect p-value
* `#4897 <https://github.com/scipy/scipy/issues/4897>`__: expm is 10x as slow as matlab according to http://stackoverflow.com/questions/30048315
* `#5103 <https://github.com/scipy/scipy/issues/5103>`__: Docs suggest scipy.sparse.linalg.expm_multiply supports LinearOperator...
* `#5266 <https://github.com/scipy/scipy/issues/5266>`__: Deprecated routines in Netlib LAPACK >3.5.0
* `#5890 <https://github.com/scipy/scipy/issues/5890>`__: Undefined behavior when using scipy.interpolate.RegularGridInterpolator...
* `#5982 <https://github.com/scipy/scipy/issues/5982>`__: Keyword collision in scipy.stats.levy_stable.interval
* `#6472 <https://github.com/scipy/scipy/issues/6472>`__: scipy.stats.invwishart does not check if scale matrix is symmetric
* `#6551 <https://github.com/scipy/scipy/issues/6551>`__: BUG: stats: inconsistency in docs and behavior of gmean and hmean
* `#6624 <https://github.com/scipy/scipy/issues/6624>`__: incorrect handling of nan by RegularGridInterpolator
* `#6882 <https://github.com/scipy/scipy/issues/6882>`__: Certain recursive scipy.integrate.quad (e.g. dblquad and nquad)...
* `#7469 <https://github.com/scipy/scipy/issues/7469>`__: Misleading interp2d documentation
* `#7560 <https://github.com/scipy/scipy/issues/7560>`__: Should RegularGridInterpolator support length 1 dimensions?
* `#8850 <https://github.com/scipy/scipy/issues/8850>`__: Scipy.interpolate.griddata Error : Exception ignored in: 'scipy.spatial.qhull._Qhull.__dealloc__'
* `#8928 <https://github.com/scipy/scipy/issues/8928>`__: BUG: scipy.stats.norm wrong expected value of function when loc...
* `#9213 <https://github.com/scipy/scipy/issues/9213>`__: __STDC_VERSION__ check in C++ code
* `#9231 <https://github.com/scipy/scipy/issues/9231>`__: infinite loop in stats.fisher_exact
* `#9313 <https://github.com/scipy/scipy/issues/9313>`__: geometric distribution stats.geom returns negative values if...
* `#9524 <https://github.com/scipy/scipy/issues/9524>`__: interpn returns nan with perfectly valid data
* `#9591 <https://github.com/scipy/scipy/issues/9591>`__: scipy.interpolate.interp1d with kind=“previous” doesn't extrapolate...
* `#9815 <https://github.com/scipy/scipy/issues/9815>`__: stats.mode's nan_policy 'propagate' not working?
* `#9944 <https://github.com/scipy/scipy/issues/9944>`__: documentation for \`scipy.interpolate.RectBivariateSpline\` is...
* `#9999 <https://github.com/scipy/scipy/issues/9999>`__: BUG: malloc() calls in Cython and C that are not checked for...
* `#10096 <https://github.com/scipy/scipy/issues/10096>`__: Add literature reference for circstd (and circvar?)
* `#10446 <https://github.com/scipy/scipy/issues/10446>`__: RuntimeWarning: invalid value encountered in stats.genextreme
* `#10577 <https://github.com/scipy/scipy/issues/10577>`__: Additional discussion for scipy.stats roadmap
* `#10821 <https://github.com/scipy/scipy/issues/10821>`__: Errors with the Yeo-Johnson Transform that also Appear in Scikit-Learn
* `#10983 <https://github.com/scipy/scipy/issues/10983>`__: LOBPCG inefficinet when computing > 20% of eigenvalues
* `#11145 <https://github.com/scipy/scipy/issues/11145>`__: unexpected SparseEfficiencyWarning at scipy.sparse.linalg.splu
* `#11406 <https://github.com/scipy/scipy/issues/11406>`__: scipy.sparse.linalg.svds (v1.4.1) on singular matrix does not...
* `#11447 <https://github.com/scipy/scipy/issues/11447>`__: scipy.interpolate.interpn: Handle ValueError('The points in dimension...
* `#11673 <https://github.com/scipy/scipy/issues/11673>`__: intlinprog: integer linear program solver
* `#11742 <https://github.com/scipy/scipy/issues/11742>`__: MAINT: stats: getting skewness alone takes 34000x longer than...
* `#11806 <https://github.com/scipy/scipy/issues/11806>`__: Unexpectedly poor results when distribution fitting with \`weibull_min\`...
* `#11828 <https://github.com/scipy/scipy/issues/11828>`__: UnivariateSpline gives varying results when multithreaded on...
* `#11948 <https://github.com/scipy/scipy/issues/11948>`__: fitting discrete distributions
* `#12073 <https://github.com/scipy/scipy/issues/12073>`__: Add note in documentation
* `#12370 <https://github.com/scipy/scipy/issues/12370>`__: truncnorm.rvs is painfully slow on version 1.5.0rc2
* `#12456 <https://github.com/scipy/scipy/issues/12456>`__: Add generalized mean calculation
* `#12480 <https://github.com/scipy/scipy/issues/12480>`__: RectBivariateSpline derivative evaluator is slow
* `#12485 <https://github.com/scipy/scipy/issues/12485>`__: linprog returns an incorrect message
* `#12506 <https://github.com/scipy/scipy/issues/12506>`__: ENH: stats: one-sided p-values for statistical tests
* `#12545 <https://github.com/scipy/scipy/issues/12545>`__: stats.pareto.fit raises RuntimeWarning
* `#12548 <https://github.com/scipy/scipy/issues/12548>`__: scipy.stats.skew returning MaskedArray
* `#12633 <https://github.com/scipy/scipy/issues/12633>`__: Offer simpler development workflow?
* `#12658 <https://github.com/scipy/scipy/issues/12658>`__: scipy.stats.levy_stable.pdf can be inaccurate and return nan
* `#12733 <https://github.com/scipy/scipy/issues/12733>`__: scipy.stats.truncnorm.cdf slow
* `#12838 <https://github.com/scipy/scipy/issues/12838>`__: Accept multiple matrices in \`scipy.linalg.expm\`
* `#12848 <https://github.com/scipy/scipy/issues/12848>`__: DOC: stats: multivariate distribution documentation issues
* `#12870 <https://github.com/scipy/scipy/issues/12870>`__: Levy Stable Random Variates Code has a typo
* `#12871 <https://github.com/scipy/scipy/issues/12871>`__: Levy Stable distribution uses parameterisation that is not location...
* `#13200 <https://github.com/scipy/scipy/issues/13200>`__: Errors made by scipy.optimize.linprog
* `#13462 <https://github.com/scipy/scipy/issues/13462>`__: Too many warnings and results objects in public API for scipy.stats
* `#13582 <https://github.com/scipy/scipy/issues/13582>`__: ENH: stats: \`rv_continuous.stats\` with array shapes: use \`_stats\`...
* `#13615 <https://github.com/scipy/scipy/issues/13615>`__: RFC: switch to Meson as a build system
* `#13632 <https://github.com/scipy/scipy/issues/13632>`__: stats.rv_discrete is not checking that xk values are integers
* `#13655 <https://github.com/scipy/scipy/issues/13655>`__: MAINT: stats.rv_generic: \`moment\` method falls back to \`_munp\`...
* `#13689 <https://github.com/scipy/scipy/issues/13689>`__: Wilcoxon does not appropriately detect ties when mode=exact.
* `#13835 <https://github.com/scipy/scipy/issues/13835>`__: Change name of \`alpha\` parameter in \`interval()\` method
* `#13872 <https://github.com/scipy/scipy/issues/13872>`__: Add method details or reference to \`scipy.integrate.dblquad\`
* `#13912 <https://github.com/scipy/scipy/issues/13912>`__: Adding Poisson Disc sampling to QMC
* `#13996 <https://github.com/scipy/scipy/issues/13996>`__: Fisk distribution documentation typo
* `#14035 <https://github.com/scipy/scipy/issues/14035>`__: \`roots_jacobi\` support for large parameter values
* `#14081 <https://github.com/scipy/scipy/issues/14081>`__: \`scipy.optimize._linprog_simplex._apply_pivot\` relies on asymmetric...
* `#14095 <https://github.com/scipy/scipy/issues/14095>`__: scipy.stats.norm.pdf takes too much time and memory
* `#14162 <https://github.com/scipy/scipy/issues/14162>`__: Thread safety RectBivariateSpline
* `#14267 <https://github.com/scipy/scipy/issues/14267>`__: BUG: online doc returns 404 - wrong \`reference\` in url
* `#14313 <https://github.com/scipy/scipy/issues/14313>`__: ks_2samp: example description does not match example output
* `#14418 <https://github.com/scipy/scipy/issues/14418>`__: \`ttest_ind\` for two sampled distributions with the same single...
* `#14455 <https://github.com/scipy/scipy/issues/14455>`__: Adds Mixed Integer Linear Programming from highs
* `#14462 <https://github.com/scipy/scipy/issues/14462>`__: Shapiro test returning negative p-value
* `#14471 <https://github.com/scipy/scipy/issues/14471>`__: methods 'revised simplex' and 'interior-point' are extremely...
* `#14505 <https://github.com/scipy/scipy/issues/14505>`__: \`Optimization converged to parameters that are outside the range\`...
* `#14527 <https://github.com/scipy/scipy/issues/14527>`__: Segmentation fault with KDTree
* `#14548 <https://github.com/scipy/scipy/issues/14548>`__: Add convention flag to quanternion in \`Scipy.spatial.transform.rotation.Rotation\`
* `#14565 <https://github.com/scipy/scipy/issues/14565>`__: optimize.minimize: Presence of callback causes method TNC to...
* `#14622 <https://github.com/scipy/scipy/issues/14622>`__: BUG: (sort of) mannwhitneyu hits max recursion limit with imbalanced...
* `#14645 <https://github.com/scipy/scipy/issues/14645>`__: ENH: MemoryError when trying to bootstrap with large amounts...
* `#14716 <https://github.com/scipy/scipy/issues/14716>`__: BUG: stats: The \`loguniform\` distribution is overparametrized.
* `#14731 <https://github.com/scipy/scipy/issues/14731>`__: BUG: Incorrect residual graph in scipy.sparse.csgraph.maximum_flow
* `#14745 <https://github.com/scipy/scipy/issues/14745>`__: BUG: scipy.ndimage.convolve documentation is incorrect
* `#14750 <https://github.com/scipy/scipy/issues/14750>`__: ENH: Add one more derivative-free optimization method
* `#14753 <https://github.com/scipy/scipy/issues/14753>`__: Offer to collaborate on truncated normal estimation by minimax...
* `#14777 <https://github.com/scipy/scipy/issues/14777>`__: BUG: Wrong limit and no warning in stats.t for df=np.inf
* `#14793 <https://github.com/scipy/scipy/issues/14793>`__: BUG: Missing pairs in cKDTree.query_pairs when coordinates contain...
* `#14861 <https://github.com/scipy/scipy/issues/14861>`__: BUG: unclear error message when all bounds are all equal for...
* `#14889 <https://github.com/scipy/scipy/issues/14889>`__: BUG: NumPy's \`random\` module should not be in the \`scipy\`...
* `#14914 <https://github.com/scipy/scipy/issues/14914>`__: CI job with code coverage is failing (yet again)
* `#14926 <https://github.com/scipy/scipy/issues/14926>`__: RegularGridInterpolator should be called RectilinearGridInterpolator
* `#14986 <https://github.com/scipy/scipy/issues/14986>`__: Prevent new Python versions from trying to install older releases...
* `#14994 <https://github.com/scipy/scipy/issues/14994>`__: BUG: Levy stable
* `#15009 <https://github.com/scipy/scipy/issues/15009>`__: BUG: scipy.stats.multiscale_graphcorr p-values are computed differently...
* `#15059 <https://github.com/scipy/scipy/issues/15059>`__: BUG: documentation inconsistent with code for find_peaks_cwt
* `#15082 <https://github.com/scipy/scipy/issues/15082>`__: DOC: Sampling from the truncated normal
* `#15110 <https://github.com/scipy/scipy/issues/15110>`__: BUG: truncnorm.cdf returns incorrect values at tail
* `#15125 <https://github.com/scipy/scipy/issues/15125>`__: Deprecate \`scipy.spatial.distance.kulsinski\`
* `#15133 <https://github.com/scipy/scipy/issues/15133>`__: BUG: Log_norm description is incorrect and produces incorrect...
* `#15150 <https://github.com/scipy/scipy/issues/15150>`__: BUG: RBFInterpolator is much slower than Rbf for vector data
* `#15172 <https://github.com/scipy/scipy/issues/15172>`__: BUG: special: High relative error in \`log_ndtr\`
* `#15195 <https://github.com/scipy/scipy/issues/15195>`__: BUGS: stats: Tracking issue for distributions that warn and/or...
* `#15199 <https://github.com/scipy/scipy/issues/15199>`__: BUG: Error occured \`spsolve_triangular\`
* `#15210 <https://github.com/scipy/scipy/issues/15210>`__: BUG: A sparse matrix raises a ValueError when \`__rmul__\` with...
* `#15245 <https://github.com/scipy/scipy/issues/15245>`__: MAINT: scipy.stats._levy_stable should be treated as subpackage...
* `#15252 <https://github.com/scipy/scipy/issues/15252>`__: DOC: Multivariate normal CDF docstring typo
* `#15296 <https://github.com/scipy/scipy/issues/15296>`__: BUG: SciPy 1.7.x build failure on Cygwin
* `#15308 <https://github.com/scipy/scipy/issues/15308>`__: BUG: OpenBLAS 0.3.18 support
* `#15338 <https://github.com/scipy/scipy/issues/15338>`__: DOC: Rename \`\*args\` param in \`f_oneway\` to \`\*samples\`
* `#15345 <https://github.com/scipy/scipy/issues/15345>`__: BUG: boschloo_exact gives pvalue > 1 (and sometimes nan)
* `#15368 <https://github.com/scipy/scipy/issues/15368>`__: build warnings for \`unuran_wrapper.pyx\`
* `#15373 <https://github.com/scipy/scipy/issues/15373>`__: BUG: Tippett’s and Pearson’s method for combine_pvalues are not...
* `#15415 <https://github.com/scipy/scipy/issues/15415>`__: \`integrate.quad_vec\` missing documentation for \`limit\` parameter
* `#15456 <https://github.com/scipy/scipy/issues/15456>`__: Segfault in HiGHS code when building with Mingw-w64 on Windows
* `#15458 <https://github.com/scipy/scipy/issues/15458>`__: DOC: Documentation inaccuracy of scipy.interpolate.bisplev
* `#15488 <https://github.com/scipy/scipy/issues/15488>`__: ENH: missing examples for scipy.optimize in docs
* `#15507 <https://github.com/scipy/scipy/issues/15507>`__: BUG: scipy.optimize.linprog: the algorithm determines the problem...
* `#15508 <https://github.com/scipy/scipy/issues/15508>`__: BUG: Incorrect error message in multivariate_normal
* `#15541 <https://github.com/scipy/scipy/issues/15541>`__: BUG: scipy.stats.powerlaw, why should x ∈ (0,1)? x can exceed...
* `#15551 <https://github.com/scipy/scipy/issues/15551>`__: MAINT: stats: deprecating non-numeric array support in \`stats.mode\`
* `#15568 <https://github.com/scipy/scipy/issues/15568>`__: BENCH/CI: Benchmark timeout
* `#15572 <https://github.com/scipy/scipy/issues/15572>`__: BUG: \`scipy.spatial.transform.rotation\`, wrong deprecation...
* `#15575 <https://github.com/scipy/scipy/issues/15575>`__: BUG: Tests failing for initial build [arm64 machine]
* `#15589 <https://github.com/scipy/scipy/issues/15589>`__: BUG: scipy.special.factorialk docstring inconsistent with behaviour
* `#15601 <https://github.com/scipy/scipy/issues/15601>`__: BUG: Scalefactors for \`signal.csd\` with \`average=='median'\`...
* `#15617 <https://github.com/scipy/scipy/issues/15617>`__: ENH: stats: all multivariate distributions should be freezable
* `#15631 <https://github.com/scipy/scipy/issues/15631>`__: BUG: stats.fit: intermittent failure in doctest
* `#15635 <https://github.com/scipy/scipy/issues/15635>`__: CI:ASK: Remove LaTeX doc builds?
* `#15638 <https://github.com/scipy/scipy/issues/15638>`__: DEV: \`dev.py\` missing PYTHONPATH when building doc
* `#15644 <https://github.com/scipy/scipy/issues/15644>`__: DOC: stats.ks_1samp: incorrect commentary in examples
* `#15666 <https://github.com/scipy/scipy/issues/15666>`__: CI: CircleCI build_docs failure on main
* `#15670 <https://github.com/scipy/scipy/issues/15670>`__: BUG: AssertionError in test__dual_annealing.py in test_bounds_class
* `#15689 <https://github.com/scipy/scipy/issues/15689>`__: BUG: default value of shape parameter in fit method of rv_continuous...
* `#15692 <https://github.com/scipy/scipy/issues/15692>`__: CI: scipy.scipy (Main refguide_asv_check) failure in main
* `#15696 <https://github.com/scipy/scipy/issues/15696>`__: DOC: False information in docs - scipy.stats.ttest_1samp
* `#15700 <https://github.com/scipy/scipy/issues/15700>`__: BUG: AssertionError in test_propack.py
* `#15730 <https://github.com/scipy/scipy/issues/15730>`__: BUG: "terminate called after throwing an instance of 'std::out_of_range'"...
* `#15732 <https://github.com/scipy/scipy/issues/15732>`__: DEP: execute deprecation of inexact indices into sparse matrices
* `#15734 <https://github.com/scipy/scipy/issues/15734>`__: DEP: deal with deprecation of ndim >1 in bspline
* `#15735 <https://github.com/scipy/scipy/issues/15735>`__: DEP: add actual DeprecationWarning for sym_pos-keyword of scipy.linalg.solve
* `#15736 <https://github.com/scipy/scipy/issues/15736>`__: DEP: Remove \`debug\` keyword from \`scipy.linalg.solve_\*\`
* `#15737 <https://github.com/scipy/scipy/issues/15737>`__: DEP: Execute deprecation of pinv2
* `#15739 <https://github.com/scipy/scipy/issues/15739>`__: DEP: sharpen deprecation for >1-dim inputs in optimize.minimize
* `#15740 <https://github.com/scipy/scipy/issues/15740>`__: DEP: Execute deprecation for squeezing input vectors in spatial.distance
* `#15741 <https://github.com/scipy/scipy/issues/15741>`__: DEP: remove spatial.distance.matching
* `#15742 <https://github.com/scipy/scipy/issues/15742>`__: DEP: raise if fillvalue cannot be cast to output type in \`signal.convolve2d\`
* `#15743 <https://github.com/scipy/scipy/issues/15743>`__: DEP: enforce radius for \`spatial.SphericalVoronoi\`
* `#15744 <https://github.com/scipy/scipy/issues/15744>`__: DEP: sharpen deprecation of dual_annealing argument 'local_search_options'
* `#15745 <https://github.com/scipy/scipy/issues/15745>`__: DEP: remove signal.windows.hanning
* `#15746 <https://github.com/scipy/scipy/issues/15746>`__: DEP: remove k=None from KDTree.query
* `#15747 <https://github.com/scipy/scipy/issues/15747>`__: DEP: stats: remove support for \`_rvs\` without \`size\` parameter
* `#15750 <https://github.com/scipy/scipy/issues/15750>`__: DEP: remove \`n_jobs\` from kdtree
* `#15751 <https://github.com/scipy/scipy/issues/15751>`__: DEP: remove ftol/xtol from neldermead
* `#15752 <https://github.com/scipy/scipy/issues/15752>`__: DEP: remove right keyword from interpolate.PPoly.extend
* `#15753 <https://github.com/scipy/scipy/issues/15753>`__: DEP: remove \`_ppform\`
* `#15754 <https://github.com/scipy/scipy/issues/15754>`__: DEP: Remove mlab mode from dendrogram
* `#15757 <https://github.com/scipy/scipy/issues/15757>`__: DEP: docstring-related deprecations
* `#15758 <https://github.com/scipy/scipy/issues/15758>`__: DEP: remove LAPACK \*gegv functions
* `#15759 <https://github.com/scipy/scipy/issues/15759>`__: DEP: remove old BSR methods
* `#15760 <https://github.com/scipy/scipy/issues/15760>`__: DEP: remove py_vq2
* `#15761 <https://github.com/scipy/scipy/issues/15761>`__: DEP: remove stats.itemfreq
* `#15762 <https://github.com/scipy/scipy/issues/15762>`__: DEP: remove stats.median_absolute_deviation
* `#15773 <https://github.com/scipy/scipy/issues/15773>`__: BUG: iirfilter allows Wn[1] < Wn[0] for band-pass and band-stop...
* `#15780 <https://github.com/scipy/scipy/issues/15780>`__: BUG: CI on Azure broken with PyTest 7.1
* `#15843 <https://github.com/scipy/scipy/issues/15843>`__: BUG: scipy.stats.brunnermunzel incorrectly returns nan for undocumented...
* `#15854 <https://github.com/scipy/scipy/issues/15854>`__: CI: Windows Meson job failing sometimes on OpenBLAS binary download
* `#15866 <https://github.com/scipy/scipy/issues/15866>`__: BUG/CI: Wrong python version used for tests labeled "Linux Tests...
* `#15871 <https://github.com/scipy/scipy/issues/15871>`__: BUG: stats: Test failure of \`TestTruncnorm.test_moments\` on...
* `#15899 <https://github.com/scipy/scipy/issues/15899>`__: BUG: _calc_uniform_order_statistic_medians documentation example...
* `#15927 <https://github.com/scipy/scipy/issues/15927>`__: BUG: Inconsistent handling of INF and NAN in signal.convolve
* `#15931 <https://github.com/scipy/scipy/issues/15931>`__: BUG: scipy/io/arff/tests/test_arffread.py::TestNoData::test_nodata...
* `#15960 <https://github.com/scipy/scipy/issues/15960>`__: BUG: Documentation Error in scipy.signal.lfilter
* `#15961 <https://github.com/scipy/scipy/issues/15961>`__: BUG: scipy.stats.beta and bernoulli fails with float32 inputs
* `#15962 <https://github.com/scipy/scipy/issues/15962>`__: Race condition in macOS Meson build between \`_matfuncs_expm\`...
* `#15987 <https://github.com/scipy/scipy/issues/15987>`__: CI: \`np.matrix\` deprecation warning
* `#16007 <https://github.com/scipy/scipy/issues/16007>`__: BUG: Confusing documentation in \`ttest_ind_from_stats\`
* `#16011 <https://github.com/scipy/scipy/issues/16011>`__: BUG: typo in documentation for scipy.optimize.basinhopping
* `#16020 <https://github.com/scipy/scipy/issues/16020>`__: BUG: dev.py FileNotFoundError
* `#16027 <https://github.com/scipy/scipy/issues/16027>`__: jc should be (n-1)/2
* `#16031 <https://github.com/scipy/scipy/issues/16031>`__: BUG: scipy.sparse.linalg.norm does not work on sparse arrays
* `#16036 <https://github.com/scipy/scipy/issues/16036>`__: Missing \`f\` prefix on f-strings
* `#16054 <https://github.com/scipy/scipy/issues/16054>`__: Bug: Meson build with dev.py fails to detect SciPy with debian...
* `#16065 <https://github.com/scipy/scipy/issues/16065>`__: BUG: Gitpod build with \`python runtests.py\` fails; move to...
* `#16074 <https://github.com/scipy/scipy/issues/16074>`__: BUG: refguide check fails with \`numpydoc==1.3\`
* `#16081 <https://github.com/scipy/scipy/issues/16081>`__: CI, MAINT: minor refguide failure with stats.describe
* `#16121 <https://github.com/scipy/scipy/issues/16121>`__: DOC: scipy.interpolate.RegularGridInterpolator and interpn works...
* `#16162 <https://github.com/scipy/scipy/issues/16162>`__: BUG: curve_fit gives wrong results with Pandas float32
* `#16171 <https://github.com/scipy/scipy/issues/16171>`__: BUG: scipy.stats.multivariate_hypergeom.rvs raises ValueError...
* `#16219 <https://github.com/scipy/scipy/issues/16219>`__: \`TestSobol.test_0dim\` failure on 32-bit Linux job
* `#16233 <https://github.com/scipy/scipy/issues/16233>`__: BUG: Memory leak in function \`sf_error\` due to new reference...
* `#16254 <https://github.com/scipy/scipy/issues/16254>`__: DEP: add deprecation warning to \`maxiter\` kwarg in \`_minimize_tnc\`
* `#16292 <https://github.com/scipy/scipy/issues/16292>`__: BUG: compilation error: no matching constructor for initialization...
* `#16300 <https://github.com/scipy/scipy/issues/16300>`__: BLD: pip install build issue with meson in Ubuntu virtualenv
* `#16337 <https://github.com/scipy/scipy/issues/16337>`__: TST: stats/tests/test_axis_nan_policy.py::test_axis_nan_policy_full...
* `#16347 <https://github.com/scipy/scipy/issues/16347>`__: TST, MAINT: 32-bit Linux test failures in wheels repo
* `#16358 <https://github.com/scipy/scipy/issues/16358>`__: TST, MAINT: test_theilslopes_warnings fails on 32-bit Windows
* `#16378 <https://github.com/scipy/scipy/issues/16378>`__: DOC: pydata-sphinx-theme v0.9 defaults to darkmode depending...
* `#16381 <https://github.com/scipy/scipy/issues/16381>`__: BUG: bootstrap get ValueError for paired statistic
* `#16382 <https://github.com/scipy/scipy/issues/16382>`__: BUG: truncnorm.fit does not fit correctly
* `#16403 <https://github.com/scipy/scipy/issues/16403>`__: MAINT: NumPy main will require a few updates due to new floating...
* `#16409 <https://github.com/scipy/scipy/issues/16409>`__: BUG: SIGSEGV in qhull when array type is wrong
* `#16418 <https://github.com/scipy/scipy/issues/16418>`__: BUG: breaking change: scipy.stats.mode returned value has changed...
* `#16419 <https://github.com/scipy/scipy/issues/16419>`__: BUG: scipy.stats.nbinom.logcdf returns wrong results when some...
* `#16426 <https://github.com/scipy/scipy/issues/16426>`__: BUG: stats.shapiro inplace modification of user array
* `#16446 <https://github.com/scipy/scipy/issues/16446>`__: BUG: Issue with stripping on macOS Monterey + xcode 13.2
* `#16465 <https://github.com/scipy/scipy/issues/16465>`__: BLD: new sdist has some metadata issues
* `#16466 <https://github.com/scipy/scipy/issues/16466>`__: BUG: linprog failure - OptimizeResult.x returns NoneType
* `#16495 <https://github.com/scipy/scipy/issues/16495>`__: HiGHS does not compile on windows (on conda-forge infra)
* `#16523 <https://github.com/scipy/scipy/issues/16523>`__: BUG: test failure in pre-release job: \`TestFactorized.test_singular_with_umfpack\`
* `#16540 <https://github.com/scipy/scipy/issues/16540>`__: BLD: meson 0.63.0 and new CI testing failures on Linux
* `#16555 <https://github.com/scipy/scipy/issues/16555>`__: Building 1.9.x branch from source requires fix in meson-python...
* `#16609 <https://github.com/scipy/scipy/issues/16609>`__: BUG: \`scipy.optimize.linprog\` reports optimal for trivially...
* `#16681 <https://github.com/scipy/scipy/issues/16681>`__: BUG: linprog integrality only accepts list, not array
* `#16718 <https://github.com/scipy/scipy/issues/16718>`__: BUG: memoryview error with Cython 0.29.31

***********************
Pull requests for 1.9.0
***********************

* `#9523 <https://github.com/scipy/scipy/pull/9523>`__: ENH: improvements to the Stable distribution
* `#11829 <https://github.com/scipy/scipy/pull/11829>`__: Fixes safe handling of small singular values in svds.
* `#13490 <https://github.com/scipy/scipy/pull/13490>`__: DEV: stats: check for distribution/method keyword name collisions
* `#13572 <https://github.com/scipy/scipy/pull/13572>`__: ENH: n-D and nan_policy support for scipy.stats.percentileofscore
* `#13918 <https://github.com/scipy/scipy/pull/13918>`__: ENH: Poisson Disk sampling for QMC
* `#13955 <https://github.com/scipy/scipy/pull/13955>`__: DOC: SciPy extensions for code style and docstring guidelines.
* `#14003 <https://github.com/scipy/scipy/pull/14003>`__: DOC: clarify the definition of the pdf of \`stats.fisk\`
* `#14036 <https://github.com/scipy/scipy/pull/14036>`__: ENH: fix numerical issues in roots_jacobi and related special...
* `#14087 <https://github.com/scipy/scipy/pull/14087>`__: DOC: explain null hypotheses in ttest functions
* `#14142 <https://github.com/scipy/scipy/pull/14142>`__: DOC: Add better error message for unpacking issue
* `#14143 <https://github.com/scipy/scipy/pull/14143>`__: Support LinearOperator in expm_multiply
* `#14300 <https://github.com/scipy/scipy/pull/14300>`__: ENH: Adding DIRECT algorithm to \`\`scipy.optimize\`\`
* `#14576 <https://github.com/scipy/scipy/pull/14576>`__: ENH: stats: add one-sample Monte Carlo hypothesis test
* `#14642 <https://github.com/scipy/scipy/pull/14642>`__: ENH: add Lloyd's algorithm to \`scipy.spatial\` to improve a...
* `#14718 <https://github.com/scipy/scipy/pull/14718>`__: DOC: stats: adjust bootstrap doc to emphasize that batch controls...
* `#14781 <https://github.com/scipy/scipy/pull/14781>`__: BUG: stats: handle infinite \`df\` in \`t\` distribution
* `#14847 <https://github.com/scipy/scipy/pull/14847>`__: ENH: BLD: enable building SciPy with Meson
* `#14877 <https://github.com/scipy/scipy/pull/14877>`__: DOC: ndimage convolve origin documentation (#14745)
* `#15001 <https://github.com/scipy/scipy/pull/15001>`__: ENH: sparse.linalg: More comprehensive tests (Not only for 1-D...
* `#15026 <https://github.com/scipy/scipy/pull/15026>`__: ENH: allow approx_fprime to work with vector-valued func
* `#15079 <https://github.com/scipy/scipy/pull/15079>`__: ENH:linalg: expm overhaul and ndarray processing
* `#15140 <https://github.com/scipy/scipy/pull/15140>`__: ENH: Make \`stats.kappa3\` work with array inputs
* `#15154 <https://github.com/scipy/scipy/pull/15154>`__: DOC: a small bug in docstring example of \`lobpcg\`
* `#15165 <https://github.com/scipy/scipy/pull/15165>`__: MAINT: Avoid using del to remove numpy symbols in scipy.__init__.py
* `#15168 <https://github.com/scipy/scipy/pull/15168>`__: REL: set version to 1.9.0.dev0
* `#15169 <https://github.com/scipy/scipy/pull/15169>`__: DOC: fix formatting of Methods in multivariate distributions
* `#15171 <https://github.com/scipy/scipy/pull/15171>`__: \`AttrDict\` raises \`AttributeError\` on missing attributes,...
* `#15176 <https://github.com/scipy/scipy/pull/15176>`__: BUG: special: Clean up some private namespaces and fix \`special.__all__\`
* `#15182 <https://github.com/scipy/scipy/pull/15182>`__: MAINT: fix typos principle -> principal
* `#15184 <https://github.com/scipy/scipy/pull/15184>`__: MAINT: CI: Rename 'Nightly CPython' job to 'NumPy main'
* `#15187 <https://github.com/scipy/scipy/pull/15187>`__: BUG: special: Fix numerical precision issue of log_ndtr
* `#15188 <https://github.com/scipy/scipy/pull/15188>`__: MAINT: sparse.linalg: Using more concise and user-friendly f-string...
* `#15190 <https://github.com/scipy/scipy/pull/15190>`__: MAINT: interpolate: speed up the RBFInterpolator evaluation with...
* `#15196 <https://github.com/scipy/scipy/pull/15196>`__: BUG: stats: Fix handling of support endpoints in two distributions.
* `#15197 <https://github.com/scipy/scipy/pull/15197>`__: MAINT: build dependency updates
* `#15202 <https://github.com/scipy/scipy/pull/15202>`__: MAINT: special: Don't use macro for 'extern "C"' in strictly...
* `#15205 <https://github.com/scipy/scipy/pull/15205>`__: BUG: stats: Fix spurious warnings generated by several distributions.
* `#15207 <https://github.com/scipy/scipy/pull/15207>`__: MAINT: sparse.linalg: Using the interface with the trace of sparse...
* `#15219 <https://github.com/scipy/scipy/pull/15219>`__: DOC: Corrected docstring of ndimage.sum_labels
* `#15223 <https://github.com/scipy/scipy/pull/15223>`__: DOC: x0->x for finite_diff_rel_step docstring closes #15208
* `#15230 <https://github.com/scipy/scipy/pull/15230>`__: ENH: expose submodules via \`__getattr__\` to allow lazy access
* `#15234 <https://github.com/scipy/scipy/pull/15234>`__: TST: stats: mark very slow tests as \`xslow\`
* `#15235 <https://github.com/scipy/scipy/pull/15235>`__: BUG: Fix rmul dispatch of spmatrix
* `#15243 <https://github.com/scipy/scipy/pull/15243>`__: DOC: stats: add reference for gstd
* `#15244 <https://github.com/scipy/scipy/pull/15244>`__: Added example for morphology: binary_dilation and erosion
* `#15250 <https://github.com/scipy/scipy/pull/15250>`__: ENH: Make \`stats.kappa4\` work with array
* `#15251 <https://github.com/scipy/scipy/pull/15251>`__: [MRG] ENH: Update \`laplacian\` function introducing the new...
* `#15255 <https://github.com/scipy/scipy/pull/15255>`__: MAINT: Remove \`distutils\` usage in \`runtests.py\` to fix deprecation...
* `#15259 <https://github.com/scipy/scipy/pull/15259>`__: MAINT: optimize, special, signal: Use custom warnings instead...
* `#15261 <https://github.com/scipy/scipy/pull/15261>`__: DOC: Add inline comment in Hausdorff distance calculation
* `#15265 <https://github.com/scipy/scipy/pull/15265>`__: DOC: update .mailmap
* `#15266 <https://github.com/scipy/scipy/pull/15266>`__: CI: remove coverage usage from Windows jobs
* `#15269 <https://github.com/scipy/scipy/pull/15269>`__: BLD: add setup.py for \`stats/_levy_stable\`
* `#15272 <https://github.com/scipy/scipy/pull/15272>`__: BUG: Fix owens_t function when a tends to infinity
* `#15274 <https://github.com/scipy/scipy/pull/15274>`__: DOC: fix docstring in _cdf() function of _multivariate.py
* `#15284 <https://github.com/scipy/scipy/pull/15284>`__: TST: silence RuntimeWarning from \`np.det\` in \`signal.place_poles\`...
* `#15285 <https://github.com/scipy/scipy/pull/15285>`__: CI: simplify 32-bit Linux testing
* `#15286 <https://github.com/scipy/scipy/pull/15286>`__: MAINT: Highs submodule CI issue - use shallow cloning
* `#15289 <https://github.com/scipy/scipy/pull/15289>`__: DOC: Misc numpydoc formatting.
* `#15291 <https://github.com/scipy/scipy/pull/15291>`__: DOC: some more docstring/numpydoc formatting.
* `#15294 <https://github.com/scipy/scipy/pull/15294>`__: ENH: add integrality constraints for linprog
* `#15300 <https://github.com/scipy/scipy/pull/15300>`__: DOC: Misc manual docs updates.
* `#15302 <https://github.com/scipy/scipy/pull/15302>`__: DOC: More docstring reformatting.
* `#15304 <https://github.com/scipy/scipy/pull/15304>`__: CI: fix Gitpod build by adding HiGHS submodule checkout
* `#15305 <https://github.com/scipy/scipy/pull/15305>`__: BLD: update NumPy to >=1.18.5, setuptools to <60.0
* `#15309 <https://github.com/scipy/scipy/pull/15309>`__: CI: update OpenBLAS to 0.3.18 in Azure jobs
* `#15310 <https://github.com/scipy/scipy/pull/15310>`__: ENH: signal: Add Kaiser-Bessel derived window function
* `#15312 <https://github.com/scipy/scipy/pull/15312>`__: BUG: special: Fix loss of precision in pseudo_huber when r/delta...
* `#15314 <https://github.com/scipy/scipy/pull/15314>`__: MAINT: changed needed after renaming \`master\` branch to \`main\`
* `#15315 <https://github.com/scipy/scipy/pull/15315>`__: MAINT: account for NumPy master -> main renaming
* `#15325 <https://github.com/scipy/scipy/pull/15325>`__: CI: reshuffle two Windows Azure CI jobs, and don't run 'full'...
* `#15330 <https://github.com/scipy/scipy/pull/15330>`__: ENH: optimize: support undocumented option \`full_output\` for...
* `#15336 <https://github.com/scipy/scipy/pull/15336>`__: DOC: update detailed roadmap
* `#15344 <https://github.com/scipy/scipy/pull/15344>`__: MAINT:stats: Renamed \`\*args\` param to \`\*samples\`
* `#15347 <https://github.com/scipy/scipy/pull/15347>`__: ENH: stats: add weights in harmonic mean
* `#15352 <https://github.com/scipy/scipy/pull/15352>`__: BLD: put upper bound \`setuptools<60.0\` in conda environment...
* `#15357 <https://github.com/scipy/scipy/pull/15357>`__: ENH: interpolate: add new methods for RegularGridInterpolator.
* `#15360 <https://github.com/scipy/scipy/pull/15360>`__: MAINT: speed up rvs of nakagami in scipy.stats
* `#15361 <https://github.com/scipy/scipy/pull/15361>`__: MAINT: sparse.linalg: Remove unnecessary operations
* `#15366 <https://github.com/scipy/scipy/pull/15366>`__: Make signal functions respect input dtype.
* `#15370 <https://github.com/scipy/scipy/pull/15370>`__: DOC: governance members moved to scipy.org
* `#15371 <https://github.com/scipy/scipy/pull/15371>`__: MAINT: stats: fix unuran compile-time warnings
* `#15378 <https://github.com/scipy/scipy/pull/15378>`__: MAINT: remove version pinning on gmpy2
* `#15380 <https://github.com/scipy/scipy/pull/15380>`__: ENH/MAINT: Version switcher from the sphinx theme
* `#15385 <https://github.com/scipy/scipy/pull/15385>`__: DOC: fix typo
* `#15387 <https://github.com/scipy/scipy/pull/15387>`__: MAINT: Fix a couple build warnings.
* `#15388 <https://github.com/scipy/scipy/pull/15388>`__: DOC: interpolate: improve \`RectBivariateSpline\` doc
* `#15391 <https://github.com/scipy/scipy/pull/15391>`__: ENH: graph Laplacian as LinearOperator, add dtype and symmetrized...
* `#15392 <https://github.com/scipy/scipy/pull/15392>`__: ENH: integrality constraints for differential_evolution
* `#15394 <https://github.com/scipy/scipy/pull/15394>`__: ENH: optimize: improvements to \`LinearConstraint\` class
* `#15396 <https://github.com/scipy/scipy/pull/15396>`__: DOC: Git:// protocol on github pending removal.
* `#15399 <https://github.com/scipy/scipy/pull/15399>`__: ENH: stats: add \`axis\` tuple and \`nan_policy\` to \`hmean\`
* `#15400 <https://github.com/scipy/scipy/pull/15400>`__: MAINT: sparse.linalg: Move the test function of GMRES to the...
* `#15401 <https://github.com/scipy/scipy/pull/15401>`__: MAINT: DOC: analytics from analytics.scientific-python
* `#15402 <https://github.com/scipy/scipy/pull/15402>`__: DOC: update pip_quickstart (submodules)
* `#15406 <https://github.com/scipy/scipy/pull/15406>`__: MAINT: use \`Rotation.Random\` instead of manual generation
* `#15407 <https://github.com/scipy/scipy/pull/15407>`__: BLD: meson: split pyx->c and Python extension build
* `#15408 <https://github.com/scipy/scipy/pull/15408>`__: MAINT: check for negative weights in \`Rotation.align_vectors\`
* `#15410 <https://github.com/scipy/scipy/pull/15410>`__: ENH: add \`order\` parameter to specify quaternion format
* `#15413 <https://github.com/scipy/scipy/pull/15413>`__: ENH: stats: add \`rvs\` method for \`gennorm\`
* `#15424 <https://github.com/scipy/scipy/pull/15424>`__: ENH: bypass LinearOperator in lobpcg for small-size cases
* `#15427 <https://github.com/scipy/scipy/pull/15427>`__: MAINT: Manage imports in \`sparse.linalg\`
* `#15431 <https://github.com/scipy/scipy/pull/15431>`__: Revert "ENH: add \`order\` parameter to specify quaternion format"
* `#15436 <https://github.com/scipy/scipy/pull/15436>`__: ENH: stats: fit: function for fitting discrete and continuous...
* `#15439 <https://github.com/scipy/scipy/pull/15439>`__: ENH: differential_evolution vectorized kwd
* `#15440 <https://github.com/scipy/scipy/pull/15440>`__: MAINT: Try to detect scipy path in \`runtests.py\` while not...
* `#15442 <https://github.com/scipy/scipy/pull/15442>`__: MAINT: Fix meson build warnings on windows
* `#15443 <https://github.com/scipy/scipy/pull/15443>`__: DOC, BUG: Fix error in heading remapping for custom \`scipy.optimize:function\` domain directive
* `#15445 <https://github.com/scipy/scipy/pull/15445>`__: ENH: stats: add \`nnlf\` method for discrete distributions
* `#15451 <https://github.com/scipy/scipy/pull/15451>`__: BLD: further refinement of Cython dependencies
* `#15452 <https://github.com/scipy/scipy/pull/15452>`__: BUG/DOC/TST: combine_pvalues: fix Tippett and Pearson
* `#15453 <https://github.com/scipy/scipy/pull/15453>`__: ENH: Make dual_annealing work with Bounds class
* `#15454 <https://github.com/scipy/scipy/pull/15454>`__: BLD: remove dependency on libnpymath from \`spatial._distance_wrap\`
* `#15455 <https://github.com/scipy/scipy/pull/15455>`__: ENH: Support Bounds class in shgo
* `#15459 <https://github.com/scipy/scipy/pull/15459>`__: DOC: documents parameter \`limit\` for function \`integrate.quad_vec\`.
* `#15460 <https://github.com/scipy/scipy/pull/15460>`__: ENH: optimize: milp: mixed integer linear programming
* `#15462 <https://github.com/scipy/scipy/pull/15462>`__: CI: switch one macOS CI job from distutils to meson
* `#15464 <https://github.com/scipy/scipy/pull/15464>`__: ENH: Performance improvements for \`linear_sum_assignment\`
* `#15465 <https://github.com/scipy/scipy/pull/15465>`__: DOC: stats: add weights in formulas and examples for gmean and...
* `#15466 <https://github.com/scipy/scipy/pull/15466>`__: MAINT: fix compile errors with CPython 3.11
* `#15469 <https://github.com/scipy/scipy/pull/15469>`__: MAINT: Remove \`distutils\` usage
* `#15470 <https://github.com/scipy/scipy/pull/15470>`__: ENH: \`stats.qmc\`: faster hypercube point comparison and scrambling...
* `#15472 <https://github.com/scipy/scipy/pull/15472>`__: ENH: stats: add \`axis\` tuple and \`nan_policy\` to \`skew\`
* `#15485 <https://github.com/scipy/scipy/pull/15485>`__: BLD: updates to Meson build files for more correct linking and...
* `#15487 <https://github.com/scipy/scipy/pull/15487>`__: MAINT: typo in bsplines.py
* `#15496 <https://github.com/scipy/scipy/pull/15496>`__: DOC: signal: fixed parameter 'order' for butter bandpass
* `#15497 <https://github.com/scipy/scipy/pull/15497>`__: MAINT: update vendored uarray
* `#15499 <https://github.com/scipy/scipy/pull/15499>`__: CI: remove matplotlib from 32-bit linux job, it fails to build
* `#15501 <https://github.com/scipy/scipy/pull/15501>`__: MAINT: Remove unused variable warnings
* `#15502 <https://github.com/scipy/scipy/pull/15502>`__: DEV: meson: allow specifying build directory and install prefix
* `#15512 <https://github.com/scipy/scipy/pull/15512>`__: MAINT: optimize.linprog: make HiGHS default and deprecate old...
* `#15523 <https://github.com/scipy/scipy/pull/15523>`__: DOC: fixed the link for fluiddyn's transonic vision in dev/roadmap.html.
* `#15526 <https://github.com/scipy/scipy/pull/15526>`__: MAINT: add qrvs method to NumericalInversePolynomial in scipy.stats
* `#15529 <https://github.com/scipy/scipy/pull/15529>`__: DOC: forward port 1.8.0 relnotes
* `#15532 <https://github.com/scipy/scipy/pull/15532>`__: TST: parametrize test_ldl_type_size_combinations
* `#15546 <https://github.com/scipy/scipy/pull/15546>`__: DOC: missing section for metrics
* `#15555 <https://github.com/scipy/scipy/pull/15555>`__: MAINT: make unuran clone shallow
* `#15557 <https://github.com/scipy/scipy/pull/15557>`__: DOC: fixes inaccuracy in bisplev documentation
* `#15559 <https://github.com/scipy/scipy/pull/15559>`__: BENCH: selection of linalg solvers to facilitate expansion
* `#15560 <https://github.com/scipy/scipy/pull/15560>`__: DOC: types and return values for Bessel Functions
* `#15561 <https://github.com/scipy/scipy/pull/15561>`__: MAINT: update HiGHS submodule to include fix for Windows segfault
* `#15563 <https://github.com/scipy/scipy/pull/15563>`__: CI: add a Windows CI job on GitHub Actions using Meson
* `#15564 <https://github.com/scipy/scipy/pull/15564>`__: DOC: stray backticks
* `#15565 <https://github.com/scipy/scipy/pull/15565>`__: DOC: incorrect underline lenght in section.
* `#15567 <https://github.com/scipy/scipy/pull/15567>`__: ENH: stats.pareto fit improvement for parameter combinations
* `#15569 <https://github.com/scipy/scipy/pull/15569>`__: DOC: pip quickstart: setup.py -> meson
* `#15570 <https://github.com/scipy/scipy/pull/15570>`__: MAINT: bump test tolerance in test_linprog
* `#15571 <https://github.com/scipy/scipy/pull/15571>`__: DOC: Wrong underline length
* `#15578 <https://github.com/scipy/scipy/pull/15578>`__: Make Windows Python setup more standard
* `#15581 <https://github.com/scipy/scipy/pull/15581>`__: MAINT: clarify deprecation warning spatial.transform.rotation
* `#15583 <https://github.com/scipy/scipy/pull/15583>`__: DOC: clarify O(N) SO(N) in random rotations
* `#15586 <https://github.com/scipy/scipy/pull/15586>`__: ENH: stats: Add 'alternative' and confidence interval to pearsonr
* `#15590 <https://github.com/scipy/scipy/pull/15590>`__: DOC: factorialk docstring inconsistent with code
* `#15597 <https://github.com/scipy/scipy/pull/15597>`__: DOC: update \`hyp2f1\` docstring example based on doctest
* `#15598 <https://github.com/scipy/scipy/pull/15598>`__: BUG/ENH: \`lsq_linear\`: fixed incorrect \`lsmr_tol\` in first...
* `#15603 <https://github.com/scipy/scipy/pull/15603>`__: BENCH: optimize: milp: add MILP benchmarks
* `#15606 <https://github.com/scipy/scipy/pull/15606>`__: MAINT: allow multiplication sign \`×\`
* `#15611 <https://github.com/scipy/scipy/pull/15611>`__: BUG:signal: Fix median bias in csd(..., average="median")
* `#15616 <https://github.com/scipy/scipy/pull/15616>`__: CI: pin asv to avoid slowdowns in 0.5/0.5.1
* `#15619 <https://github.com/scipy/scipy/pull/15619>`__: DOC: stats: update interval and moment method signatures
* `#15625 <https://github.com/scipy/scipy/pull/15625>`__: MAINT: Clean up \`type: ignore\` comments related to third-party...
* `#15626 <https://github.com/scipy/scipy/pull/15626>`__: TST, MAINT: ignore np distutils dep
* `#15629 <https://github.com/scipy/scipy/pull/15629>`__: MAINT: stats: fix \`trim1\` \`axis\` behavior
* `#15632 <https://github.com/scipy/scipy/pull/15632>`__: ENH: stats.wilcoxon: return z-statistic (as requested)
* `#15634 <https://github.com/scipy/scipy/pull/15634>`__: CI: Improve concurrency to cancel running jobs on PR update
* `#15645 <https://github.com/scipy/scipy/pull/15645>`__: DOC: Add code example to the documentation of \`sparse.linalg.cg\`.
* `#15646 <https://github.com/scipy/scipy/pull/15646>`__: DOC: stats.ks_1samp: correct examples
* `#15647 <https://github.com/scipy/scipy/pull/15647>`__: ENH: add variable bits to \`stats.qmc.Sobol\`
* `#15648 <https://github.com/scipy/scipy/pull/15648>`__: DOC: Add examples to documentation for \`scipy.special.ellipr{c,d,f,g,j}\`
* `#15649 <https://github.com/scipy/scipy/pull/15649>`__: DEV/DOC: remove latex/pdf documentation
* `#15651 <https://github.com/scipy/scipy/pull/15651>`__: DOC: stats.ks_2samp/stats.kstest: correct examples
* `#15652 <https://github.com/scipy/scipy/pull/15652>`__: DOC: stats.circstd: add reference, notes, comments
* `#15655 <https://github.com/scipy/scipy/pull/15655>`__: REL: fix small issue in pavement.py for release note writing
* `#15656 <https://github.com/scipy/scipy/pull/15656>`__: DOC: Fix example for subset_by_index in eigh doc
* `#15661 <https://github.com/scipy/scipy/pull/15661>`__: DOC: Additional examples for optimize user guide
* `#15662 <https://github.com/scipy/scipy/pull/15662>`__: DOC: stats.fit: fix intermittent failure in doctest
* `#15663 <https://github.com/scipy/scipy/pull/15663>`__: DOC: stats.burr12: fix typo
* `#15664 <https://github.com/scipy/scipy/pull/15664>`__: BENCH: Add benchmarks for special.factorial/factorial2/factorialk
* `#15673 <https://github.com/scipy/scipy/pull/15673>`__: DOC: fix intersphinx links
* `#15682 <https://github.com/scipy/scipy/pull/15682>`__: MAINT: sparse.linalg: Clear up unnecessary modules imported in...
* `#15684 <https://github.com/scipy/scipy/pull/15684>`__: DOC: add formula and documentation improvements for scipy.special.chndtr...
* `#15690 <https://github.com/scipy/scipy/pull/15690>`__: ENH: add uarray multimethods for fast Hankel transforms
* `#15694 <https://github.com/scipy/scipy/pull/15694>`__: MAINT,CI: signal: fix failing refguide check
* `#15699 <https://github.com/scipy/scipy/pull/15699>`__: DOC: stats.ttest_1samp: update example
* `#15701 <https://github.com/scipy/scipy/pull/15701>`__: BUG: Fix dual_annealing bounds test
* `#15703 <https://github.com/scipy/scipy/pull/15703>`__: BUG: fix test fail in test_propack.py (loosen atol)
* `#15710 <https://github.com/scipy/scipy/pull/15710>`__: MAINT: sparse.linalg: \`bnorm\` only calculate once
* `#15712 <https://github.com/scipy/scipy/pull/15712>`__: ENH: \`scipy.stats.qmc.Sobol\`: allow 32 or 64 bit computation
* `#15715 <https://github.com/scipy/scipy/pull/15715>`__: ENH: stats: add _axis_nan_policy_factory to moment
* `#15718 <https://github.com/scipy/scipy/pull/15718>`__: ENH: Migration of \`write_release_and_log\` into standalone script
* `#15723 <https://github.com/scipy/scipy/pull/15723>`__: TST: stats: make \`check_sample_var\` two-sided
* `#15724 <https://github.com/scipy/scipy/pull/15724>`__: TST: stats: simplify \`check_sample_mean\`
* `#15725 <https://github.com/scipy/scipy/pull/15725>`__: DEV: Try to detect scipy from dev installed path
* `#15728 <https://github.com/scipy/scipy/pull/15728>`__: ENH: changed vague exception messages to a more descriptive ones...
* `#15729 <https://github.com/scipy/scipy/pull/15729>`__: ENH: stats: add weighted power mean
* `#15763 <https://github.com/scipy/scipy/pull/15763>`__: ENH: stats: replace ncf with Boost non_central_f distribution
* `#15766 <https://github.com/scipy/scipy/pull/15766>`__: BUG: improve exceptions for private attributes in refactored...
* `#15768 <https://github.com/scipy/scipy/pull/15768>`__: [DOC] fix typo in cython optimize help example
* `#15769 <https://github.com/scipy/scipy/pull/15769>`__: MAINT: stats: check integrality in \`_argcheck\` as needed
* `#15771 <https://github.com/scipy/scipy/pull/15771>`__: MAINT: stats: resolve discrete rvs dtype platform dependency
* `#15774 <https://github.com/scipy/scipy/pull/15774>`__: MAINT: stats: remove deprecated \`median_absolute_deviation\`
* `#15775 <https://github.com/scipy/scipy/pull/15775>`__: DOC: stats.lognorm: rephrase note about parameterization
* `#15776 <https://github.com/scipy/scipy/pull/15776>`__: DOC: stats.powerlaw: more explicit explanation of support
* `#15777 <https://github.com/scipy/scipy/pull/15777>`__: MAINT: stats.shapiro: subtract median from shapiro input
* `#15778 <https://github.com/scipy/scipy/pull/15778>`__: MAINT: stats: more specific error type from \`rv_continuous.fit\`
* `#15779 <https://github.com/scipy/scipy/pull/15779>`__: CI: don't run meson tests on forks and remove skip flags
* `#15782 <https://github.com/scipy/scipy/pull/15782>`__: DEPR: remove k=None in KDTree.query
* `#15783 <https://github.com/scipy/scipy/pull/15783>`__: CI:Pin pytest version to 7.0.1 on Azure
* `#15785 <https://github.com/scipy/scipy/pull/15785>`__: MAINT: stats: remove deprecated itemfreq
* `#15786 <https://github.com/scipy/scipy/pull/15786>`__: DOC: Add examples of integrals to integrate.quadpack
* `#15788 <https://github.com/scipy/scipy/pull/15788>`__: DOC: update macOS and Linux contributor docs to use Python 3.9
* `#15789 <https://github.com/scipy/scipy/pull/15789>`__: DOC, MAINT: Remove numpydoc submodule
* `#15791 <https://github.com/scipy/scipy/pull/15791>`__: MAINT: add ShapeInfo to continuous distributions in scipy.stats
* `#15795 <https://github.com/scipy/scipy/pull/15795>`__: DEP: remove n_jobs from cKDTree
* `#15797 <https://github.com/scipy/scipy/pull/15797>`__: scipy/_lib/boost: Update to d8626c9d2d937abf6a38a844522714ad72e63281
* `#15799 <https://github.com/scipy/scipy/pull/15799>`__: DEP: add warning for documented-as-deprecated extradoc
* `#15802 <https://github.com/scipy/scipy/pull/15802>`__: DOC: Import Error in examples
* `#15803 <https://github.com/scipy/scipy/pull/15803>`__: DOC: error in TransferFunctionDiscrete example
* `#15804 <https://github.com/scipy/scipy/pull/15804>`__: DEP: sharpen warning message on >1-dim for optimize.minimize
* `#15805 <https://github.com/scipy/scipy/pull/15805>`__: DEP: specify version to remove dual_annealing argument 'local_search_options'
* `#15809 <https://github.com/scipy/scipy/pull/15809>`__: DOC,MAINT: remove \`quad_explain\` that has become irrelevant.
* `#15810 <https://github.com/scipy/scipy/pull/15810>`__: DOC: stats.mood: validity only when observations are unique
* `#15811 <https://github.com/scipy/scipy/pull/15811>`__: DOC: fix evaluate_all_bspl example.
* `#15812 <https://github.com/scipy/scipy/pull/15812>`__: DOC: Couple of single to double backticks
* `#15813 <https://github.com/scipy/scipy/pull/15813>`__: DOC: information about skip on CircleCI
* `#15817 <https://github.com/scipy/scipy/pull/15817>`__: MAINT: stats.fisher_exact: improve docs and fix bugs
* `#15819 <https://github.com/scipy/scipy/pull/15819>`__: DEP: docstring-related deprecations (#15757)
* `#15821 <https://github.com/scipy/scipy/pull/15821>`__: DEP: add actual DeprecationWarning for sym_pos-keyword of scipy.linalg.solve
* `#15822 <https://github.com/scipy/scipy/pull/15822>`__: DEP: remove \`right\` from interpolate.PPoly.extend
* `#15823 <https://github.com/scipy/scipy/pull/15823>`__: DOC: Interpolative tutorial - wrong matrix fill var
* `#15824 <https://github.com/scipy/scipy/pull/15824>`__: BUG: Handle base case for scipy.integrate.simpson when span along...
* `#15825 <https://github.com/scipy/scipy/pull/15825>`__: TST: stats: xfail_on_32bit studentized_range moment test
* `#15827 <https://github.com/scipy/scipy/pull/15827>`__: DOC: change docs that specify the SNR ratio definition for find_peaks_cwt().
* `#15828 <https://github.com/scipy/scipy/pull/15828>`__: DEP: raise value error for object arrays
* `#15830 <https://github.com/scipy/scipy/pull/15830>`__: MAINT: stats: collocate bootstrap/permutation_test/monte_carlo_test
* `#15831 <https://github.com/scipy/scipy/pull/15831>`__: MAINT: stats.rv_generic: fix unnecessary call to \`_munp\` in...
* `#15835 <https://github.com/scipy/scipy/pull/15835>`__: FIX: Incorect boschloo pvalue
* `#15837 <https://github.com/scipy/scipy/pull/15837>`__: DOC: Simplify conda command
* `#15840 <https://github.com/scipy/scipy/pull/15840>`__: DOC: special: Add 'Examples' for wrightomega.
* `#15842 <https://github.com/scipy/scipy/pull/15842>`__: DOC: Add examples for \`CGS\`, \`GCROTMK\` and \`BiCGSTAB\` iterative...
* `#15846 <https://github.com/scipy/scipy/pull/15846>`__: DOC: Add efficiency condition for CSC sparse matrix and remove...
* `#15847 <https://github.com/scipy/scipy/pull/15847>`__: BUG: adds warning to scipy.stats.brunnermunzel
* `#15848 <https://github.com/scipy/scipy/pull/15848>`__: DOC: fix interp2d docs showing wrong Z array ordering.
* `#15850 <https://github.com/scipy/scipy/pull/15850>`__: MAINT: sparse.linalg: Missing tfqmr in the re-entrancy test
* `#15853 <https://github.com/scipy/scipy/pull/15853>`__: DEP: remove the keyword debug from linalg.solve
* `#15855 <https://github.com/scipy/scipy/pull/15855>`__: ENH: stats.rv_continuous.expect: split interval to improve reliability
* `#15867 <https://github.com/scipy/scipy/pull/15867>`__: CI: fix python version matrix in linux workflow
* `#15868 <https://github.com/scipy/scipy/pull/15868>`__: CI: fix Azure workflows
* `#15872 <https://github.com/scipy/scipy/pull/15872>`__: DEP: remove mlab from dendrogram
* `#15874 <https://github.com/scipy/scipy/pull/15874>`__: DEP: remove py_vq2
* `#15875 <https://github.com/scipy/scipy/pull/15875>`__: DEP: remove old BSR methods
* `#15876 <https://github.com/scipy/scipy/pull/15876>`__: DEP: remove _ppform
* `#15881 <https://github.com/scipy/scipy/pull/15881>`__: DEP: remove signal.windows.hanning
* `#15882 <https://github.com/scipy/scipy/pull/15882>`__: DEP: enforced radius in spherical voronoi
* `#15885 <https://github.com/scipy/scipy/pull/15885>`__: DOC: stats: clarify truncnorm shape parameter definition
* `#15886 <https://github.com/scipy/scipy/pull/15886>`__: BUG: check that iirfilter argument Wn satisfies Wn[0] < Wn[1]
* `#15887 <https://github.com/scipy/scipy/pull/15887>`__: DEP: remove ftol/xtol from neldermead
* `#15894 <https://github.com/scipy/scipy/pull/15894>`__: [BUG] make p-values consistent with the literature
* `#15895 <https://github.com/scipy/scipy/pull/15895>`__: CI: remove pin on Jinja2
* `#15898 <https://github.com/scipy/scipy/pull/15898>`__: DOC: stats: correct documentation of \`wilcoxon\`'s behavior...
* `#15900 <https://github.com/scipy/scipy/pull/15900>`__: DOC: fix import in example in _morestats
* `#15905 <https://github.com/scipy/scipy/pull/15905>`__: MAINT: stats._moment: warn when catastrophic cancellation occurs
* `#15909 <https://github.com/scipy/scipy/pull/15909>`__: DEP: deal with deprecation of ndim >1 in bspline
* `#15911 <https://github.com/scipy/scipy/pull/15911>`__: MAINT: stats: fix \`gibrat\` name
* `#15914 <https://github.com/scipy/scipy/pull/15914>`__: MAINT: special: Clean up C style in ndtr.c
* `#15916 <https://github.com/scipy/scipy/pull/15916>`__: MAINT: stats: adjust tolerance of failing TestTruncnorm
* `#15917 <https://github.com/scipy/scipy/pull/15917>`__: MAINT: stats: remove support for \`_rvs\` without \`size\` parameter
* `#15920 <https://github.com/scipy/scipy/pull/15920>`__: ENH: stats.mannwhitneyu: add iterative implementation
* `#15923 <https://github.com/scipy/scipy/pull/15923>`__: MAINT: stats: attempt to consolidate warnings and errors
* `#15932 <https://github.com/scipy/scipy/pull/15932>`__: MAINT: stats: fix and thoroughly test \`rv_sample\` at non-integer...
* `#15933 <https://github.com/scipy/scipy/pull/15933>`__: TST: test_nodata respect endianness
* `#15938 <https://github.com/scipy/scipy/pull/15938>`__: DOC: sparse.linalg: add citations for COLAMD
* `#15939 <https://github.com/scipy/scipy/pull/15939>`__: Update _dual_annealing.py
* `#15945 <https://github.com/scipy/scipy/pull/15945>`__: BUG/ENH: \`MultinomialQMC.random\` shape to (n, pvals)
* `#15946 <https://github.com/scipy/scipy/pull/15946>`__: DEP: remove inheritance to \`QMCEngine\` in \`MultinomialQMC\`...
* `#15947 <https://github.com/scipy/scipy/pull/15947>`__: DOC: Revamp contributor setup guides
* `#15953 <https://github.com/scipy/scipy/pull/15953>`__: DOC: Add meson docs to use gcc, clang build in parallel and optimization...
* `#15955 <https://github.com/scipy/scipy/pull/15955>`__: BUG Fix signature of D_IIR_forback(1,2)
* `#15959 <https://github.com/scipy/scipy/pull/15959>`__: ENH: Developer CLI for SciPy
* `#15965 <https://github.com/scipy/scipy/pull/15965>`__: MAINT: stats: ensure that \`rv_continuous._fitstart\` shapes...
* `#15968 <https://github.com/scipy/scipy/pull/15968>`__: BUG: Fix debug and coverage arguments with dev.py
* `#15970 <https://github.com/scipy/scipy/pull/15970>`__: BLD: specify \`cython_lapack\` dependency for \`matfuncs_expm\`
* `#15973 <https://github.com/scipy/scipy/pull/15973>`__: DOC: Add formula renderings to integrate.nquad.
* `#15981 <https://github.com/scipy/scipy/pull/15981>`__: ENH: optimize: Add Newton-TFQMR method and some tests for Newton-Krylov
* `#15982 <https://github.com/scipy/scipy/pull/15982>`__: BENCH: stats: Distribution memory and CDF/PPF round trip benchmarks
* `#15983 <https://github.com/scipy/scipy/pull/15983>`__: TST: sparse.linalg: Add tests for the parameter \`show\`
* `#15991 <https://github.com/scipy/scipy/pull/15991>`__: TST: fix for np.kron matrix issue.
* `#15992 <https://github.com/scipy/scipy/pull/15992>`__: DOC: Fixed \`degrees\` parameter in return section
* `#15997 <https://github.com/scipy/scipy/pull/15997>`__: MAINT: integrate: add \`recursive\` to QUADPACK Fortran sources
* `#15998 <https://github.com/scipy/scipy/pull/15998>`__: BUG: Fix yeojohnson when transformed data has zero variance
* `#15999 <https://github.com/scipy/scipy/pull/15999>`__: MAINT: Adds doit.db.db to gitignore
* `#16004 <https://github.com/scipy/scipy/pull/16004>`__: MAINT: rename MaximumFlowResult.residual to flow
* `#16005 <https://github.com/scipy/scipy/pull/16005>`__: DOC: sparse.linalg: Fixed the description of input matrix of...
* `#16010 <https://github.com/scipy/scipy/pull/16010>`__: MAINT: Add a check to verify all \`.pyi\` files are installed...
* `#16012 <https://github.com/scipy/scipy/pull/16012>`__: DOC: Fix broken link and add python headers to contributing guide
* `#16015 <https://github.com/scipy/scipy/pull/16015>`__: DEP: bump version for deprecating residual to flow.
* `#16018 <https://github.com/scipy/scipy/pull/16018>`__: Doc: fix arch linux building from source local dependencies instructions
* `#16019 <https://github.com/scipy/scipy/pull/16019>`__: DOC: fix conda env name in quickstart guide [skip ci]
* `#16021 <https://github.com/scipy/scipy/pull/16021>`__: DOC: typos in basinhopping documentation
* `#16024 <https://github.com/scipy/scipy/pull/16024>`__: CI: unpin pytest and pytest-xdist
* `#16026 <https://github.com/scipy/scipy/pull/16026>`__: BUG: Allow \`spsolve_triangular\` to work with matrices with...
* `#16029 <https://github.com/scipy/scipy/pull/16029>`__: BUG: Fix meson-info file errors and add more informative exception
* `#16030 <https://github.com/scipy/scipy/pull/16030>`__: MAINT: stats: more accurate error message for \`multivariate_normal\`
* `#16032 <https://github.com/scipy/scipy/pull/16032>`__: FIX: show warning when passing NAN into input of convolve method
* `#16037 <https://github.com/scipy/scipy/pull/16037>`__: MAINT: fix missing \`f\` prefix on f-strings
* `#16042 <https://github.com/scipy/scipy/pull/16042>`__: MAINT: stats.dirichlet: fix interface inconsistency
* `#16044 <https://github.com/scipy/scipy/pull/16044>`__: DEV: do.py, adoption of pkg pydevtool (removed non SciPy specific...
* `#16045 <https://github.com/scipy/scipy/pull/16045>`__: ENH: Use circleci-artifacts-redirector-action
* `#16051 <https://github.com/scipy/scipy/pull/16051>`__: MAINT: Miscellaneous small changes to filter_design
* `#16053 <https://github.com/scipy/scipy/pull/16053>`__: Mark fitpack sources as \`recursive\`
* `#16055 <https://github.com/scipy/scipy/pull/16055>`__: MAINT: stats: replace \`np.var\` with \`_moment(..., 2)\` to...
* `#16058 <https://github.com/scipy/scipy/pull/16058>`__: DEV: Fix meson debian python build
* `#16060 <https://github.com/scipy/scipy/pull/16060>`__: MAINT: Allow all Latin-1 Unicode letters in the source code.
* `#16062 <https://github.com/scipy/scipy/pull/16062>`__: DOC: Document QUADPACK routines used in \`\*quad\`
* `#16067 <https://github.com/scipy/scipy/pull/16067>`__: DEP: remove spatial.distance.matching
* `#16070 <https://github.com/scipy/scipy/pull/16070>`__: ENH: interpolate: handle length-1 grid axes in RegularGridInterpolator
* `#16073 <https://github.com/scipy/scipy/pull/16073>`__: DOC: expand RegularGridInterpolator docstring
* `#16075 <https://github.com/scipy/scipy/pull/16075>`__: CI: Fix refguidecheck failures; unpin Sphinx
* `#16077 <https://github.com/scipy/scipy/pull/16077>`__: BUG: interpolate: RGI(nan) is nan
* `#16078 <https://github.com/scipy/scipy/pull/16078>`__: DEV,BLD: Use Meson in Gitpod builds
* `#16082 <https://github.com/scipy/scipy/pull/16082>`__: BUG: refguide-check: allow multiline namedtuples
* `#16083 <https://github.com/scipy/scipy/pull/16083>`__: DOC: fixing a sign issue in FFTlog function documentation
* `#16092 <https://github.com/scipy/scipy/pull/16092>`__: ENH: interpolate: Add functionality to accept descending points...
* `#16095 <https://github.com/scipy/scipy/pull/16095>`__: MAINT: Remove old filtered warnings
* `#16100 <https://github.com/scipy/scipy/pull/16100>`__: MAINT: Fix a couple compiler warnings.
* `#16104 <https://github.com/scipy/scipy/pull/16104>`__: DOC: stats: symmetry not checked for (inv)wishart distributions
* `#16111 <https://github.com/scipy/scipy/pull/16111>`__: BUG: Fix norm for sparse arrays
* `#16115 <https://github.com/scipy/scipy/pull/16115>`__: MAINT: merge \`environment.yml\` and \`environment_meson.yml\`
* `#16117 <https://github.com/scipy/scipy/pull/16117>`__: MAINT: stats.wilcoxon: return \`zstatistic\` only when \`method='approx'\`
* `#16118 <https://github.com/scipy/scipy/pull/16118>`__: Download openblas binary from GH repo
* `#16122 <https://github.com/scipy/scipy/pull/16122>`__: CI: Speed up ci build that keeps timing out
* `#16125 <https://github.com/scipy/scipy/pull/16125>`__: DOC: interpolate: fix typos "the the" -> "the"
* `#16126 <https://github.com/scipy/scipy/pull/16126>`__: DOC: interpolate: details rectilinear grids in docstrings
* `#16128 <https://github.com/scipy/scipy/pull/16128>`__: BUG: interpolate: fix extrapolation behaviors of \`previous\`...
* `#16130 <https://github.com/scipy/scipy/pull/16130>`__: Increase time to timeout on azure
* `#16134 <https://github.com/scipy/scipy/pull/16134>`__: BUG: signal: Fix calculation of extended image indices in convolve2d.
* `#16135 <https://github.com/scipy/scipy/pull/16135>`__: MAINT: sparse.linalg: A minor improvement with zero initial guess
* `#16137 <https://github.com/scipy/scipy/pull/16137>`__: Clean up fitpack smoke tests
* `#16138 <https://github.com/scipy/scipy/pull/16138>`__: TST: interpolate: mark rbf chunking tests as slow
* `#16141 <https://github.com/scipy/scipy/pull/16141>`__: DOC: Plot poles as x and zeros as o in signal
* `#16144 <https://github.com/scipy/scipy/pull/16144>`__: DEP: Execute deprecation for squeezing input vectors in spatial.distance
* `#16145 <https://github.com/scipy/scipy/pull/16145>`__: ENH: Fix signal.iircomb w0 bugs, add support for both frequency...
* `#16150 <https://github.com/scipy/scipy/pull/16150>`__: Add typing info for Rotation.concatenate
* `#16165 <https://github.com/scipy/scipy/pull/16165>`__: BUG: fix extension module initialization, needs use of \`PyMODINIT_FUNC\`
* `#16166 <https://github.com/scipy/scipy/pull/16166>`__: MAINT:linalg: Expose Cython functions for generic use
* `#16167 <https://github.com/scipy/scipy/pull/16167>`__: ENH: Tweak theilslopes and siegelslopes to return a tuple_bunch
* `#16168 <https://github.com/scipy/scipy/pull/16168>`__: BUG: special: Fix the test 'test_d' that is run when SCIPY_XSLOW...
* `#16173 <https://github.com/scipy/scipy/pull/16173>`__: Adds note to the curve_fit() docstring to use float64.
* `#16176 <https://github.com/scipy/scipy/pull/16176>`__: MAINT: remove questionable uses of \`Py_FatalError\` in module...
* `#16177 <https://github.com/scipy/scipy/pull/16177>`__: MAINT: Cleanup unused code in meson-files
* `#16180 <https://github.com/scipy/scipy/pull/16180>`__: DEV: do.py build. On setup checks if intro-buildoptions.json...
* `#16181 <https://github.com/scipy/scipy/pull/16181>`__: BUG: stats: fix multivariate_hypergeom.rvs method
* `#16183 <https://github.com/scipy/scipy/pull/16183>`__: ENH: Simplify return names in stats.theil/siegelslopes (and fix...
* `#16184 <https://github.com/scipy/scipy/pull/16184>`__: DEP: raise if fillvalue cannot be cast to output type in signal.convolve2d
* `#16185 <https://github.com/scipy/scipy/pull/16185>`__: BUG: stats: Fix handling of float32 inputs for the boost-based...
* `#16187 <https://github.com/scipy/scipy/pull/16187>`__: BLD: default to Meson in pyproject.toml
* `#16194 <https://github.com/scipy/scipy/pull/16194>`__: BLD: add a build option to force use of the g77 ABI with Meson
* `#16198 <https://github.com/scipy/scipy/pull/16198>`__: DEP: sharpen deprecation in NumericalInverseHermite
* `#16206 <https://github.com/scipy/scipy/pull/16206>`__: CI: Test NumPy main branch also with Python 3.11
* `#16220 <https://github.com/scipy/scipy/pull/16220>`__: Create a new spline from a partial derivative of a bivariate...
* `#16223 <https://github.com/scipy/scipy/pull/16223>`__: MAINT: interpolate: move RGI to a separate file
* `#16228 <https://github.com/scipy/scipy/pull/16228>`__: TST: interpolate: move test_spalde_scalar to other fitpack tests
* `#16229 <https://github.com/scipy/scipy/pull/16229>`__: REL: DOC: fix documentation URLs
* `#16230 <https://github.com/scipy/scipy/pull/16230>`__: BUG: fix extension module initialization, needs use of PyMODINIT_FUNC,...
* `#16239 <https://github.com/scipy/scipy/pull/16239>`__: MAINT: tools: Add more output to a refguide-check error message.
* `#16241 <https://github.com/scipy/scipy/pull/16241>`__: DOC: stats: update roadmap
* `#16242 <https://github.com/scipy/scipy/pull/16242>`__: BUG: Make KDTree more robust against nans.
* `#16245 <https://github.com/scipy/scipy/pull/16245>`__: DEP: Execute deprecation of pinv2
* `#16247 <https://github.com/scipy/scipy/pull/16247>`__: DOC:linalg: Remove references to removed pinv2 function
* `#16248 <https://github.com/scipy/scipy/pull/16248>`__: DOC: prep 1.9.0 release notes
* `#16249 <https://github.com/scipy/scipy/pull/16249>`__: Refguide check verbosity abs names
* `#16257 <https://github.com/scipy/scipy/pull/16257>`__: DEP: Deprecation follow-ups
* `#16259 <https://github.com/scipy/scipy/pull/16259>`__: Revert "CI: pin Pip to 22.0.4 to avoid issues with \`--no-build-isolation\`"
* `#16261 <https://github.com/scipy/scipy/pull/16261>`__: DEP: add deprecation warning to maxiter kwarg in _minimize_tnc
* `#16264 <https://github.com/scipy/scipy/pull/16264>`__: DOC: update the RegularGridInterpolator docstring
* `#16265 <https://github.com/scipy/scipy/pull/16265>`__: DEP: deprecate spatial.distance.kulsinski
* `#16267 <https://github.com/scipy/scipy/pull/16267>`__: DOC: broken donation link on GitHub
* `#16273 <https://github.com/scipy/scipy/pull/16273>`__: DOC: remove deprecated functions from refguide
* `#16276 <https://github.com/scipy/scipy/pull/16276>`__: MAINT: sparse.linalg: Update some docstrings.
* `#16279 <https://github.com/scipy/scipy/pull/16279>`__: MAINT: stats: override \`loguniform.fit\` to resolve overparameterization
* `#16282 <https://github.com/scipy/scipy/pull/16282>`__: BUG: special: DECREF scipy_special object before exiting sf_error().
* `#16283 <https://github.com/scipy/scipy/pull/16283>`__: Corrections To Docs
* `#16287 <https://github.com/scipy/scipy/pull/16287>`__: BLD: sync pyproject.toml changes from oldest-supported-numpy
* `#16289 <https://github.com/scipy/scipy/pull/16289>`__: MAINT: stats: remove function-specific warning messages
* `#16290 <https://github.com/scipy/scipy/pull/16290>`__: BLD: fix issue with \`python setup.py install\` and \`_directmodule\`
* `#16295 <https://github.com/scipy/scipy/pull/16295>`__: MAINT: move \`import_array\` before module creation in module...
* `#16296 <https://github.com/scipy/scipy/pull/16296>`__: DOC: REL: fix \`make dist\` issue with missing dependencies
* `#16303 <https://github.com/scipy/scipy/pull/16303>`__: MAINT: revert addition of multivariate_beta
* `#16304 <https://github.com/scipy/scipy/pull/16304>`__: MAINT: add a more informative error message for broken installs
* `#16309 <https://github.com/scipy/scipy/pull/16309>`__: BLD: CI: fix issue in wheel metadata, and add basic "build in...
* `#16316 <https://github.com/scipy/scipy/pull/16316>`__: REL: update version switcher for 1.8.1
* `#16321 <https://github.com/scipy/scipy/pull/16321>`__: DOC: fix incorrect formatting of deprecation tags
* `#16326 <https://github.com/scipy/scipy/pull/16326>`__: REL: update version switcher for 1.9
* `#16329 <https://github.com/scipy/scipy/pull/16329>`__: MAINT: git security shim for 1.9.x
* `#16339 <https://github.com/scipy/scipy/pull/16339>`__: MAINT, TST: bump tol for _axis_nan_policy_test
* `#16341 <https://github.com/scipy/scipy/pull/16341>`__: BLD: update Pythran requirement to 0.11.0, to support Clang >=13
* `#16353 <https://github.com/scipy/scipy/pull/16353>`__: MAINT: version bounds 1.9.0rc1
* `#16360 <https://github.com/scipy/scipy/pull/16360>`__: MAINT, TST: sup warning for theilslopes
* `#16361 <https://github.com/scipy/scipy/pull/16361>`__: MAINT: SCIPY_USE_PROPACK
* `#16370 <https://github.com/scipy/scipy/pull/16370>`__: MAINT: update Boost submodule to include Cygwin fix
* `#16374 <https://github.com/scipy/scipy/pull/16374>`__: MAINT: update pydata-sphinx-theme
* `#16379 <https://github.com/scipy/scipy/pull/16379>`__: DOC: dark theme css adjustments
* `#16390 <https://github.com/scipy/scipy/pull/16390>`__: TST, MAINT: adjust 32-bit xfails for HiGHS
* `#16393 <https://github.com/scipy/scipy/pull/16393>`__: MAINT: use correct type for element wise comparison
* `#16414 <https://github.com/scipy/scipy/pull/16414>`__: BUG: spatial: Handle integer arrays in HalfspaceIntersection.
* `#16420 <https://github.com/scipy/scipy/pull/16420>`__: MAINT: next round of 1.9.0 backports
* `#16422 <https://github.com/scipy/scipy/pull/16422>`__: TST: fix test issues with casting-related warnings with numpy...
* `#16427 <https://github.com/scipy/scipy/pull/16427>`__: MAINT: stats.shapiro: don't modify input in place
* `#16429 <https://github.com/scipy/scipy/pull/16429>`__: MAINT: stats.mode: revert gh-15423
* `#16436 <https://github.com/scipy/scipy/pull/16436>`__: DOC: optimize: Mark deprecated linprog methods explicitly
* `#16444 <https://github.com/scipy/scipy/pull/16444>`__: BUG: fix fail to open tempfile in messagestream.pyx (#8850)
* `#16451 <https://github.com/scipy/scipy/pull/16451>`__: MAINT: few more 1.9.0 backports
* `#16453 <https://github.com/scipy/scipy/pull/16453>`__: DOC: Copy-edit 1.9.0-notes.rst
* `#16457 <https://github.com/scipy/scipy/pull/16457>`__: TST: skip 32-bit test_pdist_correlation_iris_nonC
* `#16458 <https://github.com/scipy/scipy/pull/16458>`__: MAINT: 1.9.0 backports
* `#16473 <https://github.com/scipy/scipy/pull/16473>`__: REL: update 1.9.0 release notes
* `#16482 <https://github.com/scipy/scipy/pull/16482>`__: DOC: Update Returns section of optimize.linprog.
* `#16484 <https://github.com/scipy/scipy/pull/16484>`__: MAINT: remove raw html from README.rst
* `#16485 <https://github.com/scipy/scipy/pull/16485>`__: BLD: fix warnings from f2py templating parsing
* `#16493 <https://github.com/scipy/scipy/pull/16493>`__: BLD: clean up unwanted files in sdist, via \`.gitattributes\`
* `#16507 <https://github.com/scipy/scipy/pull/16507>`__: REL: more tweaks to sdist contents
* `#16512 <https://github.com/scipy/scipy/pull/16512>`__: [1.9] MAINT: skip complex128 propack tests on windows
* `#16514 <https://github.com/scipy/scipy/pull/16514>`__: DOC: reflect correctly where windows wheels are built
* `#16526 <https://github.com/scipy/scipy/pull/16526>`__: MAINT: 1.9.0rc2 backports
* `#16530 <https://github.com/scipy/scipy/pull/16530>`__: MAINT: fix umfpack test failure with numpy 1.23
* `#16539 <https://github.com/scipy/scipy/pull/16539>`__: MAINT: more 1.9.0rc2 backports
* `#16541 <https://github.com/scipy/scipy/pull/16541>`__: BLD: fix regression in building _lsap with symbol visibility
* `#16549 <https://github.com/scipy/scipy/pull/16549>`__: BLD: fix an outdated requirement for macOS arm64 in pyproject.toml
* `#16551 <https://github.com/scipy/scipy/pull/16551>`__: BLD: fix \`__STDC_VERSION__\` check in \`special/_round.h\`
* `#16553 <https://github.com/scipy/scipy/pull/16553>`__: BLD: raise an error with clear message for too-new Python version
* `#16556 <https://github.com/scipy/scipy/pull/16556>`__: DOC: small tweaks to 1.9.0 release notes
* `#16563 <https://github.com/scipy/scipy/pull/16563>`__: DOC: Reflect MSVC minimum toolchain requirement
* `#16570 <https://github.com/scipy/scipy/pull/16570>`__: MAINT: backports before 1.9.0rc3
* `#16572 <https://github.com/scipy/scipy/pull/16572>`__: MAINT: update bundled licenses for removal of scipy-sphinx-theme
* `#16581 <https://github.com/scipy/scipy/pull/16581>`__: MAINT: stats: fix skew/kurtosis empty 1d input
* `#16586 <https://github.com/scipy/scipy/pull/16586>`__: MAINT: stats.truncnorm: improve CDF accuracy/speed
* `#16593 <https://github.com/scipy/scipy/pull/16593>`__: TST: stats: replace TestTruncnorm::test_moments
* `#16599 <https://github.com/scipy/scipy/pull/16599>`__: MAINT: stats.truncnorm.rvs: improve performance
* `#16605 <https://github.com/scipy/scipy/pull/16605>`__: MAINT: stats.truncnorm: simplify remaining methods
* `#16622 <https://github.com/scipy/scipy/pull/16622>`__: ENH: FIX: update HiGHS submodule to resolve MIP infeasibility...
* `#16638 <https://github.com/scipy/scipy/pull/16638>`__: DOC: update docs on building with Meson
* `#16664 <https://github.com/scipy/scipy/pull/16664>`__: MAINT: stats._axis_nan_policy: preserve dtype of masked arrays...
* `#16671 <https://github.com/scipy/scipy/pull/16671>`__: BLD: update \`meson\` and \`meson-python\` versions for 1.9.0...
* `#16684 <https://github.com/scipy/scipy/pull/16684>`__: MAINT: optimize.linprog: ensure integrality can be an array
* `#16688 <https://github.com/scipy/scipy/pull/16688>`__: DOC: a few mailmap updates
* `#16719 <https://github.com/scipy/scipy/pull/16719>`__: MAINT: stats: Work around Cython bug.
* `#16721 <https://github.com/scipy/scipy/pull/16721>`__: MAINT: stats.monte_carlo_test: used biased estimate of p-value

# ===== SOURCE: https://raw.githubusercontent.com/scipy/scipy/main/doc/source/release/1.10.0-notes.rst =====

==========================
SciPy 1.10.0 Release Notes
==========================

.. contents::

SciPy 1.10.0 is the culmination of 6 months of hard work. It contains
many new features, numerous bug-fixes, improved test coverage and better
documentation. There have been a number of deprecations and API changes
in this release, which are documented below. All users are encouraged to
upgrade to this release, as there are a large number of bug-fixes and
optimizations. Before upgrading, we recommend that users check that
their own code does not use deprecated SciPy functionality (to do so,
run your code with ``python -Wd`` and check for ``DeprecationWarning`` s).
Our development attention will now shift to bug-fix releases on the
1.10.x branch, and on adding new features on the main branch.

This release requires Python 3.8+ and NumPy 1.19.5 or greater.

For running on PyPy, PyPy3 6.0+ is required.


**************************
Highlights of this release
**************************

- A new dedicated datasets submodule (`scipy.datasets`) has been added, and is
  now preferred over usage of `scipy.misc` for dataset retrieval.
- A new `scipy.interpolate.make_smoothing_spline` function was added. This
  function constructs a smoothing cubic spline from noisy data, using the
  generalized cross-validation (GCV) criterion to find the tradeoff between
  smoothness and proximity to data points.
- `scipy.stats` has three new distributions, two new hypothesis tests, three
  new sample statistics, a class for greater control over calculations
  involving covariance matrices, and many other enhancements.

************
New features
************

`scipy.datasets` introduction
=============================
- A new dedicated ``datasets`` submodule has been added. The submodules
  is meant for datasets that are relevant to other SciPy submodules ands
  content (tutorials, examples, tests), as well as contain a curated
  set of datasets that are of wider interest. As of this release, all
  the datasets from `scipy.misc` have been added to `scipy.datasets`
  (and deprecated in `scipy.misc`).
- The submodule is based on [Pooch](https://www.fatiando.org/pooch/latest/)
  (a new optional dependency for SciPy), a Python package to simplify fetching
  data files. This move will, in a subsequent release, facilitate SciPy
  to trim down the sdist/wheel sizes, by decoupling the data files and
  moving them out of the SciPy repository, hosting them externally and
  downloading them when requested. After downloading the datasets once,
  the files are cached to avoid network dependence and repeated usage.
- Added datasets from ``scipy.misc``: `scipy.datasets.face`,
  `scipy.datasets.ascent`, `scipy.datasets.electrocardiogram`
- Added download and caching functionality:

  - `scipy.datasets.download_all`: a function to download all the `scipy.datasets`
    associated files at once.
  - `scipy.datasets.clear_cache`: a simple utility function to clear cached dataset
    files from the file system.
  - ``scipy/datasets/_download_all.py`` can be run as a standalone script for
    packaging purposes to avoid any external dependency at build or test time.
    This can be used by SciPy packagers (e.g., for Linux distros) which may
    have to adhere to rules that forbid downloading sources from external
    repositories at package build time.

`scipy.integrate` improvements
==============================
- Added parameter ``complex_func`` to `scipy.integrate.quad`, which can be set
  ``True`` to integrate a complex integrand.


`scipy.interpolate` improvements
================================
- `scipy.interpolate.interpn` now supports tensor-product interpolation methods
  (``slinear``, ``cubic``, ``quintic`` and ``pchip``)
- Tensor-product interpolation methods (``slinear``, ``cubic``, ``quintic`` and
  ``pchip``) in `scipy.interpolate.interpn` and
  `scipy.interpolate.RegularGridInterpolator` now allow values with trailing
  dimensions.
- `scipy.interpolate.RegularGridInterpolator` has a new fast path for
  ``method="linear"`` with 2D data, and ``RegularGridInterpolator`` is now
  easier to subclass
- `scipy.interpolate.interp1d` now can take a single value for non-spline
  methods.
- A new ``extrapolate`` argument is available to `scipy.interpolate.BSpline.design_matrix`,
  allowing extrapolation based on the first and last intervals.
- A new function `scipy.interpolate.make_smoothing_spline` has been added. It is an
  implementation of the generalized cross-validation spline smoothing
  algorithm. The ``lam=None`` (default) mode of this function is a clean-room
  reimplementation of the classic ``gcvspl.f`` Fortran algorithm for
  constructing GCV splines.
- A new ``method="pchip"`` mode was aded to
  `scipy.interpolate.RegularGridInterpolator`. This mode constructs an
  interpolator using tensor products of C1-continuous monotone splines
  (essentially, a `scipy.interpolate.PchipInterpolator` instance per
  dimension).



`scipy.sparse.linalg` improvements
==================================
- The spectral 2-norm is now available in `scipy.sparse.linalg.norm`.
- The performance of `scipy.sparse.linalg.norm` for the default case (Frobenius
  norm) has been improved.
- LAPACK wrappers were added for ``trexc`` and ``trsen``.
- The `scipy.sparse.linalg.lobpcg` algorithm was rewritten, yielding
  the following improvements:

  - a simple tunable restart potentially increases the attainable
    accuracy for edge cases,
  - internal postprocessing runs one final exact Rayleigh-Ritz method
    giving more accurate and orthonormal eigenvectors,
  - output the computed iterate with the smallest max norm of the residual
    and drop the history of subsequent iterations,
  - remove the check for ``LinearOperator`` format input and thus allow
    a simple function handle of a callable object as an input,
  - better handling of common user errors with input data, rather
    than letting the algorithm fail.


`scipy.linalg` improvements
===========================
- `scipy.linalg.lu_factor` now accepts rectangular arrays instead of being restricted
  to square arrays.


`scipy.ndimage` improvements
============================
- The new `scipy.ndimage.value_indices` function provides a time-efficient method to
  search for the locations of individual values with an array of image data.
- A new ``radius`` argument is supported by `scipy.ndimage.gaussian_filter1d` and
  `scipy.ndimage.gaussian_filter` for adjusting the kernel size of the filter.


`scipy.optimize` improvements
=============================
- `scipy.optimize.brute` now coerces non-iterable/single-value ``args`` into a
  tuple.
- `scipy.optimize.least_squares` and `scipy.optimize.curve_fit` now accept
  `scipy.optimize.Bounds` for bounds constraints.
- Added a tutorial for `scipy.optimize.milp`.
- Improved the pretty-printing of `scipy.optimize.OptimizeResult` objects.
- Additional options (``parallel``, ``threads``, ``mip_rel_gap``) can now
  be passed to `scipy.optimize.linprog` with ``method='highs'``.


`scipy.signal` improvements
===========================
- The new window function `scipy.signal.windows.lanczos` was added to compute a
  Lanczos window, also known as a sinc window.


`scipy.sparse.csgraph` improvements
===================================
- the performance of `scipy.sparse.csgraph.dijkstra` has been improved, and
  star graphs in particular see a marked performance improvement


`scipy.special` improvements
============================
- The new function `scipy.special.powm1`, a ufunc with signature
  ``powm1(x, y)``, computes ``x**y - 1``. The function avoids the loss of
  precision that can result when ``y`` is close to 0 or when ``x`` is close to
  1.
- `scipy.special.erfinv` is now more accurate as it leverages the Boost equivalent under
  the hood.


`scipy.stats` improvements
==========================
- Added `scipy.stats.goodness_of_fit`, a generalized goodness-of-fit test for
  use with any univariate distribution, any combination of known and unknown
  parameters, and several choices of test statistic (Kolmogorov-Smirnov,
  Cramer-von Mises, and Anderson-Darling).
- Improved `scipy.stats.bootstrap`: Default method ``'BCa'`` now supports
  multi-sample statistics. Also, the bootstrap distribution is returned in the
  result object, and the result object can be passed into the function as
  parameter ``bootstrap_result`` to add additional resamples or change the
  confidence interval level and type.
- Added maximum spacing estimation to `scipy.stats.fit`.
- Added the Poisson means test ("E-test") as `scipy.stats.poisson_means_test`.
- Added new sample statistics.

  - Added `scipy.stats.contingency.odds_ratio` to compute both the conditional
    and unconditional odds ratios and corresponding confidence intervals for
    2x2 contingency tables.
  - Added `scipy.stats.directional_stats` to compute sample statistics of
    n-dimensional directional data.
  - Added `scipy.stats.expectile`, which generalizes the expected value in the
    same way as quantiles are a generalization of the median.

- Added new statistical distributions.

  - Added `scipy.stats.uniform_direction`, a multivariate distribution to
    sample uniformly from the surface of a hypersphere.
  - Added `scipy.stats.random_table`, a multivariate distribution to sample
    uniformly from m x n contingency tables with provided marginals.
  - Added `scipy.stats.truncpareto`, the truncated Pareto distribution.

- Improved the ``fit`` method of several distributions.

  - `scipy.stats.skewnorm` and `scipy.stats.weibull_min` now use an analytical
    solution when ``method='mm'``, which also serves a starting guess to
    improve the performance of ``method='mle'``.
  - `scipy.stats.gumbel_r` and `scipy.stats.gumbel_l`: analytical maximum
    likelihood estimates have been extended to the cases in which location or
    scale are fixed by the user.
  - Analytical maximum likelihood estimates have been added for
    `scipy.stats.powerlaw`.

- Improved random variate sampling of several distributions.

  - Drawing multiple samples from `scipy.stats.matrix_normal`,
    `scipy.stats.ortho_group`, `scipy.stats.special_ortho_group`, and
    `scipy.stats.unitary_group` is faster.
  - The ``rvs`` method of `scipy.stats.vonmises` now wraps to the interval
    ``[-np.pi, np.pi]``.
  - Improved the reliability of `scipy.stats.loggamma` ``rvs`` method for small
    values of the shape parameter.

- Improved the speed and/or accuracy of functions of several statistical
  distributions.

  - Added `scipy.stats.Covariance` for better speed, accuracy, and user control
    in multivariate normal calculations.
  - `scipy.stats.skewnorm` methods ``cdf``, ``sf``, ``ppf``, and ``isf``
    methods now use the implementations from Boost, improving speed while
    maintaining accuracy. The calculation of higher-order moments is also
    faster and more accurate.
  - `scipy.stats.invgauss` methods ``ppf`` and ``isf`` methods now use the
    implementations from Boost, improving speed and accuracy.
  - `scipy.stats.invweibull` methods ``sf`` and ``isf`` are more accurate for
    small probability masses.
  - `scipy.stats.nct` and `scipy.stats.ncx2` now rely on the implementations
    from Boost, improving speed and accuracy.
  - Implemented the ``logpdf`` method of `scipy.stats.vonmises` for reliability
    in extreme tails.
  - Implemented the ``isf`` method of `scipy.stats.levy` for speed and
    accuracy.
  - Improved the robustness of `scipy.stats.studentized_range` for large ``df``
    by adding an infinite degree-of-freedom approximation.
  - Added a parameter ``lower_limit`` to `scipy.stats.multivariate_normal`,
    allowing the user to change the integration limit from -inf to a desired
    value.
  - Improved the robustness of ``entropy`` of `scipy.stats.vonmises` for large
    concentration values.

- Enhanced `scipy.stats.gaussian_kde`.

  - Added `scipy.stats.gaussian_kde.marginal`, which returns the desired
    marginal distribution of the original kernel density estimate distribution.
  - The ``cdf`` method of `scipy.stats.gaussian_kde` now accepts a
    ``lower_limit`` parameter for integrating the PDF over a rectangular region.
  - Moved calculations for `scipy.stats.gaussian_kde.logpdf` to Cython,
    improving speed.
  - The global interpreter lock is released by the ``pdf`` method of
    `scipy.stats.gaussian_kde` for improved multithreading performance.
  - Replaced explicit matrix inversion with Cholesky decomposition for speed
    and accuracy.

- Enhanced the result objects returned by many `scipy.stats` functions

  - Added a ``confidence_interval`` method to the result object returned by
    `scipy.stats.ttest_1samp` and `scipy.stats.ttest_rel`.
  - The `scipy.stats` functions ``combine_pvalues``, ``fisher_exact``,
    ``chi2_contingency``, ``median_test`` and ``mood`` now return
    bunch objects rather than plain tuples, allowing attributes to be
    accessed by name.
  - Attributes of the result objects returned by ``multiscale_graphcorr``,
    ``anderson_ksamp``, ``binomtest``, ``crosstab``, ``pointbiserialr``,
    ``spearmanr``, ``kendalltau``, and ``weightedtau`` have been renamed to
    ``statistic`` and ``pvalue`` for consistency throughout `scipy.stats`.
    Old attribute names are still allowed for backward compatibility.
  - `scipy.stats.anderson` now returns the parameters of the fitted
    distribution in a `scipy.stats._result_classes.FitResult` object.
  - The ``plot`` method of `scipy.stats._result_classes.FitResult` now accepts
    a ``plot_type`` parameter; the options are ``'hist'`` (histogram, default),
    ``'qq'`` (Q-Q plot), ``'pp'`` (P-P plot), and ``'cdf'`` (empirical CDF
    plot).
  - Kolmogorov-Smirnov tests (e.g. `scipy.stats.kstest`) now return the
    location (argmax) at which the statistic is calculated and the variant
    of the statistic used.

- Improved the performance of several `scipy.stats` functions.

  - Improved the performance of `scipy.stats.cramervonmises_2samp` and
    `scipy.stats.ks_2samp` with ``method='exact'``.
  - Improved the performance of `scipy.stats.siegelslopes`.
  - Improved the performance of `scipy.stats.mstats.hdquantile_sd`.
  - Improved the performance of `scipy.stats.binned_statistic_dd` for several
    NumPy statistics, and binned statistics methods now support complex data.

- Added the ``scramble`` optional argument to `scipy.stats.qmc.LatinHypercube`.
  It replaces ``centered``, which is now deprecated.
- Added a parameter ``optimization`` to all `scipy.stats.qmc.QMCEngine`
  subclasses to improve characteristics of the quasi-random variates.
- Added tie correction to `scipy.stats.mood`.
- Added tutorials for resampling methods in `scipy.stats`.
- `scipy.stats.bootstrap`, `scipy.stats.permutation_test`, and
  `scipy.stats.monte_carlo_test` now automatically detect whether the provided
  ``statistic`` is vectorized, so passing the ``vectorized`` argument
  explicitly is no longer required to take advantage of vectorized statistics.
- Improved the speed of `scipy.stats.permutation_test` for permutation types
  ``'samples'`` and ``'pairings'``.
- Added ``axis``, ``nan_policy``, and masked array support to
  `scipy.stats.jarque_bera`.
- Added the ``nan_policy`` optional argument to `scipy.stats.rankdata`.


*******************
Deprecated features
*******************
- `scipy.misc` module and all the methods in ``misc`` are deprecated in v1.10
  and will be completely removed in SciPy v2.0.0. Users are suggested to
  utilize the `scipy.datasets` module instead for the dataset methods.
- `scipy.stats.qmc.LatinHypercube` parameter ``centered`` has been deprecated.
  It is replaced by the ``scramble`` argument for more consistency with other
  QMC engines.
- `scipy.interpolate.interp2d` class has been deprecated.  The docstring of the
  deprecated routine lists recommended replacements.

********************
Expired Deprecations
********************
- There is an ongoing effort to follow through on long-standing deprecations.
- The following previously deprecated features are affected:

  - Removed ``cond`` & ``rcond`` kwargs in ``linalg.pinv``
  - Removed wrappers ``scipy.linalg.blas.{clapack, flapack}``
  - Removed ``scipy.stats.NumericalInverseHermite`` and removed ``tol`` & ``max_intervals`` kwargs from ``scipy.stats.sampling.NumericalInverseHermite``
  - Removed ``local_search_options`` kwarg frrom ``scipy.optimize.dual_annealing``.


*************
Other changes
*************
- `scipy.stats.bootstrap`, `scipy.stats.permutation_test`, and
  `scipy.stats.monte_carlo_test` now automatically detect whether the provided
  ``statistic`` is vectorized by looking for an ``axis`` parameter in the
  signature of ``statistic``. If an ``axis`` parameter is present in
  ``statistic`` but should not be relied on for vectorized calls, users must
  pass option ``vectorized==False`` explicitly.
- `scipy.stats.multivariate_normal` will now raise a ``ValueError`` when the
  covariance matrix is not positive semidefinite, regardless of which method
  is called.



*******
Authors
*******

* Name (commits)
* h-vetinari (10)
* Jelle Aalbers (1)
* Oriol Abril-Pla (1) +
* Alan-Hung (1) +
* Tania Allard (7)
* Oren Amsalem (1) +
* Sven Baars (10)
* Balthasar (1) +
* Ross Barnowski (1)
* Christoph Baumgarten (2)
* Peter Bell (2)
* Sebastian Berg (1)
* Aaron Berk (1) +
* boatwrong (1) +
* boeleman (1) +
* Jake Bowhay (50)
* Matthew Brett (4)
* Evgeni Burovski (93)
* Matthias Bussonnier (6)
* Dominic C (2)
* Mingbo Cai (1) +
* James Campbell (2) +
* CJ Carey (4)
* cesaregarza (1) +
* charlie0389 (1) +
* Hood Chatham (5)
* Andrew Chin (1) +
* Daniel Ching (1) +
* Leo Chow (1) +
* chris (3) +
* John Clow (1) +
* cm7S (1) +
* cmgodwin (1) +
* Christopher Cowden (2) +
* Henry Cuzco (2) +
* Anirudh Dagar (12)
* Hans Dembinski (2) +
* Jaiden di Lanzo (24) +
* Felipe Dias (1) +
* Dieter Werthmüller (1)
* Giuseppe Dilillo (1) +
* dpoerio (1) +
* drpeteb (1) +
* Christopher Dupuis (1) +
* Jordan Edmunds (1) +
* Pieter Eendebak (1) +
* Jérome Eertmans (1) +
* Fabian Egli (2) +
* Sebastian Ehlert (2) +
* Kian Eliasi (1) +
* Tomohiro Endo (1) +
* Stefan Endres (1)
* Zeb Engberg (4) +
* Jonas Eschle (1) +
* Thomas J. Fan (9)
* fiveseven (1) +
* Neil Flood (1) +
* Franz Forstmayr (1)
* Sara Fridovich-Keil (1)
* David Gilbertson (1) +
* Ralf Gommers (251)
* Marco Gorelli (2) +
* Matt Haberland (387)
* Andrew Hawryluk (2) +
* Christoph Hohnerlein (2) +
* Loïc Houpert (2) +
* Shamus Husheer (1) +
* ideasrule (1) +
* imoiwm (1) +
* Lakshaya Inani (1) +
* Joseph T. Iosue (1)
* iwbc-mzk (1) +
* Nathan Jacobi (3) +
* Julien Jerphanion (5)
* He Jia (1)
* jmkuebler (1) +
* Johannes Müller (1) +
* Vedant Jolly (1) +
* Juan Luis Cano Rodríguez (2)
* Justin (1) +
* jvavrek (1) +
* jyuv (2)
* Kai Mühlbauer (1) +
* Nikita Karetnikov (3) +
* Reinert Huseby Karlsen (1) +
* kaspar (2) +
* Toshiki Kataoka (1)
* Robert Kern (3)
* Joshua Klein (1) +
* Andrew Knyazev (7)
* Jozsef Kutas (16) +
* Eric Larson (4)
* Lechnio (1) +
* Antony Lee (2)
* Aditya Limaye (1) +
* Xingyu Liu (2)
* Christian Lorentzen (4)
* Loïc Estève (2)
* Thibaut Lunet (2) +
* Peter Lysakovski (1)
* marianasalamoni (2) +
* mariprudencio (1) +
* Paige Martin (1) +
* Arno Marty (1) +
* matthewborish (3) +
* Damon McDougall (1)
* Nicholas McKibben (22)
* McLP (1) +
* mdmahendri (1) +
* Melissa Weber Mendonça (9)
* Jarrod Millman (1)
* Naoto Mizuno (2)
* Shashaank N (1)
* Pablo S Naharro (1) +
* nboudrie (2) +
* Andrew Nelson (52)
* Nico Schlömer (1)
* NiMlr (1) +
* o-alexandre-felipe (1) +
* Maureen Ononiwu (1) +
* Dimitri Papadopoulos (2) +
* partev (1) +
* Tirth Patel (10)
* Paulius Šarka (1) +
* Josef Perktold (1)
* Giacomo Petrillo (3) +
* Matti Picus (1)
* Rafael Pinto (1) +
* PKNaveen (1) +
* Ilhan Polat (6)
* Akshita Prasanth (2) +
* Sean Quinn (1)
* Tyler Reddy (155)
* Martin Reinecke (1)
* Ned Richards (1)
* Marie Roald (1) +
* Sam Rosen (4) +
* Pamphile Roy (105)
* sabonerune (2) +
* Atsushi Sakai (94)
* Daniel Schmitz (27)
* Anna Scholtz (1) +
* Eli Schwartz (11)
* serge-sans-paille (2)
* JEEVANSHI SHARMA (1) +
* ehsan shirvanian (2) +
* siddhantwahal (2)
* Mathieu Dutour Sikiric (1) +
* Sourav Singh (1)
* Alexander Soare (1) +
* Bjørge Solli (2) +
* Scott Staniewicz (1)
* Ethan Steinberg (3) +
* Albert Steppi (3)
* Thomas Stoeger (1) +
* Kai Striega (4)
* Tartopohm (1) +
* Mamoru TASAKA (2) +
* Ewout ter Hoeven (5)
* TianyiQ (1) +
* Tiger (1) +
* Will Tirone (1)
* Ajay Shanker Tripathi (1) +
* Edgar Andrés Margffoy Tuay (1) +
* Dmitry Ulyumdzhiev (1) +
* Hari Vamsi (1) +
* VitalyChait (1) +
* Rik Voorhaar (1) +
* Samuel Wallan (4)
* Stefan van der Walt (2)
* Warren Weckesser (145)
* wei2222 (1) +
* windows-server-2003 (3) +
* Marek Wojciechowski (2) +
* Niels Wouda (1) +
* WRKampi (1) +
* Yeonjoo Yoo (1) +
* Rory Yorke (1)
* Xiao Yuan (2) +
* Meekail Zain (2) +
* Fabio Zanini (1) +
* Steffen Zeile (1) +
* Egor Zemlyanoy (19)
* Gavin Zhang (3) +

A total of 184 people contributed to this release.
People with a "+" by their names contributed a patch for the first time.
This list of names is automatically generated, and may not be fully complete.


************************
Issues closed for 1.10.0
************************

* `#1261 <https://github.com/scipy/scipy/issues/1261>`__: errors in fmin_bfgs and some improvements (Trac #734)
* `#2167 <https://github.com/scipy/scipy/issues/2167>`__: BivariateSpline errors with kx=ky=1 (Trac #1642)
* `#2304 <https://github.com/scipy/scipy/issues/2304>`__: funm gives incorrect results for non-diagonalizable inputs (Trac...
* `#3421 <https://github.com/scipy/scipy/issues/3421>`__: Rename information theory functions?
* `#3854 <https://github.com/scipy/scipy/issues/3854>`__: KroghInterpolator doesn't pass through points
* `#4043 <https://github.com/scipy/scipy/issues/4043>`__: scipy.interpolate.interp1d should be able to take a single value
* `#4555 <https://github.com/scipy/scipy/issues/4555>`__: leastsq should use cholesky not inv for hessian inversion
* `#4598 <https://github.com/scipy/scipy/issues/4598>`__: von Mises random variate sampling broken for non-zero location...
* `#4975 <https://github.com/scipy/scipy/issues/4975>`__: Documentation for s in UnivariateSpline is confusing
* `#6173 <https://github.com/scipy/scipy/issues/6173>`__: scipy.interpolate.lagrange implemented through coefficients
* `#6688 <https://github.com/scipy/scipy/issues/6688>`__: ENH: optimize.basinhopping: call an acceptance test before local...
* `#7104 <https://github.com/scipy/scipy/issues/7104>`__: scipy.stats.nct - wrong values in tails
* `#7268 <https://github.com/scipy/scipy/issues/7268>`__: scipy.sparse.linalg.norm does not implement spectral norm
* `#7521 <https://github.com/scipy/scipy/issues/7521>`__: scipy.UnivariateSpline smoothing condition documentation inaccuracy
* `#7857 <https://github.com/scipy/scipy/issues/7857>`__: griddata sensible to size of original grid when it should not
* `#8376 <https://github.com/scipy/scipy/issues/8376>`__: InterpolatedUnivariateSpline.roots() seems to miss roots sometimes
* `#9119 <https://github.com/scipy/scipy/issues/9119>`__: documentation issues of functions in scipy.stats.mstats
* `#9389 <https://github.com/scipy/scipy/issues/9389>`__: Kolmogorov Smirnov 2 samples returning max distance location...
* `#9440 <https://github.com/scipy/scipy/issues/9440>`__: Unexpected successful optimization with minimize when number...
* `#9451 <https://github.com/scipy/scipy/issues/9451>`__: Add shgo to optimize benchmarks
* `#10737 <https://github.com/scipy/scipy/issues/10737>`__: Goodness of fit tests for distributions with unknown parameters
* `#10911 <https://github.com/scipy/scipy/issues/10911>`__: scipy.optimize.minimize_scalar does not automatically select...
* `#11026 <https://github.com/scipy/scipy/issues/11026>`__: rv_discrete.interval returning wrong values for alpha = 1
* `#11053 <https://github.com/scipy/scipy/issues/11053>`__: scipy.stats: Allow specifying inverse-variance matrix to multivariate_normal
* `#11131 <https://github.com/scipy/scipy/issues/11131>`__: DOC: stats.fisher_exact does not match R functionality for \`oddsratio\`...
* `#11406 <https://github.com/scipy/scipy/issues/11406>`__: scipy.sparse.linalg.svds (v1.4.1) on singular matrix does not...
* `#11475 <https://github.com/scipy/scipy/issues/11475>`__: Filter radius as optional argument for gaussian_filter1d/gaussian_filter
* `#11772 <https://github.com/scipy/scipy/issues/11772>`__: Cache covariance matrix decomposition in frozen multivariate_normal
* `#11777 <https://github.com/scipy/scipy/issues/11777>`__: non-central chi2 (scipy.stats.ncx2.pdf) gets clipped to zero...
* `#11790 <https://github.com/scipy/scipy/issues/11790>`__: NaN handling of stats.rankdata
* `#11860 <https://github.com/scipy/scipy/issues/11860>`__: Occurrence of nan values when using multinomial.pmf from scipy.stats?
* `#11916 <https://github.com/scipy/scipy/issues/11916>`__: Improve documentation for smoothing in interpolate.UnivariateSpline...
* `#12041 <https://github.com/scipy/scipy/issues/12041>`__: Spherical mean/variance
* `#12246 <https://github.com/scipy/scipy/issues/12246>`__: Interpolation 2D with SmoothBivariateSpline
* `#12621 <https://github.com/scipy/scipy/issues/12621>`__: Scalar minimization functions have no references
* `#12632 <https://github.com/scipy/scipy/issues/12632>`__: curve_fit algorithm try to transform xdata in an array of floats
* `#12963 <https://github.com/scipy/scipy/issues/12963>`__: shgo is not correctly passing jac to minimizer
* `#13021 <https://github.com/scipy/scipy/issues/13021>`__: 2D Interpolation Scaling Issues
* `#13049 <https://github.com/scipy/scipy/issues/13049>`__: Examples missing import numpy as np?
* `#13452 <https://github.com/scipy/scipy/issues/13452>`__: Calling \`len()\` on the \`scipy.spatial.transform.rotation.Rotation\`...
* `#13529 <https://github.com/scipy/scipy/issues/13529>`__: signal.decimate doesn't use sosfilters and sosfiltfilt
* `#14098 <https://github.com/scipy/scipy/issues/14098>`__: DOC-Update for InterpolatedUnivariateSpline and LSQUnivariateSpline
* `#14198 <https://github.com/scipy/scipy/issues/14198>`__: better description of solveh_banded limitations
* `#14348 <https://github.com/scipy/scipy/issues/14348>`__: Extract spline coefficient from splprep: tck
* `#14386 <https://github.com/scipy/scipy/issues/14386>`__: Let CloughTocher2DInterpolator fit "nearest" for points outside...
* `#14472 <https://github.com/scipy/scipy/issues/14472>`__: scipy.interpolate.CubicSpline boundary conditions appear to be...
* `#14533 <https://github.com/scipy/scipy/issues/14533>`__: optimize.shgo gives unexpected TypeError
* `#14541 <https://github.com/scipy/scipy/issues/14541>`__: Raspberry Pi 4 aarch64: ModuleNotFoundError: No module named...
* `#14584 <https://github.com/scipy/scipy/issues/14584>`__: scipy.signal.filter_design.zpk2sos doctests fail (values different...
* `#14809 <https://github.com/scipy/scipy/issues/14809>`__: BUG: scipy.signal.periodogram window parameter
* `#14853 <https://github.com/scipy/scipy/issues/14853>`__: BUG: sqrtm dtype
* `#14922 <https://github.com/scipy/scipy/issues/14922>`__: Question: Seemingly unused, non-working script \`isolve/tests/demo_lgres.py\`
* `#15049 <https://github.com/scipy/scipy/issues/15049>`__: BUG: Visualization of CWT matrix in signal.cwt example code
* `#15072 <https://github.com/scipy/scipy/issues/15072>`__: BUG: signal.decimate returns NaN with large float32 arrays
* `#15393 <https://github.com/scipy/scipy/issues/15393>`__: BUG: signal.decimate returns unexpected values with float32 arrays
* `#15473 <https://github.com/scipy/scipy/issues/15473>`__: ENH: \`skewnorm.cdf\` is very slow. Consider a much more efficient...
* `#15618 <https://github.com/scipy/scipy/issues/15618>`__: ENH: Generation of random 2D tables with given marginal totals
* `#15675 <https://github.com/scipy/scipy/issues/15675>`__: ENH: \`multivariate_normal\` should accept eigendecomposition...
* `#15685 <https://github.com/scipy/scipy/issues/15685>`__: ENH: The exact p-value calculation in \`stats.cramervonmises_2samp\`...
* `#15733 <https://github.com/scipy/scipy/issues/15733>`__: DEP: remove quiet parameter from fitpack
* `#15749 <https://github.com/scipy/scipy/issues/15749>`__: DEP: remove tol from \`NumericalInverseHermite\`
* `#15792 <https://github.com/scipy/scipy/issues/15792>`__: MAINT: There is no unittest and documentation of Improper integral...
* `#15807 <https://github.com/scipy/scipy/issues/15807>`__: DEP: remove dual_annealing argument 'local_search_options'
* `#15844 <https://github.com/scipy/scipy/issues/15844>`__: It's not that obvious that \`firls\` requires an even number...
* `#15883 <https://github.com/scipy/scipy/issues/15883>`__: BUG: stats.bootstrap bca implementation triggers ValueError for...
* `#15936 <https://github.com/scipy/scipy/issues/15936>`__: Please add citations to the papers for COLAMD
* `#15996 <https://github.com/scipy/scipy/issues/15996>`__: Symbol hiding when using GNU linker in the Meson build should...
* `#16148 <https://github.com/scipy/scipy/issues/16148>`__: Documentation in spearmanr
* `#16235 <https://github.com/scipy/scipy/issues/16235>`__: BUG: Memory leak in function \`Py_FindObjects\` due to new reference...
* `#16236 <https://github.com/scipy/scipy/issues/16236>`__: BUG: Memory leak in function \`py_filter2d\` due to new reference...
* `#16251 <https://github.com/scipy/scipy/issues/16251>`__: DEP: Execute deprecation of scipy.linalg.blas.{clapack, flapack}
* `#16252 <https://github.com/scipy/scipy/issues/16252>`__: DEP: add deprecation warnings to kwargs \`turbo\` / \`eigvals\`...
* `#16253 <https://github.com/scipy/scipy/issues/16253>`__: DEP: add deprecation warning for kwargs \`nyq\` / \`Hz\` in firwin\*
* `#16256 <https://github.com/scipy/scipy/issues/16256>`__: DEP: add deprecation warning for binom_test
* `#16272 <https://github.com/scipy/scipy/issues/16272>`__: BUG: unclear error for invalid bracketing
* `#16291 <https://github.com/scipy/scipy/issues/16291>`__: BUG: lambertw returns nan's on small values
* `#16297 <https://github.com/scipy/scipy/issues/16297>`__: DOC: minor release procedure adjustment
* `#16319 <https://github.com/scipy/scipy/issues/16319>`__: ENH: improved accuracy and orthonormality of output eigenvectors...
* `#16333 <https://github.com/scipy/scipy/issues/16333>`__: DOC: rvalue description is missing in stats.probplot
* `#16334 <https://github.com/scipy/scipy/issues/16334>`__: BUG: CLI help is not accessible using light themes
* `#16338 <https://github.com/scipy/scipy/issues/16338>`__: ENH: Add option to clip out of bounds input values to minimum...
* `#16342 <https://github.com/scipy/scipy/issues/16342>`__: BUG: IIRdesign function ftype='bessel' not recognized
* `#16344 <https://github.com/scipy/scipy/issues/16344>`__: ENH: improved \`stats.ortho_group\`
* `#16364 <https://github.com/scipy/scipy/issues/16364>`__: ENH: stats: return bunches rather than plain tuples
* `#16380 <https://github.com/scipy/scipy/issues/16380>`__: BUG: RegularGridInterpolator error message is wrong
* `#16386 <https://github.com/scipy/scipy/issues/16386>`__: TST: sparse/linalg/tests/test_expm_multiply.py::test_expm_multiply_dtype...
* `#16399 <https://github.com/scipy/scipy/issues/16399>`__: \`test_mio.py::test_recarray\` failure due to dtype handling...
* `#16413 <https://github.com/scipy/scipy/issues/16413>`__: DOC: rvs method docstrings refer to seed argument instead of...
* `#16433 <https://github.com/scipy/scipy/issues/16433>`__: ENH: scipy.stats.bootstrap() should do BCa for multivariate statistics...
* `#16472 <https://github.com/scipy/scipy/issues/16472>`__: handle spline interpolation methods in \`interpn\`
* `#16476 <https://github.com/scipy/scipy/issues/16476>`__: dev.py does not propagate error codes, thus hides errors on CI
* `#16490 <https://github.com/scipy/scipy/issues/16490>`__: DOC: err on example for \`scipy.signal.upfirdn\`
* `#16558 <https://github.com/scipy/scipy/issues/16558>`__: BUG: leaves_color_list incorrect when distance=0
* `#16580 <https://github.com/scipy/scipy/issues/16580>`__: Typo in scipy/optimize/tests/test_optimize.py, logit instead...
* `#16582 <https://github.com/scipy/scipy/issues/16582>`__: TST: RegularGridInterpolator tests should be parameterised
* `#16603 <https://github.com/scipy/scipy/issues/16603>`__: ENH, DOC: Add policy on typo and small docs fixes
* `#16663 <https://github.com/scipy/scipy/issues/16663>`__: BUG: \`bool(rotation)\` leads to error
* `#16673 <https://github.com/scipy/scipy/issues/16673>`__: Test failure for \`TestPoisson.test_mindist\` in Azure CI job
* `#16713 <https://github.com/scipy/scipy/issues/16713>`__: BUG/DOC: spatial: docstrings of \`Rotation\` methods are missing...
* `#16726 <https://github.com/scipy/scipy/issues/16726>`__: CI: Python 3.11 tests are failing because a dependency is using...
* `#16741 <https://github.com/scipy/scipy/issues/16741>`__: BUG: DOC: editing docstring example in svds
* `#16759 <https://github.com/scipy/scipy/issues/16759>`__: DOC: Add 'import numpy as np' to the 'Examples' section of docstrings.
* `#16763 <https://github.com/scipy/scipy/issues/16763>`__: BUG: numpy version requirement mismatch docs vs setup.py
* `#16773 <https://github.com/scipy/scipy/issues/16773>`__: BUG: indexing error in scipy.spatial.Voronoi in 3D
* `#16796 <https://github.com/scipy/scipy/issues/16796>`__: DOC: Method "bisect" for root_scalar lacks correct argument list
* `#16819 <https://github.com/scipy/scipy/issues/16819>`__: BUG: stats.binned_statistic_2d is ~8x slower when using \`statistic=np.mean\`...
* `#16833 <https://github.com/scipy/scipy/issues/16833>`__: Runtime performance in BSpline.design_matrix is inferior to BSpline().__call__()
* `#16892 <https://github.com/scipy/scipy/issues/16892>`__: Add legend to \`rv_histogram\` plot in docs
* `#16912 <https://github.com/scipy/scipy/issues/16912>`__: MAINT: stats: optimize: Move \`_contains_nan\` function to more...
* `#16914 <https://github.com/scipy/scipy/issues/16914>`__: BUG: documentation of scipy.stats.truncnorm could be clearer
* `#17031 <https://github.com/scipy/scipy/issues/17031>`__: BUG: stats: Intermittent failure of the test 'test_plot_iv'
* `#17033 <https://github.com/scipy/scipy/issues/17033>`__: New CI failures in \`sparse\` with nightly numpy
* `#17047 <https://github.com/scipy/scipy/issues/17047>`__: BUG: Documentation error in scipy.signal
* `#17056 <https://github.com/scipy/scipy/issues/17056>`__: Mypy failure in CI for \`numpy/__init__.pyi\` positional-only...
* `#17065 <https://github.com/scipy/scipy/issues/17065>`__: BUG: minimize(method=’L-BFGS-B’) documentation is contradictory
* `#17070 <https://github.com/scipy/scipy/issues/17070>`__: Using Meson-built 1.10.0.dev0 nightly wheel in a conda environment...
* `#17074 <https://github.com/scipy/scipy/issues/17074>`__: BUG: scipy.optimize.linprog does not fulfill integer constraints...
* `#17078 <https://github.com/scipy/scipy/issues/17078>`__: DOC: "These are not universal functions" difficult to understand...
* `#17089 <https://github.com/scipy/scipy/issues/17089>`__: ENH: Documentation on test behind p-values of .spearmanr
* `#17129 <https://github.com/scipy/scipy/issues/17129>`__: DOC: inconsistency in when a new feature was added
* `#17155 <https://github.com/scipy/scipy/issues/17155>`__: BUG: stats: Bug in XSLOW tests in TestNumericalInverseHermite
* `#17167 <https://github.com/scipy/scipy/issues/17167>`__: BUG: bernoulli.pmf returns non-zero values with non-integer arguments
* `#17168 <https://github.com/scipy/scipy/issues/17168>`__: \`test_powm1\` failing in CI on Windows
* `#17174 <https://github.com/scipy/scipy/issues/17174>`__: MAINT, REL: wheels not uploaded to staging on push to maintenance
* `#17241 <https://github.com/scipy/scipy/issues/17241>`__: BUG: CubicSpline segfaults when passing empty values for \`y\`with...
* `#17336 <https://github.com/scipy/scipy/issues/17336>`__: BUG: Meson build unconditionally probes for pythran, despite...
* `#17375 <https://github.com/scipy/scipy/issues/17375>`__: BUG: resample_poly() freezes with large data and specific samplerate...
* `#17380 <https://github.com/scipy/scipy/issues/17380>`__: BUG: optimize: using \`integrality\` prevents \`linprog\` from...
* `#17382 <https://github.com/scipy/scipy/issues/17382>`__: BUG/DOC: optimize: \`minimize\` doc should reflect tnc's deprecation...
* `#17412 <https://github.com/scipy/scipy/issues/17412>`__: BUG: Meson error:compiler for language "cpp", not specified for...
* `#17444 <https://github.com/scipy/scipy/issues/17444>`__: BUG: beta.ppf causes segfault
* `#17468 <https://github.com/scipy/scipy/issues/17468>`__: Weird errors with running the tests \`scipy.stats.tests.test_distributions\`...
* `#17518 <https://github.com/scipy/scipy/issues/17518>`__: ENH: stats.pearsonr: support complex data
* `#17523 <https://github.com/scipy/scipy/issues/17523>`__: BUG: \`[source]\` button in the docs sending to the wrong place
* `#17578 <https://github.com/scipy/scipy/issues/17578>`__: TST, BLD, CI: 1.10.0rc1 wheel build/test failures
* `#17619 <https://github.com/scipy/scipy/issues/17619>`__: BUG: core dump when calling scipy.optimize.linprog
* `#17644 <https://github.com/scipy/scipy/issues/17644>`__: BUG: 1.10.0rc2 Windows wheel tests runs all segfault
* `#17650 <https://github.com/scipy/scipy/issues/17650>`__: BUG: Assertion failed when using HiGHS

************************
Pull requests for 1.10.0
************************

* `#9072 <https://github.com/scipy/scipy/pull/9072>`__: ENH: Added rectangular integral to multivariate_normal
* `#9932 <https://github.com/scipy/scipy/pull/9932>`__: ENH: stats.gaussian_kde: add method that returns marginal distribution
* `#11712 <https://github.com/scipy/scipy/pull/11712>`__: BUG: trust-constr evaluates function out of bounds
* `#12211 <https://github.com/scipy/scipy/pull/12211>`__: DOC: Dice similiarity index
* `#12312 <https://github.com/scipy/scipy/pull/12312>`__: ENH: Accelerate matrix normal sampling using matmul
* `#12594 <https://github.com/scipy/scipy/pull/12594>`__: BUG: fixed indexing error when using bounds in Powell's method...
* `#13053 <https://github.com/scipy/scipy/pull/13053>`__: ENH: add MLE for stats.powerlaw.fit
* `#13265 <https://github.com/scipy/scipy/pull/13265>`__: ENH: Kstest exact performance improvements
* `#13340 <https://github.com/scipy/scipy/pull/13340>`__: ENH: stats: Add the function odds_ratio.
* `#13663 <https://github.com/scipy/scipy/pull/13663>`__: ENH: linalg: Add LAPACK wrappers for trexc and trsen.
* `#13753 <https://github.com/scipy/scipy/pull/13753>`__: DOC: optimize: update Powell docs to reflect API
* `#13957 <https://github.com/scipy/scipy/pull/13957>`__: ENH: stats.ks_2samp: Pythranize remaining exact p-value calculations
* `#14248 <https://github.com/scipy/scipy/pull/14248>`__: MAINT:linalg: Make lu_factor accept rectangular arrays
* `#14317 <https://github.com/scipy/scipy/pull/14317>`__: ENH: Optimize sparse frobenius norm
* `#14402 <https://github.com/scipy/scipy/pull/14402>`__: DOC: Clarify argument documentation for \`solve\`
* `#14430 <https://github.com/scipy/scipy/pull/14430>`__: ENH: improve siegelslopes via pythran
* `#14563 <https://github.com/scipy/scipy/pull/14563>`__: WIP: stats: bins=auto in docstrings
* `#14579 <https://github.com/scipy/scipy/pull/14579>`__: BENCH: optimize: add DFO CUTEST benchmark
* `#14638 <https://github.com/scipy/scipy/pull/14638>`__: DOC: added mention of the limitations of Thomas' algorithm
* `#14840 <https://github.com/scipy/scipy/pull/14840>`__: ENH: Addition of Poisson Means Test (E-test).
* `#15097 <https://github.com/scipy/scipy/pull/15097>`__: ENH: add radius to gaussian_filter1d and gaussian_filter
* `#15444 <https://github.com/scipy/scipy/pull/15444>`__: ENH: Infinite df approximation for Studentized Range PDF
* `#15493 <https://github.com/scipy/scipy/pull/15493>`__: ENH: Convert gaussian_kde logpdf to Cython
* `#15607 <https://github.com/scipy/scipy/pull/15607>`__: ENH: Add \`scipy.datasets\` submodule
* `#15709 <https://github.com/scipy/scipy/pull/15709>`__: ENH: improve the computation time of stats.cramervonmises_2samp()
* `#15770 <https://github.com/scipy/scipy/pull/15770>`__: ENH: stats: replace ncx2 stats distribution with Boost non_central_chi_squared
* `#15878 <https://github.com/scipy/scipy/pull/15878>`__: DEP: remove local_search_options of dual_annealing
* `#15892 <https://github.com/scipy/scipy/pull/15892>`__: BUG: stats: use mean behavior for percentileofscore in bootstrap
* `#15901 <https://github.com/scipy/scipy/pull/15901>`__: DEP: Deprecate scipy.misc in favour of scipy.datasets
* `#15967 <https://github.com/scipy/scipy/pull/15967>`__: TST/DOC: stats: explain/check 100% interval for discrete distributions
* `#15972 <https://github.com/scipy/scipy/pull/15972>`__: DOC: length of \`bands\` param. specified in \`firls\`
* `#16002 <https://github.com/scipy/scipy/pull/16002>`__: ENH: Allow specyfing inverse covariance of a multivariate normal...
* `#16017 <https://github.com/scipy/scipy/pull/16017>`__: ENH: special: Use boost for a couple ufuncs.
* `#16069 <https://github.com/scipy/scipy/pull/16069>`__: ENH: add additional MLE for fixed parameters in gumbel_r.fit
* `#16096 <https://github.com/scipy/scipy/pull/16096>`__: BUG: use SOS filters in decimate for numerical stability
* `#16109 <https://github.com/scipy/scipy/pull/16109>`__: ENH: add \`optimization\` to \`QMCEngine\`
* `#16140 <https://github.com/scipy/scipy/pull/16140>`__: ENH: stats: Add \`nan_policy\` optional argument for \`stats.rankdata\`
* `#16224 <https://github.com/scipy/scipy/pull/16224>`__: Add a \`pchip\` mode to RegularGridInterpolator.
* `#16227 <https://github.com/scipy/scipy/pull/16227>`__: BUG: special: Fix a couple issues with the 'double-double' code...
* `#16238 <https://github.com/scipy/scipy/pull/16238>`__: MAINT: stats: support string array for _contains_nan and add...
* `#16268 <https://github.com/scipy/scipy/pull/16268>`__: DOC: optimize: add marginals/slack example to \`linprog\`
* `#16294 <https://github.com/scipy/scipy/pull/16294>`__: BUG: linalg: Add precision preservation for \`sqrtm\`
* `#16298 <https://github.com/scipy/scipy/pull/16298>`__: REL: set version to 1.10.0.dev0
* `#16299 <https://github.com/scipy/scipy/pull/16299>`__: DEP: Execute deprecation of scipy.linalg.blas.{clapack, flapack}
* `#16307 <https://github.com/scipy/scipy/pull/16307>`__: DEP: add deprecation warning for binom_test
* `#16315 <https://github.com/scipy/scipy/pull/16315>`__: DEP: add deprecation warning for kwargs nyq / Hz in firwin
* `#16317 <https://github.com/scipy/scipy/pull/16317>`__: ENH: stats: add truncated (i.e. upper bounded) Pareto distribution...
* `#16320 <https://github.com/scipy/scipy/pull/16320>`__: ENH: improved accuracy and orthonormality of output eigenvectors...
* `#16327 <https://github.com/scipy/scipy/pull/16327>`__: DOC: BLD: remove \`-scipyopt\` from html Make command and build...
* `#16328 <https://github.com/scipy/scipy/pull/16328>`__: MAINT: retry openblas download in CI
* `#16332 <https://github.com/scipy/scipy/pull/16332>`__: BLD: ensure we get understandable messages when git submodules...
* `#16335 <https://github.com/scipy/scipy/pull/16335>`__: BLD: update NumPy to >=1.19.5
* `#16336 <https://github.com/scipy/scipy/pull/16336>`__: MAINT: forward port git scoping
* `#16340 <https://github.com/scipy/scipy/pull/16340>`__: DEP: remove tol & max_intervals from NumericalInverseHermite
* `#16346 <https://github.com/scipy/scipy/pull/16346>`__: DEV: add meson-python to environment.yml
* `#16351 <https://github.com/scipy/scipy/pull/16351>`__: Added "import numpy as np" statement to filter examples
* `#16354 <https://github.com/scipy/scipy/pull/16354>`__: DOC: optimize: remove callback doc from the options in \`_minimize_lbfgsb\`...
* `#16355 <https://github.com/scipy/scipy/pull/16355>`__: DEP: add deprecation warnings to kwargs turbo / eigvals of linalg.eigh
* `#16356 <https://github.com/scipy/scipy/pull/16356>`__: DOC: add examples to \`signal.medfilt2d\`
* `#16357 <https://github.com/scipy/scipy/pull/16357>`__: BENCH: Add SHGO and DIRECT to optimization benchmark
* `#16362 <https://github.com/scipy/scipy/pull/16362>`__: ENH: Provide more information when a value is out of bounds in...
* `#16367 <https://github.com/scipy/scipy/pull/16367>`__: BUG: unclear error for invalid bracketing
* `#16371 <https://github.com/scipy/scipy/pull/16371>`__: MAINT: remove last (already safe) usage of \`mktemp\`
* `#16372 <https://github.com/scipy/scipy/pull/16372>`__: MAINT: rename \`do.py\` to \`dev.py\`
* `#16373 <https://github.com/scipy/scipy/pull/16373>`__: DOC: added rvalue description in \`stats.probplot\`
* `#16377 <https://github.com/scipy/scipy/pull/16377>`__: ENH: stats.bootstrap: update warning to mention np.min
* `#16383 <https://github.com/scipy/scipy/pull/16383>`__: BUG: fix error message of RegularGridInterpolator
* `#16387 <https://github.com/scipy/scipy/pull/16387>`__: ENH: stats.combine_pvalues: convert output tuple to Bunch
* `#16388 <https://github.com/scipy/scipy/pull/16388>`__: DEP: deprecate \`stats.kendalltau\` kwarg \`initial_lexsort\`
* `#16389 <https://github.com/scipy/scipy/pull/16389>`__: DEP: sharpen stats deprecations
* `#16392 <https://github.com/scipy/scipy/pull/16392>`__: DEP: add warning to \`sparse.gmres\` deprecated kwarg \`restrt\`
* `#16397 <https://github.com/scipy/scipy/pull/16397>`__: MAINT: fix two refcounting issues in \`ndimage\`
* `#16398 <https://github.com/scipy/scipy/pull/16398>`__: MAINT: Replace find_common_types
* `#16406 <https://github.com/scipy/scipy/pull/16406>`__: MAINT: stats.rankdata: change default to nan_policy='propagate'
* `#16407 <https://github.com/scipy/scipy/pull/16407>`__: ENH: stats.fisher_exact: convert output tuple to Bunch
* `#16411 <https://github.com/scipy/scipy/pull/16411>`__: MAINT: optimize.brute should coerce non-tuple args to tuple
* `#16415 <https://github.com/scipy/scipy/pull/16415>`__: DOC: stats: fix seed -> random_state in \`rvs\` docstring
* `#16423 <https://github.com/scipy/scipy/pull/16423>`__: MAINT: stats: not using nested TypeErrors in _contains_nan
* `#16424 <https://github.com/scipy/scipy/pull/16424>`__: MAINT: future-proof \`stats.kde\` for changes in numpy casting...
* `#16425 <https://github.com/scipy/scipy/pull/16425>`__: DOC: Procedure adjustment in file doc/source/dev/core-dev/releasing.rst.inc
* `#16428 <https://github.com/scipy/scipy/pull/16428>`__: MAINT: fix up \`_sputils.get_index_dtype\` for NEP 50 casting...
* `#16431 <https://github.com/scipy/scipy/pull/16431>`__: CI: fix Gitpod build after dev.py update to the new CLI
* `#16432 <https://github.com/scipy/scipy/pull/16432>`__: Docstring fixes in lobpcg.py
* `#16434 <https://github.com/scipy/scipy/pull/16434>`__: DOC: stats.mstats.sen_seasonal_slopes: add docstring
* `#16435 <https://github.com/scipy/scipy/pull/16435>`__: ENH: directional mean
* `#16438 <https://github.com/scipy/scipy/pull/16438>`__: MAINT: remove unused \`DeprecatedImport\`
* `#16439 <https://github.com/scipy/scipy/pull/16439>`__: ENH: stats.chi2_contingency: convert output tuple to Bunch
* `#16440 <https://github.com/scipy/scipy/pull/16440>`__: ENH: stats.median_test: convert output tuple to Bunch
* `#16441 <https://github.com/scipy/scipy/pull/16441>`__: ENH: stats.mood: convert output tuple to Bunch
* `#16442 <https://github.com/scipy/scipy/pull/16442>`__: MAINT: fix issues with Python scalar related casting behavior...
* `#16447 <https://github.com/scipy/scipy/pull/16447>`__: BLD: make it easier to build with AddressSanitizer
* `#16449 <https://github.com/scipy/scipy/pull/16449>`__: ENH: improve scipy.interpolate.RegularGridInterpolator performance
* `#16450 <https://github.com/scipy/scipy/pull/16450>`__: BUG: Fix CLI Help in light themes
* `#16454 <https://github.com/scipy/scipy/pull/16454>`__: ENH: stats.bootstrap: return bootstrap distribution
* `#16455 <https://github.com/scipy/scipy/pull/16455>`__: ENH: stats.bootstrap: add BCa method for multi-sample statistic
* `#16462 <https://github.com/scipy/scipy/pull/16462>`__: CI: Update Python 3.8-dbg job to ubuntu-20.04
* `#16463 <https://github.com/scipy/scipy/pull/16463>`__: ENH: stats.jarque_bera: add axis, nan_policy, masked array support
* `#16470 <https://github.com/scipy/scipy/pull/16470>`__: DOC: stats.spearmanr: add information about p-value calculation
* `#16471 <https://github.com/scipy/scipy/pull/16471>`__: MAINT: interpolate/RGI: only call \`find_indices\` when needed
* `#16474 <https://github.com/scipy/scipy/pull/16474>`__: DOC: Add more information to entropy docstring
* `#16475 <https://github.com/scipy/scipy/pull/16475>`__: BLD: build the f2py shared source file once and link to each...
* `#16481 <https://github.com/scipy/scipy/pull/16481>`__: BUG: Change (n+1) to n for correct jackknife calculation of hd...
* `#16486 <https://github.com/scipy/scipy/pull/16486>`__: DOC: special.entr: add context
* `#16487 <https://github.com/scipy/scipy/pull/16487>`__: MAINT: Improve test speed, add timeouts
* `#16496 <https://github.com/scipy/scipy/pull/16496>`__: add notes for x and y array sorted in decreasing order
* `#16497 <https://github.com/scipy/scipy/pull/16497>`__: DOC: special: Add 'Examples' section to spence docstring.
* `#16498 <https://github.com/scipy/scipy/pull/16498>`__: ENH: Speed up hdquantile_sd via cumulative sums
* `#16501 <https://github.com/scipy/scipy/pull/16501>`__: DOC: Fix typo in spatial.Delaunay
* `#16502 <https://github.com/scipy/scipy/pull/16502>`__: DOC: Minor Rst syntax update.
* `#16503 <https://github.com/scipy/scipy/pull/16503>`__: ENH: stats: Implement _munp() for the skewnorm distribution.
* `#16505 <https://github.com/scipy/scipy/pull/16505>`__: DOC: correct errs on examples for scipy.signal.upfirdn
* `#16508 <https://github.com/scipy/scipy/pull/16508>`__: BUG/ENH: handle spline interpolation methods in \`interpn\` and...
* `#16511 <https://github.com/scipy/scipy/pull/16511>`__: add reference to regulargridinterpolator
* `#16513 <https://github.com/scipy/scipy/pull/16513>`__: MAINT: skip complex128 propack tests on windows (& module clean-up)
* `#16516 <https://github.com/scipy/scipy/pull/16516>`__: DOC: add a hint on what to use in case of matlab v7.3
* `#16518 <https://github.com/scipy/scipy/pull/16518>`__: CI: pip and conda caching in all workflows
* `#16524 <https://github.com/scipy/scipy/pull/16524>`__: TST: stats.permutation_test: strengthen test against \`ks_2samp\`
* `#16529 <https://github.com/scipy/scipy/pull/16529>`__: CI: clean up scikit-umfpack and scikit-sparse usage in CI
* `#16532 <https://github.com/scipy/scipy/pull/16532>`__: Deprecated imports in docstring examples in \`io.harwell_boeing\`...
* `#16533 <https://github.com/scipy/scipy/pull/16533>`__: ENH: signal: add Lanczos window function
* `#16534 <https://github.com/scipy/scipy/pull/16534>`__: CI: fix scikit-umfpack and scikit-sparse install in Azure job
* `#16535 <https://github.com/scipy/scipy/pull/16535>`__: MAINT: signal: Fix matplotlib deprecation warning in the chirp...
* `#16543 <https://github.com/scipy/scipy/pull/16543>`__: DOC: update cwt doc examples
* `#16544 <https://github.com/scipy/scipy/pull/16544>`__: DOC: add better example for \`MultinomialQMC\`.
* `#16546 <https://github.com/scipy/scipy/pull/16546>`__: DOC: Add alt-text to tutorial images
* `#16547 <https://github.com/scipy/scipy/pull/16547>`__: ENH: correct bounds warnings in \`minimize\`
* `#16550 <https://github.com/scipy/scipy/pull/16550>`__: TST: fix flaky sparse.linalg.exmp test
* `#16552 <https://github.com/scipy/scipy/pull/16552>`__: CI: test distro Python install on Ubuntu Jammy (22.04 LTS)
* `#16554 <https://github.com/scipy/scipy/pull/16554>`__: TST: add timeout to \`test_kappa4_array_gh13582\`
* `#16557 <https://github.com/scipy/scipy/pull/16557>`__: BUG: fix \`interpolate.RegularGridInterpolator\` \`out_of_bounds\`...
* `#16559 <https://github.com/scipy/scipy/pull/16559>`__: ENH: adding a logpdf function to von-mises distribution
* `#16560 <https://github.com/scipy/scipy/pull/16560>`__: vectorize ortho_group.rvs
* `#16561 <https://github.com/scipy/scipy/pull/16561>`__: DOC: optimize: Fix warning in differential_evolution docstring
* `#16565 <https://github.com/scipy/scipy/pull/16565>`__: [DOC] improper type syntax in basinhopping docstring.
* `#16566 <https://github.com/scipy/scipy/pull/16566>`__: fix window function doc string for Window length
* `#16567 <https://github.com/scipy/scipy/pull/16567>`__: DOC: Add note about inaccuracies in matrix functions
* `#16571 <https://github.com/scipy/scipy/pull/16571>`__: DOC: sparse.linalg: add references for UMFPACK.
* `#16574 <https://github.com/scipy/scipy/pull/16574>`__: ENH: vectorize along samples \`stats.ortho_group.rvs\` and \`stats.unitary_group.rvs\`
* `#16576 <https://github.com/scipy/scipy/pull/16576>`__: testing documentation broken link fix
* `#16587 <https://github.com/scipy/scipy/pull/16587>`__: DOC: add import NumPy in QMC examples.
* `#16589 <https://github.com/scipy/scipy/pull/16589>`__: DOC: update toolchain.rst after EOL of manylinux_2_24; allow...
* `#16591 <https://github.com/scipy/scipy/pull/16591>`__: ENH: stats.nct: replace with boost implementation
* `#16592 <https://github.com/scipy/scipy/pull/16592>`__: DOC: interpolate: document the .roots() workaround
* `#16594 <https://github.com/scipy/scipy/pull/16594>`__: MAINT: Better pytest-timeout support
* `#16596 <https://github.com/scipy/scipy/pull/16596>`__: MAINT: stats.rv_continuous: consistently return NumPy scalars
* `#16607 <https://github.com/scipy/scipy/pull/16607>`__: MAINT: remove unnecessary \`__future__\` imports
* `#16608 <https://github.com/scipy/scipy/pull/16608>`__: TST: stats.rv_continuous: more direct test for numpy scalar output
* `#16612 <https://github.com/scipy/scipy/pull/16612>`__: ENH: vectorize along samples \`stats.special_ortho_group.rvs\`
* `#16614 <https://github.com/scipy/scipy/pull/16614>`__: DOC: add import NumPy in linalg decomposition function examples
* `#16615 <https://github.com/scipy/scipy/pull/16615>`__: DOC: Adding import numpy to several files
* `#16616 <https://github.com/scipy/scipy/pull/16616>`__: DOC: Adding import numpy to examples in some stats files
* `#16617 <https://github.com/scipy/scipy/pull/16617>`__: DOC: Update instructions for debugging using dev.py
* `#16618 <https://github.com/scipy/scipy/pull/16618>`__: DOC: add import NumPy in bsplines examples
* `#16619 <https://github.com/scipy/scipy/pull/16619>`__: DOC: add import numpy in some stats examples
* `#16620 <https://github.com/scipy/scipy/pull/16620>`__: DOC: Add numpy import to examples
* `#16621 <https://github.com/scipy/scipy/pull/16621>`__: FIX: upstream fix for binomial distribution divide-by-zero
* `#16624 <https://github.com/scipy/scipy/pull/16624>`__: DOC: add NumPy imports in \`_mstats_basic.py\` examples
* `#16625 <https://github.com/scipy/scipy/pull/16625>`__: DOC: add \`import numpy as np\` to examples
* `#16626 <https://github.com/scipy/scipy/pull/16626>`__: BUG: cluster: fix \`leaves_color_list\` issue
* `#16627 <https://github.com/scipy/scipy/pull/16627>`__: TST: spatial.directed_hausdorff: Parametrized test_random_state_None_int
* `#16629 <https://github.com/scipy/scipy/pull/16629>`__: DOC: Modifiy the scipy.stats.mode example to be nontrivial.
* `#16631 <https://github.com/scipy/scipy/pull/16631>`__: MAINT: stats.gaussian_kde: raise informative message with degenerate...
* `#16632 <https://github.com/scipy/scipy/pull/16632>`__: MAINT: signal:corrected peak_finding example
* `#16633 <https://github.com/scipy/scipy/pull/16633>`__: DOC: update benchmarking docs to use dev.py user interface
* `#16634 <https://github.com/scipy/scipy/pull/16634>`__: DOC: Add example to fft.fht
* `#16635 <https://github.com/scipy/scipy/pull/16635>`__: DOC: fix default_rng namespace and linestyle of an example
* `#16639 <https://github.com/scipy/scipy/pull/16639>`__: DOC: better links in readme for newcomers
* `#16640 <https://github.com/scipy/scipy/pull/16640>`__: MAINT: optimize: always return a float from goal functional wrapper
* `#16641 <https://github.com/scipy/scipy/pull/16641>`__: DOC: optimize: fix doc that \`curve_fit\` xdata should be float...
* `#16644 <https://github.com/scipy/scipy/pull/16644>`__: DOC: io: Add Examples section for mminfo, mmread and mmwrite.
* `#16646 <https://github.com/scipy/scipy/pull/16646>`__: MAINT: have get_index_dtype follow its documentation and return...
* `#16647 <https://github.com/scipy/scipy/pull/16647>`__: MAINT: Fix expit function name typo in test_optimize.py
* `#16650 <https://github.com/scipy/scipy/pull/16650>`__: DOC: io: Add 'Examples' to the 'whosmat' docstring.
* `#16651 <https://github.com/scipy/scipy/pull/16651>`__: ENH: stats.resampling: automatically detect whether statistic...
* `#16652 <https://github.com/scipy/scipy/pull/16652>`__: MAINT: Remove unused imports.
* `#16653 <https://github.com/scipy/scipy/pull/16653>`__: DEV: generalized cross-validation smoothing spline
* `#16654 <https://github.com/scipy/scipy/pull/16654>`__: ENH: stats: add aliases to results objects
* `#16658 <https://github.com/scipy/scipy/pull/16658>`__: BUG: signal: Compare window_length to correct axis in savgol_filter
* `#16659 <https://github.com/scipy/scipy/pull/16659>`__: DOC: replace \`sphinx_panels\` and \`sphinx_tabs\` with \`sphinx_design\`
* `#16666 <https://github.com/scipy/scipy/pull/16666>`__: MAINT: remove unused \`__main__\` code from \`optimize\` submodule
* `#16667 <https://github.com/scipy/scipy/pull/16667>`__: DOC: spatial: Correct barycentric description in Delaunay
* `#16668 <https://github.com/scipy/scipy/pull/16668>`__: DOC: signal: Update values in zpk2sos docstring examples.
* `#16670 <https://github.com/scipy/scipy/pull/16670>`__: MAINT: fix a compiler warning in \`signal/_firfilter.c\`
* `#16672 <https://github.com/scipy/scipy/pull/16672>`__: BLD: update minimum \`meson\` and \`meson-python\` versions
* `#16675 <https://github.com/scipy/scipy/pull/16675>`__: TST: sparse.linalg: increase \`lobpcg\` solve tolerance in test
* `#16676 <https://github.com/scipy/scipy/pull/16676>`__: MAINT: stats.mstats.mode: refactor to keep \`kwargs\` out of...
* `#16677 <https://github.com/scipy/scipy/pull/16677>`__: TST: speed up mindist test
* `#16678 <https://github.com/scipy/scipy/pull/16678>`__: DOC: remove custom colours in css
* `#16680 <https://github.com/scipy/scipy/pull/16680>`__: MAINT: stats.gmean: corrections with \`axis=None\` when masked-array...
* `#16683 <https://github.com/scipy/scipy/pull/16683>`__: DEV: add \`--durations\` argument to dev.py interface
* `#16685 <https://github.com/scipy/scipy/pull/16685>`__: BLD: implement compiler version checks for GCC and MSVC
* `#16687 <https://github.com/scipy/scipy/pull/16687>`__: DOC: signal: Update the examples in the remez docstring.
* `#16689 <https://github.com/scipy/scipy/pull/16689>`__: MAINT: sparse.linalg: remove LGMRES demo
* `#16690 <https://github.com/scipy/scipy/pull/16690>`__: random uniform -> normal to initiate lobpcg and arpack in svds
* `#16691 <https://github.com/scipy/scipy/pull/16691>`__: ENH: stats: Implement isf for the levy distribution.
* `#16692 <https://github.com/scipy/scipy/pull/16692>`__: ENH: stats.gaussian_kde: replace use of inv_cov in pdf
* `#16696 <https://github.com/scipy/scipy/pull/16696>`__: ENH: Speed up sparse.csgraph.dijkstra
* `#16699 <https://github.com/scipy/scipy/pull/16699>`__: DOC: stats: resampling and Monte Carlo methods tutorial
* `#16703 <https://github.com/scipy/scipy/pull/16703>`__: BLD: upgrade meson(-python) min versions and remove explicit...
* `#16704 <https://github.com/scipy/scipy/pull/16704>`__: DOC: improve some MSVC links in toolchain.rst
* `#16705 <https://github.com/scipy/scipy/pull/16705>`__: MAINT: add \`__bool__\` method to spatial.transform.Rotation
* `#16706 <https://github.com/scipy/scipy/pull/16706>`__: CI: add Meson version number in environment.yml to rebuild Docker...
* `#16707 <https://github.com/scipy/scipy/pull/16707>`__: DOC: expand the \`scipy.interpolate\` tutorial
* `#16712 <https://github.com/scipy/scipy/pull/16712>`__: BUG: Update _svds.py: orthogonalize eigenvectors from arpack...
* `#16714 <https://github.com/scipy/scipy/pull/16714>`__: ENH: stats.bootstrap: extend previous bootstrap result
* `#16715 <https://github.com/scipy/scipy/pull/16715>`__: DOC: interpolate: add an example of splPrep/PPoly.from_spline...
* `#16717 <https://github.com/scipy/scipy/pull/16717>`__: DOC: reformat seed docstrings
* `#16722 <https://github.com/scipy/scipy/pull/16722>`__: MAINT: additional test truthiness and length the empty Rotation
* `#16730 <https://github.com/scipy/scipy/pull/16730>`__: MAINT: interpolate: use _fitpack_impl in fitpack2
* `#16731 <https://github.com/scipy/scipy/pull/16731>`__: ENH: interpolate.KroghInterpolator: raise warning about numerical...
* `#16732 <https://github.com/scipy/scipy/pull/16732>`__: DOC: Replace runtests.py with dev.py where appropriate
* `#16733 <https://github.com/scipy/scipy/pull/16733>`__: DOC: Add link to development workflow
* `#16735 <https://github.com/scipy/scipy/pull/16735>`__: DOC: forward port 1.9.0 relnotes
* `#16738 <https://github.com/scipy/scipy/pull/16738>`__: REL: DOC: update version switcher
* `#16739 <https://github.com/scipy/scipy/pull/16739>`__: CI: move the py311-dev job over to Meson
* `#16740 <https://github.com/scipy/scipy/pull/16740>`__: DOC: Fix Sphinx markup.
* `#16742 <https://github.com/scipy/scipy/pull/16742>`__: CI: move test_numpy_main to linux_meson
* `#16743 <https://github.com/scipy/scipy/pull/16743>`__: DEP: interpolate: revert docstring only deprecation of fitpack...
* `#16747 <https://github.com/scipy/scipy/pull/16747>`__: DOC: sparse.linalg: Fix output in an example in the lobpcg docstring.
* `#16753 <https://github.com/scipy/scipy/pull/16753>`__: DOC: Integrate: Add improper integral examples for \`dblquad\`...
* `#16754 <https://github.com/scipy/scipy/pull/16754>`__: DOC: optimize: Fix mistake in a linprog example.
* `#16755 <https://github.com/scipy/scipy/pull/16755>`__: TST: sparse.linalg: Loosen tolerance for the lobpcg test 'test_tolerance_float32'
* `#16756 <https://github.com/scipy/scipy/pull/16756>`__: TST: test fixes for pypy
* `#16758 <https://github.com/scipy/scipy/pull/16758>`__: ENH: Release the GIL while computing KDE kernel estimate
* `#16761 <https://github.com/scipy/scipy/pull/16761>`__: DOC: add logo to readme.
* `#16762 <https://github.com/scipy/scipy/pull/16762>`__: MAINT: stats: mark slow tests
* `#16766 <https://github.com/scipy/scipy/pull/16766>`__: DOC: toolchain: fix numpy dependency for 1.7.2/3
* `#16770 <https://github.com/scipy/scipy/pull/16770>`__: ENH: stats: use Boost implementation of skewnorm cdf/ppf
* `#16772 <https://github.com/scipy/scipy/pull/16772>`__: DOC: add one :math: to docstring for consistency
* `#16776 <https://github.com/scipy/scipy/pull/16776>`__: BUG: Set nperseg size to the size of an already-initialized window...
* `#16778 <https://github.com/scipy/scipy/pull/16778>`__: MAINT: fix a couple of Mypy errors that appeared recently
* `#16779 <https://github.com/scipy/scipy/pull/16779>`__: TST: Interpolate: Move incorrectly located NDInterpolator tests
* `#16788 <https://github.com/scipy/scipy/pull/16788>`__: DOC, TST: clarify Voronoi Qz
* `#16790 <https://github.com/scipy/scipy/pull/16790>`__: ENH: stats.invgauss: use Boost implementation of ppf/isf
* `#16791 <https://github.com/scipy/scipy/pull/16791>`__: MAINT: stats.skewnorm: fix fit when data skewness is greater...
* `#16793 <https://github.com/scipy/scipy/pull/16793>`__: DOC: optimize: add tutorial for milp
* `#16795 <https://github.com/scipy/scipy/pull/16795>`__: DOC: Embed method signatures of \`spatial.transform.Rotation\`
* `#16797 <https://github.com/scipy/scipy/pull/16797>`__: ENH add extrapolate to BSpline.design_matrix
* `#16799 <https://github.com/scipy/scipy/pull/16799>`__: DOC: optimize.root_scalar: improve parametrization of methods
* `#16800 <https://github.com/scipy/scipy/pull/16800>`__: MAINT: remove \`_lib/_c99compat.h\` and use C99 rather than \`npy_math.h\`...
* `#16801 <https://github.com/scipy/scipy/pull/16801>`__: ENH: added the spectral 2-norm to _norm.py
* `#16804 <https://github.com/scipy/scipy/pull/16804>`__: ENH: stats.weibull_min: override fit
* `#16806 <https://github.com/scipy/scipy/pull/16806>`__: DEV: update pydevtool version to propagate exit codes
* `#16809 <https://github.com/scipy/scipy/pull/16809>`__: Doc: Added missing "import numpy as np" to docstring examples...
* `#16811 <https://github.com/scipy/scipy/pull/16811>`__: DOC: fix broken links
* `#16816 <https://github.com/scipy/scipy/pull/16816>`__: MAINT: special: remove one \`libnpymath\` dependency; more \`NPY_\`...
* `#16817 <https://github.com/scipy/scipy/pull/16817>`__: MAINT: remove \`NPY_INLINE\`, use \`inline\` instead
* `#16818 <https://github.com/scipy/scipy/pull/16818>`__: MAINT: update PROPACK git submodule to get rid of prints in test...
* `#16826 <https://github.com/scipy/scipy/pull/16826>`__: MAINT: fix some build warnings from \`special/ellip_harm.pxd\`
* `#16828 <https://github.com/scipy/scipy/pull/16828>`__: DOC: add NumPy import in scipy.io examples
* `#16829 <https://github.com/scipy/scipy/pull/16829>`__: Interpn nonscalar followup
* `#16830 <https://github.com/scipy/scipy/pull/16830>`__: DOC: Add plot to circmean docstring
* `#16831 <https://github.com/scipy/scipy/pull/16831>`__: DOC: special: Several docstring updates.
* `#16832 <https://github.com/scipy/scipy/pull/16832>`__: DOC: add NumPy import in scipy.optimize examples
* `#16834 <https://github.com/scipy/scipy/pull/16834>`__: DOC: Improve circular stats doc
* `#16835 <https://github.com/scipy/scipy/pull/16835>`__: ENH: stats.ttest_1samp: add confidence_interval and df
* `#16837 <https://github.com/scipy/scipy/pull/16837>`__: DOC: interpolate: small example code improvement for \`BSpline.basis_element\`
* `#16840 <https://github.com/scipy/scipy/pull/16840>`__: ENH: BSplines.design_matrix performance improvement
* `#16843 <https://github.com/scipy/scipy/pull/16843>`__: ENH: Handle np array methods in stats.binned_statistic_dd
* `#16847 <https://github.com/scipy/scipy/pull/16847>`__: DOC: interpolate.{RegularGridInterpolator, interpn} add note...
* `#16848 <https://github.com/scipy/scipy/pull/16848>`__: ENH: stats.anderson: add fit parameters to result
* `#16853 <https://github.com/scipy/scipy/pull/16853>`__: DOC: interpolate: improve \`interpolate.make_interp.spline\`...
* `#16854 <https://github.com/scipy/scipy/pull/16854>`__: MAINT: Delay \`pooch\` import error for \`scipy.datasets\`
* `#16855 <https://github.com/scipy/scipy/pull/16855>`__: Roadmap update: scipy.interpolate and Fortran libs
* `#16856 <https://github.com/scipy/scipy/pull/16856>`__: DOC: interpolate: add default spline degree value for \`InterpolatedUnivariateSpline\`
* `#16857 <https://github.com/scipy/scipy/pull/16857>`__: ENH : remove an expected warning in BarycentricInterpolator
* `#16858 <https://github.com/scipy/scipy/pull/16858>`__: ENH: Modify scipy.optimize.least_squares to accept bounds of...
* `#16860 <https://github.com/scipy/scipy/pull/16860>`__: DOC: interpolate: improve spline smoothing parameter docs.
* `#16863 <https://github.com/scipy/scipy/pull/16863>`__: DOC: Adding docs contribution guidelines
* `#16864 <https://github.com/scipy/scipy/pull/16864>`__: DOC: stats: Some updates:
* `#16865 <https://github.com/scipy/scipy/pull/16865>`__: DOC: interpolate: improve \`make_lsq_spline\` docs
* `#16866 <https://github.com/scipy/scipy/pull/16866>`__: DEP, DOC: Show deprecated methods in docs and fix overwriting...
* `#16867 <https://github.com/scipy/scipy/pull/16867>`__: DOC: fix an accuracy issue in the docstring of \`Rotation.align_vectors\`
* `#16869 <https://github.com/scipy/scipy/pull/16869>`__: DOC: Added missing 'import numpy as np' to docstring examples...
* `#16873 <https://github.com/scipy/scipy/pull/16873>`__: MAINT: stats.multinomial: don't alter p[-1] when p[:-1].sum()...
* `#16874 <https://github.com/scipy/scipy/pull/16874>`__: DOC: signal: Add 'Examples' to the 'normalize' docstring.
* `#16884 <https://github.com/scipy/scipy/pull/16884>`__: DOC: improve installing from source instructions
* `#16885 <https://github.com/scipy/scipy/pull/16885>`__: TST: Interpolate: Parameterise RegularGridInterpolator tests
* `#16886 <https://github.com/scipy/scipy/pull/16886>`__: CI: wheels only on scipy [skip azp][skip github]
* `#16887 <https://github.com/scipy/scipy/pull/16887>`__: DOC: optimize.linprog: adjust tutorial to address gh16531
* `#16888 <https://github.com/scipy/scipy/pull/16888>`__: DOC: outline how cibuildwheel is triggered and runs in CI
* `#16889 <https://github.com/scipy/scipy/pull/16889>`__: MAINT: interpolate: Remove a couple unused imports.
* `#16890 <https://github.com/scipy/scipy/pull/16890>`__: ENH: optimize.OptimizeResult: improve pretty-printing
* `#16891 <https://github.com/scipy/scipy/pull/16891>`__: TST: Interpolate: rename test so that is executed
* `#16893 <https://github.com/scipy/scipy/pull/16893>`__: DOC: add diagram explaining how Docker images get built and used...
* `#16896 <https://github.com/scipy/scipy/pull/16896>`__: DOC: Fix broken link in the "Additional Git Resources" page.
* `#16897 <https://github.com/scipy/scipy/pull/16897>`__: Pass down mip_rel_gap to the HiGHS optimizer
* `#16899 <https://github.com/scipy/scipy/pull/16899>`__: DOC: add legend to rv_histogram plot
* `#16902 <https://github.com/scipy/scipy/pull/16902>`__: ENH: stats.ttest_rel: add confidence_interval to result
* `#16903 <https://github.com/scipy/scipy/pull/16903>`__: DOC: interpolate: add actual smoothing condition for \`UnivariateSpline\`
* `#16906 <https://github.com/scipy/scipy/pull/16906>`__: DOC: fixes for refguide check issues
* `#16907 <https://github.com/scipy/scipy/pull/16907>`__: BUG: stats: expect method of the vonmises distribution
* `#16910 <https://github.com/scipy/scipy/pull/16910>`__: MAINT: forward port 1.9.1 relnotes
* `#16913 <https://github.com/scipy/scipy/pull/16913>`__: ENH:interpolate: allow interp1d to take single value
* `#16916 <https://github.com/scipy/scipy/pull/16916>`__: DOC: add note about using interpn for data on a regular grid
* `#16923 <https://github.com/scipy/scipy/pull/16923>`__: MAINT: integrate.qmc_quad: add QMC quadrature
* `#16924 <https://github.com/scipy/scipy/pull/16924>`__: Fix compilation with -Wincompatible-function-pointer-types
* `#16931 <https://github.com/scipy/scipy/pull/16931>`__: DOC: add details on Meson build debugging and introspection
* `#16933 <https://github.com/scipy/scipy/pull/16933>`__: MAINT : interpolate: added test for DivideByZero warning silencing...
* `#16937 <https://github.com/scipy/scipy/pull/16937>`__: MAINT: refer to python3 in refguide_check
* `#16939 <https://github.com/scipy/scipy/pull/16939>`__: MAINT: stats: move \`_contains_nan\` function to \`_lib._util.py\`
* `#16940 <https://github.com/scipy/scipy/pull/16940>`__: DOC: Documentation note update for truncnorm
* `#16941 <https://github.com/scipy/scipy/pull/16941>`__: MAINT: support logpdf in NumericalInverseHermite (stats.sampling)
* `#16948 <https://github.com/scipy/scipy/pull/16948>`__: DOC: sparse.linalg.svds: fix intermittent refguide check failure
* `#16950 <https://github.com/scipy/scipy/pull/16950>`__: DOC: Add examples for common Bessel functions
* `#16951 <https://github.com/scipy/scipy/pull/16951>`__: ENH: stats.fit: add plot_types to FitResult.plot
* `#16953 <https://github.com/scipy/scipy/pull/16953>`__: DEV: update dev.py to only install changed files
* `#16955 <https://github.com/scipy/scipy/pull/16955>`__: BLD: fix up or suppress Fortran build warnings
* `#16956 <https://github.com/scipy/scipy/pull/16956>`__: BLD: fix meson version checks for MSVC
* `#16958 <https://github.com/scipy/scipy/pull/16958>`__: ENH: stats.crosstab: convert output tuple to bunch
* `#16959 <https://github.com/scipy/scipy/pull/16959>`__: DOC: Add example for morlet in scipy.signal
* `#16960 <https://github.com/scipy/scipy/pull/16960>`__: DOC: Fix indentation in benchmarking.rst
* `#16963 <https://github.com/scipy/scipy/pull/16963>`__: DOC: Update 2 links to point to stable.
* `#16967 <https://github.com/scipy/scipy/pull/16967>`__: ENH: stats.goodness_of_fit: a general goodness of fit test
* `#16968 <https://github.com/scipy/scipy/pull/16968>`__: ENH: Close parenthesis in numpy version warning
* `#16976 <https://github.com/scipy/scipy/pull/16976>`__: DOC: stats.qmc: fix description of seed parameter
* `#16980 <https://github.com/scipy/scipy/pull/16980>`__: DOC: fix duplicate word typos.
* `#16986 <https://github.com/scipy/scipy/pull/16986>`__: DOC: Fix link to rendered docs in documentation guide
* `#16987 <https://github.com/scipy/scipy/pull/16987>`__: ENH: stats.gaussian_kde: replace use of inv_cov in logpdf
* `#16989 <https://github.com/scipy/scipy/pull/16989>`__: DOC: edited t_span parameter description in integrate.solve_ivp
* `#16990 <https://github.com/scipy/scipy/pull/16990>`__: CI: enable uploads for (weekly) nightlies and update how action...
* `#16992 <https://github.com/scipy/scipy/pull/16992>`__: CI: upgrade CI image to run on Ubuntu 22.04 instead of 20.04
* `#16995 <https://github.com/scipy/scipy/pull/16995>`__: DOC: stats: fix incorrectly documented statistic attribute for...
* `#17003 <https://github.com/scipy/scipy/pull/17003>`__: DOC: Add examples for a few Bessel functions
* `#17005 <https://github.com/scipy/scipy/pull/17005>`__: CI: pin OpenBLAS to specific build in macOS job to avoid gges...
* `#17006 <https://github.com/scipy/scipy/pull/17006>`__: ENH: stats.spearmanr: add statistic attribute to result object...
* `#17007 <https://github.com/scipy/scipy/pull/17007>`__: ENH: stats.kendalltau: add statistic attribute to result object...
* `#17008 <https://github.com/scipy/scipy/pull/17008>`__: ENH: stats.weightedtau: add statistic attribute to result object
* `#17009 <https://github.com/scipy/scipy/pull/17009>`__: Revert "CI: pin OpenBLAS to specific build in macOS job to avoid...
* `#17014 <https://github.com/scipy/scipy/pull/17014>`__: MAINT: remove unused variables and imports
* `#17016 <https://github.com/scipy/scipy/pull/17016>`__: ENH: stats.pearsonr, stats.pointbiserialr: add statistic/correlation...
* `#17017 <https://github.com/scipy/scipy/pull/17017>`__: ENH: stats.somersd: add correlation attribute to result object
* `#17021 <https://github.com/scipy/scipy/pull/17021>`__: FIX: \`dev.py build\` parallelism behaviour and fixed typos
* `#17022 <https://github.com/scipy/scipy/pull/17022>`__: Explain where LIL comes from
* `#17027 <https://github.com/scipy/scipy/pull/17027>`__: Fix explanation of LIst of List sparse matrix
* `#17029 <https://github.com/scipy/scipy/pull/17029>`__: CI: cirrus for building aarch64
* `#17030 <https://github.com/scipy/scipy/pull/17030>`__: ENH: stats.permutation_test: improve performance of samples/pairings...
* `#17032 <https://github.com/scipy/scipy/pull/17032>`__: TST: stats.fit: fix random state
* `#17034 <https://github.com/scipy/scipy/pull/17034>`__: TST: stats.jarque_bera: fix test failure due to NumPy update
* `#17036 <https://github.com/scipy/scipy/pull/17036>`__: DEV: Update GPG key in Docker [Gitpod]
* `#17038 <https://github.com/scipy/scipy/pull/17038>`__: deduplicate \`splint\` in FITPACK wrappers; take 3
* `#17039 <https://github.com/scipy/scipy/pull/17039>`__: ENH: add a \`stats.expectile\` function
* `#17041 <https://github.com/scipy/scipy/pull/17041>`__: DOC: Add examples for integrals of Bessel functions
* `#17048 <https://github.com/scipy/scipy/pull/17048>`__: DOC:signal: Fix typo in TransferFunction
* `#17049 <https://github.com/scipy/scipy/pull/17049>`__: TST: stats.jarque_bera: fix test failure due to NumPy update
* `#17051 <https://github.com/scipy/scipy/pull/17051>`__: ENH: support complex functions in integrate.quad
* `#17052 <https://github.com/scipy/scipy/pull/17052>`__: BLD: implement symbol hiding for Meson through a linker version...
* `#17057 <https://github.com/scipy/scipy/pull/17057>`__: Fix or avoid various test failures that are showing up in CI
* `#17062 <https://github.com/scipy/scipy/pull/17062>`__: Add location and sign to KS test result
* `#17063 <https://github.com/scipy/scipy/pull/17063>`__: CI: fix uploading of nightly wheels
* `#17068 <https://github.com/scipy/scipy/pull/17068>`__: MAINT: Removed unused imports.
* `#17071 <https://github.com/scipy/scipy/pull/17071>`__: DOC: update maxfun in scipy.optimize.minimize(method=’L-BFGS-B’)...
* `#17073 <https://github.com/scipy/scipy/pull/17073>`__: DOC: examples for derivatives of Bessel functions
* `#17076 <https://github.com/scipy/scipy/pull/17076>`__: DOC: spatial: Copy-edit the voronoi_plot_2d example.
* `#17079 <https://github.com/scipy/scipy/pull/17079>`__: BUG: fix \`signal.sosfilt\` issue with complex dtypes and Intel...
* `#17081 <https://github.com/scipy/scipy/pull/17081>`__: DOC: Fix formatting in svds docstrings
* `#17083 <https://github.com/scipy/scipy/pull/17083>`__: DOC: Fix broken link for environment variables NumPy doc
* `#17085 <https://github.com/scipy/scipy/pull/17085>`__: DOC: optimize: add link to SciPy cookbooks milp tutorials
* `#17091 <https://github.com/scipy/scipy/pull/17091>`__: MAINT: interpolate remove duplication of FITPACK interface \`sproot\`.
* `#17093 <https://github.com/scipy/scipy/pull/17093>`__: ENH: Improves behavior of scipy.optimize.linprog (#17074)
* `#17094 <https://github.com/scipy/scipy/pull/17094>`__: DOC: examples for roots of Bessel functions
* `#17099 <https://github.com/scipy/scipy/pull/17099>`__: BLD: turn off fast-math for Intel compilers
* `#17103 <https://github.com/scipy/scipy/pull/17103>`__: ENH: stats.Covariance: add CovViaDiagonal
* `#17106 <https://github.com/scipy/scipy/pull/17106>`__: CI: fix testing of \`SCIPY_USE_PYTHRAN=0\`, and upgrade to pythran...
* `#17108 <https://github.com/scipy/scipy/pull/17108>`__: DOC: Reformulate ufunc description in special doc page
* `#17109 <https://github.com/scipy/scipy/pull/17109>`__: BLD: Ensure Intel Fortran handles negative 0 as expected.
* `#17110 <https://github.com/scipy/scipy/pull/17110>`__: DOC: add Numpy import to scipy.sparse examples
* `#17112 <https://github.com/scipy/scipy/pull/17112>`__: ENH: Add support for bounds class in curve_fit
* `#17115 <https://github.com/scipy/scipy/pull/17115>`__: DOC: add Numpy import to examples
* `#17117 <https://github.com/scipy/scipy/pull/17117>`__: ENH: stats.logistic: override fit for remaining cases
* `#17118 <https://github.com/scipy/scipy/pull/17118>`__: ENH: Support for complex functions in binned_statistic_dd
* `#17122 <https://github.com/scipy/scipy/pull/17122>`__: ENH: remove duplicate function call
* `#17126 <https://github.com/scipy/scipy/pull/17126>`__: MAINT, ENH: scipy.stats: Refactor \`directionalmean\` to return...
* `#17128 <https://github.com/scipy/scipy/pull/17128>`__: ENH: stats.covariance: add CovViaCholesky
* `#17130 <https://github.com/scipy/scipy/pull/17130>`__: DOC: remove inconsistent messages
* `#17135 <https://github.com/scipy/scipy/pull/17135>`__: ENH: stats.Covariance: specifying covariance matrix by its eigendecomposition
* `#17138 <https://github.com/scipy/scipy/pull/17138>`__: CI: add permission to GH actions.
* `#17140 <https://github.com/scipy/scipy/pull/17140>`__: BUG: Fix issue with shgo not correctly passing jac to minimizer
* `#17141 <https://github.com/scipy/scipy/pull/17141>`__: ENH: stats.fit: add maximum spacing estimation
* `#17144 <https://github.com/scipy/scipy/pull/17144>`__: DOC: replace \`set_tight_layout\` with \`set_layout_engine\`...
* `#17147 <https://github.com/scipy/scipy/pull/17147>`__: BENCH: remove \`--quick\` flag to \`asv run\` in dev.py
* `#17149 <https://github.com/scipy/scipy/pull/17149>`__: MAINT: remove certifi py3.11 warning filter
* `#17152 <https://github.com/scipy/scipy/pull/17152>`__: ENH/MAINT: \`qmc.LatinHypercube\`: deprecate centered with scramble
* `#17157 <https://github.com/scipy/scipy/pull/17157>`__: ENH: Added value_indices() function to scipy.ndimage
* `#17159 <https://github.com/scipy/scipy/pull/17159>`__: MAINT: spatial: Skip \`test_massive_arr_overflow\` on systems...
* `#17161 <https://github.com/scipy/scipy/pull/17161>`__: MAINT: stats.sampling.NumericalInverseHermite: private distribution...
* `#17163 <https://github.com/scipy/scipy/pull/17163>`__: ENH: Add \`download_all\` utility method & script
* `#17169 <https://github.com/scipy/scipy/pull/17169>`__: MAINT: special: Loosen the tolerance for a test of powm1.
* `#17170 <https://github.com/scipy/scipy/pull/17170>`__: MAINT: better handling of mode/center outside of the domain in...
* `#17175 <https://github.com/scipy/scipy/pull/17175>`__: MAINT: forward port 1.9.2 relnotes
* `#17177 <https://github.com/scipy/scipy/pull/17177>`__: DOC: stats: Fix versionadded markup for odds_ratio
* `#17178 <https://github.com/scipy/scipy/pull/17178>`__: DOC: interpolate: discuss failure modes of SmoothBivariateSpline
* `#17180 <https://github.com/scipy/scipy/pull/17180>`__: DEP: interpolate: deprecate interp2d
* `#17181 <https://github.com/scipy/scipy/pull/17181>`__: CI: Fix when wheels are built for staging
* `#17182 <https://github.com/scipy/scipy/pull/17182>`__: MAINT: fix typo "mat[r]ix"
* `#17183 <https://github.com/scipy/scipy/pull/17183>`__: DOC: examples for \`ive\` and \`kve\`
* `#17184 <https://github.com/scipy/scipy/pull/17184>`__: DOC: stats: Fix the 1.9.0 release note about the 'weights' parameter...
* `#17188 <https://github.com/scipy/scipy/pull/17188>`__: DOC: update version switcher for 1.9.2
* `#17198 <https://github.com/scipy/scipy/pull/17198>`__: MAINT: stats: remove use of interp2d from levy_stable._fitstart
* `#17199 <https://github.com/scipy/scipy/pull/17199>`__: DOC: Fix typos in IIR design argument documentation
* `#17215 <https://github.com/scipy/scipy/pull/17215>`__: MAINT: remove code for old numpy versions
* `#17217 <https://github.com/scipy/scipy/pull/17217>`__: MAINT: interpolate/RGI: make all _evaluate_YYY methods use self.values
* `#17223 <https://github.com/scipy/scipy/pull/17223>`__: DOC: linalg: Expand the qz example.
* `#17227 <https://github.com/scipy/scipy/pull/17227>`__: TST: stats.sampling.NumericalInverseHermite: filter all RuntimeWarnings
* `#17230 <https://github.com/scipy/scipy/pull/17230>`__: ENH: subclass-friendly refactor RegularGridInterpolator
* `#17233 <https://github.com/scipy/scipy/pull/17233>`__: DOC: examples for Struve functions
* `#17236 <https://github.com/scipy/scipy/pull/17236>`__: stats/distributions: make rv_sample public, allow subclassing
* `#17237 <https://github.com/scipy/scipy/pull/17237>`__: ENH: add conditional_table to SciPy.stats.
* `#17238 <https://github.com/scipy/scipy/pull/17238>`__: DOC: linalg: Several docstring updates.
* `#17243 <https://github.com/scipy/scipy/pull/17243>`__: DOC: special: Updates for smirnov and smirnovi
* `#17247 <https://github.com/scipy/scipy/pull/17247>`__: MAINT: optimize.leastsq: fix covariance not SPD
* `#17256 <https://github.com/scipy/scipy/pull/17256>`__: doc/RegularizedIncompleteBetaFunction
* `#17258 <https://github.com/scipy/scipy/pull/17258>`__: MAINT: stats.multivariate_normal: frozen rvs should pass cov_object...
* `#17259 <https://github.com/scipy/scipy/pull/17259>`__: DOC: CI: Add note about skipping Cirrus CI.
* `#17262 <https://github.com/scipy/scipy/pull/17262>`__: MAINT: forward port 1.9.3 relnotes
* `#17264 <https://github.com/scipy/scipy/pull/17264>`__: DOC: update version switcher for 1.9.3
* `#17273 <https://github.com/scipy/scipy/pull/17273>`__: TST: linalg: temporarily silence failure in test_solve_discrete_are
* `#17276 <https://github.com/scipy/scipy/pull/17276>`__: MAINT/ENH: stats.multivariate_normal.rvs: fix shape and speed...
* `#17277 <https://github.com/scipy/scipy/pull/17277>`__: ENH: Random unit vector distribution
* `#17279 <https://github.com/scipy/scipy/pull/17279>`__: TST: mark no_segmentation fault test for DIRECT as xslow
* `#17280 <https://github.com/scipy/scipy/pull/17280>`__: DOC: example for voigt_profile
* `#17283 <https://github.com/scipy/scipy/pull/17283>`__: STY: stats.Covariance: fix lint issue in \`main\`
* `#17284 <https://github.com/scipy/scipy/pull/17284>`__: MAINT: special: Loosen tolerance in test_sinpi() and test_cospi().
* `#17291 <https://github.com/scipy/scipy/pull/17291>`__: Cythonize 2D linear code path in RegularGridInterpolator
* `#17296 <https://github.com/scipy/scipy/pull/17296>`__: Fix test fails caused by pytest 7.1.3
* `#17298 <https://github.com/scipy/scipy/pull/17298>`__: DOC: Add examples to Stats Anderson
* `#17299 <https://github.com/scipy/scipy/pull/17299>`__: DOC: interpolate: Extrapolation tips and tricks
* `#17301 <https://github.com/scipy/scipy/pull/17301>`__: DOC, MAINT: remove use of inspect.formatargspec during doc build
* `#17302 <https://github.com/scipy/scipy/pull/17302>`__: MAINT: special: Use boost for special.hyp1f1 with real inputs.
* `#17303 <https://github.com/scipy/scipy/pull/17303>`__: Remove handwritten \`_fitpack.spalde\` : a rebase of pr/17145
* `#17304 <https://github.com/scipy/scipy/pull/17304>`__: ENH: stats: implement _sf and _isf for invweibull.
* `#17305 <https://github.com/scipy/scipy/pull/17305>`__: BUG: interpolate: allow zero-sized data arrays
* `#17313 <https://github.com/scipy/scipy/pull/17313>`__: DOC: interpolate: add a note on data with different scales
* `#17314 <https://github.com/scipy/scipy/pull/17314>`__: DOC: interpolate/tutorial: add a length-1 example
* `#17315 <https://github.com/scipy/scipy/pull/17315>`__: MAINT: special: Remove tests of numpy functions arccosh, arcsinh...
* `#17317 <https://github.com/scipy/scipy/pull/17317>`__: DOC: interpolate/tutorial: add an example for equally-spaced...
* `#17319 <https://github.com/scipy/scipy/pull/17319>`__: DOC: references and examples for huber/pseudo_huber
* `#17331 <https://github.com/scipy/scipy/pull/17331>`__: CI: On Azure, pin pytest-xdist to version 2.5.0
* `#17340 <https://github.com/scipy/scipy/pull/17340>`__: DOC: clarify use of bounds with basinhopping
* `#17345 <https://github.com/scipy/scipy/pull/17345>`__: ENH: commit to close #1261 (trac #734) by adding xtol argument.
* `#17346 <https://github.com/scipy/scipy/pull/17346>`__: BLD: fix \`SCIPY_USE_PYTHRAN=0\` usage for the Meson build
* `#17349 <https://github.com/scipy/scipy/pull/17349>`__: DOC: Fix signal docstrings; finish adding 'import numpy as np'
* `#17351 <https://github.com/scipy/scipy/pull/17351>`__: CI: Pin ninja==1.10.2.4 to avoid bug in 1.11.1 that breaks meson.
* `#17355 <https://github.com/scipy/scipy/pull/17355>`__: DOC: spatial: Fix some docstrings.
* `#17359 <https://github.com/scipy/scipy/pull/17359>`__: CI: ninja packages are repaired, so unpin.
* `#17361 <https://github.com/scipy/scipy/pull/17361>`__: DOC: examples for gdtr and gdtrc
* `#17363 <https://github.com/scipy/scipy/pull/17363>`__: DOC: adjust the deprecation notice for interp2d
* `#17366 <https://github.com/scipy/scipy/pull/17366>`__: DOC/MAINT: clean doctests namespace
* `#17367 <https://github.com/scipy/scipy/pull/17367>`__: DOC: Add missing \`build\` parameter to \`dev.py\`
* `#17369 <https://github.com/scipy/scipy/pull/17369>`__: DOC: consistent use of \`=\` for argument documentation
* `#17371 <https://github.com/scipy/scipy/pull/17371>`__: DOC: update RBF tutorial with new \`RBFInterpolator\`
* `#17372 <https://github.com/scipy/scipy/pull/17372>`__: BLD: update to Meson 0.64.0, remove \`pure: false\` lines
* `#17374 <https://github.com/scipy/scipy/pull/17374>`__: DOC: \`special.itairy\` example
* `#17376 <https://github.com/scipy/scipy/pull/17376>`__: DOC: Add examples to stats.mstats.find_repeats
* `#17395 <https://github.com/scipy/scipy/pull/17395>`__: DOC: optimize: minimize doc to reflect tnc's deprecation of maxiter
* `#17397 <https://github.com/scipy/scipy/pull/17397>`__: BUG: signal: Change types in the upfirdn utility function _output_len()
* `#17399 <https://github.com/scipy/scipy/pull/17399>`__: DOC: signal.iirdesign: remove \`bessel\` from supported filter...
* `#17400 <https://github.com/scipy/scipy/pull/17400>`__: TST: use norm in signal.TestBessel.test_fs_param
* `#17409 <https://github.com/scipy/scipy/pull/17409>`__: DOC: Examples for special functions related to F distribution
* `#17415 <https://github.com/scipy/scipy/pull/17415>`__: MAINT: Python 3.8 typing simplify
* `#17416 <https://github.com/scipy/scipy/pull/17416>`__: BLD: fix a lot of configuration warnings by using \`fs.copyfile\`
* `#17417 <https://github.com/scipy/scipy/pull/17417>`__: BUG: integrate: simpson didn't handle integer n-d arrays.
* `#17418 <https://github.com/scipy/scipy/pull/17418>`__: DOC: special: Remove duplicate imports from special examples.
* `#17423 <https://github.com/scipy/scipy/pull/17423>`__: Documentation to fix #17089
* `#17426 <https://github.com/scipy/scipy/pull/17426>`__: BLD: fix for propack and boost submodules - don't ask for native...
* `#17427 <https://github.com/scipy/scipy/pull/17427>`__: DOC: optimize.linprog: adjust HiGHS URL
* `#17430 <https://github.com/scipy/scipy/pull/17430>`__: BLD: define NDEBUG to mimic cmake release build
* `#17433 <https://github.com/scipy/scipy/pull/17433>`__: MAINT/TST: improved test coverage for DIRECT optimizer
* `#17439 <https://github.com/scipy/scipy/pull/17439>`__: DOC: Improve example for uniform_direction distribution
* `#17446 <https://github.com/scipy/scipy/pull/17446>`__: MAINT: stats.gaussian_kde: error early if n_features > n_data
* `#17447 <https://github.com/scipy/scipy/pull/17447>`__: MAINT: optimize.fminbound/minimize_scalar: add references, distinguish...
* `#17448 <https://github.com/scipy/scipy/pull/17448>`__: MAINT: optimize.minimize_scalar: always acknowledge 'bounds'...
* `#17449 <https://github.com/scipy/scipy/pull/17449>`__: MAINT: remove remaining occurrences of unicode
* `#17457 <https://github.com/scipy/scipy/pull/17457>`__: DOC: Double Integral Example Typo
* `#17466 <https://github.com/scipy/scipy/pull/17466>`__: BUG: stats: Fix for gh-17444.
* `#17467 <https://github.com/scipy/scipy/pull/17467>`__: BUG: ndimage: Don't use np.int0 (it is the same as np.intp)
* `#17469 <https://github.com/scipy/scipy/pull/17469>`__: BUG: stats: Random parameters in \`pytest.mark.parametrize()\`...
* `#17471 <https://github.com/scipy/scipy/pull/17471>`__: MAINT: stats.rv_count: revert gh-17236
* `#17472 <https://github.com/scipy/scipy/pull/17472>`__: Getting rid of _make_points_and_values_ascending and its unnecessary...
* `#17478 <https://github.com/scipy/scipy/pull/17478>`__: ENH: Add clear_cache utility for \`scipy.datasets\`
* `#17481 <https://github.com/scipy/scipy/pull/17481>`__: MAINT: special: remove more \`npy_math.h\` usage
* `#17482 <https://github.com/scipy/scipy/pull/17482>`__: MAINT: stats: Unconditionally disable boost double promotion.
* `#17484 <https://github.com/scipy/scipy/pull/17484>`__: DOC: remove hard-coded value from PoissonDisk example
* `#17485 <https://github.com/scipy/scipy/pull/17485>`__: ENH: increase range of vonmises entropy
* `#17487 <https://github.com/scipy/scipy/pull/17487>`__: CI: pin setuptools for musllinux
* `#17489 <https://github.com/scipy/scipy/pull/17489>`__: BUG: ndimage: Work around gh-17270
* `#17496 <https://github.com/scipy/scipy/pull/17496>`__: DEV: dev.py: make lint task consistent with CI
* `#17500 <https://github.com/scipy/scipy/pull/17500>`__: MAINT: special: Remove references to nonexistent function exp1m.
* `#17501 <https://github.com/scipy/scipy/pull/17501>`__: Minor: Misspelling typos fixed in _svds.py
* `#17504 <https://github.com/scipy/scipy/pull/17504>`__: CI: PRs run against merged main [skip circle][skip gh][skip azp]
* `#17512 <https://github.com/scipy/scipy/pull/17512>`__: TST: interpolate: stop skipping a test with zero-sized arrays
* `#17513 <https://github.com/scipy/scipy/pull/17513>`__: BUG: optimize: fixed issue 17380
* `#17526 <https://github.com/scipy/scipy/pull/17526>`__: BUG, DOC: stats: fix \`[source]\` button redicting to the wrong...
* `#17534 <https://github.com/scipy/scipy/pull/17534>`__: DOC: 1.10.0 release notes
* `#17536 <https://github.com/scipy/scipy/pull/17536>`__: DOC: Examples for \`yve\` and \`jve\`
* `#17540 <https://github.com/scipy/scipy/pull/17540>`__: DOC: fix documentation of \`make_smoothing_spline\`
* `#17543 <https://github.com/scipy/scipy/pull/17543>`__: CI: fix gh17539 failures of the alpine linux run
* `#17545 <https://github.com/scipy/scipy/pull/17545>`__: BUG: special: Fix handling of subnormal input for lambertw.
* `#17551 <https://github.com/scipy/scipy/pull/17551>`__: BUG Fix: Update lobpcg.py to turn history arrays into lists for...
* `#17569 <https://github.com/scipy/scipy/pull/17569>`__: MAINT: version bounds for 1.10.0rc1/relnotes fixes
* `#17579 <https://github.com/scipy/scipy/pull/17579>`__: Revert "ENH: stats.ks_2samp: Pythranize remaining exact p-value...
* `#17580 <https://github.com/scipy/scipy/pull/17580>`__: CI: native cp38-macosx_arm64 [wheel build][skip azp][skip circle][ski…
* `#17583 <https://github.com/scipy/scipy/pull/17583>`__: MAINT: 1.10.0rc1 backports round 2
* `#17591 <https://github.com/scipy/scipy/pull/17591>`__: MAINT: stats.pearsonr: raise error for complex input
* `#17600 <https://github.com/scipy/scipy/pull/17600>`__: DOC: update version switcher for 1.10
* `#17611 <https://github.com/scipy/scipy/pull/17611>`__: MAINT: Update ascent.dat file hash
* `#17614 <https://github.com/scipy/scipy/pull/17614>`__: MAINT: optimize.milp: don't warn about \`mip_rel_gap\` option
* `#17627 <https://github.com/scipy/scipy/pull/17627>`__: MAINT: Cast \`datasets.ascent\` image to float64
* `#17634 <https://github.com/scipy/scipy/pull/17634>`__: MAINT: casting errstate for NumPy 1.24
* `#17638 <https://github.com/scipy/scipy/pull/17638>`__: MAINT, TST: alpine/musl segfault shim
* `#17640 <https://github.com/scipy/scipy/pull/17640>`__: MAINT: prepare for SciPy 1.10.0rc2
* `#17645 <https://github.com/scipy/scipy/pull/17645>`__: MAINT: stats.rankdata: ensure consistent shape handling
* `#17653 <https://github.com/scipy/scipy/pull/17653>`__: MAINT: pybind11 win exclusion
* `#17656 <https://github.com/scipy/scipy/pull/17656>`__: MAINT: 1.10.0rc2 backports, round two
* `#17662 <https://github.com/scipy/scipy/pull/17662>`__: Fix undefined behavior within scipy.fft
* `#17686 <https://github.com/scipy/scipy/pull/17686>`__: REV: integrate.qmc_quad: delay release to SciPy 1.11.0
* `#17689 <https://github.com/scipy/scipy/pull/17689>`__: REL: integrate.qmc_quad: remove from release notes

# ===== SOURCE: https://raw.githubusercontent.com/scipy/scipy/main/doc/source/release/1.11.0-notes.rst =====

==========================
SciPy 1.11.0 Release Notes
==========================

.. contents::

SciPy 1.11.0 is the culmination of 6 months of hard work. It contains
many new features, numerous bug-fixes, improved test coverage and better
documentation. There have been a number of deprecations and API changes
in this release, which are documented below. All users are encouraged to
upgrade to this release, as there are a large number of bug-fixes and
optimizations. Before upgrading, we recommend that users check that
their own code does not use deprecated SciPy functionality (to do so,
run your code with ``python -Wd`` and check for ``DeprecationWarning`` s).
Our development attention will now shift to bug-fix releases on the
1.11.x branch, and on adding new features on the main branch.

This release requires Python 3.9+ and NumPy 1.21.6 or greater.

For running on PyPy, PyPy3 6.0+ is required.


**************************
Highlights of this release
**************************

- Several `scipy.sparse` array API improvements, including `sparse.sparray`, a new
  public base class distinct from the older `sparse.spmatrix` class,
  proper 64-bit index support, and numerous deprecations paving the way to a
  modern sparse array experience.
- `scipy.stats` added tools for survival analysis, multiple hypothesis testing,
  sensitivity analysis, and working with censored data.
- A new function was added for quasi-Monte Carlo integration, and linear
  algebra functions ``det`` and ``lu`` now accept nD-arrays.
- An ``axes`` argument was added broadly to ``ndimage`` functions, facilitating
  analysis of stacked image data.


************
New features
************

`scipy.integrate` improvements
==============================
- Added `scipy.integrate.qmc_quad` for quasi-Monte Carlo integration.
- For an even number of points, `scipy.integrate.simpson` now calculates
  a parabolic segment over the last three points which gives improved
  accuracy over the previous implementation.

`scipy.cluster` improvements
============================
- ``disjoint_set`` has a new method ``subset_size`` for providing the size
  of a particular subset.


`scipy.constants` improvements
================================
- The ``quetta``, ``ronna``, ``ronto``, and ``quecto`` SI prefixes were added.


`scipy.linalg` improvements
===========================
- `scipy.linalg.det` is improved and now accepts nD-arrays.
- `scipy.linalg.lu` is improved and now accepts nD-arrays. With the new
  ``p_indices`` switch the output permutation argument can be 1D ``(n,)``
  permutation index instead of the full ``(n, n)`` array.


`scipy.ndimage` improvements
============================
- ``axes`` argument was added to ``rank_filter``, ``percentile_filter``,
  ``median_filter``, ``uniform_filter``, ``minimum_filter``,
  ``maximum_filter``, and ``gaussian_filter``, which can be useful for
  processing stacks of image data.


`scipy.optimize` improvements
=============================
- `scipy.optimize.linprog` now passes unrecognized options directly to HiGHS.
- `scipy.optimize.root_scalar` now uses Newton's method to be used without
  providing ``fprime`` and the ``secant`` method to be used without a second
  guess.
- `scipy.optimize.lsq_linear` now accepts ``bounds`` arguments of type
  `scipy.optimize.Bounds`.
- `scipy.optimize.minimize` ``method='cobyla'`` now supports simple bound
  constraints.
- Users can opt into a new callback interface for most methods of
  `scipy.optimize.minimize`: If the provided callback callable accepts
  a single keyword argument, ``intermediate_result``, `scipy.optimize.minimize`
  now passes both the current solution and the optimal value of the objective
  function to the callback as an instance of `scipy.optimize.OptimizeResult`.
  It also allows the user to terminate optimization by raising a
  ``StopIteration`` exception from the callback function.
  `scipy.optimize.minimize` will return normally, and the latest solution
  information is provided in the result object.
- `scipy.optimize.curve_fit` now supports an optional ``nan_policy`` argument.
- `scipy.optimize.shgo` now has parallelization with the ``workers`` argument,
  symmetry arguments that can improve performance, class-based design to
  improve usability, and generally improved performance.


`scipy.signal` improvements
===========================
- ``istft`` has an improved warning message when the NOLA condition fails.

`scipy.sparse` improvements
===========================
- A new public base class `scipy.sparse.sparray` was introduced, allowing further
  extension of the sparse array API (such as the support for 1-dimensional
  sparse arrays) without breaking backwards compatibility.
  ``isinstance(x, scipy.sparse.sparray)`` to select the new sparse array classes,
  while ``isinstance(x, scipy.sparse.spmatrix)`` selects only the old sparse
  matrix classes.
- Division of sparse arrays by a dense array now returns sparse arrays.
- `scipy.sparse.isspmatrix` now only returns `True` for the sparse matrices instances.
  `scipy.sparse.issparse` now has to be used instead to check for instances of sparse
  arrays or instances of sparse matrices.
- Sparse arrays constructed with int64 indices will no longer automatically
  downcast to int32.
- The ``argmin`` and ``argmax`` methods now return the correct result when explicit
  zeros are present.

`scipy.sparse.linalg` improvements
==================================
- dividing ``LinearOperator`` by a number now returns a
  ``_ScaledLinearOperator``
- ``LinearOperator`` now supports right multiplication by arrays
- ``lobpcg`` should be more efficient following removal of an extraneous
  QR decomposition.


`scipy.spatial` improvements
============================
- Usage of new C++ backend for additional distance metrics, the majority of
  which will see substantial performance improvements, though a few minor
  regressions are known. These are focused on distances between boolean
  arrays.


`scipy.special` improvements
============================
- The factorial functions ``factorial``, ``factorial2`` and ``factorialk``
  were made consistent in their behavior (in terms of dimensionality,
  errors etc.). Additionally, ``factorial2`` can now handle arrays with
  ``exact=True``, and ``factorialk`` can handle arrays.


`scipy.stats` improvements
==========================

New Features
------------
- `scipy.stats.sobol_indices`, a method to compute Sobol' sensitivity indices.
- `scipy.stats.dunnett`, which performs Dunnett's test of the means of multiple
  experimental groups against the mean of a control group.
- `scipy.stats.ecdf` for computing the empirical CDF and complementary
  CDF (survival function / SF) from uncensored or right-censored data. This
  function is also useful for survival analysis / Kaplan-Meier estimation.
- `scipy.stats.logrank` to compare survival functions underlying samples.
- `scipy.stats.false_discovery_control` for adjusting p-values to control the
  false discovery rate of multiple hypothesis tests using the
  Benjamini-Hochberg or Benjamini-Yekutieli procedures.
- `scipy.stats.CensoredData` to represent censored data. It can be used as
  input to the ``fit`` method of univariate distributions and to the new
  ``ecdf`` function.
- Filliben's goodness of fit test as ``method='Filliben'`` of
  `scipy.stats.goodness_of_fit`.
- `scipy.stats.ttest_ind` has a new method, ``confidence_interval`` for
  computing a confidence interval of the difference between means.
- `scipy.stats.MonteCarloMethod`, `scipy.stats.PermutationMethod`, and
  `scipy.stats.BootstrapMethod` are new classes to configure resampling and/or
  Monte Carlo versions of hypothesis tests. They can currently be used with
  `scipy.stats.pearsonr`.

Statistical Distributions
-------------------------
- Added the von-Mises Fisher distribution as `scipy.stats.vonmises_fisher`.
  This distribution is the most common analogue of the normal distribution
  on the unit sphere.
- Added the relativistic Breit-Wigner distribution as
  `scipy.stats.rel_breitwigner`.
  It is used in high energy physics to model resonances.
- Added the Dirichlet multinomial distribution as
  `scipy.stats.dirichlet_multinomial`.
- Improved the speed and precision of several univariate statistical
  distributions.

  - `scipy.stats.anglit` ``sf``
  - `scipy.stats.beta` ``entropy``
  - `scipy.stats.betaprime` ``cdf``, ``sf``, ``ppf``
  - `scipy.stats.chi` ``entropy``
  - `scipy.stats.chi2` ``entropy``
  - `scipy.stats.dgamma` ``entropy``, ``cdf``, ``sf``, ``ppf``, and ``isf``
  - `scipy.stats.dweibull` ``entropy``, ``sf``, and ``isf``
  - `scipy.stats.exponweib` ``sf`` and ``isf``
  - `scipy.stats.f` ``entropy``
  - `scipy.stats.foldcauchy` ``sf``
  - `scipy.stats.foldnorm` ``cdf`` and ``sf``
  - `scipy.stats.gamma` ``entropy``
  - `scipy.stats.genexpon` ``ppf``, ``isf``, ``rvs``
  - `scipy.stats.gengamma` ``entropy``
  - `scipy.stats.geom` ``entropy``
  - `scipy.stats.genlogistic` ``entropy``, ``logcdf``, ``sf``, ``ppf``,
    and ``isf``
  - `scipy.stats.genhyperbolic` ``cdf`` and ``sf``
  - `scipy.stats.gibrat` ``sf`` and ``isf``
  - `scipy.stats.gompertz` ``entropy``, ``sf``. and ``isf``
  - `scipy.stats.halflogistic` ``sf``, and ``isf``
  - `scipy.stats.halfcauchy` ``sf`` and ``isf``
  - `scipy.stats.halfnorm` ``cdf``, ``sf``, and ``isf``
  - `scipy.stats.invgamma` ``entropy``
  - `scipy.stats.invgauss` ``entropy``
  - `scipy.stats.johnsonsb` ``pdf``, ``cdf``, ``sf``, ``ppf``, and ``isf``
  - `scipy.stats.johnsonsu` ``pdf``, ``sf``, ``isf``, and ``stats``
  - `scipy.stats.lognorm` ``fit``
  - `scipy.stats.loguniform` ``entropy``, ``logpdf``, ``pdf``, ``cdf``, ``ppf``,
    and ``stats``
  - `scipy.stats.maxwell` ``sf`` and ``isf``
  - `scipy.stats.nakagami` ``entropy``
  - `scipy.stats.powerlaw` ``sf``
  - `scipy.stats.powerlognorm` ``logpdf``, ``logsf``, ``sf``, and ``isf``
  - `scipy.stats.powernorm` ``sf`` and ``isf``
  - `scipy.stats.t` ``entropy``, ``logpdf``, and ``pdf``
  - `scipy.stats.truncexpon` ``sf``, and ``isf``
  - `scipy.stats.truncnorm` ``entropy``
  - `scipy.stats.truncpareto` ``fit``
  - `scipy.stats.vonmises` ``fit``

- `scipy.stats.multivariate_t` now has ``cdf`` and ``entropy`` methods.
- `scipy.stats.multivariate_normal`, `scipy.stats.matrix_normal`, and
  `scipy.stats.invwishart` now have an ``entropy`` method.

Other Improvements
------------------
- `scipy.stats.monte_carlo_test` now supports multi-sample statistics.
- `scipy.stats.bootstrap` can now produce one-sided confidence intervals.
- `scipy.stats.rankdata` performance was improved for ``method=ordinal`` and
  ``method=dense``.
- `scipy.stats.moment` now supports non-central moment calculation.
- `scipy.stats.anderson` now supports the ``weibull_min`` distribution.
- `scipy.stats.sem` and `scipy.stats.iqr` now support ``axis``, ``nan_policy``,
  and masked array input.

*******************
Deprecated features
*******************

- Multi-Ellipsis sparse matrix indexing has been deprecated and will
  be removed in SciPy 1.13.
- Several methods were deprecated for sparse arrays: ``asfptype``, ``getrow``,
  ``getcol``, ``get_shape``, ``getmaxprint``, ``set_shape``,
  ``getnnz``, and ``getformat``. Additionally, the ``.A`` and ``.H``
  attributes were deprecated. Sparse matrix types are not affected.
- The `scipy.linalg` functions ``tri``, ``triu`` & ``tril`` are deprecated and
  will be removed in SciPy 1.13. Users are recommended to use the NumPy
  versions of these functions with identical names.
- The `scipy.signal` functions ``bspline``, ``quadratic`` & ``cubic`` are
  deprecated and will be removed in SciPy 1.13. Users are recommended to use
  `scipy.interpolate.BSpline` instead.
- The ``even`` keyword of `scipy.integrate.simpson` is deprecated and will be
  removed in SciPy 1.13.0. Users should leave this as the default as this
  gives improved accuracy compared to the other methods.
- Using ``exact=True`` when passing integers in a float array to ``factorial``
  is deprecated and will be removed in SciPy 1.13.0.
- float128 and object dtypes are deprecated for `scipy.signal.medfilt` and
  `scipy.signal.order_filter`
- The functions ``scipy.signal.{lsim2, impulse2, step2}`` had long been
  deprecated in documentation only. They now raise a DeprecationWarning and
  will be removed in SciPy 1.13.0.
- Importing window functions directly from `scipy.window` has been soft
  deprecated since SciPy 1.1.0. They now raise a ``DeprecationWarning`` and
  will be removed in SciPy 1.13.0. Users should instead import them from
  `scipy.signal.window` or use the convenience function
  `scipy.signal.get_window`.

******************************
Backwards incompatible changes
******************************
- The default for the ``legacy`` keyword of `scipy.special.comb` has changed
  from ``True`` to ``False``, as announced since its introduction.

********************
Expired Deprecations
********************
There is an ongoing effort to follow through on long-standing deprecations.
The following previously deprecated features are affected:

- The ``n`` keyword has been removed from `scipy.stats.moment`.
- The ``alpha`` keyword has been removed from `scipy.stats.interval`.
- The misspelt ``gilbrat`` distribution has been removed (use
  `scipy.stats.gibrat`).
- The deprecated spelling of the ``kulsinski`` distance metric has been
  removed (use `scipy.spatial.distance.kulczynski1`).
- The ``vertices`` keyword of `scipy.spatial.Delauney.qhull` has been removed
  (use simplices).
- The ``residual`` property of `scipy.sparse.csgraph.maximum_flow` has been
  removed (use ``flow``).
- The ``extradoc`` keyword of `scipy.stats.rv_continuous`,
  `scipy.stats.rv_discrete` and `scipy.stats.rv_sample` has been removed.
- The ``sym_pos`` keyword of `scipy.linalg.solve` has been removed.
- The `scipy.optimize.minimize` function now raises an error for ``x0`` with
  ``x0.ndim > 1``.
- In `scipy.stats.mode`, the default value of ``keepdims`` is now ``False``,
  and support for non-numeric input has been removed.
- The function `scipy.signal.lsim` does not support non-uniform time steps
  anymore.


*************
Other changes
*************
- Rewrote the source build docs and restructured the contributor guide.
- Improved support for cross-compiling with meson build system.
- MyST-NB notebook infrastructure has been added to our documentation.



*******
Authors
*******

* h-vetinari (69)
* Oriol Abril-Pla (1) +
* Tom Adamczewski (1) +
* Anton Akhmerov (13)
* Andrey Akinshin (1) +
* alice (1) +
* Oren Amsalem (1)
* Ross Barnowski (13)
* Christoph Baumgarten (2)
* Dawson Beatty (1) +
* Doron Behar (1) +
* Peter Bell (1)
* John Belmonte (1) +
* boeleman (1) +
* Jack Borchanian (1) +
* Matt Borland (3) +
* Jake Bowhay (41)
* Larry Bradley (1) +
* Sienna Brent (1) +
* Matthew Brett (1)
* Evgeni Burovski (39)
* Matthias Bussonnier (2)
* Maria Cann (1) +
* Alfredo Carella (1) +
* CJ Carey (34)
* Hood Chatham (2)
* Anirudh Dagar (3)
* Alberto Defendi (1) +
* Pol del Aguila (1) +
* Hans Dembinski (1)
* Dennis (1) +
* Vinayak Dev (1) +
* Thomas Duvernay (1)
* DWesl (4)
* Stefan Endres (66)
* Evandro (1) +
* Tom Eversdijk (2) +
* Isuru Fernando (1)
* Franz Forstmayr (4)
* Joseph Fox-Rabinovitz (1)
* Stefano Frazzetto (1) +
* Neil Girdhar (1)
* Caden Gobat (1) +
* Ralf Gommers (153)
* GonVas (1) +
* Marco Gorelli (1)
* Brett Graham (2) +
* Matt Haberland (388)
* harshvardhan2707 (1) +
* Alex Herbert (1) +
* Guillaume Horel (1)
* Geert-Jan Huizing (1) +
* Jakob Jakobson (2)
* Julien Jerphanion (10)
* jyuv (2)
* Rajarshi Karmakar (1) +
* Ganesh Kathiresan (3) +
* Robert Kern (4)
* Andrew Knyazev (4)
* Sergey Koposov (1)
* Rishi Kulkarni (2) +
* Eric Larson (1)
* Zoufiné Lauer-Bare (2) +
* Antony Lee (3)
* Gregory R. Lee (8)
* Guillaume Lemaitre (2) +
* lilinjie (2) +
* Yannis Linardos (1) +
* Christian Lorentzen (5)
* Loïc Estève (1)
* Adam Lugowski (1) +
* Charlie Marsh (2) +
* Boris Martin (1) +
* Nicholas McKibben (11)
* Melissa Weber Mendonça (58)
* Michał Górny (1) +
* Jarrod Millman (5)
* Stefanie Molin (2) +
* Mark W. Mueller (1) +
* mustafacevik (1) +
* Takumasa N (1) +
* nboudrie (1)
* Andrew Nelson (112)
* Nico Schlömer (4)
* Lysandros Nikolaou (2) +
* Kyle Oman (1)
* OmarManzoor (2) +
* Simon Ott (1) +
* Geoffrey Oxberry (1) +
* Geoffrey M. Oxberry (2) +
* Sravya papaganti (1) +
* Tirth Patel (2)
* Ilhan Polat (32)
* Quentin Barthélemy (1)
* Matteo Raso (12) +
* Tyler Reddy (143)
* Lucas Roberts (1)
* Pamphile Roy (225)
* Jordan Rupprecht (1) +
* Atsushi Sakai (11)
* Omar Salman (7) +
* Leo Sandler (1) +
* Ujjwal Sarswat (3) +
* Saumya (1) +
* Daniel Schmitz (79)
* Henry Schreiner (2) +
* Dan Schult (8) +
* Eli Schwartz (6)
* Tomer Sery (2) +
* Scott Shambaugh (10) +
* Gagandeep Singh (1)
* Ethan Steinberg (6) +
* stepeos (2) +
* Albert Steppi (3)
* Strahinja Lukić (1)
* Kai Striega (4)
* suen-bit (1) +
* Tartopohm (2)
* Logan Thomas (2) +
* Jacopo Tissino (1) +
* Matus Valo (12) +
* Jacob Vanderplas (2)
* Christian Veenhuis (1) +
* Isaac Virshup (3)
* Stefan van der Walt (14)
* Warren Weckesser (63)
* windows-server-2003 (1)
* Levi John Wolf (3)
* Nobel Wong (1) +
* Benjamin Yeh (1) +
* Rory Yorke (1)
* Younes (2) +
* Zaikun ZHANG (1) +
* Alex Zverianskii (1) +

A total of 134 people contributed to this release.
People with a "+" by their names contributed a patch for the first time.
This list of names is automatically generated, and may not be fully complete.


************************
Issues closed for 1.11.0
************************

* `#1766 <https://github.com/scipy/scipy/issues/1766>`__: __fitpack.h work array computations pretty much one big bug....
* `#1953 <https://github.com/scipy/scipy/issues/1953>`__: use custom warnings instead of print statements (Trac #1428)
* `#3089 <https://github.com/scipy/scipy/issues/3089>`__: brentq, nan returns, and bounds
* `#4257 <https://github.com/scipy/scipy/issues/4257>`__: scipy.optimize.line_search returns None
* `#4532 <https://github.com/scipy/scipy/issues/4532>`__: box constraint in scipy optimize cobyla
* `#5584 <https://github.com/scipy/scipy/issues/5584>`__: Suspected underflow issue with sign check in bisection method
* `#5618 <https://github.com/scipy/scipy/issues/5618>`__: Solution for low accuracy of simps with even number of points
* `#5899 <https://github.com/scipy/scipy/issues/5899>`__: minimize_scalar -- strange behaviour
* `#6414 <https://github.com/scipy/scipy/issues/6414>`__: scipy.stats Breit-Wigner distribution
* `#6842 <https://github.com/scipy/scipy/issues/6842>`__: Covariance matrix returned by ODR needs to be scaled by the residual...
* `#7306 <https://github.com/scipy/scipy/issues/7306>`__: any way of stopping optimization?
* `#7799 <https://github.com/scipy/scipy/issues/7799>`__: basinhopping result violates constraints
* `#8176 <https://github.com/scipy/scipy/issues/8176>`__: optimize.minimize should provide a way to return the cost function...
* `#8394 <https://github.com/scipy/scipy/issues/8394>`__: brentq returns solutions outside of the bounds
* `#8485 <https://github.com/scipy/scipy/issues/8485>`__: freqz() output for fifth order butterworth bandpass (low cut...
* `#8922 <https://github.com/scipy/scipy/issues/8922>`__: Bug in Solve_ivp with BDF and Radau solvers and numpy arrays
* `#9061 <https://github.com/scipy/scipy/issues/9061>`__: Will a vectorized fun offer advantages for scipy.integrate.LSODA?
* `#9265 <https://github.com/scipy/scipy/issues/9265>`__: DOC: optimize.minimize: recipe for avoiding redundant work when...
* `#9412 <https://github.com/scipy/scipy/issues/9412>`__: Callback return value erroneously ignored in minimize
* `#9728 <https://github.com/scipy/scipy/issues/9728>`__: DOC: scipy.integrate.solve_ivp
* `#9955 <https://github.com/scipy/scipy/issues/9955>`__: stats.mode nan_policy='omit' unexpected behavior when data are...
* `#10050 <https://github.com/scipy/scipy/issues/10050>`__: [Bug] inconsistent canonical format for coo_matrix
* `#10370 <https://github.com/scipy/scipy/issues/10370>`__: SciPy errors out expecting square matrix using for root-finding...
* `#10437 <https://github.com/scipy/scipy/issues/10437>`__: scipy.optimize.dual_annealing always rejects non-improving state
* `#10554 <https://github.com/scipy/scipy/issues/10554>`__: ndimage.gaussian_filter provide axis option
* `#10829 <https://github.com/scipy/scipy/issues/10829>`__: Extend Anderson Darling to cover Weibull distribution
* `#10853 <https://github.com/scipy/scipy/issues/10853>`__: ImportError: cannot import name spatial
* `#11052 <https://github.com/scipy/scipy/issues/11052>`__: optimize.dual_annealing does not pass arguments to jacobian.
* `#11564 <https://github.com/scipy/scipy/issues/11564>`__: LinearOperator objects cannot be applied to sparse matrices
* `#11723 <https://github.com/scipy/scipy/issues/11723>`__: Monte Carlo methods for scipy.integrate
* `#11775 <https://github.com/scipy/scipy/issues/11775>`__: Multi xatol for Nedler-Mead algorithm
* `#11841 <https://github.com/scipy/scipy/issues/11841>`__: Ignore NaN with scipy.optimize.curve_fit
* `#12114 <https://github.com/scipy/scipy/issues/12114>`__: scipy.optimize.shgo(): 'args' is incorrectly passed to constraint...
* `#12715 <https://github.com/scipy/scipy/issues/12715>`__: Why the covariance from curve_fit depends so sharply on the overall...
* `#13122 <https://github.com/scipy/scipy/issues/13122>`__: The test suite fails on Python 3.10: issue with factorial() on...
* `#13258 <https://github.com/scipy/scipy/issues/13258>`__: \*\*kwargs for optimize.root_scalar and alike
* `#13407 <https://github.com/scipy/scipy/issues/13407>`__: \`if rtol < _rtol / 4\` should be changed?
* `#13535 <https://github.com/scipy/scipy/issues/13535>`__: Newton-iteration should not be done after secant interpolation
* `#13547 <https://github.com/scipy/scipy/issues/13547>`__: optimize.shgo: handle objective functions that return the gradient...
* `#13554 <https://github.com/scipy/scipy/issues/13554>`__: The correct root for test APS13 is 0
* `#13757 <https://github.com/scipy/scipy/issues/13757>`__: API for representing censored data
* `#13974 <https://github.com/scipy/scipy/issues/13974>`__: BUG: optimize.shgo: not using options
* `#14059 <https://github.com/scipy/scipy/issues/14059>`__: Bound on absolute tolerance 'xtol' in 'optimize/zeros.py' is...
* `#14262 <https://github.com/scipy/scipy/issues/14262>`__: cython_blas does not use const in signatures
* `#14414 <https://github.com/scipy/scipy/issues/14414>`__: brentq does converge and not raise an error for np.nan functions
* `#14486 <https://github.com/scipy/scipy/issues/14486>`__: One bug, one mistake and one refactorization proposal for the...
* `#14519 <https://github.com/scipy/scipy/issues/14519>`__: scipy/stats/tests/test_continuous_basic.py::test_cont_basic[500-200-ncf-arg74] test fails with IntegrationWarning
* `#14525 <https://github.com/scipy/scipy/issues/14525>`__: scipy.signal.bspline does not work for integer types
* `#14858 <https://github.com/scipy/scipy/issues/14858>`__: BUG: scipy.optimize.bracket sometimes fails silently
* `#14901 <https://github.com/scipy/scipy/issues/14901>`__: BUG: stats: distribution methods emit unnecessary warnings from...
* `#15089 <https://github.com/scipy/scipy/issues/15089>`__: BUG: scipy.optimize.minimize() does not report lowest energy...
* `#15136 <https://github.com/scipy/scipy/issues/15136>`__: ENH: Bump boost.math version
* `#15177 <https://github.com/scipy/scipy/issues/15177>`__: BUG: element-wise division between sparse matrices and array-likes...
* `#15212 <https://github.com/scipy/scipy/issues/15212>`__: BUG: stange behavior of scipy.integrate.quad for divergent integrals
* `#15514 <https://github.com/scipy/scipy/issues/15514>`__: BUG: optimize.shgo: error with vector constraints
* `#15600 <https://github.com/scipy/scipy/issues/15600>`__: BUG: handle inconsistencies in factorial functions and their...
* `#15613 <https://github.com/scipy/scipy/issues/15613>`__: ENH: Provide functions to compute log-integrals numerically (e.g.,...
* `#15702 <https://github.com/scipy/scipy/issues/15702>`__: MAINT:linalg: Either silent import NumPy versions or deprecate...
* `#15706 <https://github.com/scipy/scipy/issues/15706>`__: DEP: remove deprecated parameters from stats distributions
* `#15755 <https://github.com/scipy/scipy/issues/15755>`__: DEP: absorb lsim2 into lsim
* `#15756 <https://github.com/scipy/scipy/issues/15756>`__: DEP: remove non-numeric array support in stats.mode
* `#15790 <https://github.com/scipy/scipy/issues/15790>`__: BUG: \`isspmatrix\` doesn't account for sparse arrays
* `#15808 <https://github.com/scipy/scipy/issues/15808>`__: DEP: raise on >1-dim inputs for optimize.minimize
* `#15814 <https://github.com/scipy/scipy/issues/15814>`__: CI: move Azure jobs to GitHub Actions
* `#15818 <https://github.com/scipy/scipy/issues/15818>`__: DEP: remove extradoc keyword in _distn_infrastructure
* `#15829 <https://github.com/scipy/scipy/issues/15829>`__: DEP: remove sym_pos-keyword of scipy.linalg.solve
* `#15852 <https://github.com/scipy/scipy/issues/15852>`__: DOC: helper function to seed examples
* `#15906 <https://github.com/scipy/scipy/issues/15906>`__: Missing degree of freedom parameter in return value from \`stats.ttest_ind\`
* `#15985 <https://github.com/scipy/scipy/issues/15985>`__: ENH, DOC: Add section explaining why and when to use a custom...
* `#15988 <https://github.com/scipy/scipy/issues/15988>`__: DEP: remove deprecated gilbrat distribution
* `#16014 <https://github.com/scipy/scipy/issues/16014>`__: DEP: remove MaximumFlowResult.residual
* `#16068 <https://github.com/scipy/scipy/issues/16068>`__: BUG: Missing Constant in Documentation
* `#16079 <https://github.com/scipy/scipy/issues/16079>`__: BUG: hypergeom.cdf slower in 1.8.0 than 1.7.3
* `#16196 <https://github.com/scipy/scipy/issues/16196>`__: BUG: OptimizeResult from optimize.minimize_scalar changes 'x'...
* `#16269 <https://github.com/scipy/scipy/issues/16269>`__: DEP: remove \`maxiter\` kwarg in \`_minimize_tnc\`
* `#16270 <https://github.com/scipy/scipy/issues/16270>`__: DEP: remove \`vertices\` kwarg in qhull
* `#16271 <https://github.com/scipy/scipy/issues/16271>`__: DEP: remove \`scipy.spatial.distance.kulsinski\`
* `#16312 <https://github.com/scipy/scipy/issues/16312>`__: Meson complains about an absolute include path
* `#16322 <https://github.com/scipy/scipy/issues/16322>`__: DOC: building on Windows uses GCC with Meson, not MSVC
* `#16595 <https://github.com/scipy/scipy/issues/16595>`__: BUG: stats.mode emits annoying RuntimeWarning about nans even...
* `#16734 <https://github.com/scipy/scipy/issues/16734>`__: BUG: function p1evl in povevl.h not making what's described
* `#16803 <https://github.com/scipy/scipy/issues/16803>`__: Update \`scipy/__config__.py\` to contain useful information
* `#16810 <https://github.com/scipy/scipy/issues/16810>`__: ENH: implement Dirichlet-multinomial distribution
* `#16917 <https://github.com/scipy/scipy/issues/16917>`__: BUG: Windows Built SciPy can't import _fblas via pip install...
* `#16929 <https://github.com/scipy/scipy/issues/16929>`__: BUG: \`scipy.sparse.csc_matrix.argmin\` returns wrong values
* `#16949 <https://github.com/scipy/scipy/issues/16949>`__: Test failures for \`gges\` and \`qz\` for float32 input in macOS...
* `#16971 <https://github.com/scipy/scipy/issues/16971>`__: BUG: [issue in scipy.optimize.shgo, for COBYLA's minimizer_kwargs...
* `#16998 <https://github.com/scipy/scipy/issues/16998>`__: Unpickled and deepcopied distributions do not use global random...
* `#17024 <https://github.com/scipy/scipy/issues/17024>`__: ENH: Force real part of Rotation.as_quat() to be positive.
* `#17107 <https://github.com/scipy/scipy/issues/17107>`__: BUG: The signature of cKDTree.query_pairs in the docs does not...
* `#17137 <https://github.com/scipy/scipy/issues/17137>`__: BUG: optimize: Intermittent failure of \`test_milp_timeout_16545\`
* `#17146 <https://github.com/scipy/scipy/issues/17146>`__: BUG: Scipy stats probability greater than 1
* `#17214 <https://github.com/scipy/scipy/issues/17214>`__: BUG: scipy.stats.mode: inconsistent shape with \`axis=None\`...
* `#17234 <https://github.com/scipy/scipy/issues/17234>`__: BUG: cythonization / compliation failure with development branch...
* `#17250 <https://github.com/scipy/scipy/issues/17250>`__: ENH: Expose parallel HiGHS solvers in high-level API
* `#17281 <https://github.com/scipy/scipy/issues/17281>`__: BUG: using LinearOperator as RHS operand of @ causes a NumPy...
* `#17285 <https://github.com/scipy/scipy/issues/17285>`__: ENH: Expose DisjointSet._sizes
* `#17312 <https://github.com/scipy/scipy/issues/17312>`__: ENH: Clarify that ndimage.find_objects returns slices ordered...
* `#17335 <https://github.com/scipy/scipy/issues/17335>`__: ENH: change term zero to root in newton
* `#17368 <https://github.com/scipy/scipy/issues/17368>`__: BUG: import scipy.stats fails under valgrind
* `#17378 <https://github.com/scipy/scipy/issues/17378>`__: griddata linear / LinearNDInterpolator unexpected behavior
* `#17381 <https://github.com/scipy/scipy/issues/17381>`__: BUG: FutureWarning in distance_transform_cdt
* `#17388 <https://github.com/scipy/scipy/issues/17388>`__: BUG: stats.binom: Boost binomial distribution edge case bug?
* `#17403 <https://github.com/scipy/scipy/issues/17403>`__: DOC: There is no general \`scipy.sparse\` page in the user guide
* `#17431 <https://github.com/scipy/scipy/issues/17431>`__: ENH: ECDF in scipy.
* `#17456 <https://github.com/scipy/scipy/issues/17456>`__: ENH: custom stopping criteria with auxiliary function
* `#17516 <https://github.com/scipy/scipy/issues/17516>`__: BUG: Error in documentation for scipy.optimize.minimize
* `#17532 <https://github.com/scipy/scipy/issues/17532>`__: DOC: side bar renders over the top of some of the text in the...
* `#17548 <https://github.com/scipy/scipy/issues/17548>`__: CI: The Ubuntu 18.04 Actions runner image is deprecated
* `#17570 <https://github.com/scipy/scipy/issues/17570>`__: ENH: optimize.root_scalar: default to \`newton\` when only \`x0\`...
* `#17576 <https://github.com/scipy/scipy/issues/17576>`__: ENH: override fit method for von mises
* `#17593 <https://github.com/scipy/scipy/issues/17593>`__: BUG: cannot import name 'permutation_test' from 'scipy.stats'
* `#17604 <https://github.com/scipy/scipy/issues/17604>`__: DOC: optimize.curve_fit: documentation of \`fvec\` is not specific
* `#17620 <https://github.com/scipy/scipy/issues/17620>`__: ENH: Cachable normalisation parameter for frozen distributions
* `#17631 <https://github.com/scipy/scipy/issues/17631>`__: BUG: numerical issues for cdf/ppf of the betaprime distribution
* `#17639 <https://github.com/scipy/scipy/issues/17639>`__: BUG: "xl" not returned if success = False for scipy.optimize.shgo
* `#17652 <https://github.com/scipy/scipy/issues/17652>`__: Check for non-running tests because of test function name and...
* `#17667 <https://github.com/scipy/scipy/issues/17667>`__: BUG: Wrong p-values with Wilcoxon signed-rank test because of...
* `#17683 <https://github.com/scipy/scipy/issues/17683>`__: TST: stats: Several functions with no tests in \`stats.mstats\`
* `#17713 <https://github.com/scipy/scipy/issues/17713>`__: BUG: \`_axis_nan_policy\` changes some common \`TypeError\`s
* `#17725 <https://github.com/scipy/scipy/issues/17725>`__: BUG: spatial: Bad error message from \`hamming\` when \`w\` has...
* `#17749 <https://github.com/scipy/scipy/issues/17749>`__: ENH: Compute non centraled moments with \`stats.moment\`?
* `#17754 <https://github.com/scipy/scipy/issues/17754>`__: Cosine distance of vector to self returns small non-zero answer...
* `#17776 <https://github.com/scipy/scipy/issues/17776>`__: BUG: dblquad and args kwarg
* `#17788 <https://github.com/scipy/scipy/issues/17788>`__: ENH: Scipy Optimize, equal Bounds should be directly passed to...
* `#17805 <https://github.com/scipy/scipy/issues/17805>`__: BUG: stats: dgamma.sf and dgamma.cdf lose precision in the tails
* `#17809 <https://github.com/scipy/scipy/issues/17809>`__: BUG: CDF and PMF of binomial function not same with extreme values
* `#17815 <https://github.com/scipy/scipy/issues/17815>`__: DOC: improve documentation for distance_transform_{cdt,edt}
* `#17819 <https://github.com/scipy/scipy/issues/17819>`__: BUG: \`stats.ttest_ind_from_stats\` doesn't check whether standard...
* `#17828 <https://github.com/scipy/scipy/issues/17828>`__: DOC: UnivariateSpline does not have any documentation or a reference.
* `#17845 <https://github.com/scipy/scipy/issues/17845>`__: BUG: 1.10.0 FIR Decimation is broken when supplying ftype as...
* `#17846 <https://github.com/scipy/scipy/issues/17846>`__: BUG: Infinite loop in scipy.integrate.solve_ivp()
* `#17860 <https://github.com/scipy/scipy/issues/17860>`__: DOC: Incorrect link to ARPACK
* `#17866 <https://github.com/scipy/scipy/issues/17866>`__: DOC: Should \`Result Classes\` be its own top level section?
* `#17911 <https://github.com/scipy/scipy/issues/17911>`__: DOC: Formula of Tustin formula in scipy.signal.bilinear misses...
* `#17913 <https://github.com/scipy/scipy/issues/17913>`__: Unexpected behaviour of pearsonr pvalue for one sided tests
* `#17916 <https://github.com/scipy/scipy/issues/17916>`__: BUG: scipy 1.10.0 crashes when using a large float in skellam...
* `#17941 <https://github.com/scipy/scipy/issues/17941>`__: DOC: guidance on setting dev.py build -j flag in documentation,...
* `#17954 <https://github.com/scipy/scipy/issues/17954>`__: BUG: failure in lobpcg
* `#17970 <https://github.com/scipy/scipy/issues/17970>`__: BUG: ILP64 build issue on Python 3.11
* `#17985 <https://github.com/scipy/scipy/issues/17985>`__: DOC: update wheel generation process
* `#17992 <https://github.com/scipy/scipy/issues/17992>`__: BUG: matlab files with deeply lists of arrays with different...
* `#17999 <https://github.com/scipy/scipy/issues/17999>`__: DOC: incorrect example for stats.cramervonmises
* `#18026 <https://github.com/scipy/scipy/issues/18026>`__: BUG: stats: Error from e.g. \`stats.betabinom.stats(10, 2, 3,...
* `#18067 <https://github.com/scipy/scipy/issues/18067>`__: ENH: stats: resampling/Monte Carlo configuration object
* `#18069 <https://github.com/scipy/scipy/issues/18069>`__: ENH: stats.ttest_ind is inconsistent with R. It does not allow...
* `#18071 <https://github.com/scipy/scipy/issues/18071>`__: BUG: rv_continuous.stats fails to converge when trying to estimate...
* `#18074 <https://github.com/scipy/scipy/issues/18074>`__: BUG: wrong dependencies for pooch
* `#18078 <https://github.com/scipy/scipy/issues/18078>`__: BUG: \`QMCEngine.reset()\` semantics and passed \`Generator\`...
* `#18079 <https://github.com/scipy/scipy/issues/18079>`__: BUG: \`Halton(seed=rng)\` does not consume \`Generator\` PRNG...
* `#18106 <https://github.com/scipy/scipy/issues/18106>`__: BUG: Linprog reports failure despite success convergence, given...
* `#18115 <https://github.com/scipy/scipy/issues/18115>`__: BUG: ValueError: setting an array element with a sequence for...
* `#18117 <https://github.com/scipy/scipy/issues/18117>`__: BUG: stats: large errors in genhyperbolic.cdf and .sf for large...
* `#18119 <https://github.com/scipy/scipy/issues/18119>`__: DOC: The comment about \`fmin_powell\` is wrong
* `#18123 <https://github.com/scipy/scipy/issues/18123>`__: BUG: [mmread] Error while reading mtx file with spaces before...
* `#18132 <https://github.com/scipy/scipy/issues/18132>`__: BUG: invalid output and behavior of scipy.stats.somersd
* `#18139 <https://github.com/scipy/scipy/issues/18139>`__: BUG: Overflow in 'new' implementation of scipy.stats.kendalltau
* `#18143 <https://github.com/scipy/scipy/issues/18143>`__: Building from source on Windows 32-bit Python did not succeed
* `#18171 <https://github.com/scipy/scipy/issues/18171>`__: BUG: optimize.root_scalar: should return normally with \`converged=False\`...
* `#18223 <https://github.com/scipy/scipy/issues/18223>`__: BUG: cKDTree segmentation faults when NaN input and balanced_tree=False,...
* `#18226 <https://github.com/scipy/scipy/issues/18226>`__: ENH: stats.geometric.entropy: implement analytical formula
* `#18239 <https://github.com/scipy/scipy/issues/18239>`__: DOC: linking to custom BLAS/LAPACK locations is not clear
* `#18254 <https://github.com/scipy/scipy/issues/18254>`__: BUG: stats.mode: failure with array of Pandas integers
* `#18271 <https://github.com/scipy/scipy/issues/18271>`__: Broken or wrong formulas on distance definition
* `#18272 <https://github.com/scipy/scipy/issues/18272>`__: BUG: stats: occasional failure of \`test_multivariate.TestOrthoGroup.test_det_and_ortho\`
* `#18274 <https://github.com/scipy/scipy/issues/18274>`__: BUG: stats: Spurious warnings from \`betaprime.fit\`
* `#18282 <https://github.com/scipy/scipy/issues/18282>`__: Incompatible pointer warning from \`stats._rcond\`
* `#18302 <https://github.com/scipy/scipy/issues/18302>`__: BUG: beta.pdf is broken on main (1.11.0.dev0)
* `#18322 <https://github.com/scipy/scipy/issues/18322>`__: BUG: scipy.stats.shapiro gives a negative pvalue
* `#18326 <https://github.com/scipy/scipy/issues/18326>`__: ENH: milp supporting sparse inputs
* `#18329 <https://github.com/scipy/scipy/issues/18329>`__: BUG: meson generates \`warning: "MS_WIN64" redefined\` when building...
* `#18368 <https://github.com/scipy/scipy/issues/18368>`__: DOC: Issue in scipy.stats.chisquare
* `#18377 <https://github.com/scipy/scipy/issues/18377>`__: BUG: \`const\` signature changes in \`cython_blas\` and \`cython_lapack\`...
* `#18388 <https://github.com/scipy/scipy/issues/18388>`__: Question about usage of _MACHEPS
* `#18407 <https://github.com/scipy/scipy/issues/18407>`__: CI: test_enzo_example_c_with_unboundedness started failing
* `#18415 <https://github.com/scipy/scipy/issues/18415>`__: BUG: Windows compilation error with Intel Fortran in PROPACK
* `#18425 <https://github.com/scipy/scipy/issues/18425>`__: DOC: clarify that scipy.ndimage.sobel does not compute the 2D...
* `#18443 <https://github.com/scipy/scipy/issues/18443>`__: BLD: errors when building SciPy on Windows with Meson
* `#18456 <https://github.com/scipy/scipy/issues/18456>`__: ENH: Allow passing non-varying arguments for the model function...
* `#18484 <https://github.com/scipy/scipy/issues/18484>`__: DEP: Warn on deprecated windows-import in base \`scipy.signal\`...
* `#18485 <https://github.com/scipy/scipy/issues/18485>`__: DEP: deprecate multiple-ellipsis handling in sparse matrix indexing
* `#18494 <https://github.com/scipy/scipy/issues/18494>`__: CI: occasional failure of \`test_minimum_spanning_tree\`
* `#18497 <https://github.com/scipy/scipy/issues/18497>`__: MAINT, BUG: guard against non-finite kd-tree queries
* `#18498 <https://github.com/scipy/scipy/issues/18498>`__: TST: interpolate overflow xslow tests (low priority)
* `#18525 <https://github.com/scipy/scipy/issues/18525>`__: DOC: sparse doc build warning causing failure (including in CI)
* `#18535 <https://github.com/scipy/scipy/issues/18535>`__: DOC: Dev branch docs render Dev TOC while viewing API Reference
* `#18547 <https://github.com/scipy/scipy/issues/18547>`__: CI: occasionally failing test \`test_minimize_callback_copies_array[fmin]\`
* `#18595 <https://github.com/scipy/scipy/issues/18595>`__: BUG: dev.py notes needs a small shim
* `#18597 <https://github.com/scipy/scipy/issues/18597>`__: CI, BUG: Cirrus wheel upload fails on maintenance branch
* `#18600 <https://github.com/scipy/scipy/issues/18600>`__: BUG: SciPy 1.11.0rc1 not buildable on PPC due to boost submodule
* `#18632 <https://github.com/scipy/scipy/issues/18632>`__: 1.11.0rc1: remaining test failures in conda-forge
* `#18634 <https://github.com/scipy/scipy/issues/18634>`__: BUG: stats.truncnorm.moments yields error for moment order greater...
* `#18654 <https://github.com/scipy/scipy/issues/18654>`__: BUG: ci/circleci: build_scipy broken
* `#18675 <https://github.com/scipy/scipy/issues/18675>`__: BUG: \`signal.detrend\` on main no longer accepts a sequence...
* `#18732 <https://github.com/scipy/scipy/issues/18732>`__: TST, MAINT: some tests blocking 1.11.0 on MacOS ARM64 with NumPy...

************************
Pull requests for 1.11.0
************************

* `#8727 <https://github.com/scipy/scipy/pull/8727>`__: BUG: vq.kmeans() compares signed diff to a threshold.
* `#12787 <https://github.com/scipy/scipy/pull/12787>`__: ENH: add anderson darling test for weibull #10829
* `#13699 <https://github.com/scipy/scipy/pull/13699>`__: ENH: stats: Add handling of censored data to univariate cont....
* `#14069 <https://github.com/scipy/scipy/pull/14069>`__: Use warnings instead of print statements
* `#15073 <https://github.com/scipy/scipy/pull/15073>`__: TST/MAINT: Parametrize \`_METRICS_NAMES\` & replace \`assert_raises\`...
* `#15841 <https://github.com/scipy/scipy/pull/15841>`__: Overhaul \`factorial{,2,k}\`: API coherence, bug fixes & consistent...
* `#15873 <https://github.com/scipy/scipy/pull/15873>`__: DEP: remove sym_pos argument from linalg.solve
* `#15877 <https://github.com/scipy/scipy/pull/15877>`__: DEP: remove extradoc in _distn_infrastructure
* `#15929 <https://github.com/scipy/scipy/pull/15929>`__: DEP: \`lsim2\` deprecated in favor of \`lsim\`
* `#15958 <https://github.com/scipy/scipy/pull/15958>`__: CI: move \`prerelease_deps_coverage_64bit_blas\` to GitHub actions.
* `#16071 <https://github.com/scipy/scipy/pull/16071>`__: ENH: Add missing "characteristic impedance of vacuum"
* `#16313 <https://github.com/scipy/scipy/pull/16313>`__: MAINT: Update optimize.shgo
* `#16782 <https://github.com/scipy/scipy/pull/16782>`__: ENH: stats: optimised fit for the truncated Pareto distribution
* `#16839 <https://github.com/scipy/scipy/pull/16839>`__: ENH: stats: optimised MLE for the lognormal distribution
* `#16936 <https://github.com/scipy/scipy/pull/16936>`__: BUG: sparse: fix argmin/argmax when all entries are nonzero
* `#16961 <https://github.com/scipy/scipy/pull/16961>`__: ENH: optimize: Add \`nan_policy\` optional argument for \`curve_fit\`.
* `#16996 <https://github.com/scipy/scipy/pull/16996>`__: ENH: stats.anderson_ksamp: add permutation version of test
* `#17116 <https://github.com/scipy/scipy/pull/17116>`__: MAINT: Adjust Pull-Request labeler configuration
* `#17208 <https://github.com/scipy/scipy/pull/17208>`__: DOC: Add triage guide
* `#17211 <https://github.com/scipy/scipy/pull/17211>`__: ENH: Implemented Dirichlet-multinomial distribution (#16810)
* `#17212 <https://github.com/scipy/scipy/pull/17212>`__: Guard against integer overflows in fitpackmodule.c
* `#17235 <https://github.com/scipy/scipy/pull/17235>`__: MAINT: pass check_finite to the vq() call of kmeans2()
* `#17267 <https://github.com/scipy/scipy/pull/17267>`__: DOC/MAINT: special: Several updates for tklmbda
* `#17268 <https://github.com/scipy/scipy/pull/17268>`__: DOC: special: Show that lambertw can solve x = a + b\*exp(c\*x)
* `#17287 <https://github.com/scipy/scipy/pull/17287>`__: DOC: Clarify minimum_spanning_tree behavior in non-connected...
* `#17310 <https://github.com/scipy/scipy/pull/17310>`__: DOC: missing-bits: document recommendations on return object...
* `#17322 <https://github.com/scipy/scipy/pull/17322>`__: DOC: Add notebook infrastructure for the docs
* `#17326 <https://github.com/scipy/scipy/pull/17326>`__: ENH: Clarify the index of element corresponding to a label in...
* `#17334 <https://github.com/scipy/scipy/pull/17334>`__: ENH: Map the rotation quaternion double cover of rotation space...
* `#17402 <https://github.com/scipy/scipy/pull/17402>`__: ENH: stats: add false discovery rate control function
* `#17410 <https://github.com/scipy/scipy/pull/17410>`__: ENH: stats.multivariate_t: add cdf method
* `#17432 <https://github.com/scipy/scipy/pull/17432>`__: BLD: Boost.Math standalone submodule
* `#17451 <https://github.com/scipy/scipy/pull/17451>`__: DEP: Remove \`vertices\` in qhull.
* `#17455 <https://github.com/scipy/scipy/pull/17455>`__: Deprecate scipy.signal.{bspline, quadratic, cubic}
* `#17479 <https://github.com/scipy/scipy/pull/17479>`__: ENH: Add new SI prefixes
* `#17480 <https://github.com/scipy/scipy/pull/17480>`__: ENH: stats: Implement _sf and _isf for halfnorm, gibrat, gompertz.
* `#17483 <https://github.com/scipy/scipy/pull/17483>`__: MAINT: optimize.basinhopping: fix acceptance of failed local...
* `#17486 <https://github.com/scipy/scipy/pull/17486>`__: ENH: optimize.minimize: callback enhancements
* `#17499 <https://github.com/scipy/scipy/pull/17499>`__: MAINT: remove use of \`NPY_UPDATEIFCOPY\`
* `#17505 <https://github.com/scipy/scipy/pull/17505>`__: ENH: Add relativistic Breit-Wigner Distribution
* `#17529 <https://github.com/scipy/scipy/pull/17529>`__: ENH: stats: Implement powerlaw._sf
* `#17531 <https://github.com/scipy/scipy/pull/17531>`__: TST: scipy.signal.order_filter: add test coverage
* `#17535 <https://github.com/scipy/scipy/pull/17535>`__: MAINT: special: Improve comments about Cephes p1evl function.
* `#17538 <https://github.com/scipy/scipy/pull/17538>`__: ENH: Extending _distance_pybind with additional distance metrics...
* `#17541 <https://github.com/scipy/scipy/pull/17541>`__: REL: set version to 1.11.0.dev0
* `#17553 <https://github.com/scipy/scipy/pull/17553>`__: DOC: optimize.curve_fit: add note about \`pcov\` condition number
* `#17555 <https://github.com/scipy/scipy/pull/17555>`__: DEP: stats: removal of kwargs n in stats.moment and alpha in...
* `#17556 <https://github.com/scipy/scipy/pull/17556>`__: DEV: bump flake8 version used in CI job
* `#17557 <https://github.com/scipy/scipy/pull/17557>`__: MAINT: bump Ubuntu version in Azure CI
* `#17561 <https://github.com/scipy/scipy/pull/17561>`__: MAINT: stats.mode: remove deprecated features, smooth edges
* `#17562 <https://github.com/scipy/scipy/pull/17562>`__: ENH: stats: Implement _ppf for the betaprime distribution.
* `#17563 <https://github.com/scipy/scipy/pull/17563>`__: DEP: stats: remove misspelt gilbrat distribution
* `#17566 <https://github.com/scipy/scipy/pull/17566>`__: DOC: correct, update, and extend \`lobpcg\` docstring info and...
* `#17567 <https://github.com/scipy/scipy/pull/17567>`__: MAINT: Update gitpod setup
* `#17573 <https://github.com/scipy/scipy/pull/17573>`__: DOC: Update testing documentation to dev.py
* `#17574 <https://github.com/scipy/scipy/pull/17574>`__: MAINT: clean up \`NPY_OLD\` usage in Cython code and build files
* `#17581 <https://github.com/scipy/scipy/pull/17581>`__: DOC fix trivial typo in description of loggamma in _add_newdocs.py
* `#17585 <https://github.com/scipy/scipy/pull/17585>`__: ENH: Von Mises distribution fit
* `#17587 <https://github.com/scipy/scipy/pull/17587>`__: BUG: stats: Avoid overflow/underflow issues in loggamma _cdf,...
* `#17589 <https://github.com/scipy/scipy/pull/17589>`__: BUG: FutureWarning in distance_transform_cdt
* `#17590 <https://github.com/scipy/scipy/pull/17590>`__: DEP: raise on >1-dim inputs for optimize.minimize
* `#17595 <https://github.com/scipy/scipy/pull/17595>`__: DOC: optimize.line_search: note that \`pk\` must be a descent...
* `#17597 <https://github.com/scipy/scipy/pull/17597>`__: DOC: Add Legacy directive
* `#17603 <https://github.com/scipy/scipy/pull/17603>`__: DEP: remove spatial.distance.kulsinski
* `#17605 <https://github.com/scipy/scipy/pull/17605>`__: DOC: example of epidemic model with LHS
* `#17608 <https://github.com/scipy/scipy/pull/17608>`__: DOC: curve_fit - clarify fvec output
* `#17610 <https://github.com/scipy/scipy/pull/17610>`__: DOC: add example to chi2_contingency
* `#17613 <https://github.com/scipy/scipy/pull/17613>`__: DOC: curve_fit, include sigma
* `#17615 <https://github.com/scipy/scipy/pull/17615>`__: MAINT: scipy.optimize.root: fix error when both args and jac...
* `#17616 <https://github.com/scipy/scipy/pull/17616>`__: MAINT: optimize.minimize: enhance \`callback\` for remaining...
* `#17617 <https://github.com/scipy/scipy/pull/17617>`__: DEP: remove MaximumFlowResult.residual
* `#17618 <https://github.com/scipy/scipy/pull/17618>`__: DOC: fix unicode in qmc example
* `#17622 <https://github.com/scipy/scipy/pull/17622>`__: MAINT: optimize.root_scalar: raise when NaN is encountered
* `#17624 <https://github.com/scipy/scipy/pull/17624>`__: ENH: add von Mises-Fisher distribution
* `#17625 <https://github.com/scipy/scipy/pull/17625>`__: DOC: Examples for special functions related to the student t...
* `#17626 <https://github.com/scipy/scipy/pull/17626>`__: DOC: improve docstrings of exp. scaled Bessel functions
* `#17628 <https://github.com/scipy/scipy/pull/17628>`__: ENH: add Sobol' indices
* `#17629 <https://github.com/scipy/scipy/pull/17629>`__: DOC: stats: example treatment odd_ratio
* `#17637 <https://github.com/scipy/scipy/pull/17637>`__: DEP: switch default of special.comb to legacy=False
* `#17643 <https://github.com/scipy/scipy/pull/17643>`__: TST: interpolate/rgi: Add tests for descending ordered points
* `#17649 <https://github.com/scipy/scipy/pull/17649>`__: fix documentation lines
* `#17651 <https://github.com/scipy/scipy/pull/17651>`__: Update _svds.py removing no longer necessary QR for LOBPCG output
* `#17654 <https://github.com/scipy/scipy/pull/17654>`__: MAINT:interpolate:Add .c file to .gitignore
* `#17655 <https://github.com/scipy/scipy/pull/17655>`__: DEV: add check for misnamed tests
* `#17657 <https://github.com/scipy/scipy/pull/17657>`__: DEV: streamline OpenBLAS handling on Win machine
* `#17660 <https://github.com/scipy/scipy/pull/17660>`__: MAINT: optimize.newton: converged=False when secant has zero...
* `#17663 <https://github.com/scipy/scipy/pull/17663>`__: DOC: optimize.curve_fit: example output may vary
* `#17664 <https://github.com/scipy/scipy/pull/17664>`__: MAINT: optimize.root_scalar: fix underflow sign check bug
* `#17665 <https://github.com/scipy/scipy/pull/17665>`__: DOC: mention inaccuracy of curve_fit result \`pcov\`
* `#17666 <https://github.com/scipy/scipy/pull/17666>`__: DOC: optimize.root_scalar: harmonize documentation and implementation...
* `#17668 <https://github.com/scipy/scipy/pull/17668>`__: ENH: stats.loguniform: reformulate methods to avoid overflow
* `#17669 <https://github.com/scipy/scipy/pull/17669>`__: MAINT: optimize.newton: avoid error with complex \`x0\`
* `#17674 <https://github.com/scipy/scipy/pull/17674>`__: DOC: optimize: add tutorial example of passing kwargs to callable
* `#17675 <https://github.com/scipy/scipy/pull/17675>`__: ENH: update lobpcg.py
* `#17676 <https://github.com/scipy/scipy/pull/17676>`__: BUG: correctly handle array-like types in scipy.io.savemat
* `#17678 <https://github.com/scipy/scipy/pull/17678>`__: DOC: optimize: show how memoization avoids duplicating work
* `#17679 <https://github.com/scipy/scipy/pull/17679>`__: ENH: optimize.minimize: add bound constraints to COBYLA
* `#17680 <https://github.com/scipy/scipy/pull/17680>`__: DOC: examples for special functions related to neg. binomial...
* `#17682 <https://github.com/scipy/scipy/pull/17682>`__: DOC: add real example for \`stats.chisquare\`
* `#17684 <https://github.com/scipy/scipy/pull/17684>`__: ENH: support \`Bounds\` class in lsq_linear
* `#17685 <https://github.com/scipy/scipy/pull/17685>`__: ENH: stats: Implement _sf for the foldnorm distribution.
* `#17687 <https://github.com/scipy/scipy/pull/17687>`__: MAINT: optimize.toms748: correct "rtol too small" message
* `#17688 <https://github.com/scipy/scipy/pull/17688>`__: MAINT: optimize.curve_fit: memoize \`f\` and \`jac\`
* `#17691 <https://github.com/scipy/scipy/pull/17691>`__: ENH: optimize.root_scalar: allow newton without f', secant without...
* `#17692 <https://github.com/scipy/scipy/pull/17692>`__: MAINT: optimize.minimize_scalar: enforce output shape consistency
* `#17693 <https://github.com/scipy/scipy/pull/17693>`__: DOC: pointbiserialr correlation formula notation fix.
* `#17694 <https://github.com/scipy/scipy/pull/17694>`__: ENH: stats: Implement _sf and _isf for halfcauchy; _sf for foldcauchy
* `#17698 <https://github.com/scipy/scipy/pull/17698>`__: MAINT: implicit float conversion in rgi test
* `#17700 <https://github.com/scipy/scipy/pull/17700>`__: ENH: Inverse wishart entropy
* `#17701 <https://github.com/scipy/scipy/pull/17701>`__: DOC: stats: Fix a reference for the genexpon distribution.
* `#17702 <https://github.com/scipy/scipy/pull/17702>`__: DOC: stats: complete references and links for descriptive stats
* `#17704 <https://github.com/scipy/scipy/pull/17704>`__: MAINT: optimize.bracket: don't fail silently
* `#17705 <https://github.com/scipy/scipy/pull/17705>`__: DOC: optimize.minimize_scalar and friends: correct documentation...
* `#17707 <https://github.com/scipy/scipy/pull/17707>`__: DOC: add acetazolamide example to \`stats.fisher_exact\`
* `#17708 <https://github.com/scipy/scipy/pull/17708>`__: ENH: stats: Implement _ppf and _isf for genexpon.
* `#17709 <https://github.com/scipy/scipy/pull/17709>`__: MAINT: update copyright date
* `#17711 <https://github.com/scipy/scipy/pull/17711>`__: MAINT: forward port 1.10.0 relnotes
* `#17714 <https://github.com/scipy/scipy/pull/17714>`__: ENH: Provide public API for fast DisjointSet subset size.
* `#17724 <https://github.com/scipy/scipy/pull/17724>`__: DOC: spatial: Several updates:
* `#17729 <https://github.com/scipy/scipy/pull/17729>`__: STY: fix unicode error
* `#17730 <https://github.com/scipy/scipy/pull/17730>`__: MAINT: rotate CircleCI ssh key
* `#17732 <https://github.com/scipy/scipy/pull/17732>`__: MAINT: optimize.toms748: don't do newton after secant interpolation
* `#17742 <https://github.com/scipy/scipy/pull/17742>`__: ENH: override _entropy for beta, chi and chi2 distributions
* `#17747 <https://github.com/scipy/scipy/pull/17747>`__: DOC: stats.jarque_bera: add semi-realistic example
* `#17750 <https://github.com/scipy/scipy/pull/17750>`__: ENH: Support multinomial distributions with n=0 trials.
* `#17758 <https://github.com/scipy/scipy/pull/17758>`__: ENH: analytical formula for f distribution entropy
* `#17759 <https://github.com/scipy/scipy/pull/17759>`__: DOC: stats.skewtest: add semi-realistic example
* `#17762 <https://github.com/scipy/scipy/pull/17762>`__: DOC: remove space between directive name and double colon ``::``
* `#17763 <https://github.com/scipy/scipy/pull/17763>`__: DOC: single -> double colon for directive.
* `#17764 <https://github.com/scipy/scipy/pull/17764>`__: ENH: entropy for matrix normal distribution
* `#17765 <https://github.com/scipy/scipy/pull/17765>`__: DOC: stats: additional normality test examples
* `#17767 <https://github.com/scipy/scipy/pull/17767>`__: DOC: stats: reorganize hypothesis tests in main page
* `#17768 <https://github.com/scipy/scipy/pull/17768>`__: TST: special: fix incorrectly named tests
* `#17769 <https://github.com/scipy/scipy/pull/17769>`__: DOC/BUG: add missing entropy methods in docstrings
* `#17770 <https://github.com/scipy/scipy/pull/17770>`__: TST: stats: fixed misnamed tests
* `#17772 <https://github.com/scipy/scipy/pull/17772>`__: MAINT: remove unused test utility functions
* `#17773 <https://github.com/scipy/scipy/pull/17773>`__: DOC: stats: add realistic examples to correlation tests
* `#17778 <https://github.com/scipy/scipy/pull/17778>`__: DOC: stats: add realistic examples to variance tests
* `#17780 <https://github.com/scipy/scipy/pull/17780>`__: MAINT: optimize.minimize: fix new callback interface when parameter...
* `#17784 <https://github.com/scipy/scipy/pull/17784>`__: DOC: linalg: fix docstring of \`linalg.sqrtm\`
* `#17786 <https://github.com/scipy/scipy/pull/17786>`__: DOC: examples for ndtr, ndtri
* `#17791 <https://github.com/scipy/scipy/pull/17791>`__: DEP: remove maxiter kwarg in _minimize_tnc
* `#17793 <https://github.com/scipy/scipy/pull/17793>`__: MAINT: remove divide by zero in differential_evolution
* `#17794 <https://github.com/scipy/scipy/pull/17794>`__: TST: Added test suite for dgamma distribution
* `#17812 <https://github.com/scipy/scipy/pull/17812>`__: MAINT: add (optional) pre-commit hook
* `#17813 <https://github.com/scipy/scipy/pull/17813>`__: MAINT: integrate.qmc_quad: re-introduce qmc_quad
* `#17816 <https://github.com/scipy/scipy/pull/17816>`__: MAINT: allow typed method in \`stats.sobol_indices\`
* `#17817 <https://github.com/scipy/scipy/pull/17817>`__: MAINT: remove unused args parameter from \`qmc_quad\`
* `#17818 <https://github.com/scipy/scipy/pull/17818>`__: BUG/ENH: stats: several updates for dgamma.
* `#17820 <https://github.com/scipy/scipy/pull/17820>`__: DOC/BUG: plot \`ndtri\` only where it is defined
* `#17824 <https://github.com/scipy/scipy/pull/17824>`__: ENH: analytical entropy for invgauss distribution
* `#17825 <https://github.com/scipy/scipy/pull/17825>`__: DOC: optimize: change term zero to root
* `#17829 <https://github.com/scipy/scipy/pull/17829>`__: DOC: stats: document RNG behavior when distribution is deepcopied
* `#17830 <https://github.com/scipy/scipy/pull/17830>`__: MAINT: stats._axis_nan_policy: raise appropriate TypeErrors
* `#17834 <https://github.com/scipy/scipy/pull/17834>`__: MAINT: improve accuracy of betaprime cdf in scipy.stats
* `#17835 <https://github.com/scipy/scipy/pull/17835>`__: DOC: integrate: document limitation of numerical integration
* `#17836 <https://github.com/scipy/scipy/pull/17836>`__: DOC: integrate.solve_ivp: clarify impact of parameter \`vectorized\`
* `#17837 <https://github.com/scipy/scipy/pull/17837>`__: DEP: integrate.nquad: deprecate parameter \`full_output\`
* `#17838 <https://github.com/scipy/scipy/pull/17838>`__: DOC: integrate.quad: behavior is not guaranteed for divergent...
* `#17841 <https://github.com/scipy/scipy/pull/17841>`__: DOC: linalg: expand pinv example
* `#17842 <https://github.com/scipy/scipy/pull/17842>`__: DOC, MAINT: Add issue template for Documentation issues
* `#17848 <https://github.com/scipy/scipy/pull/17848>`__: ENH: implement _sf and _isf for powernorm distribution
* `#17849 <https://github.com/scipy/scipy/pull/17849>`__: ENH: special: Add the function _scaled_exp1
* `#17852 <https://github.com/scipy/scipy/pull/17852>`__: MAINT: optimize: improve \`optimize.curve_fit\` doc and error...
* `#17853 <https://github.com/scipy/scipy/pull/17853>`__: DOC: integrate.dblquad/tplquad: update result descriptions
* `#17857 <https://github.com/scipy/scipy/pull/17857>`__: MAINT: analytical formula for genlogistic entropy
* `#17865 <https://github.com/scipy/scipy/pull/17865>`__: MAINT: stats: fix recent CI and other issues
* `#17867 <https://github.com/scipy/scipy/pull/17867>`__: DOC: note on negative variables for linprog
* `#17868 <https://github.com/scipy/scipy/pull/17868>`__: ENH: add analytical formula for Nakagami distribution entropy
* `#17873 <https://github.com/scipy/scipy/pull/17873>`__: ENH: Added analytical formula for dgamma distribution entropy...
* `#17874 <https://github.com/scipy/scipy/pull/17874>`__: ENH: Added analytical formula for truncnorm entropy (#17748)
* `#17876 <https://github.com/scipy/scipy/pull/17876>`__: DOC: remove hidden stats sections from sidebar/toctree
* `#17878 <https://github.com/scipy/scipy/pull/17878>`__: Lint everything
* `#17879 <https://github.com/scipy/scipy/pull/17879>`__: DOC: add docs for the main namespace
* `#17881 <https://github.com/scipy/scipy/pull/17881>`__: BUG: Fix handling on user-supplied filters in \`signal.decimate\`
* `#17882 <https://github.com/scipy/scipy/pull/17882>`__: BLD: fix Meson build warnings about multiple targets
* `#17883 <https://github.com/scipy/scipy/pull/17883>`__: DOC: Clarified the meaning of optional arguments in optimize.leastsq
* `#17886 <https://github.com/scipy/scipy/pull/17886>`__: ENH: Warn about missing boundary when NOLA condition failed in...
* `#17889 <https://github.com/scipy/scipy/pull/17889>`__: DOC: Cleanup development guide
* `#17892 <https://github.com/scipy/scipy/pull/17892>`__: MAINT: stats: Post-"lint everything" clean up in stats.
* `#17894 <https://github.com/scipy/scipy/pull/17894>`__: MAINT: update .gitignore with meson and linter
* `#17895 <https://github.com/scipy/scipy/pull/17895>`__: DOC: config info in issue template
* `#17897 <https://github.com/scipy/scipy/pull/17897>`__: MAINT: Update the "lint everything" SHA in .git-blame-ignore-revs
* `#17898 <https://github.com/scipy/scipy/pull/17898>`__: DOC: remove hidden submodules from sidebar
* `#17899 <https://github.com/scipy/scipy/pull/17899>`__: MAINT: use conda for linters
* `#17900 <https://github.com/scipy/scipy/pull/17900>`__: Re-implement pre-commit hook in Python
* `#17906 <https://github.com/scipy/scipy/pull/17906>`__: DOC: interpolate: add a note against using triangulation based...
* `#17907 <https://github.com/scipy/scipy/pull/17907>`__: DOC: stats.wilcoxon: warn about roundoff errors in x-y
* `#17908 <https://github.com/scipy/scipy/pull/17908>`__: ENH: powerlognormal distribution improvements
* `#17909 <https://github.com/scipy/scipy/pull/17909>`__: ENH: improve accuracy of betaprime ppf in scipy.stats
* `#17915 <https://github.com/scipy/scipy/pull/17915>`__: DOC: Add warning to butter function docstring
* `#17921 <https://github.com/scipy/scipy/pull/17921>`__: CI: clean conda index upon cache invalidation
* `#17922 <https://github.com/scipy/scipy/pull/17922>`__: DOC: corrected doc of bilinear discretization of lti
* `#17929 <https://github.com/scipy/scipy/pull/17929>`__: ENH: stats.nakagami.entropy: improve formulation
* `#17930 <https://github.com/scipy/scipy/pull/17930>`__: ENH: use asymptotic expansions for entropy of \`genlogistic\`...
* `#17937 <https://github.com/scipy/scipy/pull/17937>`__: DOC: Update pip + venv instructions in the contributor documentation...
* `#17939 <https://github.com/scipy/scipy/pull/17939>`__: DOC: ttest_ind_from_stats: discuss negative stdev
* `#17943 <https://github.com/scipy/scipy/pull/17943>`__: ENH: early exit random-cd optimization in 1D
* `#17944 <https://github.com/scipy/scipy/pull/17944>`__: pre-commit should fail when fixes are made by Ruff
* `#17945 <https://github.com/scipy/scipy/pull/17945>`__: DOC: remove seed in HTML only
* `#17946 <https://github.com/scipy/scipy/pull/17946>`__: ENH: Maxwell distribution \`sf\`/\`isf\` override
* `#17947 <https://github.com/scipy/scipy/pull/17947>`__: TST: Update list of modules for import cycle checks
* `#17948 <https://github.com/scipy/scipy/pull/17948>`__: STY: fix only staged files.
* `#17949 <https://github.com/scipy/scipy/pull/17949>`__: ENH: stats.dirichlet_multinomial: vectorize implementation
* `#17950 <https://github.com/scipy/scipy/pull/17950>`__: MAINT: bump OpenBLAS version, bump macOS image used in GHA
* `#17956 <https://github.com/scipy/scipy/pull/17956>`__: MAINT: optimize.dual_annealing: fix callable jac with args
* `#17959 <https://github.com/scipy/scipy/pull/17959>`__: MAINT: update supported versions of Python and NumPy to follow...
* `#17961 <https://github.com/scipy/scipy/pull/17961>`__: ENH: optimize.linprog: pass unrecognized options to HiGHS verbatim
* `#17964 <https://github.com/scipy/scipy/pull/17964>`__: DEP: integrate.quad_vec: deprecate parameter full_output
* `#17967 <https://github.com/scipy/scipy/pull/17967>`__: MAINT: Fully qualify std::move invocations to fix clang -Wunqualified-std-cast-call
* `#17971 <https://github.com/scipy/scipy/pull/17971>`__: ENH: stats: add axis tuple and nan_policy to \`sem\` and \`iqr\`
* `#17975 <https://github.com/scipy/scipy/pull/17975>`__: BUG: Update test_lobpcg.py
* `#17976 <https://github.com/scipy/scipy/pull/17976>`__: DOC/MAINT: simplify release entries
* `#17980 <https://github.com/scipy/scipy/pull/17980>`__: FIX: CI: avoid passing Cython files to ruff
* `#17982 <https://github.com/scipy/scipy/pull/17982>`__: MAINT: add release entries move to blame ignore
* `#17987 <https://github.com/scipy/scipy/pull/17987>`__: DOC: move .rst.txt to source and cleaning around generating doc
* `#17989 <https://github.com/scipy/scipy/pull/17989>`__: MAINT: sparse.linalg: remove unused __main__ code
* `#17990 <https://github.com/scipy/scipy/pull/17990>`__: BLD: make musllinux wheels for nightly
* `#17998 <https://github.com/scipy/scipy/pull/17998>`__: ENH: optimize.RootResults: make \`RootResults\` an \`OptimizeResult\`
* `#18000 <https://github.com/scipy/scipy/pull/18000>`__: DOC: stats, interpolate: Fix some minor docstring issues.
* `#18002 <https://github.com/scipy/scipy/pull/18002>`__: ENH: override halflogistic \`sf\` and \`isf\`
* `#18003 <https://github.com/scipy/scipy/pull/18003>`__: ENH: improve halfnorm CDF precision
* `#18006 <https://github.com/scipy/scipy/pull/18006>`__: BLD: use a relative path to numpy include and library directories
* `#18008 <https://github.com/scipy/scipy/pull/18008>`__: MAINT: forward port 1.10.1 relnotes
* `#18013 <https://github.com/scipy/scipy/pull/18013>`__: MAINT: stats.vonmises.fit: maintain backward compatibility
* `#18015 <https://github.com/scipy/scipy/pull/18015>`__: TST: optimize.root_scalar: refactor tests and add Chandrupatla...
* `#18016 <https://github.com/scipy/scipy/pull/18016>`__: Add axes argument to ndimage filters
* `#18018 <https://github.com/scipy/scipy/pull/18018>`__: DOC: Add an example showing how to plot Rotations to the docs
* `#18019 <https://github.com/scipy/scipy/pull/18019>`__: add tests for \`trimmed_var\` and \`trimmed_std\` in \`stats.mstats\`
* `#18020 <https://github.com/scipy/scipy/pull/18020>`__: TST: stats.mstats: add \`median_cihs\`/\`sen_seasonal_slopes\`...
* `#18021 <https://github.com/scipy/scipy/pull/18021>`__: DEP: linalg: deprecate tri{,u,l}
* `#18022 <https://github.com/scipy/scipy/pull/18022>`__: DOC: interpolate: link to the gist with the porting guide
* `#18023 <https://github.com/scipy/scipy/pull/18023>`__: DOC: how to document examples using RNG and also self-contained...
* `#18027 <https://github.com/scipy/scipy/pull/18027>`__: DOC: fix section title typo in interpolation tutorial
* `#18028 <https://github.com/scipy/scipy/pull/18028>`__: DOC: fix underlying of title in extrapolate
* `#18029 <https://github.com/scipy/scipy/pull/18029>`__: fix error from betabinom stats using only integers for a and...
* `#18032 <https://github.com/scipy/scipy/pull/18032>`__: BLD: add NDEBUG flag for release builds
* `#18034 <https://github.com/scipy/scipy/pull/18034>`__: BLD: avoid running \`run_command(py3, ...)\`, for better cross-compiling
* `#18035 <https://github.com/scipy/scipy/pull/18035>`__: ENH: stats: add ecdf function
* `#18036 <https://github.com/scipy/scipy/pull/18036>`__: BLD: build Windows wheel for py39 against numpy 1.22.3
* `#18037 <https://github.com/scipy/scipy/pull/18037>`__: DOC/MAINT: fix source button
* `#18040 <https://github.com/scipy/scipy/pull/18040>`__: DOC: Fix error in doc of _minimize_trustregion_exact
* `#18043 <https://github.com/scipy/scipy/pull/18043>`__: MAINT: update GH bug template
* `#18045 <https://github.com/scipy/scipy/pull/18045>`__: MAINT: update codeowners.
* `#18047 <https://github.com/scipy/scipy/pull/18047>`__: DOC: Update scipy.spatial.distance.pdist docstring to match its...
* `#18049 <https://github.com/scipy/scipy/pull/18049>`__: STY: Include Python.h before any other headers.
* `#18050 <https://github.com/scipy/scipy/pull/18050>`__: MAINT: integrate.qmc_quad: correct behavior of parameter \`log\`
* `#18052 <https://github.com/scipy/scipy/pull/18052>`__: BLD: use anaconda-client to upload wheels
* `#18053 <https://github.com/scipy/scipy/pull/18053>`__: DOC fix expectile docstring - empirical CDF
* `#18058 <https://github.com/scipy/scipy/pull/18058>`__: BLD: use meson-native dependency lookup for pybind11
* `#18059 <https://github.com/scipy/scipy/pull/18059>`__: Johnson distributions \`sf\` and \`isf\` override
* `#18060 <https://github.com/scipy/scipy/pull/18060>`__: MAINT: remove pavement
* `#18061 <https://github.com/scipy/scipy/pull/18061>`__: ENH: implement array @ LinearOperator
* `#18063 <https://github.com/scipy/scipy/pull/18063>`__: DOC: improve documentation for distance_transform_{cdt,edt}
* `#18064 <https://github.com/scipy/scipy/pull/18064>`__: DOC: add examples in for xlogy
* `#18066 <https://github.com/scipy/scipy/pull/18066>`__: TST: stats.nct: add test for crash with large nc
* `#18068 <https://github.com/scipy/scipy/pull/18068>`__: TST: stats.ksone: loosen variance test tolerance
* `#18070 <https://github.com/scipy/scipy/pull/18070>`__: Docstring: note on bivariate spline axis ordering
* `#18072 <https://github.com/scipy/scipy/pull/18072>`__: DOC: Modifying t parameter documentation issue in splprep #17893
* `#18073 <https://github.com/scipy/scipy/pull/18073>`__: MAINT: avoid non-recommended numpy functions and constants
* `#18075 <https://github.com/scipy/scipy/pull/18075>`__: MAINT: update pooch deps
* `#18076 <https://github.com/scipy/scipy/pull/18076>`__: DOC: fix docstring typo for \`kurtosis\` and whitespace in \`_continuous_distns\`
* `#18077 <https://github.com/scipy/scipy/pull/18077>`__: BUG: Check for initial state finiteness
* `#18081 <https://github.com/scipy/scipy/pull/18081>`__: ENH: allow single observation for equal variance in \`stats.ttest_ind\`
* `#18082 <https://github.com/scipy/scipy/pull/18082>`__: DOC: add examples for xlog1py
* `#18083 <https://github.com/scipy/scipy/pull/18083>`__: STY: fix mypy assignment.
* `#18084 <https://github.com/scipy/scipy/pull/18084>`__: BUG: calculate VDC permutations at init of Halton
* `#18092 <https://github.com/scipy/scipy/pull/18092>`__: ENH: stats.ecdf: support right-censored data
* `#18094 <https://github.com/scipy/scipy/pull/18094>`__: ENH: improve entropy calculation of chi distribution using asymptotic...
* `#18095 <https://github.com/scipy/scipy/pull/18095>`__: ENH: asymptotic expansion for gamma distribution entropy
* `#18096 <https://github.com/scipy/scipy/pull/18096>`__: MAINT: stats.johnsonsu: override _stats
* `#18098 <https://github.com/scipy/scipy/pull/18098>`__: ENH: increase available range of Gompertz entropy using scaled_exp1
* `#18101 <https://github.com/scipy/scipy/pull/18101>`__: DOC: adding references to the UnivariateSpline docstring #17828
* `#18102 <https://github.com/scipy/scipy/pull/18102>`__: ENH: stats.goodness_of_fit: add Filliben's test
* `#18104 <https://github.com/scipy/scipy/pull/18104>`__: BUG: enable matlab nested arrs
* `#18107 <https://github.com/scipy/scipy/pull/18107>`__: ENH: add Dunnett's test
* `#18112 <https://github.com/scipy/scipy/pull/18112>`__: FIX: reset semantic in \`QMCEngine.reset\`
* `#18120 <https://github.com/scipy/scipy/pull/18120>`__: Correct the comments about \` fmin_powell\` in \`scipy/optimize\`
* `#18122 <https://github.com/scipy/scipy/pull/18122>`__: ENH: Added asymptotic expansion for invgamma entropy (#18093)
* `#18127 <https://github.com/scipy/scipy/pull/18127>`__: MAINT: cleanup inconsistencies in _continous_dists
* `#18128 <https://github.com/scipy/scipy/pull/18128>`__: MAINT: add test against generic fit method for vonmises distribution
* `#18129 <https://github.com/scipy/scipy/pull/18129>`__: TST: stats.rv_continuous.fit: use \`nnlf\` instead of \`_reduce_func\`...
* `#18130 <https://github.com/scipy/scipy/pull/18130>`__: Some doc updates and small code tweaks.
* `#18131 <https://github.com/scipy/scipy/pull/18131>`__: ENH: Added asymptotic expansion for gengamma entropy
* `#18134 <https://github.com/scipy/scipy/pull/18134>`__: ENH: stats: Improve _cdf and implement _sf for genhyperbolic
* `#18135 <https://github.com/scipy/scipy/pull/18135>`__: Added asymptotic expansion for t entropy (#18093)
* `#18136 <https://github.com/scipy/scipy/pull/18136>`__: ENH: stats.ecdf: add \`confidence_interval\` methods
* `#18137 <https://github.com/scipy/scipy/pull/18137>`__: Bugfix for somersd where an integer overflow could occur
* `#18138 <https://github.com/scipy/scipy/pull/18138>`__: ENH: improve precision of genlogistic methods
* `#18144 <https://github.com/scipy/scipy/pull/18144>`__: DOC: Add doc examples for friedmanchisquare
* `#18145 <https://github.com/scipy/scipy/pull/18145>`__: BLD: emit a warning when building from source on 32-bit Windows
* `#18149 <https://github.com/scipy/scipy/pull/18149>`__: TST: fix issue with inaccurate \`cython_blas\` tests
* `#18150 <https://github.com/scipy/scipy/pull/18150>`__: ENH: add CI and str to Dunnett's test
* `#18152 <https://github.com/scipy/scipy/pull/18152>`__: ENH: stats.moment: enable non-central moment calculation
* `#18157 <https://github.com/scipy/scipy/pull/18157>`__: CI: fix pre-release job that is failing on Cython 3.0b1
* `#18158 <https://github.com/scipy/scipy/pull/18158>`__: DOC:stats: Fix levy and levy_l descriptions
* `#18160 <https://github.com/scipy/scipy/pull/18160>`__: BUG: Wrong status returned by _check_result. See #18106. optimize
* `#18162 <https://github.com/scipy/scipy/pull/18162>`__: ENH: Dweibull entropy
* `#18168 <https://github.com/scipy/scipy/pull/18168>`__: TST: spatial: skip failing test to make CI green again
* `#18172 <https://github.com/scipy/scipy/pull/18172>`__: MAINT: optimize.root_scalar: return gracefully when callable...
* `#18173 <https://github.com/scipy/scipy/pull/18173>`__: DOC: update links for ARPACK to point to ARPACK-NG
* `#18174 <https://github.com/scipy/scipy/pull/18174>`__: DOC: cite pip issue about multiple \`--config-settings\`
* `#18178 <https://github.com/scipy/scipy/pull/18178>`__: ENH: Added \`_sf\` method for anglit distribution (#17832)
* `#18181 <https://github.com/scipy/scipy/pull/18181>`__: DOC: wheel build infra updates
* `#18187 <https://github.com/scipy/scipy/pull/18187>`__: MAINT: stats.ecdf: store number at risk just before events
* `#18188 <https://github.com/scipy/scipy/pull/18188>`__: BUG: interpolate: add x-y length validation for \`make_smoothing_spline\`.
* `#18189 <https://github.com/scipy/scipy/pull/18189>`__: DOC: Fix for side bar rendering on top of text issue
* `#18190 <https://github.com/scipy/scipy/pull/18190>`__: ENH: fix vonmises fit for bad guess of location parameter
* `#18193 <https://github.com/scipy/scipy/pull/18193>`__: MAINT: stats.kendalltau: avoid overflow
* `#18195 <https://github.com/scipy/scipy/pull/18195>`__: MAINT: interpolate: remove duplicated FITPACK interface _fitpack._spl_.
* `#18196 <https://github.com/scipy/scipy/pull/18196>`__: ENH: add Log rank for survival analysis
* `#18199 <https://github.com/scipy/scipy/pull/18199>`__: BUG: throw ValueError for mismatched w dimensions and test for...
* `#18200 <https://github.com/scipy/scipy/pull/18200>`__: TST: stats: Move genexpon from xslow to slow fit test sets.
* `#18204 <https://github.com/scipy/scipy/pull/18204>`__: MAINT/TST: fix \`Slerp\` typing and better iv in \`Rotation\`
* `#18207 <https://github.com/scipy/scipy/pull/18207>`__: ENH: improve precision of folded normal distribution cdf
* `#18209 <https://github.com/scipy/scipy/pull/18209>`__: ENH: improve integrate.simpson for even number of points
* `#18210 <https://github.com/scipy/scipy/pull/18210>`__: ENH: stats.ttest_ind: add degrees of freedom and confidence interval
* `#18212 <https://github.com/scipy/scipy/pull/18212>`__: ENH: stats.ecdf: add \`evaluate\` and \`plot\` methods; restructure...
* `#18215 <https://github.com/scipy/scipy/pull/18215>`__: DOC: stats: describe attributes of \`DunnettResult\`
* `#18216 <https://github.com/scipy/scipy/pull/18216>`__: MAINT: replace use of make_dataclass with explicit dataclasses
* `#18217 <https://github.com/scipy/scipy/pull/18217>`__: MAINT: stats: consistently return NumPy numbers
* `#18221 <https://github.com/scipy/scipy/pull/18221>`__: DOC: add guidance on how to make a dataclass for result objects
* `#18222 <https://github.com/scipy/scipy/pull/18222>`__: MAINT: stats.TTestResult: fix NaN bug in ttest confidence intervals
* `#18225 <https://github.com/scipy/scipy/pull/18225>`__: ENH:MAINT:linalg det in Cython and with nDarray support
* `#18227 <https://github.com/scipy/scipy/pull/18227>`__: ENH: stats: resampling methods configuration classes and example...
* `#18228 <https://github.com/scipy/scipy/pull/18228>`__: ENH: stats.geometric.entropy: implement analytical formula
* `#18229 <https://github.com/scipy/scipy/pull/18229>`__: ENH: stats.bootstrap: add one-sided confidence intervals
* `#18230 <https://github.com/scipy/scipy/pull/18230>`__: BUG: nan segfault in KDTree, reject non-finite input
* `#18231 <https://github.com/scipy/scipy/pull/18231>`__: ENH: stats.monte_carlo_test: add support for multi-sample statistics
* `#18232 <https://github.com/scipy/scipy/pull/18232>`__: ENH: override dweibull distribution survival and inverse survival...
* `#18237 <https://github.com/scipy/scipy/pull/18237>`__: MAINT: update typing of Rotation
* `#18238 <https://github.com/scipy/scipy/pull/18238>`__: MAINT:optimize: shgo assorted fixes
* `#18240 <https://github.com/scipy/scipy/pull/18240>`__: fix typo
* `#18241 <https://github.com/scipy/scipy/pull/18241>`__: MAINT: remove Gitpod in favour of GitHub CodeSpaces
* `#18242 <https://github.com/scipy/scipy/pull/18242>`__: MAINT: Allow scipy to be compiled in cython3
* `#18243 <https://github.com/scipy/scipy/pull/18243>`__: TST: stats.dunnett: fix seed in test_shapes
* `#18245 <https://github.com/scipy/scipy/pull/18245>`__: DOC: remove content related to \`setup.py\` usage from the docs
* `#18246 <https://github.com/scipy/scipy/pull/18246>`__: ci: touch up wheel build action
* `#18247 <https://github.com/scipy/scipy/pull/18247>`__: BLD: Add const to Cython signatures for BLAS/LAPACK
* `#18248 <https://github.com/scipy/scipy/pull/18248>`__: BLD: implement version check for minimum Cython version
* `#18251 <https://github.com/scipy/scipy/pull/18251>`__: DOC: orthogonal_procrustes fix date of reference paper and DOI
* `#18257 <https://github.com/scipy/scipy/pull/18257>`__: BLD: fix missing build dependency on cython signature .txt files
* `#18258 <https://github.com/scipy/scipy/pull/18258>`__: DOC: fix link in release notes v1.7
* `#18261 <https://github.com/scipy/scipy/pull/18261>`__: Add axes support to uniform_filter, minimum_filter, maximum_filter
* `#18263 <https://github.com/scipy/scipy/pull/18263>`__: BUG: some tweaks to PROPACK f2py wrapper and build flags
* `#18264 <https://github.com/scipy/scipy/pull/18264>`__: MAINT: remove \`from numpy.math cimport\` usages, update \`npy_blas.h\`
* `#18266 <https://github.com/scipy/scipy/pull/18266>`__: MAINT: Explicitly mark \`cdef\` functions not raising exception...
* `#18269 <https://github.com/scipy/scipy/pull/18269>`__: ENH: stats: Implement _sf and _isf for exponweib.
* `#18270 <https://github.com/scipy/scipy/pull/18270>`__: CI: test meson-python from its main branch in one CI job
* `#18275 <https://github.com/scipy/scipy/pull/18275>`__: TST: stats: infrastructure for generation of distribution function...
* `#18276 <https://github.com/scipy/scipy/pull/18276>`__: MAINT: stats.betaprime: avoid spurious warnings in \`fit\`, \`stats\`
* `#18280 <https://github.com/scipy/scipy/pull/18280>`__: DOC: spatial.distance: update formula for {s,sq}euclidean
* `#18281 <https://github.com/scipy/scipy/pull/18281>`__: BLD: Enable incompatible pointer types warnings
* `#18284 <https://github.com/scipy/scipy/pull/18284>`__: DOC: improved gmres doc on preconditioning (scipy.sparse.linalg)
* `#18285 <https://github.com/scipy/scipy/pull/18285>`__: MAINT: Remove codecov
* `#18287 <https://github.com/scipy/scipy/pull/18287>`__: DOC: \`distance_transform_bf\` example
* `#18288 <https://github.com/scipy/scipy/pull/18288>`__: TST: stats.ortho_group: improve determinant distribution test
* `#18289 <https://github.com/scipy/scipy/pull/18289>`__: MAINT: mmread allow leading whitespace
* `#18290 <https://github.com/scipy/scipy/pull/18290>`__: DEP: stats.mode: raise with non-numeric input
* `#18291 <https://github.com/scipy/scipy/pull/18291>`__: TST: stats._axis_nan_policy: add test that decorated function...
* `#18292 <https://github.com/scipy/scipy/pull/18292>`__: CI: add CircleCI API token to fix html preview link
* `#18293 <https://github.com/scipy/scipy/pull/18293>`__: BUG: fix for incompatible pointer warning from stats._rcond #18282
* `#18294 <https://github.com/scipy/scipy/pull/18294>`__: CI: remove \`setup.py\` based jobs from GitHub Actions and run...
* `#18297 <https://github.com/scipy/scipy/pull/18297>`__: MAINT: linalg.solve_discrete_are: fix typo in error message
* `#18299 <https://github.com/scipy/scipy/pull/18299>`__: DOC: interpolate: add see also references for data on regular...
* `#18301 <https://github.com/scipy/scipy/pull/18301>`__: CI: remove \`runtests.py\` and related scripts/files
* `#18303 <https://github.com/scipy/scipy/pull/18303>`__: DOC: css adjustment in dark mode and hidden toctree in dev section
* `#18304 <https://github.com/scipy/scipy/pull/18304>`__: MAINT: update boost_math
* `#18305 <https://github.com/scipy/scipy/pull/18305>`__: ENH: ndimage: add axes argument to rank_filter, percentile_filter,...
* `#18307 <https://github.com/scipy/scipy/pull/18307>`__: DOC: add cdf under methods for multivariate t distribution
* `#18311 <https://github.com/scipy/scipy/pull/18311>`__: CI: move lint job from Azure to GHA
* `#18312 <https://github.com/scipy/scipy/pull/18312>`__: CI: move gcc-8 test to GHA
* `#18313 <https://github.com/scipy/scipy/pull/18313>`__: CI: remove asv from AzureCI
* `#18314 <https://github.com/scipy/scipy/pull/18314>`__: CI: remove scikit-umfpack/sparse from Azure testing
* `#18315 <https://github.com/scipy/scipy/pull/18315>`__: CI: remove coverage jobs
* `#18318 <https://github.com/scipy/scipy/pull/18318>`__: MAINT: Mark function pointer ctypedefs as noexcept
* `#18320 <https://github.com/scipy/scipy/pull/18320>`__: CI: migrate ref guide-check to CircleCI
* `#18321 <https://github.com/scipy/scipy/pull/18321>`__: Revert "ENH: stats.anderson_ksamp: add permutation version of...
* `#18323 <https://github.com/scipy/scipy/pull/18323>`__: ENH: increase available range of vonmises \`fit\`
* `#18324 <https://github.com/scipy/scipy/pull/18324>`__: ENH: add \`entropy\` method for multivariate t distribution
* `#18325 <https://github.com/scipy/scipy/pull/18325>`__: CI: move Azure cp39/full/win job to GHA
* `#18327 <https://github.com/scipy/scipy/pull/18327>`__: MAINT: optimize.milp: improve behavior for unexpected sparse...
* `#18328 <https://github.com/scipy/scipy/pull/18328>`__: MAINT: stats.shapiro: override p-value when len(x)==3
* `#18330 <https://github.com/scipy/scipy/pull/18330>`__: BLD: avoid build warnings on Windows, bump pybind11 and meson...
* `#18332 <https://github.com/scipy/scipy/pull/18332>`__: TST: fix minor tolerance issue for \`stats.multivariate_t\` test
* `#18333 <https://github.com/scipy/scipy/pull/18333>`__: CI: windows cp311 use-pythran=false full, sdist GHA
* `#18337 <https://github.com/scipy/scipy/pull/18337>`__: MAINT: update boost_math
* `#18339 <https://github.com/scipy/scipy/pull/18339>`__: TST: optimize: fix test_milp_timeout
* `#18340 <https://github.com/scipy/scipy/pull/18340>`__: DOC: interpolate: declare Rbf legacy
* `#18341 <https://github.com/scipy/scipy/pull/18341>`__: DEP: signal: deprecate using medfilt and order_filter with float128...
* `#18342 <https://github.com/scipy/scipy/pull/18342>`__: TST: stats.mstats.median_cihs: strengthen test
* `#18343 <https://github.com/scipy/scipy/pull/18343>`__: MAINT: use math.prod (python >= 3.8)
* `#18344 <https://github.com/scipy/scipy/pull/18344>`__: MAINT: Set cython compiler directive cpow to True
* `#18345 <https://github.com/scipy/scipy/pull/18345>`__: DEV: work around pathlib bug affecting dev.py for Python 3.9...
* `#18349 <https://github.com/scipy/scipy/pull/18349>`__: MAINT: stats.dgamma.entropy: avoid deprecated NumPy usage and...
* `#18350 <https://github.com/scipy/scipy/pull/18350>`__: TST: use np not math for functions to avoid conversion of ndim>0...
* `#18351 <https://github.com/scipy/scipy/pull/18351>`__: CI: remove Azure sdist job
* `#18352 <https://github.com/scipy/scipy/pull/18352>`__: MAINT: stats: more avoidance of deprecated NumPy usage
* `#18353 <https://github.com/scipy/scipy/pull/18353>`__: Migrate ruff.toml configuration to lint.toml
* `#18355 <https://github.com/scipy/scipy/pull/18355>`__: ENH: allow dividing LinearOperator by number
* `#18357 <https://github.com/scipy/scipy/pull/18357>`__: MAINT: clearer error in \`LinearOperator \* spmatrix\`
* `#18358 <https://github.com/scipy/scipy/pull/18358>`__: ENH:MAINT:linalg:lu Cythonized and ndarray support added
* `#18359 <https://github.com/scipy/scipy/pull/18359>`__: MAINT: Fix broken link in setup.py
* `#18360 <https://github.com/scipy/scipy/pull/18360>`__: DOC: improve neg. binomial function examples in \`special\`
* `#18362 <https://github.com/scipy/scipy/pull/18362>`__: MAINT: Add noexcept function declaration to \`_cythonized_array_utils.pxd\`
* `#18369 <https://github.com/scipy/scipy/pull/18369>`__: CI: bdist_wheel windows job Azure --> GHA
* `#18370 <https://github.com/scipy/scipy/pull/18370>`__: DOC: stats.chisquare: attribute is pvalue, not p
* `#18374 <https://github.com/scipy/scipy/pull/18374>`__: CI: pin to rtools40
* `#18378 <https://github.com/scipy/scipy/pull/18378>`__: DOC: add output_type to signature of cKDTree.query_pairs
* `#18379 <https://github.com/scipy/scipy/pull/18379>`__: TST/MAINT: remove vonmises fit correctnes test for extreme kappa...
* `#18380 <https://github.com/scipy/scipy/pull/18380>`__: MAINT: Limit fittable data for von mises fisher distribution...
* `#18382 <https://github.com/scipy/scipy/pull/18382>`__: TST: stats.cosine: modify test to silence failure
* `#18383 <https://github.com/scipy/scipy/pull/18383>`__: MAINT: add smoke testing of signal.detrend
* `#18384 <https://github.com/scipy/scipy/pull/18384>`__: DOC: improve vonmises documentation
* `#18387 <https://github.com/scipy/scipy/pull/18387>`__: DOC: interpolate: deduplicate docstrings in _fitpack_py and _fitpack_impl
* `#18392 <https://github.com/scipy/scipy/pull/18392>`__: BUG: optimize.differential_evolution: fix division by zero error
* `#18399 <https://github.com/scipy/scipy/pull/18399>`__: DOC: Replace "HACKING" with "hacking"
* `#18400 <https://github.com/scipy/scipy/pull/18400>`__: DOC: improve description of the method argument in mannwhitneyu
* `#18402 <https://github.com/scipy/scipy/pull/18402>`__: TST: fix failing signal.windows tests
* `#18405 <https://github.com/scipy/scipy/pull/18405>`__: Revert "BLD: Add const to Cython signatures for BLAS/LAPACK (#18247)"
* `#18410 <https://github.com/scipy/scipy/pull/18410>`__: TST: fix test failures in linprog unboundedness test
* `#18411 <https://github.com/scipy/scipy/pull/18411>`__: BLD: an Intel Fortran fix and MinGW-related cleanups
* `#18412 <https://github.com/scipy/scipy/pull/18412>`__: MAINT: signal: simplify shape manipulations in signal.detrend
* `#18413 <https://github.com/scipy/scipy/pull/18413>`__: MAINT: Harmonized documentation for Interpolator classes
* `#18414 <https://github.com/scipy/scipy/pull/18414>`__: CI: move last Azure job to GHA
* `#18418 <https://github.com/scipy/scipy/pull/18418>`__: Fix warning when \`nogil\` is placed before \`except\`
* `#18419 <https://github.com/scipy/scipy/pull/18419>`__: MAINT: interpolate: remove unused codes in \`_fitpackmodule.c\`.
* `#18421 <https://github.com/scipy/scipy/pull/18421>`__: BLD: more PROPACK fixes, removing timer code
* `#18422 <https://github.com/scipy/scipy/pull/18422>`__: MAINT: stats: genexpon is no longer too slow for test_rvs_broadcast.
* `#18426 <https://github.com/scipy/scipy/pull/18426>`__: BLD: fix two \`-Duse-g77-abi\` regressions and a PROPACK bug
* `#18427 <https://github.com/scipy/scipy/pull/18427>`__: ENH: prevent unnecessary computation in \`scipy.stats.rankdata\`
* `#18429 <https://github.com/scipy/scipy/pull/18429>`__: DOC: rewrite all build docs and restructure build/contributor...
* `#18430 <https://github.com/scipy/scipy/pull/18430>`__: MAINT: stats.mode: improve \`nan_policy\` behavior
* `#18433 <https://github.com/scipy/scipy/pull/18433>`__: ENH: improve t distribution logpdf and pdf for large degrees...
* `#18438 <https://github.com/scipy/scipy/pull/18438>`__: BLD: DOC: fix Sphinx doc build caching behavior for \`.dev\`...
* `#18439 <https://github.com/scipy/scipy/pull/18439>`__: BLD: detect \`xsimd\` if it's installed and add to pythran dependency
* `#18441 <https://github.com/scipy/scipy/pull/18441>`__: ENH:stats: add sf method for betaprime
* `#18442 <https://github.com/scipy/scipy/pull/18442>`__: TST: fix precision of several linalg/sparse.linalg tests
* `#18444 <https://github.com/scipy/scipy/pull/18444>`__: DOC: clarify Sobel transform
* `#18446 <https://github.com/scipy/scipy/pull/18446>`__: MAINT: fix Deb03 GO benchmark
* `#18447 <https://github.com/scipy/scipy/pull/18447>`__: DOC: remove references to Azure
* `#18449 <https://github.com/scipy/scipy/pull/18449>`__: ENH: increase truncated exponential distribution sf/isf precision
* `#18451 <https://github.com/scipy/scipy/pull/18451>`__: DEV: use number of physical cores in \`dev.py build\` by default
* `#18454 <https://github.com/scipy/scipy/pull/18454>`__: DOC: add \`distance_transform_cdt\` example
* `#18455 <https://github.com/scipy/scipy/pull/18455>`__: MAINT: simplifiy detrend
* `#18458 <https://github.com/scipy/scipy/pull/18458>`__: DOC: odr: clarify \`cov_beta\` is not scaled by the residual...
* `#18459 <https://github.com/scipy/scipy/pull/18459>`__: DOC: optimize: add use of functools.partial to tutorial
* `#18460 <https://github.com/scipy/scipy/pull/18460>`__: DOC: examples for \`ndimage.generic_filter\`
* `#18461 <https://github.com/scipy/scipy/pull/18461>`__: TST: stats: ReferenceDistribution: use complementary methods...
* `#18462 <https://github.com/scipy/scipy/pull/18462>`__: MAINT: Clean up scipy/sparse/linalg/_isolve/tests/test_iterative.py
* `#18463 <https://github.com/scipy/scipy/pull/18463>`__: MAINT: parametrize scipy/sparse/linalg/_isolve/tests/test_iterative.py
* `#18466 <https://github.com/scipy/scipy/pull/18466>`__: DOC: fix issues in \`svds\` docstring examples that were failing...
* `#18468 <https://github.com/scipy/scipy/pull/18468>`__: BLD: enforce utf-8 in tools/cythonize.py, and some cleanups
* `#18472 <https://github.com/scipy/scipy/pull/18472>`__: MAINT: remove lsim2/impulse2/step2 docstring examples
* `#18475 <https://github.com/scipy/scipy/pull/18475>`__: DOC: remove warnings in doc build
* `#18476 <https://github.com/scipy/scipy/pull/18476>`__: TST: stats/optimize: filter warnings in tests
* `#18482 <https://github.com/scipy/scipy/pull/18482>`__: MAINT: ensure Nelder-Mead respects floating point type
* `#18486 <https://github.com/scipy/scipy/pull/18486>`__: DOC: remove already-resolved deprecation warning filter
* `#18489 <https://github.com/scipy/scipy/pull/18489>`__: DEP: signal: deprecate importing window functions from signal...
* `#18493 <https://github.com/scipy/scipy/pull/18493>`__: BUG: stats: Fix the variable that is checked to skip a test.
* `#18500 <https://github.com/scipy/scipy/pull/18500>`__: MAINT: tweak code comment for list of private-but-present modules
* `#18501 <https://github.com/scipy/scipy/pull/18501>`__: TST: interpolate: add a regression test for bisplev integer overflow
* `#18502 <https://github.com/scipy/scipy/pull/18502>`__: BUG: guard against non-finite kd-tree queries
* `#18503 <https://github.com/scipy/scipy/pull/18503>`__: Fix PPoly readonly issue for c parameter
* `#18504 <https://github.com/scipy/scipy/pull/18504>`__: MAINT: upload nighlighties to new location
* `#18505 <https://github.com/scipy/scipy/pull/18505>`__: MAINT: sparse: Generalize isshape to (optionally) handle non-2d...
* `#18507 <https://github.com/scipy/scipy/pull/18507>`__: Clean up sparse array API
* `#18508 <https://github.com/scipy/scipy/pull/18508>`__: ENH: Ensure that the result of divide(sparse, dense) is sparse
* `#18509 <https://github.com/scipy/scipy/pull/18509>`__: Remove indices downcasting for sparse arrays
* `#18510 <https://github.com/scipy/scipy/pull/18510>`__: TST: Add regression tests for sparse creation functions.
* `#18513 <https://github.com/scipy/scipy/pull/18513>`__: MAINT: sparse: cosmetic updates + typing for sputils
* `#18516 <https://github.com/scipy/scipy/pull/18516>`__: DOC: add user guide page introing new sparse arrays
* `#18522 <https://github.com/scipy/scipy/pull/18522>`__: Pin prerelease pipeline with Cython>=3.0.0b3
* `#18523 <https://github.com/scipy/scipy/pull/18523>`__: TST: piecemeal updates to \`test_base.py\` for sparray conversion
* `#18526 <https://github.com/scipy/scipy/pull/18526>`__: DOC: Fix broken reference to count_nonzero in See Also.
* `#18527 <https://github.com/scipy/scipy/pull/18527>`__: try stable sort in mst tree ordering
* `#18528 <https://github.com/scipy/scipy/pull/18528>`__: ENH: Update isspmatrix behavior
* `#18531 <https://github.com/scipy/scipy/pull/18531>`__: Class names to enable isinstance
* `#18532 <https://github.com/scipy/scipy/pull/18532>`__: Fix format property in _csr.py
* `#18536 <https://github.com/scipy/scipy/pull/18536>`__: Add deprecation notices to sparse array docs
* `#18538 <https://github.com/scipy/scipy/pull/18538>`__: ENH: sparse: Add _array version of \`diags\` creation functions.
* `#18539 <https://github.com/scipy/scipy/pull/18539>`__: DOC: sparse: Document sparse canonical formats
* `#18540 <https://github.com/scipy/scipy/pull/18540>`__: MAINT: sparse: Deprecate multi-Ellipsis indexing
* `#18542 <https://github.com/scipy/scipy/pull/18542>`__: ENH: sparse: add nanmin/nanmax (followup on gh-8902)
* `#18543 <https://github.com/scipy/scipy/pull/18543>`__: MAINT: optimize.root_scalar: ensure that root is a scalar
* `#18545 <https://github.com/scipy/scipy/pull/18545>`__: TST: speed up \`test_import_cycles\`
* `#18549 <https://github.com/scipy/scipy/pull/18549>`__: TST: optimize: filter RuntimeWarning that does not indicate test...
* `#18550 <https://github.com/scipy/scipy/pull/18550>`__: DOC: optimize.OptimizeResult: note that not all listed attributes...
* `#18551 <https://github.com/scipy/scipy/pull/18551>`__: Replace sparse __getattr__ with properties
* `#18553 <https://github.com/scipy/scipy/pull/18553>`__: BENCH: sparse: Add a benchmark for sparse matrix power
* `#18554 <https://github.com/scipy/scipy/pull/18554>`__: BUG: sparse: Fix DIA.tocoo canonical format setting
* `#18556 <https://github.com/scipy/scipy/pull/18556>`__: MAINT: io: replace isspmatrix with issparse in mmio module
* `#18560 <https://github.com/scipy/scipy/pull/18560>`__: MAINT: integrate: revert\`full_output\` deprecation / result...
* `#18562 <https://github.com/scipy/scipy/pull/18562>`__: fix doc strings for csr_array and friends
* `#18563 <https://github.com/scipy/scipy/pull/18563>`__: DOC: SciPy 1.11.0 release notes
* `#18591 <https://github.com/scipy/scipy/pull/18591>`__: MAINT: version bounds for 1.11.0rc1
* `#18596 <https://github.com/scipy/scipy/pull/18596>`__: DOC: Fix sidebar for API reference pages
* `#18598 <https://github.com/scipy/scipy/pull/18598>`__: CI: fix wheel upload to anaconda [wheel build]
* `#18599 <https://github.com/scipy/scipy/pull/18599>`__: Revert "ENH: sparse: Add _array version of \`diags\` creation...
* `#18608 <https://github.com/scipy/scipy/pull/18608>`__: Fix typo of module name in deprecation warning
* `#18629 <https://github.com/scipy/scipy/pull/18629>`__: Mark \`void\` functions as \`noexcept\` in _rotation.pyx
* `#18630 <https://github.com/scipy/scipy/pull/18630>`__: MAINT: stats: remove long double support for all boost ufuncs
* `#18636 <https://github.com/scipy/scipy/pull/18636>`__: MAINT: stats.truncnorm/stats.betaprime: fix _munp for higher...
* `#18657 <https://github.com/scipy/scipy/pull/18657>`__: MAINT: fix 'no such option' error in build_scipy CI
* `#18658 <https://github.com/scipy/scipy/pull/18658>`__: TST: fix two test failures that showed up on conda-forge
* `#18659 <https://github.com/scipy/scipy/pull/18659>`__: DOC: \`scipy._sensitivity_analysis\`: correct statement about...
* `#18671 <https://github.com/scipy/scipy/pull/18671>`__: MAINT: backports for 1.11.0rc2
* `#18672 <https://github.com/scipy/scipy/pull/18672>`__: BUG: small shim for release process
* `#18676 <https://github.com/scipy/scipy/pull/18676>`__: BUG: signal: fix detrend with array-like bp
* `#18697 <https://github.com/scipy/scipy/pull/18697>`__: MAINT: NumPy 1.25.0 shims for arm64
* `#18698 <https://github.com/scipy/scipy/pull/18698>`__: DEP: interpolate: delay interp2d deprecation and update link
* `#18724 <https://github.com/scipy/scipy/pull/18724>`__: MAINT, REL: prepare for SciPy 1.11.0 "final"
* `#18737 <https://github.com/scipy/scipy/pull/18737>`__: TST: flaky TestSOSFreqz::test_fs_param
* `#18738 <https://github.com/scipy/scipy/pull/18738>`__: TST: flaky \`test_complex_iir_dlti\`
