
# ===== SOURCE: https://raw.githubusercontent.com/networkx/networkx/main/doc/release/release_2.4.rst =====

NetworkX 2.4
============

Release date: 16 October 2019

Supports Python 3.5, 3.6, 3.7, and 3.8.
This is the last release to support Python 3.5.

NetworkX is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex networks.

For more information, please visit our `website <https://networkx.org/>`_
and our `gallery of examples
<https://networkx.org/documentation/latest/auto_examples/index.html>`_.
Please send comments and questions to the `networkx-discuss mailing list
<http://groups.google.com/group/networkx-discuss>`_.

Highlights
----------

This release is the result of 6 months of work with over 200 commits by
67 contributors. Highlights include:

- Remove deprecated code from 1.x
- Support for Python 3.8
- Switched to pytest for testing
- Last release to support Python 3.5

New Functions:

- barycenter functions
- Bethe Hessian matrix function
- Eulerian Path methods
- group centrality measures
- subgraph monomorphisms
- k-truss algorithms
- onion decomposition
- resistance distance
- asteroidal triples
- non-randomness measures
- linear prufing
- minimum weight bipartite matching
- Incremental closeness centrality
- ISMAGS subgraph isomorphism algorithm
- create chordal graph of a graph

New generators

- Binomial tree generator
- Directed joint degree generator
- Random internet AS graph generator

New for Layouts

- spiral node layout routine
- support for 3d layouts


Improvements
------------
- allow average shortest path to use Floyd-Warshall method
- improve read/write of GML, GEXF, GraphML
- allow string or json object as input to jit_graph
- attempt to allow numpy.array input in place of lists in more places
- faster strongly connected components
- faster Floyd-Warshall Optimization
- faster global efficiency
- faster transitive closure
- fix unionfind; betweenness_subset; lexico-topo-sort; A*;
  inverse_line_graph; async label propagation; edgelist reading;
  Gomory-Hu flow method; label_propagation; partial_duplication;
  shell_layout with 1 node in shell; from_pandas_edgelist
- Documentation improvement and fixes


API Changes
-----------

A utility function is_list_of_ints became is_bunch_of_ints
and now tests int(item)==item instead of isinstance(_, int)
This allows e.g. floats whose values are integer.

Added utility make_list_of_ints to convert containers of
integer values to lists of integers


Deprecations
------------

Removed functions (marked as deprecated in NetworkX 2.1):

- attracting_component_subgraphs
- connected_component_subgraphs
- weakly_connected_component_subgraphs
- strongly_connected_component_subgraphs
- biconnected_component_subgraphs
- See docs for component functions for how to get subgraphs.

Graph Object methods removed (marked as deprecated 2.1)

- G.add_path
- G.add_cycle
- G.add_star
- G.nodes_with_selfloops
- G.number_of_selfloops
- G.selfloop_edges
- These are now NetworkX functions, e.g. nx.add_star(G, 5)
- G.node   --> use G.nodes
- G.fresh_copy   --> use G.__class__

Remove old names for graphview functions.

- ReverseView
- SubGraph
- SubMultiGraph
- SubMultiDiGraph
- SubDiGraph
- GraphView
- DiGraphView
- MultiGraphView
- MultiDiGraphView
- MultiReverseView
- Use reverse_view, subgraph_view and generic_graph_view.

Merged PRs
----------

A total of 205 changes have been committed.

- Bump release version
- algorithms/traversal/edgebfs name fix (#3397)
- Add see also links (#3403)
- Add the reference for the Harary graph generators (#3407)
- typo: swap source and target (#3413)
- Fix spring_layout bug with fixed nodes (#3415)
- Move LFR_benchmark to generators (#3411)
- Add barycenter algorithm (#2939)
- Add bethe hessian matrix (#3401)
- Binomial trees generator (#3409)
- Fix edge_color inconsistency with node_color and description. (#3395)
- Adding module for group centrality measures (#3421)
- Improve edgelist See Also (#3423)
- Typo fix (#3424)
- Add doc warning about self-loops for adamic_adar_index (#3427)
- Fix UnionFind set extraction (#3224)
- add required argument to `write_graphml` example (#3429)
- Fix centrality betweenness subset (#3425)
- Add two versions of Simrank similarity (#3222)
- Fixed typo
- Merge pull request #3436 from nandahkrishna/fix-typo-betweenness-centrality-subset-test
- Reorder and complete doc (#3438)
- added topo_order parameter to functions that rely on topological_sort (#3447)
- Implemented subgraph monomorphism (#3435)
- Set seed in random_degree_sequence_graph docstring test (#3451)
- Replace cb.iterable with np.iterable (#3458)
- don't remove ticks of other pyplot axes (#3476)
- Fix typo in "G>raph Modelling Language" (#3468)
- Naive k-truss algorithm implementation. (#3462)
- Adding onion decomposition (#3461)
- New Feature - Resistance Distance (#3385)
- No multigraphs for betweenness (#3454)
- Wheels are python 3 only
- Fix deprecation warning with Python 3.7 (#3487)
- Fix dfs_preorder_nodes docstring saying "edges" instead of "nodes" (#3484)
- Added group closeness and group degree centralities (#3437)
- Fixed incorrect docs (#3495)
- Fixes Issue #3493 - Bug in lexicographical_topological_sort() (#3494)
- AT-free graph recognition (#3377)
- Update introduction.rst (#3504)
- Full join operation and cograph generator (#3503)
- Optimize the strongly connected components algorithm. (#3516)
- Adding non-randomness measures for graphs (#3515)
- Added safeguards (input graph G) for non-randomness measures  (#3526)
- Optimize the strongly connected components algorithm - Take 2 (#3519)
- Small fix for bug found @ issue #3524 (#3529)
- Restore checking PyPy3 (#3514)
- Linear prufer coding (#3535)
- Fix inverse_line_graph. (#3507)
- Fix A* returning wrong solution (#3508)
- Implement minimum weight full matching of bipartite graphs (#3527)
- Get chordal graph for #1054 (#3353)
- Faster transitive closure computation for DAGs (#3445)
- Write mixed-type attributes correctly in write_graphml_lxml (#3536)
- Fixes some edge cases for inverse_line_graph(). (#3538)
- explicitly stated i.j convention in to_numpy_array
- Incremental Closeness Centrality (undirected, unweighted graphs) (#3444)
- Implement ISMAGS subgraph isomorphism algorithm (#3312)
- Fixes bug in networkx.algorithms.community.label_propagation.asyn_lpa_communities (#3545)
- When exporting to GML, write non 32-bit numbers as strings. (#3540)
- Try to bug Fix #3552 (#3554)
- add Directed Joint Degree Graph generator (#3551)
- typo (#3557)
- Fix a few documentation issues for the bipartite algorithm reference (#3555)
- i,j convention in adj mat i/o in relevant funcs
- Merge pull request #3542 from malch2/doc/update
- Add 3.8-dev to travis
- Fix dict iteration for Py3.8
- Ignore other failures for now
- Fix a typo in docstring for get_edge_data (#3564)
- Fix wrong title (#3566)
- Fix typo in docstring (#3568)
- Fix and Improve docstrings in graph.py (#3569)
- Improved graph class selection table (#3570)
- Add spiral layout for graph drawing (#3534)
- #3575 return coordinates of 3d layouts (#3576)
- Handle k==n within the Watts-Strogatz graph generator (#3579)
- Floyd-Warshall Optimization (#3400)
- Use Sphinx 2.2
- Add missing link to asteroidal docs
- Fix Sphinx warnings
- Fix Sphinx latexpdf build
- Updated Contributor list (#3592)
- Prim from list to set (#3512)
- Fix issue 3491 (#3588)
- Make Travis fail on Python 3.8 failures
- Fix test_gexf to handle default serialisation order of the XML attributes
- Remove future imports needed by Py2
- add internet_as_graph generator (#3574)
- remove cyclical references from OutEdgeDataView (#3598)
- Add minimum source and target margin to draw_networkx_edges. (#3390)
- fix to_directed function (#3599)
- Fixes #3573:GEXF output problem (#3606)
- Global efficiency attempt to speed up (#3604)
- Bugfix: Added flexibility in reading values for label and id (#3603)
- Add method floyd-warshall to average_shortest_path_length (#3267)
- Replaced is with == and minor pycodestyle fixes (#3608)
- Fix many documentation based Issues (#3609)
- Resolve many documentation issues (#3611)
- Fixes #3187  transitive_closure now returns self-loops when cycles present (#3613)
- Add support for initializing pagerank_scipy (#3183)
- Add last 7 lines of Gomory-hu algorithm Fixes #3293 (#3614)
- Implemented Euler Path functions (#3399)
- Fix the direction of edges in label_propagation.py (#3619)
- Removed unused import of random module (#3620)
- Fix operation order in partial_duplication_graph (#3626)
- Keep shells with 1 node away from origin in shell_layout (#3629)
- Allow jit_graph to read json string or json object (#3628)
- Fix typo within incode documentation (#3621)
- pycodestyle and update docs for greedy_coloring.py+tests (#3631)
- Add version badges
- Load long description from README
- Add missing code block (#3630)
- Change is_list_of_ints to make_list_of_ints (#3617)
- Handle edgeattr in from_pandas_edgelist when no columns match request (#3634)
- Make draft of release notes for v2.4
- Shift notes from dev to v2.4 filename.
- Use recent pypy
- Test Py 3.8 on macos
- add check of attr type before converting inf/nan in GEXF (#3636)
- Fix sphinx errors And add links to single_source_dijkstra in docs for dijkstra_path/length (#3638)
- Document subgraph_view (#3627)
- First round of pytest fixes
- Use class methods for class setup/teardown
- Have CIs use pytest
- Use class methods for class setup/teardown, cont.
- Do less testing (until we get it working)
- replace idiom from networkx import * in test files
- Fix assert funcs override
- Fix static methods in link_prediction
- Partially fix v2userfunc tests
- Fix graph/digraph tests
- Fix multigraph checks
- Fix multidigraph checks
- Fix test_function checks
- Fix distance_measures tests
- Fix decorators tests
- Fix some raises in test_mst
- Fix clique tests
- Fix yaml tests
- Fix tests in reportviews
- Fix vf2 tests
- Fix mst tests
- Fix gdal tests
- Convert nose.tools.assert_* functions into asserts
- Remove unused imports
- Fix some warnings
- Update testing instructions
- Re-enable all test platforms
- Fix some __init__ warnings
- replace nose yield tests in test_coloring.py
- Add testing, coverage, and dev environment info
- Try pytestimportorskip
- Another pair of variations on pytest.importorskip
- fix typo and try again
- Remove deprecated weakly_connected_component_subgraphs
- replace assert_almost_equal and raises in algorithms/tests
- set places=0 on tests that use old almost_equal
- Update nx.test()
- Have pytest run doctests / not sphinx
- Revert "Remove deprecated weakly_connected_component_subgraphs"
- remove warnings for using deprecated function
- Remove deprecated functions and methods. add to release notes.
- Fix subgraph_view testing
- remove tests of deprecated views and fix use of deprecated G.node
- tracking down use of deprecated functions
- Fix deprecated use of add_path/star/cycle
- reduce warnings for deprecated functions
- skirt issues with raises in test_harmonic
- reduce the number of warnings by removing deprecated functions
- convert_matrix demo of one way to get doctests to work
- Remove deprecated from examples
- Changes to convert_matrix and others that depend on np.matrix
- clean up doctest deprecated code
- More doctest corrections
- Fix examples
- Remove nose from generators
- Remove nose from utils
- Remove nose from classes
- Replace nose.assert_raises with pytest.raises
- Replace nose.raises with pytest.raises context manager
- Replace `eq_`, `ok_` with assert
- Use pytest for doctest
- Highlight switch to pytest in release notes
- Remove `from nose.tools import *`
- Remove nose.tools.SkipTest
- Finalize transition to pytest
- Merge pull request #3639 from stefanv/pytest-port
- Test Python 3.8 with AppVeyor
- Merge pull request #3648 from jarrodmillman/windows-py3.8
- Remove deprecated weakly_connected_component_subgraphs
- Update release notes
- Update README
- Announce Python 3.8 support
- Designate 2.4rc1 release
- Bump release version
- Remove remaining SkipTests
- fix documentation notes (#3644) (#3645)
- Test Py 3.8.0 on AppVeyor
- Speed up AppVeyor
- Cleanup travis config
- Improve CI caching
- Update Py 3.8 on travis
- Merge pull request #3652 from jarrodmillman/speedup-appveyor
- Finalize release notes

It contained the following 5 merges:

- Fixed typo in betweenness centrality subset test (#3436)
- explicitly stated i.j convention in to_numpy_array (#3542)
- pytest port (#3639)
- Test Python 3.8 with AppVeyor (#3648)
- Cleanup and speedup CI (#3652)

Contributors
------------

- Rajendra Adhikari
- Antoine Allard
- Antoine
- Salim BELHADDAD
- Luca Baldesi
- Tamás Bitai
- Tobias Blass
- Malayaja Chutani
- Peter Cock
- Almog Cohen
- Diogo Cruz
- Martin Darmüntzel
- Elan Ernest
- Jacob Jona Fahlenkamp
- Michael Fedell
- Andy Garfield
- Ramiro Gómez
- Haakon
- Alex Henrie
- Steffen Hirschmann
- Martin James McHugh III
- Jacob
- Søren Fuglede Jørgensen
- Omer Katz
- Julien Klaus
- Matej Klemen
- Nanda H Krishna
- Peter C Kroon
- Anthony Labarre
- Anton Lodder
- MCer4294967296
- Eric Ma
- Fil Menczer
- Erwan Le Merrer
- Alexander Metz
- Jarrod Millman
- Subhendu Ranajn Mishra
- Jamie Morton
- James Myatt
- Kevin Newman
- Aaron Opfer
- Aditya Pal
- Pascal-Ortiz
- Peter
- Jose Pinilla
- Alexios Polyzos
- Michael Recachinas
- Efraim Rodrigues
- Adam Rosenthal
- Dan Schult
- William Schwartz
- Weisheng Si
- Kanishk Tantia
- Ivan Tham
- George Valkanas
- Stefan van der Walt
- Hsi-Hsuan Wu
- Haochen Wu
- Xiangyu Xu
- Jean-Gabriel Young
- bkief
- daniel-karl
- michelb7398
- mikedeltalima
- nandahkrishna
- skhiuk
- tbalint

# ===== SOURCE: https://raw.githubusercontent.com/networkx/networkx/main/doc/release/release_2.5.rst =====

NetworkX 2.5
============

Release date: 22 August 2020

Supports Python 3.6, 3.7, and 3.8.

NetworkX is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex networks.

For more information, please visit our `website <https://networkx.org/>`_
and our `gallery of examples
<https://networkx.org/documentation/latest/auto_examples/index.html>`_.
Please send comments and questions to the `networkx-discuss mailing list
<http://groups.google.com/group/networkx-discuss>`_.

Highlights
----------

This release is the result of 10 months of work with over 200 commits by
92 contributors. Highlights include:

- Dropped support for Python 3.5.
- add Pathlib support to work with files.
- improve performance.
- Updated docs and tests.
- Removed code designed to work with Python 2.

New Functions:

- lukes_partitioning
- triadic analysis functions
- functions for trophic levels analysis
- d_separated
- is_regular and other regular graph measures
- graph_hash using Weisfeiler Lehman methods
- common_neighbor_centrality (CCPA link prediction)
- max_weight_clique
- path_weight and is_path
- rescale_layout_dict
- junction_tree

New generators:

- paley_graph
- interval_graph

New layouts:

- multipartite_layout


Improvements
------------

- Add governance documents, developer guide and community structures
- Implement explicit deprecation policy.
- Initiate an NX Enhancement Proposal (NXEP) system
- optimize single_source_shortest_path
- improved consistent "weight" specification in shortest_path routines
- Reduce numpy.matrix usage which is discouraged by numpy.
- improved line color
- better search engine treatment of docs
- lattice and grid_graph and grid_2d_graph can use dim=tuple
- fix initializer of kamada_kawai_layout algorithm
- moral and threshold functions now included in namespace and docs
- scale arrows better when drawing
- more uniform creation of random lobster graphs
- allow editing graph during iteration over connected_components
- better column handling in conversion of pandas DataFrame
- allow simrank_similarity with directed graph input
- ensure VoteRank ability is nonnegative
- speedup kernighan_lin_bisection
- speedup negative weight cycle detection
- tree_isomorphism
- rooted_tree_isomorphism
- Gexf edge attribute "label" is available


API Changes
-----------

- enabled "copy" flag parameter in `contracted_nodes`
- allow partially periodic lattices
- return value for minimum_st_node_cut now always a set
- removed unused "has_numpy" argument from create_py_random_state
- fixed return values when drawing empty nodes and edges
- allow sets and frozensets of edges as input to nx.Graph()
- "weight" can be function for astar, directional_dijkstra, all_shortest_path
- allow named key ids for GraphML edge writing
- all keywords are now checked for validity in nx.draw and friends
- EdgeDataView "in" operator checks if nodes are "in nbunch"
- remove completeness condition from minimum weight full matching
- option to sort neighbors in bfs traversal
- draw_networkx accepts numpy array for edgelist
- relabel_nodes with 2 nodes mapped to same node can now create multiedge
- steiner_tree works with MultiGraph
- Add `show` kwarg to view_pygraphviz (#4155)
- Prepare for turning chordal_graph_cliques into a generator (#4162)
- GraphML reader keyword force_multigraph creates MultiGraph even w/o multiedges


Deprecations
------------

- [`#3680 <https://github.com/networkx/networkx/pull/3680>`_]
  Deprecate `make_str(x)` for `str(x)`.
  Deprecate `is_string_like(obj)` for `isinstance(obj, str)`.

- [`#3725 <https://github.com/networkx/networkx/pull/3725>`_]
  Deprecate `literal_stringizer` and `literal_destringizer`.

- [`#3983 <https://github.com/networkx/networkx/pull/3983>`_]
  Deprecate `reversed` context manager.

- [`#4155 <https://github.com/networkx/networkx/pull/4155>`_]
  Deprecate `display_pygraphviz`.

- [`#4162 <https://github.com/networkx/networkx/pull/4162>`_]
  Deprecate `chordal_graph_cliques` returning a set.

- [`#4161 <https://github.com/networkx/networkx/pull/4161>`_]
  Deprecate `betweenness_centrality_source`.

- [`#4161 <https://github.com/networkx/networkx/pull/4161>`_]
  Deprecate `edge_betweenness`.

- [`#4161 <https://github.com/networkx/networkx/pull/4161>`_]
  Rename `_naive_greedy_modularity_communities` as `naive_greedy_modularity_communities`.

Merged PRs
----------

A total of 256 changes have been committed.

- Bump release version
- Update release process
- Drop support for Python 3.5
- fix typo docs
- Remove old Python 2 code
- Enable more doctests
- Fix pydot tests
- Unclear how to test the test helper function
- Pathlib introduced in Py 3.4
- Remove code using sys.version_info to detect Python 2
- Use yield from
- PEP8 fixes to tests
- Remove unused imports
- Use pytest.importorskip
- PEP8 fixes
- Remove unused imports
- Add pep8_speaks conf
- Use itertools accumulate
- Fixes issue 3610: Bug in version attribute of gexf.py
- Ignore W503
- Run doctest without optional dependencies
- Skip doctests when missing dependencies
- Remove sed imports
- Enable tests (#3678)
- `contracted_nodes` copy flag added (#3646)
- Deprecate make_str
- Deprecate is_string_like
- Fix PEP8 issues
- Enable ThinGraph tests (#3681)
- Optimize _single_shortest_path_length (#3647)
- Fix issue 3431: Return error in case of bad input to make_small_graph (#3676)
- avoid duplicate tests due to imports (#3684)
- Fix typo: Laplacian -> Laplacian (#3689)
- Add tests
- Lukes algorithm implementation (#3666)
- Remove shim that worked around using starmap
- Add back to gallery
- Add colormap and color limits to LineCollection (#3698)
- Fix matplotlib deprecation (#3697)
- Adapt SciPy CoC
- Update docs to be more accurate about speed of G.neighbors (#3699)
- Use canonical url to help search engines
- Remove duplicate license parameter (#3710)
- Fix documentation issues for exceptions in a few places
- Fix more documentation issues with exceptions
- Remove old Python 2 code
- Remove boiler plate from top of modules
- Remove superfluous encoding information
- Update examples
- Simplify package docstring
- Remove shebang from non-executables
- Add contributors
- K-truss is defined for edges being in (k-2) triangles and not for k triangles (#3713)
- Enable optional tests on Python 3.8
- Fix test_numpy_type to pass under Python 3.8
- Add links to data files
- Deprecate Python 2/3 compatibility code
- Update style
- Update style
- Separate easy and hard to install optional requirements
- Install optional dependencies by default
- Refactor tests
- Sample code for subgraph copy: add parenthesis to is_multigraph (#3734)
- Fixed typo (#3735)
- fix citation links (#3741)
- remove f strings from setup.py for clear error message < py3.6 (#3738)
- 3511 gml list support (#3649)
- added linestyle as argument (#3747)
- Link to files needed for example (#3752)
- fixed a typo
- Merge pull request #3759 from yohm/patch-1
- remove unused variable so grid_graph supports dim=tuple (#3760)
- Sudoku generator issue 3756 (#3757)
- Fix scaling of single node shells in shall_layout (#3764)
- Adding triadic analysis functions (#3742)
- Improve test coverage
- Update contribs script
- Convert %-format to fstring
- Upgrade to Py36 syntax
- Upgrade to Py36 syntax
- Update string format
- Fix scipy deprecation warnings
- Update year
- Silence known warnings (#3770)
- Fix docstring for asyn_fluidc (#3779)
- Fix #3703 (#3784)
- fix initializer for kamada_kawai_layout (networkx #3658) (#3782)
- Minor comments issue (#3787)
- Adding moral and threshold packages to main namespace (#3788)
- Add weight functions to bidirectional_dijkstra and astar (#3799)
- Shrink the source side of an arrow properly when drawing a directed edge. #3805 (#3806)
- option for partially-periodic lattices (networkx #3586) (#3807)
- Prevent KeyError on subgraph_is_monomorphic (#3798)
- Trophic Levels #3736 (#3804)
- UnionFind's union doesn't accurately track set sizes (#3810)
- Remove whitespace (#3816)
- reconsider the lobster generator (#3822)
- Fix typo (#3838)
- fix typo slightly confusing the meaning (#3840)
- Added fix for issue #3846 (#3848)
- Remove unused variable has_numpy from create_py_random_state (#3852)
- Fix return values when drawing empty nodes and edges  #3833 (#3854)
- Make connected_components safe to component set mutation (#3859)
- Fix example in docstring (#3866)
- Update README.rst website link to https (#3888)
- typo (#3894)
- Made CONTRIBUTING.rst more clearer (#3895)
- Fixing docs for nx.info(), along with necessary tests (#3893)
- added default arg for json dumps for jit_data func (#3891)
- Fixed nx.Digraph to nx.DiGraph (#3909)
- Use Sphinx 3.0.1
- Fix Sphinx deprecation
- Add logo to docs
- allow set of edge nodes (#3907)
- Add extra information when casting 'id' to int() fails. (Resolves #3910) (#3916)
- add paley graph (#3900)
- add paley graph to doc (#3927)
- Update astar.py (#3947)
- use keywords for positional arguments (#3952)
- fix documentation (#3959)
- Add option for named key ids to GraphML writing. (#3960)
- fix documentation (#3958)
- Correct handling of zero-weight edges in all_shortest_paths (#3783)
- Fix documentation typo (#3965)
- Fix: documentation of simrank_similarity_numpy (#3954)
- Fix for #3930 (source & target columns not overwritten when converting to pd.DataFrame) (#3935)
- Add weight function for shortest simple paths for #3948 (#3949)
- Fix definition of communicability (#3973)
- Fix simrank_similarity with directed graph input (#3961)
- Fixed weakening of voting ability (#3970)
- implemented faster sweep algorithm for kernighan_lin_bisection (#3858)
- Fix issue #3926 (#3928)
- Update CONTRIBUTORS.rst (#3982)
- Deprecate context_manager reversed in favor of reversed_view (#3983)
- Update CONTRIBUTORS.rst (#3987)
- Enhancement for voterank (#3972)
- add d-separation algorithm (#3974)
- DOC: added see also section to find_cycle (#3999)
- improve docs for subgraph_view filter_edge (#4010)
- Fix exception causes in dag.py (#4000)
- use raise from for exceptions in to_networkx_graph (#4009)
- Fix exception causes and messages in 12 modules (#4012)
- Fix typo: `np.int` -> `np.int_` (#4013)
- fix a typo (#4017)
- change documentation (#3981)
- algorithms for regular graphs (#3925)
- Typo Hand should be Hans (#4025)
- DOC: Add testing bullet to CONTRIBUTING. (#4035)
- Update Sphinx
- Update optional/test deps
- Add governance/values/nexp/roadmap
- Improve formatting of None in tutorial (#3986)
- Fixes DiGraph spelling in docstring (#3892)
- Update links to Py3 docs (#4042)
- Add method to clear edges only (#3477)
- Fix exception causes and messages all over the codebase (#4015)
- Handle kwds explicitly in draw_networkx (#4033)
- return empty generator instead of empty list (#3967)
- Correctly infer numpy float types (#3919)
- MAINT: Update from_graph6_bytes arg/docs. (#4034)
- Add URLs/banner/titlebar to documentation (#4044)
- Add negative cycle detection heuristic (#3879)
- Remove unused imports (#3855)
- Fixed Bug in generate_gml(G, stringizer=None) (#3841)
- Raise NetworkXError when k < 2 (#3761)
- MAINT: rm np.matrix from alg. conn. module
- MAINT: rm np.matrix from attribute_ac.
- MAINT,TST: Parametrize methods in TestAlgebraicConnectivity.
- MAINT,TST: parametrize buckminsterfullerene test.
- MAINT,TST: Remove unused _methods class attr
- MAINT,TST: Parametrize TestSpectralOrdering.
- excluded self/recursive edges  (#4037)
- WIP: Change EdgeDataView __contains__ feature (2nd attempt) (#3845)
- Index edges for multi graph simple paths (#3358)
- ENH: Add new graph_hashing feature
- Fix pandas deprecation
- Organize removal of deprecated code
- Update sphinx
- ENH: Add roots and timeout to GED (#4026)
- Make gallery more prominent
- Add an implementation for interval_graph and its unit tests (#3705)
- Fixed typo in kamada_kawai_layout docstring (#4059)
- Remove completeness condition from minimum weight full matching (#4057)
- Implemented multipartite_layout (#3815)
- added new Link Prediction algorithm (CCPA) (#4028)
- add the option of sorting node's neighbors during bfs traversal  (#4029)
- TST: remove int64 specification from test. (#4055)
- Ran pyupgrade --py36plus
- Remove trailing spaces
- Tell psf/black to ignore specific np.arrays
- Format w/ black
- Add pre-commit hook to for psf/black
- Merge pull request #4060 from jarrodmillman/black
- Fix a few typos in matching docstrings (#4063)
- fix bug for to_scipy_sparse_matrix function (#3985)
- Update documentation of minimum weight full matching (#4062)
- Add maximum weight clique algorithm (#4016)
- Clear pygraphviz object after creating networkx object (#4070)
- Use newer osx on travis (#4075)
- Install Python after updating brew (#4079)
- Add link to black (#4078)
- Improves docs regarding aliases of erdos-reyni graph generators (#4074)
- MAINT: Remove dependency version info from INSTALL (#4081)
- Simplify top-level directory (#4087)
- DOC: Fix return types in laplacianmatrix. (#4090)
- add modularity to the docs (#4096)
- Allow G.remove_edges_from(nx.selfloops_edges(G)) (#4080)
- MAINT: rm private fn in favor of numpy builtin. (#4094)
- Allow custom keys for multiedges in from_pandas_edgelist (#4076)
- Fix planar_layout docstring (#4097)
- DOC: Rewording re: numpy.matrix
- MAINT: rm to/from_numpy_matrix internally
- Merge pull request #4093 from rossbar/rm_npmatrix
- Remove copyright boilerplate (#4105)
- Update contributor guide (#4088)
- Add function to calculate path cost for a specified path (#4069)
- Update docstring for from_pandas_edgelist (#4108)
- Add max_weight_clique to doc (#4110)
- Update deprecation policy (#4112)
- Improve modularity calculation (#4103)
- Add team gallery (#4117)
- CI: Setup circle CI for documentation builds (#4119)
- Build pdf (#4123)
- DOC: Suggestions and improvements from tutorial readthrough (#4121)
- Enable 3.9-dev on travis (#4124)
- Fix parse_edgelist behavior with multiple attributes (#4125)
- CI: temporary fix for CI latex installation issues (#4131)
- Updated draw_networkx to accept numpy array for edgelist (#4132)
- Add tree isomorphism (#4067)
- MAINT: Switch to abc-based isinstance checks in to_networkx_graph (#4136)
- Use dict instead of OrderedDict since dict is ordered by default from Python 3.6. (#4145)
- MAINT: fixups to parse_edgelist. (#4128)
- Update apt-get on circleci image (#4147)
- add rescale_layout_dict to change scale of the layout_dicts (#4154)
- Update dependencies
- Remove gdal from requirements
- relabel_nodes now preserves edges in multigraphs (#4066)
- MAINT,TST: Improve coverage of nx_agraph module (#4156)
- Get steiner_tree to work with MultiGraphs by postprocessing (#4160)
- junction_tree for #1012 (#4004)
- API: Add `show` kwarg to view_pygraphviz. (#4155)
- Prepare for turning chordal_graph_cliques into a generator (#4162)
- Docs update (#4161)
- Remove unnecessary nx imports from doctests (#4163)
- MultiGraph from graphml with explicit edge ids #3470 (#3763)
- Update sphinx dep (#4164)
- Add edge label in GEXF writer as an optional attribute (#3347)
- First Draft of Release Notes for v2.5 (#4159)
- Designate 2.5rc1 release
- Bump release version
- Update deprecations in release notes (#4166)
- DOC: Update docstrings for public functions in threshold module (#4167)
- Format python in docstrings (#4168)
- DOC,BLD: Fix doc build warning from markup error. (#4174)

It contained the following 3 merges:

- fixed a typo (#3759)
- Use psf/black (#4060)
- MAINT: Replace internal usage of to_numpy_matrix and from_numpy_matrix (#4093)


Contributors
------------

- Adnan Abdulmuttaleb
- Abhi
- Antoine-H
- Salim BELHADDAD
- Ross Barnowski
- Lukas Bernwald
- Isaac Boates
- Kelly Boothby
- Matthias Bruhns
- Mahmut Bulut
- Rüdiger Busche
- Gaetano Carpinato
- Nikos Chan
- Harold Chan
- Camden Cheek
- Daniel
- Daniel-Davies
- Bastian David
- Christoph Deil
- Tanguy Fardet
- 赵丰 (Zhao Feng)
- Andy Garfield
- Oded Green
- Drew H
- Alex Henrie
- Kang Hong Jin
- Manas Joshi
- Søren Fuglede Jørgensen
- Aabir Abubaker Kar
- Folgert Karsdorp
- Suny Kim
- Don Kirkby
- Katherine Klise
- Steve Kowalik
- Ilia Kurenkov
- Whi Kwon
- Paolo Lammens
- Zachary Lawrence
- Sanghack Lee
- Anton Lodder
- Lukas Lösche
- Eric Ma
- Mackyboy12
- Christoph Martin
- Alex Marvin
- Mattwmaster58
- James McDermott
- Jarrod Millman
- Ibraheem Moosa
- Yohsuke Murase
- Neil
- Harri Nieminen
- Danny Niquette
- Carlos G. Oliver
- Juan Orduz
- Austin Orr
- Pedro Ortale
- Aditya Pal
- PalAditya
- Jose Pinilla
- PranayAnchuri
- Jorge Martín Pérez
- Pradeep Reddy Raamana
- Ram Rachum
- David Radcliffe
- Federico Rosato
- Tom Russell
- Craig Schmidt
- Jonathan Schneider
- Dan Schult
- Mridul Seth
- Karthikeyan Singaravelan
- Songyu-Wang
- Kanishk Tantia
- Jeremias Traub
- James Trimble
- Shashi Tripathi
- Stefan van der Walt
- Jonatan Westholm
- Kazimierz Wojciechowski
- Jangwon Yie
- adnanmuttaleb
- anentropic
- arunwise
- beckedorf
- ernstklrb
- farhanbhoraniya
- fj128
- gseva
- haochenucr
- johnthagen
- kiryph
- muratgu
- ryan-duve
- sauxpa
- tombeek111
- willpeppo

# ===== SOURCE: https://raw.githubusercontent.com/networkx/networkx/main/doc/release/release_2.6.rst =====

.. _networkx_2.6:

NetworkX 2.6
============

Release date: 08 July 2021

Supports Python 3.7, 3.8, and 3.9.

This release has a larger than normal number of changes in preparation for the upcoming 3.0 release.
The current plan is to release 2.7 near the end of summer and 3.0 in late 2021.
See :doc:`migration_guide_from_2.x_to_3.0` for more details.

NetworkX is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex networks.

For more information, please visit our `website <https://networkx.org/>`_
and our :ref:`gallery of examples <examples_gallery>`
Please send comments and questions to the `networkx-discuss mailing list
<http://groups.google.com/group/networkx-discuss>`_.

Highlights
----------

This release is the result of 11 months of work with over 363 pull requests by
91 contributors. Highlights include:

- Dropped support for Python 3.6
- Dropped "decorator" library dependency
- Improved example gallery
- Removed code for supporting Jython/IronPython
- The ``__str__`` method for graph objects is more informative and concise.
- Improved import time
- Improved test coverage
- New documentation theme
- Add functionality for drawing self-loop edges
- Add approximation algorithms for Traveling Salesman Problem

New functions:

- Panther algorithm
- maximum cut heuristics
- equivalence_classes
- dedensification
- random_ordered_tree
- forest_str
- snap_aggregation
- networkx.approximation.diameter
- partition_quality
- prominent_group
- prefix_tree_recursive
- topological_generations

NXEPs
-----

**N**\etwork\ **X** **E**\nhancement **P**\roposals capture changes
that are larger in scope than typical pull requests, such as changes to
fundamental data structures.
The following proposals have come under consideration since the previous
release:

- :ref:`NXEP2`
- :ref:`NXEP3`

Improvements
------------

- [`#3886 <https://github.com/networkx/networkx/pull/3886>`_]
  Adds the Panther algorithm for top-k similarity search.
- [`#4138 <https://github.com/networkx/networkx/pull/4138>`_]
  Adds heuristics for approximating solution to the maximum cut problem.
- [`#4183 <https://github.com/networkx/networkx/pull/4183>`_]
  Adds ``equivalence_classes`` to public API.
- [`#4193 <https://github.com/networkx/networkx/pull/4193>`_]
  ``nx.info`` is more concise.
- [`#4198 <https://github.com/networkx/networkx/pull/4198>`_]
  Improve performance of ``transitivity``.
- [`#4206 <https://github.com/networkx/networkx/pull/4206>`_]
  UnionFind.union selects the heaviest root as the new root
- [`#4240 <https://github.com/networkx/networkx/pull/4240>`_]
  Adds ``dedensification`` function in a new ``summarization`` module.
- [`#4294 <https://github.com/networkx/networkx/pull/4294>`_]
  Adds ``forest_str`` for string representation of trees.
- [`#4319 <https://github.com/networkx/networkx/pull/4319>`_]
  pagerank uses scipy by default now.
- [`#4841 <https://github.com/networkx/networkx/pull/4841>`_]
  simrank_similarity uses numpy by default now.
- [`#4317 <https://github.com/networkx/networkx/pull/4317>`_]
  New ``source`` argument to ``has_eulerian_path`` to look for path starting at
  source.
- [`#4356 <https://github.com/networkx/networkx/pull/4356>`_]
  Use ``bidirectional_dijkstra`` in ``shortest_path`` for weighted graphs
  to improve performance.
- [`#4361 <https://github.com/networkx/networkx/pull/4361>`_]
  Adds ``nodelist`` argument to ``triadic_census``
- [`#4435 <https://github.com/networkx/networkx/pull/4435>`_]
  Improve ``group_betweenness_centrality``.
- [`#4446 <https://github.com/networkx/networkx/pull/4446>`_]
  Add ``sources`` parameter to allow computing ``harmonic_centrality`` from a
  subset of nodes.
- [`#4463 <https://github.com/networkx/networkx/pull/4463>`_]
  Adds the ``snap`` summarization algorithm.
- [`#4476 <https://github.com/networkx/networkx/pull/4476>`_]
  Adds the ``diameter`` function for approximating the lower bound on the
  diameter of a graph.
- [`#4519 <https://github.com/networkx/networkx/pull/4519>`_]
  Handle negative weights in clustering algorithms.
- [`#4528 <https://github.com/networkx/networkx/pull/4528>`_]
  Improved performance of ``edge_boundary``.
- [`#4560 <https://github.com/networkx/networkx/pull/4560>`_]
  Adds ``prominent_group`` function to find prominent group of size k in
  G according to group_betweenness_centrality.
- [`#4588 <https://github.com/networkx/networkx/pull/4588>`_]
  Graph intersection now works when input graphs don't have the same node sets.
- [`#4607 <https://github.com/networkx/networkx/pull/4607>`_]
  Adds approximation algorithms for solving the traveling salesman problem,
  including ``christofides``, ``greedy_tsp``, ``simulated_annealing_tsp``,
  and ``threshold_accepting_tsp``.
- [`#4640 <https://github.com/networkx/networkx/pull/4640>`_]
  ``prefix_tree`` now uses a non-recursive algorithm. The original recursive
  algorithm is still available via ``prefix_tree_recursive``.
- [`#4659 <https://github.com/networkx/networkx/pull/4659>`_]
  New ``initial_graph`` argument to ``barabasi_albert_graph`` and
  ``dual_barabasi_albert_graph`` to supply an initial graph to the model.
- [`#4690 <https://github.com/networkx/networkx/pull/4690>`_]
  ``modularity_max`` now supports edge weights.
- [`#4727 <https://github.com/networkx/networkx/pull/4727>`_]
  Improved performance of ``scale_free_graph``.
- [`#4739 <https://github.com/networkx/networkx/pull/4739>`_]
  Added `argmap` function to replace the decorator library dependence
- [`#4757 <https://github.com/networkx/networkx/pull/4757>`_]
  Adds ``topological_generations`` function for DAG stratification.
- [`#4768 <https://github.com/networkx/networkx/pull/4768>`_]
  Improved reproducibility of geometric graph generators.
- [`#4769 <https://github.com/networkx/networkx/pull/4769>`_]
  Adds ``margins`` keyword to ``draw_networkx_nodes`` to control node clipping
  in images with large node sizes.
- [`#4812 <https://github.com/networkx/networkx/pull/4812>`_]
  Use ``scipy`` implementation for ``hits`` algorithm to improve performance.
- [`#4847 <https://github.com/networkx/networkx/pull/4847>`_]
  Improve performance of ``scipy`` implementation of ``hits`` algorithm.

API Changes
-----------

- [`#4183 <https://github.com/networkx/networkx/pull/4183>`_]
  ``partition`` argument of `quotient_graph` now accepts dicts
- [`#4190 <https://github.com/networkx/networkx/pull/4190>`_]
  Removed ``tracemin_chol``.  Use ``tracemin_lu`` instead.
- [`#4216 <https://github.com/networkx/networkx/pull/4216>`_]
  In `to_*_array/matrix`, nodes in nodelist but not in G now raise an exception.
  Use G.add_nodes_from(nodelist) to add them to G before converting.
- [`#4360  <https://github.com/networkx/networkx/pull/4360>`_]
  Internally `.nx_pylab.draw_networkx_edges` now always generates a
  list of `matplotlib.patches.FancyArrowPatch` rather than using
  a `matplotlib.collections.LineCollection` for un-directed graphs.  This
  unifies interface for all types of graphs.  In
  addition to the API change this may cause a performance regression for
  large graphs.
- [`#4384 <https://github.com/networkx/networkx/pull/4384>`_]
  Added ``edge_key`` parameter for MultiGraphs in to_pandas_edgelist
- [`#4461 <https://github.com/networkx/networkx/pull/4461>`_]
  Added ``create_using`` parameter to ``binomial_tree``
- [`#4466 <https://github.com/networkx/networkx/pull/4466>`_]
  `relabel_nodes` used to raise a KeyError for a key in `mapping` that is not
  a node in the graph, but it only did this when `copy` was `False`. Now
  any keys in `mapping` which are not in the graph are ignored.
- [`#4502 <https://github.com/networkx/networkx/pull/4502>`_]
  Moves ``maximum_independent_set`` to the ``clique`` module in ``approximation``.
- [`#4536 <https://github.com/networkx/networkx/pull/4536>`_]
  Deprecate ``performance`` and ``coverage`` in favor of ``partition_quality``,
  which computes both metrics simultaneously and is more efficient.
- [`#4573 <https://github.com/networkx/networkx/pull/4573>`_]
  `label_propagation_communities` returns a `dict_values` object of community
  sets of nodes instead of a generator of community sets. It is still iterable,
  so likely will still work in most user code and a simple fix otherwise:
  e.g., add ``iter( ... )`` surrounding the function call.
- [`#4545 <https://github.com/networkx/networkx/pull/4545>`_]
  `prefix_tree` used to return `tree, root` but root is now always 0
  instead of a UUID generate string. So the function returns `tree`.
- [`#4545 <https://github.com/networkx/networkx/pull/4545>`_]
  The variable `NIL` ="NIL" has been removed from `networkx.generators.trees`
- [`#3620 <https://github.com/networkx/networkx/pull/3620>`_]
  The function `naive_greedy_modularity_communities` now returns a
  list of communities (like `greedy_modularity_communities`) instead
  of a generator of communities.
- [`#4786 <https://github.com/networkx/networkx/pull/4786>`_]
  Deprecate the ``attrs`` keyword argument in favor of explicit keyword
  arguments in the ``json_graph`` module.
- [`#4843 <https://github.com/networkx/networkx/pull/4843>`_]
  The unused ``normalized`` parameter has been removed
  from ``communicability_betweenness_centrality``
- [`#4850 <https://github.com/networkx/networkx/pull/4850>`_]
  Added ``dtype`` parameter to adjacency_matrix
- [`#4851 <https://github.com/networkx/networkx/pull/4851>`_]
  Output of `numeric_mixing_matrix` and `degree_mixing_matrix` no longer
  includes rows with all entries zero by default. The functions now accept
  a parameter `mapping` keyed by value to row index to identify each row.
- [`#4867 <https://github.com/networkx/networkx/pull/4867>`_]
  The function ``spring_layout`` now ignores 'fixed' nodes not in the graph

Deprecations
------------

- [`#4238 <https://github.com/networkx/networkx/pull/4238>`_]
  Deprecate ``to_numpy_matrix`` and ``from_numpy_matrix``.
- [`#4279 <https://github.com/networkx/networkx/pull/4279>`_]
  Deprecate ``networkx.utils.misc.is_iterator``.
  Use ``isinstance(obj, collections.abc.Iterator)`` instead.
- [`#4280 <https://github.com/networkx/networkx/pull/4280>`_]
  Deprecate ``networkx.utils.misc.is_list_of_ints`` as it is no longer used.
  See ``networkx.utils.misc.make_list_of_ints`` for related functionality.
- [`#4281 <https://github.com/networkx/networkx/pull/4281>`_]
  Deprecate ``read_yaml`` and ``write_yaml``.
- [`#4282 <https://github.com/networkx/networkx/pull/4282>`_]
  Deprecate ``read_gpickle`` and ``write_gpickle``.
- [`#4298 <https://github.com/networkx/networkx/pull/4298>`_]
  Deprecate ``read_shp``, ``edges_from_line``, and ``write_shp``.
- [`#4319 <https://github.com/networkx/networkx/pull/4319>`_]
  Deprecate ``pagerank_numpy``, ``pagerank_scipy``.
- [`#4355 <https://github.com/networkx/networkx/pull/4355>`_]
  Deprecate ``copy`` method in the coreview Filtered-related classes.
- [`#4384 <https://github.com/networkx/networkx/pull/4384>`_]
  Deprecate unused ``order`` parameter in to_pandas_edgelist.
- [`#4428 <https://github.com/networkx/networkx/pull/4428>`_]
  Deprecate ``jit_data`` and ``jit_graph``.
- [`#4449 <https://github.com/networkx/networkx/pull/4449>`_]
  Deprecate ``consume``.
- [`#4448 <https://github.com/networkx/networkx/pull/4448>`_]
  Deprecate ``iterable``.
- [`#4536 <https://github.com/networkx/networkx/pull/4536>`_]
  Deprecate ``performance`` and ``coverage`` in favor of ``partition_quality``.
- [`#4545 <https://github.com/networkx/networkx/pull/4545>`_]
  Deprecate ``generate_unique_node``.
- [`#4599 <https://github.com/networkx/networkx/pull/4599>`_]
  Deprecate ``empty_generator``.
- [`#4600 <https://github.com/networkx/networkx/pull/4600>`_]
  Deprecate ``default_opener``.
- [`#4617 <https://github.com/networkx/networkx/pull/4617>`_]
  Deprecate ``hub_matrix`` and ``authority_matrix``
- [`#4629 <https://github.com/networkx/networkx/pull/4629>`_]
  Deprecate the ``Ordered`` graph classes.
- [`#4802 <https://github.com/networkx/networkx/pull/4802>`_]
  The ``nx_yaml`` function has been removed along with the dependency on
  ``pyyaml``. Removal implemented via module ``__getattr__`` to patch security
  warnings related to ``pyyaml.Loader``.
- [`#4826 <https://github.com/networkx/networkx/pull/4826>`_]
  Deprecate ``preserve_random_state``.
- [`#4827 <https://github.com/networkx/networkx/pull/4827>`_]
  Deprecate ``almost_equal``.
- [`#4833 <https://github.com/networkx/networkx/pull/4833>`_]
  Deprecate ``run``.
- [`#4829 <https://github.com/networkx/networkx/pull/4829>`_]
  Deprecate ``assert_nodes_equal``, ``assert_edges_equal``, and ``assert_graphs_equal``.
- [`#4850 <https://github.com/networkx/networkx/pull/4850>`_]
  Deprecate ``adj_matrix``.
- [`#4841 <https://github.com/networkx/networkx/pull/4841>`_]
  Deprecate ``simrank_similarity_numpy``.
- [`#4923 <https://github.com/networkx/networkx/pull/4923>`_]
  Deprecate ``numeric_mixing_matrix``.
- [`#4937 <https://github.com/networkx/networkx/pull/4937>`_]
  Deprecate ``k_nearest_neighbors``.

Merged PRs
----------

- Bump release version
- Update release process
- Update website doc
- fix issue #4173: cytoscape_graph(input_data) did modify the original data (#4176)
- Some docstring fixes for draw_networkx_edge_labels() in nx_pylab.py + one typo (#4182)
- TST: add dtype to pandas test (#4185)
- Partitions for quotient graphs (#4183)
- graphml: re-add graph attribute type 'long' after 857aa81 removed it (#4189)
- Test mac osx via actions (#4201)
- DOC: Update docstrings in cytoscape module (#4180)
- rewrite add_nodes_from to relax code meant to allow ironpython pre-2.7.5 (#4200)
- Speed up transitivity, remove redundant call (#4198)
- NXEP 2 — API design of view slices (#4101)
- Cleanup old platforms (#4202)
- Fixed "topological_sort" typo (#4211)
- Make optional dependencies default on CPython
- Simplify imports
- Populate setup.py requires from requirements
- Update dependencies
- Remove _CholeskySolver
- to_numpy/scipy array functions should not allow non-nodes in nodelist (#4216)
- fix "see also" links in json_graph.tree (#4222)
- MAINT: changed is_string_like to isinstance (#4223)
- Fix UnionFind.union to select the heaviest root as the new root (#4206)
- CI: Configure circleCI to deploy docs. (#4134)
- MAINT: Update nx.info (#4193)
- Fix indexing in kernighan_lin_bisection (#4177)
- CI: Add GH fingerprint (#4229)
- Create ssh dir for circleci
- CI: update circleci doc deployment. (#4230)
- Revert "CI: Configure circleCI to deploy docs. (#4134)" (#4231)
- DOC: Add discussion to NXEP 2.
- Update format dependencies
- Use black for linting
- Format w/ black==20.8b1
- Check formatting of PRs via black (#4235)
- TST: Modify heuristic for astar path test. (#4237)
- MAINT: Deprecate numpy matrix conversion functions (#4238)
- Add roadmap (#4234)
- Add nx.info to str dunder for graph classes (#4241)
- DOC: Minor reformatting of contract_nodes docstring. (#4245)
- Fix betweenness_centrality doc paper links (#4257)
- Fix bug in has_eulerian_path for directed graphs  (#4246)
- Add PR template (#4258)
- Use seed to make plot fixed (#4260)
- Update giant component example (#4267)
- Update "house with colors" gallery example (#4263)
- Replace degree_histogram and degree_rank with a single example (#4265)
- Update Knuth miles example. (#4251)
- Update "four_grids" gallery example (#4264)
- Improve legibility of labels in plot_labels_and_colors example (#4266)
- Improve readability of chess_example in gallery (#4252)
- Fix contracted_edge for multiple edges (#4274)
- Add seeds to gallery examples for reproducibility (#4276)
- Add a 3D plotting example with matplotlib to the gallery (#4268)
- Deprecate `utils.is_iterator` (#4279)
- Deprecate utils.is_list_of_ints (#4280)
- Improve axes layout in plot_decomposition example (#4278)
- Update homepage URL (#4285)
- Build docs for deployment on Travis CI (#4286)
- Add simple graph w/ manual layout (#4291)
- Deprecate nx_yaml (#4281)
- Deprecate gpickle (#4282)
- Improve relabel coverage, tweak docstrings (#4299)
- Switch to travis-ci.com
- TST: Increase test coverage of convert_matrix (#4301)
- Add descriptive error message for Node/EdgeView slicing. NEXP2 (#4300)
- Don't import other people's version.py (#4289)
- TST: Refactor to improve coverage. (#4307)
- Improve readwrite test coverage (#4310)
- Fix typo (#4312)
- Update docstring of to_dict_of_dicts.
- Add tests for edge_data param.
- Minor touchups to docstring
- adds dedensification function (#4240)
- TST: improve multigraph test coverage to 100% (#4340)
- Add rainbow coloring example to gallery. (#4330)
- Test on Python 3.9 (#4303)
- Sphinx33 (#4342)
- fix order of yield and seen.update in all cc routines (see #4331 & #3859 & 3823) (#4333)
- Updates to slicing error message for reportviews (#4304)
- Eulerian path fix (#4317)
- Add FutureWarning in preparation for simplifying cytoscape function signatures. (#4284)
- Move a few imports inside functions to improve import speed of the library (#4296)
- Address comments from code review.
- Cleanup algebraicconnectivity (#4287)
- Switch from travis to gh actions (#4320)
- Fix (#4345)
- Fix travis doc deployment
- Fix gdal version on travis
- Update to_dict_of_dict edge_data (#4321)
- Update adjacency_iter to adjacency (#4339)
- Test and document missing nodes/edges in set_{node/edge}_attributes (#4346)
- Update tests and docs for has_eulerian_path (#4344)
- Deprecate nx_shp (#4298)
- Refactor and improve test coverage for restricted_view and selfloop_edges (#4351)
- Enable mayavi in sphinx gallery. (#4297)
- CI: Add mayavi conf to travis and GH for doc deploy (#4354)
- Fix doc build w/ GH actions
- Install vtk before mayavi
- Install vtk before mayavi
- Install vtk before mayavi
- Use bidirectional_dijkstra as default in weighted shortest_path (#4356)
- Add unit tests for utils.misc.flatten (#4359)
- Improve test coverage for coreviews.py (#4355)
- Update tutorial.rst - Fixes #4249 (#4358)
- Bugfix for issue 4336, moving try/except and adding else clause (#4365)
- Added nodelist attribute to triadic_census (#4361)
- API: always use list of FancyArrowPatch rather than LineCollection (#4360)
- MNT: make the self-loop appear in all cases (#4370)
- Add additional libraries to intersphinx mapping (#4372)
- Make nx.pagerank a wrapper around different implementations, use scipy one by default (#4319)
- MAINT: remove deprecated numpy type aliases. (#4373)
- DOC: Fix return type for random_tournament and hamiltonian_path (#4376)
- Skip memory leak test for PyPy (#4385)
- add OSMnx example (#4383)
- Update docstring for to_pandas_edgelist and add edgekey parameter (#4384)
- TST: Boost test coverage of nx_pylab module (#4375)
- Fixed issue where edge attributes were being silently overwritten during node contraction (#4273)
- CI: Fix CircleCI doc build failure (#4388)
- Improve test coverage of convert module (#4306)
- Add gene-gene network (#4269)
- Ignore expected warnings (#4391)
- Use matrix multiplication operator (#4390)
- code and doc fix for square_clustering algorithm in cluster.py (#4392)
- Remove xml import checks (#4393)
- fix typo in NXEP template (#4396)
- Add Panther algorithm per #3849 (#3886)
- Pagerank followup (#4399)
- Don't import nx from networkx (#4403)
- Modify and document behavior of nodelist param in draw_networkx_edges. (#4378)
- Add circuit plot (#4408)
- Add words graph plot (#4409)
- DOC: Remove repeated words (#4410)
- Add plot for rcm example (#4411)
- Fix small index iteration bug in kernighan_lin algorithm (#4398)
- Use str dunder (#4412)
- Use xetex for uft8 latex backend (#4326)
- Add recommended fonts to travis.yml. (#4414)
- CI: Workaround font naming bug. (#4416)
- DOC: geospatial example using lines (#4407)
- Add plotting examples for geospatial data (#4366)
- Increase coverage in graphviews.py (#4418)
- Refactor gallery (#4422)
- Safer repr format of variables (#4413)
- Updates to docs and imports for classic.py (#4424)
- Remove advanced example section (#4429)
- Add coreview objects to documentation (#4431)
- Add gallery example for drawing self-loops. (#4430)
- Add igraph example (#4404)
- Standard imports (#4401)
- Collect graphviz examples (#4427)
- NXEP 3: Allow generators to yield from edgelists (#4395)
- Update geospatial readme (#4417)
- DOC: Fix broken links in shortest_path docstrings (#4434)
- Improves description bfs_predecessors and bfs_successors. (#4438)
- Deprecate jit (#4428)
- JavaScript example: fix link (#4450)
- Deprecate utils.misc.consume (#4449)
- DOC: Switch from napoleon to numpydoc sphinx extension (#4447)
- Correct networkxsimplex docstring re: multigraph
- Correct networkxsimplex docstring re: multigraph (#4455)
- Maxcut heuristics (#4138)
- binomial_tree() with "create_using parameter (#4461)
- Reorganize tests (#4467)
- Drop Py3.6 support per NEP 29 (#4469)
- Add random_ordered_tree and forest_str (#4294)
- Deprecate iterable (#4448)
- Allow relabel_nodes mapping to have non-node keys that get ignored (#4466)
- Fixed docs + added decorator for k_components approx (#4474)
- Update docs for clustering Fixes #4348 (#4477)
- Handle self-loops for single self-loop (drawing) (#4425)
- Update GH actions links in README (#4482)
- Improve code coverage for cuts.py (#4473)
- Re-enable tests (#4488)
- Update Sphinx (#4494)
- Update pre-commit (#4495)
- Simplify example dependencies (#4506)
- Update geospatial readme (#4504)
- Update year (#4509)
- Drop Travis CI (#4510)
- Run pypy tests separately (#4512)
- Simplify version information (#4492)
- Delete old test (#4513)
- Gallery support for pygraphviz examples (#4464)
- TST: An approach to parametrizing read_edgelist tests. (#4292)
- Setup cross-repo doc deploy via actions. (#4480)
- use issue templates to redirect to discussions tab, add a bug report template (#4524)
- Fix performance issue in nx.edge_boundary (#4528)
- clean up list comp (#4499)
- Improve code coverage of swap.py (#4529)
- Clustering for signed weighted graphs (#4519)
- Fix docstrings and remove unused variables (#4501)
- Improving code coverage of chordal.py (#4471)
- Cliques on multigraph/directed graph types (#4502)
- Approximated Diameter  (#4476)
- `arrows` should be True by default for directed graphs (#4522)
- Remove unnecessary node_list from gallery example (#4505)
- fixing the width argument description of the function draw_networkx (#4479)
- Partially revert #4378 - Modify behavior of nodelist param in draw_networkx_edges. (#4531)
- Replace generate_unique_node internally where not needed (#4537)
- Extend harmonic centrality to include source nodes (#4446)
- improve group betweenness centrality (#4435)
- fixes GitHub Actions failures (#4548)
- updated cutoff def in weighted.py (#4546)
- Less strict on mayavi constraint for doc building. (#4547)
- Update docstring for ancestor and descendents (#4550)
- TST: Fix error in katz centrality test setup. (#4554)
- Correct mu parameter documentation for LFR (#4557)
- Pin pygeos==0.8 (#4563)
- Unpin pygeos (#4570)
- Test Windows via GH actions (#4567)
- Update documentation and testing of arbitrary_element (#4451)
- added test for max_iter argument
- reformatted test_kernighan_lin.py
- Simplify test pylab (#4577)
- Update README.rst
- Fix search (#4580)
- Add test Kernighan Lin Algorithm (#4575)
- Fix typos (#4581)
- Boiler plate for mentored projects documentation (#4576)
- Deprecate generate_unique_node (#4545)
- Check nodelist input to floyd_warshall (#4589)
- Improve intersection function (#4588)
- Pygraphviz choco (#4583)
- Add prominent group algorithm (#4560)
- Add partition_quality to compute coverage and performance  (coverage and perfor… (#4536)
- Use Pillow for viewing AGraph output and deprecate default_opener (#4600)
- Remove mktemp usage (#4593)
- Add an FAQ to the developer guide for new contributors (#4556)
- Improve test coverage and docs for nonrandomness (#4613)
- Collect label propagation communities in one go (#4573)
- Deprecate networkx.utils.empty_generator. (#4599)
- return earlier from `clique.graph_clique_number` (#4622)
- More for projects page: TSP and Graph Isomorphism (#4620)
- add recommended venv directory to .gitignore (#4619)
- adding weight description to centrality metrics (#4610)
- Add a good first issue badge to README  (#4627)
- add test to regular (#4624)
- Add scipy-1.6.1 to blocklist. (#4628)
- Deprecate hub_matrix and authority_matrix (#4617)
- Fix issue #3153: generalized modularity maximization  (#3260)
- Improve doc example for find_cycle. (#4639)
- Correct and update Atlas example (#4635)
- Remove attr_dict from parameters list in the docstring (#4642)
- Verify edges are valid in is_matching() (#4638)
- Remove old file reference (#4646)
- Deprecate Ordered graph classes (#4629)
- Update CI to use main (#4651)
- Make main default branch (and remove gitwash) (#4649)
- Fix link for Katz centrality definition (#4655)
- fix for negative_edge_cycle weight kwarg to bellman_ford (#4658)
- Refactor bipartite and multipartite layout (#4653)
- Volunteering for mentorship (#4671)
- Adding an iterative version of prefix tree (#4640)
- Increase code coverage tournament (#4665)
- Fix to_vertex_cover (#4667)
- Reorganize minor submodule as subpackage (#4349)
- modularity_max: account for edge weights (#4690)
- Remove instances of random.sample from sets (deprecated in Python 3.9) (#4602)
- Fixing Bug in Transitive Reduction, resulting in loss of node/edge attributes (#4684)
- direct links to the tutorial and discussions in README (#4711)
- Pin upper bound of decorator dep. (#4721)
- fix typo (#4724)
- Updating average_clustering() documentation - Issue #4734 (#4735)
- rm nx import from docstring example. (#4738)
- CI: persist pip cache between circleci runs (#4714)
- Use pydata sphinx theme (#4741)
- O(n^2) -> O(n) implementation for scale_free_graph (#4727)
- TST: be more explicit about instance comparison. (#4748)
- fix typo in docstring (ismorphism -> isomorphism) (#4756)
- CI: Fix cartopy build failure in docs workflow (#4751)
- Add missing __all__'s to utils modules + test. (#4753)
- Add 2 articles for TSP project as references (#4758)
- Improve reproducibility of geometric graphs (#4768)
- Updated decorator requirement for #4718 (#4773)
- Gallery Example: Drawing custom node icons on network using MPL (#4633)
- Get rid of invalid escape sequences. (#4789)
- imread(url) is deprecated, use pillow + urllib to load image from URL (#4790)
- Add auto-margin scaling in draw_networkx_nodes function (fix for issue 3443) (#4769)
- Update documentation dependencies (#4794)
- Fix sphinx warnings during doc build. (#4795)
- Remove mayavi and cartopy dependencies (#4800)
- make plots less dense, enable plotting for igraph (#4791)
- fix urllib import (#4793)
- Improve documentation look (#4801)
- Add approximation algorithms for traveling salesman problem (#4607)
- adds implementation of SNAP summarization algorithm (#4463)
- Update black (#4814)
- Restructure documentation (#4744)
- Pin upper bound on decorator for 2.6 release. (#4815)
- Use `callable()` to check if the object is callable (#1) (#4678)
- Remove dictionary from signature of tree_graph and tree_data (#4786)
- Make nx.hits a wrapper around different implementations, use scipy one by default (#4812)
- restructured networksimplex.py and added test_networksimplex.py (#4685)
- Update requirements (#4625)
- Fix Sphinx errors (#4817)
- Add topological_generations function (#4757)
- Add `initial_graph` parameter to simple and dual Barábasi-Albert random graphs (#4659)
- Link to guides (#4818)
- switch alias direction of spring_layout and fruchterman_reingold_layout (#4820)
- Fix to_undirected doc typo (#4821)
- Deprecate preserve_random_state (#4826)
- Fixes read/write_gml with nan/inf attributes (#4497)
- Remove pyyaml dependency via module getattr (#4802)
- Use pytest.approx (#4827)
- DOC: Clarify behaviour of k_crust(G, k) (#4831)
- Limit number of threads used by OMP in circleci. (#4830)
- Deprecate run (#4833)
- Fix a few broken links in the html docs (#4572)
- Refactor testing utilities (#4829)
- Fix edge drawing performance regression (#4825)
- Draft 2.6 release notes (#4828)
- Fix bad import pattern (#4839)
- Add info about testing and examples (#4582)
- Remove unused `normalized` parameter from communicability_betweenness_centrality (#4843)
- add special processing of `multigraph_input` upon graph init (#4823)
- Add dtype argument to adjacency_matrix (#4850)
- Use scipy to compute eigenvalues (#4847)
- Default to NumPy for simrank_similarity (#4841)
- Remove "networkx" from top-level networkx namespace (#4840)
- Designate 2.6rc1 release
- Bump release version
- DOC: point towards web archive link in GML docs (#4864)
- Fix docstring typo (#4871)
- Reformatted  table to address issue #4852 (#4875)
- spring_layout: ignore 'fixed' nodes not in the graph nodes (#4867)
- Deserializing custom default properties graph ml (#4872)
- DOC: Fix links, use DOI links, wayback machine where required (#4868)
- Fix conda instructions (#4884)
- Decode GraphML/yEd shape type (#4694)
- bugfix-for-issue-4353: modify default edge_id format (#4842)
- Raise ValueError if None is added as a node. (#4892)
- Update arrows default value in draw_networkx. (#4883)
- Doc/fix 403 error drawing custom icons (#4906)
- Remove decorator dependency (#4739)
- Update docstrings for dfs and bfs edges and fix cross links (#4900)
- Fix graph_class usage in to_undirected method (#4912)
- Fix assortativity coefficient calculation (#4851)
- Deprecate numeric_mixing_matrix. (#4923)
- Update read_gml docstring with destringizer ex (#4916)
- Update release process (#4866)
- Designate 2.6rc2 release
- Bump release version
- Add 3.0 migration guide (#4927)
- quotient_graph doc fix (#4930)
- Page number for Katz centrality reference (#4932)
- Expand destringizer example in read_gml docstring (#4925)
- move partition checking outside private _quotient_graph function (#4931)
- Fixes #4275 - Add comment to parallel betweenness example (#4926)
- Minor Improvements on Networkx/algorithms/community/quality.py (#4939)
- Fix numeric and degree assortativity coefficient calculation (#4928)
- fix spelling in docstring of conftest.py (#4945)
- fix trouble with init_cycle argument to two TSP functions (#4938)
- split out deprecation. remove all changes to neighbor_degree (#4937)
- Add matrix market to readwrite reference (#4934)
- fix typo for PR number of deprecation (#4949)
- Fix neighbor degree for directed graphs (#4948)
- `descendants_at_distance` also for non-DiGraphs (#4952)
- Changes to rst files to make doctests pass (#4947)
- Fix version pull down (#4954)
- Finalize 2.6 release notes (#4958)

Contributors
------------

- AbhayGoyal
- Suvayu Ali
- Alexandre Amory
- Francesco Andreuzzi
- Salim BELHADDAD
- Ross Barnowski
- Raffaele Basile
- Jeroen Bergmans
- R. Bernstein
- Geoff Boeing
- Kelly Boothby
- Jeff Bradberry
- Erik Brendel
- Justin Cai
- Thomas A Caswell
- Jonas Charfreitag
- Berlin Cho
- ChristopherReinartz
- Jon Crall
- Michael Dorner
- Harshal Dupare
- Andrew Eckart
- Tomohiro Endo
- Douglas Fenstermacher
- Martin Fleischmann
- Martha Frysztacki [frɨʂtat͡skʲ]
- Debargha Ganguly
- CUI Hao
- Floris Hermsen
- Ward Huang
- Elgun Jabrayilzade
- Han Jaeseung
- Mohammed Kashif
- Alex Korbonits
- Mario Kostelac
- Sebastiaan Lokhorst
- Lonnen
- Delille Louis
- Xiaoyan Lu
- Alex Malins
- Oleh Marshev
- Jordan Matelsky
- Fabio Mazza
- Chris McBride
- Abdulelah S. Al Mesfer
- Attila Mester
- Jarrod Millman
- Miroslav Šedivý
- Harsh Mishra
- S Murthy
- Matthias Nagel
- Attila Nagy
- Mehdi Nemati
- Dimitrios Papageorgiou
- Vitaliy Pozdnyakov
- Bharat Raghunathan
- Randy
- Michael Recachinas
- Carlos González Rotger
- Taxo Rubio
- Dan Schult
- Mridul Seth
- Kunal Shah
- Eric Sims
- Ludovic Stephan
- Justin Timmons
- Andrea Tomassilli
- Matthew Treinish
- Milo Trujillo
- Danylo Ulianych
- Alex Walker
- Stefan van der Walt
- Anthony Wilder Wohns
- Levi John Wolf
- Xiangyu Xu
- Shichu Zhu
- alexpsimone
- as1371
- cpurmessur
- dbxnr
- wim glenn
- goncaloasimoes
- happy
- jason-crowley
- jebogaert
- josch
- ldelille
- marcusjcrook
- guy rozenberg
- tom
- walkeralexander

# ===== SOURCE: https://raw.githubusercontent.com/networkx/networkx/main/doc/release/release_2.7.rst =====

.. _networkx_2.7:

NetworkX 2.7
============

Release date: 28 February 2022

Supports Python 3.8, 3.9, and 3.10

NetworkX is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex networks.

For more information, please visit our `website <https://networkx.org/>`_
and our :ref:`gallery of examples <examples_gallery>`.
Please send comments and questions to the `networkx-discuss mailing list
<http://groups.google.com/group/networkx-discuss>`_.

Highlights
----------

This release is the result of 7 months of work with over 166 pull requests by
33 contributors. Highlights include:

.. warning::
   Hash values observed in outputs of
   `~networkx.algorithms.graph_hashing.weisfeiler_lehman_graph_hash`
   have changed in version 2.7 due to bug fixes. See gh-4946_ for details.
   This means that comparing hashes of the same graph computed with different
   versions of NetworkX (i.e. before and after version 2.7)
   could wrongly fail an isomorphism test (isomorphic graphs always have matching
   Weisfeiler-Lehman hashes). Users are advised to recalculate any stored graph
   hashes they may have on upgrading.

.. _gh-4946: https://github.com/networkx/networkx/pull/4946#issuecomment-914623654

- Dropped support for Python 3.7.
- Added the Asadpour algorithm for solving the asymmetric traveling salesman
  problem: `~networkx.algorithms.approximation.traveling_salesman.asadpour_atsp`.
- Added the Louvain community detection algorithm:
  `~networkx.algorithms.community.louvain.louvain_communities` and
  `~networkx.algorithms.community.louvain.louvain_partitions`
- Removed all internal usage of the `numpy.matrix` class, and added a
  `FutureWarning` to all functions that return a `numpy.matrix` instance.
  The `numpy.matrix` class will be replaced with 2D `numpy.ndarray` instances
  in NetworkX 3.0.
- Added support for the `scipy.sparse` array interface. This includes
  `~networkx.convert_matrix.to_scipy_sparse_array` and
  `~networkx.convert_matrix.from_scipy_sparse_array`. In NetworkX 3.0,
  sparse arrays will replace sparse matrices as the primary interface to
  `scipy.sparse`. New code should use ``to_scipy_sparse_array`` and
  ``from_scipy_sparse_array`` instead of their matrix counterparts.
  In addition, many functions that currently return sparse matrices now raise
  a `FutureWarning` to indicate that they will return sparse arrays instead in
  NetworkX 3.0.
- Added generic dtype support to `~networkx.convert_matrix.to_numpy_array`.
  This adds support for generic attributes, such as adjacency matrices with
  complex weights. This also adds support for generic reduction functions in
  handling multigraph weights, such as ``mean`` or ``median``. Finally, this
  also includes support for structured dtypes, which enables the creation of
  multi-attribute adjacency matrices and replaces the less generic
  ``to_numpy_recarray``.
- Added support for computing betweenness centrality on multigraphs
- Added support for directed graphs and multigraphs to ``greedy_modularity_communities``.

GSoC PRs
--------

We added the work from four Google Summer of Code projects:

- `Louvain community detection algorithm`_
    - Program: Google Summer of Code 2021
    - Contributor: `@z3y50n <https://github.com/z3y50n/>`__
    - Link to Proposal:  `GSoC 2021: Community Detection Algorithms <https://github.com/networkx/archive/blob/main/proposals-gsoc/GSoC-2021-Community-Detection-Algorithms.pdf>`__

- `Asadpour algorithm for directed travelling salesman problem`_
    - Program: Google Summer of Code 2021
    - Contributor: `@mjschwenne <https://github.com/mjschwenne/>`__
    - Link to Proposal:  `GSoC 2021: Asadpour algorithm <https://github.com/networkx/archive/blob/main/proposals-gsoc/GSoC-2021-Asadpour-Asymmetric-Traveling%20Salesman-Problem.pdf>`__

- Pedagogical notebook: `Directed acyclic graphs and topological sort`_
    - Program: Google Summer of Code 2021
    - Contributor:  `@vdshk <https://github.com/vdshk>`__

- Pedagogical notebooks: `Graph assortativity`_ & `Network flow analysis and Dinitz algorithm`_
    - Program: Google Summer of Code 2021
    - Contributor: `@harshal-dupare <https://github.com/harshal-dupare/>`__

.. _`Louvain community detection algorithm`: https://github.com/networkx/networkx/pull/4929
.. _`Asadpour algorithm for directed travelling salesman problem`: https://github.com/networkx/networkx/pull/4740
.. _`Directed acyclic graphs and topological sort`: https://github.com/networkx/nx-guides/pull/44
.. _`Graph assortativity`: https://github.com/networkx/nx-guides/pull/42
.. _`Network flow analysis and Dinitz algorithm`: https://github.com/networkx/nx-guides/pull/46

Improvements
------------

- [`#4740 <https://github.com/networkx/networkx/pull/4740>`_]
  Add the Asadpour algorithm for solving the asymmetric traveling salesman
  problem.
- [`#4897 <https://github.com/networkx/networkx/pull/4897>`_]
  Improve the validation and performance of ``nx.is_matching``,
  ``nx.is_maximal_matching`` and ``nx.is_perfect_matching``.
- [`#4924 <https://github.com/networkx/networkx/pull/4924>`_]
  Fix handling of disconnected graphs when computing
  ``nx.common_neighbor_centrality``.
- [`#4929 <https://github.com/networkx/networkx/pull/4929>`_]
  Add Louvain community detection.
- [`#4946 <https://github.com/networkx/networkx/pull/4946>`_]
  Add Weisfeiler-Lehman hashing subgraph hashing.
- [`#4950 <https://github.com/networkx/networkx/pull/4950>`_]
  Add an ``n_communities`` parameter to ``greedy_modularity_communities`` to
  terminate the search when the desired number of communities is found.
- [`#4965 <https://github.com/networkx/networkx/pull/4965>`_] and
  [`#4996 <https://github.com/networkx/networkx/pull/4996>`_]
  Fix handling of relabeled nodes in ``greedy_modularity_communities``.
- [`#4976 <https://github.com/networkx/networkx/pull/4976>`_]
  Add betweenness centrality for multigraphs.
- [`#4999 <https://github.com/networkx/networkx/pull/4999>`_]
  Fix ``degree_assortativity_coefficient`` for directed graphs.
- [`#5007 <https://github.com/networkx/networkx/pull/5007>`_]
  Add support for directed graphs and multigraphs to ``greedy_modularity_communities``.
- [`#5017 <https://github.com/networkx/networkx/pull/5017>`_]
  Improve implementation and documentation of ``descendants`` and ``ancestors``
- [`#5019 <https://github.com/networkx/networkx/pull/5019>`_]
  Improve documentation and testing for directed acyclic graph module.
- [`#5029 <https://github.com/networkx/networkx/pull/5029>`_]
  Improve documentation and testing of ``descendants_at_distance``.
- [`#5032 <https://github.com/networkx/networkx/pull/5032>`_]
  Improve performance of ``complement_edges``.
- [`#5045 <https://github.com/networkx/networkx/pull/5045>`_]
  Add ``geometric_edges`` to the ``nx`` namespace.
- [`#5051 <https://github.com/networkx/networkx/pull/5051>`_]
  Add support for comment characters for reading data with ``read_edgelist``.
- [`#5052 <https://github.com/networkx/networkx/pull/5052>`_]
  Improve performance and add support for undirected graphs and multigraphs to
  ``transitive_closure``.
- [`#5058 <https://github.com/networkx/networkx/pull/5058>`_]
  Improve exception handling for writing data in GraphML format.
- [`#5065 <https://github.com/networkx/networkx/pull/5065>`_]
  Improve support for floating point weights and resolution values in
  ``greedy_modularity_communities``.
- [`#5077 <https://github.com/networkx/networkx/pull/5077>`_]
  Fix edge probability in ``fast_gnp_random_graph`` for directed graphs.
- [`#5086 <https://github.com/networkx/networkx/pull/5086>`_]
  Fix defect in ``lowest_common_ancestors``.
- [`#5089 <https://github.com/networkx/networkx/pull/5089>`_]
  Add ``find_negative_cycle`` for finding negative cycles in weighted graphs.
- [`#5099 <https://github.com/networkx/networkx/pull/5099>`_]
  Improve documentation and testing of binary operators.
- [`#5104 <https://github.com/networkx/networkx/pull/5104>`_]
  Add support for self-loop edges and improve performance of ``vertex_cover``.
- [`#5121 <https://github.com/networkx/networkx/pull/5121>`_]
  Improve performance of ``*_all`` binary operators.
- [`#5131 <https://github.com/networkx/networkx/pull/5131>`_]
  Allow ``edge_style`` to be a list of styles when drawing edges for DiGraphs.
- [`#5139 <https://github.com/networkx/networkx/pull/5139>`_]
  Add support for the `scipy.sparse` array interface.
- [`#5144 <https://github.com/networkx/networkx/pull/5144>`_]
  Improve readability of ``node_classification`` functions.
- [`#5145 <https://github.com/networkx/networkx/pull/5145>`_]
  Adopt `math.hypot` which was added in Python 3.8.
- [`#5153 <https://github.com/networkx/networkx/pull/5153>`_]
  Fix ``multipartite_layout`` for graphs with non-numeric nodes.
- [`#5154 <https://github.com/networkx/networkx/pull/5154>`_]
  Allow ``arrowsize`` to be a list of arrow sizes for drawing edges.
- [`#5172 <https://github.com/networkx/networkx/pull/5172>`_]
  Add a ``nodes`` keyword argument to ``find_cliques`` to add support for
  finding maximal cliques containing only a set of nodes.
- [`#5197 <https://github.com/networkx/networkx/pull/5197>`_]
  Improve ``resistance_distance`` with advanced indexing.
- [`#5216 <https://github.com/networkx/networkx/pull/5216>`_]
  Make ``omega()`` closer to the published algorithm. The value changes slightly.
  The ``niter`` parameter default changes from 1->5 in ``lattice_reference()``
  and from 100->5 in ``omega``.
- [`#5217 <https://github.com/networkx/networkx/pull/5217>`_]
  Improve performance and readability of ``betweenness_centrality``.
- [`#5232 <https://github.com/networkx/networkx/pull/5232>`_]
  Add support for `None` edge weights to bidirectional Dijkstra algorithm.
- [`#5247 <https://github.com/networkx/networkx/pull/5247>`_]
  Improve performance of asynchronous label propagation algorithm for
  community detection, ``asyn_lpa_communities``.
- [`#5250 <https://github.com/networkx/networkx/pull/5250>`_]
  Add generic dtype support to ``to_numpy_array``.
- [`#5285 <https://github.com/networkx/networkx/pull/5285>`_]
  Improve ``karate_club_graph`` by updating to the weighted version from the original
  publication.
- [`#5287 <https://github.com/networkx/networkx/pull/5287>`_]
  Improve input validation for ``json_graph``.
- [`#5288 <https://github.com/networkx/networkx/pull/5288>`_]
  Improve performance of ``strongly_connected_components``.
- [`#5324 <https://github.com/networkx/networkx/pull/5324>`_]
  Add support for structured dtypes to ``to_numpy_array``.
- [`#5336 <https://github.com/networkx/networkx/pull/5336>`_]
  Add support for the `numpy.random.Generator` interface for random number
  generation.

API Changes
-----------

- The values in the dictionary returned by
  `~networkx.drawing.layout.rescale_layout_dict` are now `numpy.ndarray` objects
  instead of tuples. This makes the return type of ``rescale_layout_dict``
  consistent with that of all of the other layout functions.
- A ``FutureWarning`` has been added to ``google_matrix`` to indicate that the
  return type will change from a ``numpy.matrix`` object to a ``numpy.ndarray``
  in NetworkX 3.0.
- A ``FutureWarning`` has been added to ``attr_matrix`` to indicate that the
  return type will change from a ``numpy.matrix`` object to a ``numpy.ndarray``
  object in NetworkX 3.0.
- The ``is_*_matching`` functions now raise exceptions for nodes not in G in
  any edge.

Deprecations
------------

- [`#5055 <https://github.com/networkx/networkx/pull/5055>`_]
  Deprecate the ``random_state`` alias in favor of ``np_random_state``
- [`#5114 <https://github.com/networkx/networkx/pull/5114>`_]
  Deprecate the ``name`` kwarg from ``union`` as it isn't used.
- [`#5143 <https://github.com/networkx/networkx/pull/5143>`_]
  Deprecate ``euclidean`` in favor of ``math.dist``.
- [`#5166 <https://github.com/networkx/networkx/pull/5166>`_]
  Deprecate the ``hmn`` and ``lgc`` modules in ``node_classification``.
- [`#5262 <https://github.com/networkx/networkx/pull/5262>`_]
  Deprecate ``to_scipy_sparse_matrix`` and ``from_scipy_sparse_matrix`` in
  favor of ``to_scipy_sparse_array`` and ``from_scipy_sparse_array``, respectively.
- [`#5283 <https://github.com/networkx/networkx/pull/5283>`_]
  Deprecate ``make_small_graph`` and ``make_small_undirected_graph`` from the
  ``networkx.generators.small`` module.
- [`#5330 <https://github.com/networkx/networkx/pull/5330>`_]
  Deprecate ``to_numpy_recarray`` in favor of ``to_numpy_array`` with a
  structured dtype.
- [`#5341 <https://github.com/networkx/networkx/pull/5341>`_]
  Deprecate redundant ``info``.

Merged PRs
----------

A total of 166 changes have been committed.

- Support `comments=None` in read/parse edgelist (#5051)
- Add see also refs to de/stringizers in gml docstrings. (#5053)
- Add weisfeiler lehman subgraph hashing (#4946)
- Deprecate `random_state` decorator (#5055)
- Bug fix for issue #5023 :  corner-case bug in single_source_dijkstra (#5033)
- More informative GraphML exceptions (#5058)
- Minor updates to tutorial.rst and add docstring for data method of nodes/edges (#5039)
- Document `geometric_edges` and add it to main namespace (#5045)
- Fix small typo in `trophic_levels` documentation (#5087)
- Refactor `transitive_closure` (#5052)
- Fix fast_gnp_random_graph for directed graphs (issue #3389) (#5077)
- Get number of edges by calling the proper method (#5095)
- Update mentored projects section in docs (#5056)
- Parametrize shortest path node-checking tests. (#5078)
- Create FUNDING.yml
- Deprecate union name param (#5114)
- Update FUNDING.yml
- vertex_cover: Added support for self-loop nodes (#5104)
- Update core dev team (#5119)
- Faster operators in algorithms/operators/all.py (#5121)
- DOC: Add links to proposals for completed projects (#5122)
- Consistent return type in dictionary output of rescale_layout and rescale_layout_dict (#5091)
- Change exception varname e to err (#5130)
- minor tweaks in assortativity docs and code (#5129)
- Allow edge style to be a list of styles for DiGraphs (#5131)
- Add examples and minor documentation refactor for operators/binary.py (#5099)
- Improve random graphs test suite for gnp generators (issue #5092) (#5115)
- Add note about checking for path existence to all_simple_paths. (#5059)
- Fix message of raised exception in decorators. (#5136)
- Refactor linestyle test for FancyArrowPatches. (#5132)
- Drop Py37 (#5143)
- Use math.hypot (#5145)
- Add pyupgrade to pre-commit (#5146)
- Test on Python 3.10 (#4807)
- Use black 21.9b0 (#5148)
- Use sphinx 4.2 (#5150)
- Update example requirements (#5151)
- Update nx_pylab drawing edge color and width tests (#5134)
- Refactor node_classification to improve conciseness and readability (#5144)
- Add temporary pyparsing pin to fix CI. (#5156)
- Add option for arrowsize to be a list (#5154)
- List policies (#5159)
- Bugfix for issue 5123 (#5153)
- Test scipy and pandas on py3.10 (#5174)
- Deprecate `hmn` and `lgc` modules from the `node_classification` package (#5166)
- Rm passing ax.transOffset to LineCollection. (#5173)
- Add a function to find the negative cycle using bellman_ford (#5089)
- Add a Q&A to the contributor FAQ about algorithm acceptance policy. (#5177)
- DOC: Fix typo in docs for weighted shortest paths (#5181)
- Revert "Add temporary pyparsing pin to fix CI. (#5156)" (#5180)
- Only compute shortest path lengths when used (#5183)
- Add Mypy type checking infrastructure (#5127)
- xfail pydot tests. (#5187)
- Remove unused internal solver from algebraicconnectivity (#5190)
- Remove check/comment for scipy 1.1 behavior. (#5191)
- Test on Python 3.10 (#5185)
- Add regression test for ancestors/descendants w/ undir. G. (#5188)
- Rm internal function, use advanced indexing instead. (#5197)
- Fix missing import + tests in laplacian fns. (#5194)
- Investigate pre-release test failures (#5208)
- Rm assertion method in favor of assert statements. (#5214)
- Remove unused variable in mycielski.py (#5210)
- used queue instead of ordinary list (#5217)
- Add FutureWarning about matrix->array output to `google_matrix` (#5219)
- A few `np.matrix` cleanups (#5218)
- Rm internal laplacian in favor of laplacian_matrix. (#5196)
- [MRG] Create plot_subgraphs.py example (#5165)
- Add traveling salesman problem to example gallery (#4874)
- Fixed inconsistent documentation for nbunch parameter in DiGraph.edges() (#5037)
- Compatibility updates from testing with numpy/scipy/pytest rc's (#5226)
- Replace internal `close` fn with `math.isclose`. (#5224)
- Fix Python 3.10 deprecation warning w/ int div. (#5231)
- Touchups and suggestions for subgraph gallery example (#5225)
- Use new package name (#5234)
- Allowing None edges in weight function of bidirectional Dijkstra (#5232)
- Add an FAQ about assigning issues. (#5182)
- Update dev deps (#5243)
- Update minor doc issues with tex notation (#5244)
- Minor changes to speed up asynchronous label propagation for community detection. (#5247)
- Docstrings for the small.py module (#5240)
- Use scipy.sparse array datastructure (#5139)
- Update sphinx (#5272)
- Update year (#5273)
- Update extra dependencies (#5263)
- Update gexf website link in documentation (#5275)
- Update numpydoc (#5274)
- Initial setup of lazy_import functions. (#4909)
- Deprecate scipy sparse matrix conversion functions (#5262)
- Fix lowest_common_ancestors (issue #4942) (#5086)
- Make small graph generator node test more specific. (#5282)
- Use from_dict_of_lists instead of make_small_graph in generators.small (#5267)
- Refactor `to_numpy_array` with advanced indexing (#5250)
- Fix: Update louvain_partitions for threshold (update mod to new_mod in each level) (#5284)
- Add exception for unconnected graph (#5287)
- Fixing Tarjan's strongly connected components algorithm implementation to have `O(|E|+|V|)` time complexity instead of `O(|V|^3)`. (#5288)
- Add weights to karate club graph (#5285)
- Fix functions appearing in variables `__all__` but not in docs for NX2.7 (#5289)
- Update to stable version of black (#5296)
- Add FutureWarning to `attr_matrix` to notify users of return type change (#5300)
- DOC: change status to accepted for NXEP2, add resolution (#5297)
- Update test requirements (#5304)
- Update scipy (#5276)
- DOC: Update documentation to include callables for weight argument (#5307)
- Update pygraphviz (#5314)
- Document default dtype in to_numpy_recarray docstring. (#5315)
- Rm unused AbstractSet. (#5317)
- Deprecate `make_small_graph` and `make_small_undirected_graph` (#5283)
- Update `draw_<layout>` docstrings with usage examples (#5264)
- More numpy.matrix cleanups for NX2.7 (#5319)
- MAINT: Cleanup assortativity module, remove unused variables (#5301)
- Add informative exception for drawing multiedge labels. (#5316)
- Potential resolution to full paths to functions in docs (#5049)
- MAINT: Cleanup link analysis module, remove unused variables (#5306)
- Use pytest-mpl (#4579)
- Keep omega within [-1, 1] bounds (#5216)
- Add support for finding maximal cliques containing a set of nodes (#5172)
- MAINT: Remove unnecessary helper functions, use inbuilt methods for line graph generator (#5327)
- sampling from dict_keys objects is deprecated. (#5337)
- Add support for `numpy.random.Generator` (#5336)
- Update matching functions for error validation and speed (#4897)
- Update release requirements (#5338)
- Add structured dtypes to `to_numpy_array` (#5324)
- Deprecate `to_numpy_recarray` (#5330)
- First pass at 2.7 release notes. (#5342)
- Add pickle and yaml migration info (#5345)
- Deprecate info (#5341)
- Fix pandas warning (#5346)
- Test on 3.11-dev (#5339)
- Designate 2.7rc1 release
- Bump release version
- Update release process (#5348)
- Update mentored project info with the expected time commitment (#5349)
- Use np.random.default_rng in example + other updates. (#5356)
- Remove stuff conda doesn't support (#5361)
- Fix spiral_layout when equidistant=True (#5354)
- Fix docs (#5364)

Contributors
------------

- Will Badart
- Ross Barnowski
- Mathieu Bastian
- Martin Becker
- Anutosh Bhat
- Alejandro Candioti
- Divyansh
- Andrew Eckart
- Yossi Eliaz
- Casper van Elteren
- Simone Gasperini
- Daniel Haden
- Leo Klarner
- Andrew Knyazev
- Fabrizio Kuruc
- Paarth Madan
- Jarrod Millman
- Achille Nazaret
- NikHoh
- Sultan Orazbayev
- Dimitrios Papageorgiou
- Aishwarya Ramasethu
- Ryuki
- Katalin Schmidt
- Dan Schult
- Mridul Seth
- Cirus Thenter
- James Trimble
- Vadim
- Hnatiuk Vladyslav
- Aaron Z
- eskountis
- kpberry

# ===== SOURCE: https://raw.githubusercontent.com/networkx/networkx/main/doc/release/release_2.8.rst =====

NetworkX 2.8
============

Release date: 9 April 2022

Supports Python 3.8, 3.9, and 3.10

NetworkX is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex networks.

For more information, please visit our `website <https://networkx.org/>`_
and our :ref:`gallery of examples <examples_gallery>`.
Please send comments and questions to the `networkx-discuss mailing list
<http://groups.google.com/group/networkx-discuss>`_.

Highlights
----------

This release is the result of over five weeks of work with 48 pull requests by
18 contributors. This is the last release before NetworkX 3.0. For a preview of the
upcoming 3.0 release, please see the draft of our
`migration guide <https://networkx.org/documentation/latest/release/migration_guide_from_2.x_to_3.0.html>`_
for people moving from 2.X to 3.0.


Improvements
------------

- Correction to the treatment of directed graphs for `average_neighbor_degree`
  which used to sum the degrees of outgoing neighbors only but then divide by
  the number of "in" or "out" or "in+out" neighbors. So it wasn't even an average.
  The correction makes it an average degree of whatever population of neighbors
  is specified by `source` = "in" or "out" or "in+out".
  For example:

      >>> G = nx.path_graph(3, create_using=nx.DiGraph)
      >>> print(nx.average_neighbor_degree(G, source="in", target="in"))
      {0: 0.0, 1: 1.0, 2: 1.0}

  This used to produce `{0: 0.0, 1: 1.0, 2: 0.0}`
  Note: node 0 and 2 were treated nonsensically.
  Node 0 had calculated value 1/0 which was converted to 0.
  (numerator looking at successors while denominator counting predecessors)
  Node 2 had caluated value 0/1 = 0.0 (again succs on top, but preds in bottom)

  Now node 0 has calculated value 0.0/0 which we treat as 0.0. And node 2 has
  calculated value 1/1 = 1.0. Both handle the same nbrhood on top and bottom.

API Changes
-----------

- [`#5394 <https://github.com/networkx/networkx/pull/5394>`_]
  The function ``min_weight_matching`` no longer acts upon the parameter ``maxcardinality``
  because setting it to False would result in the min_weight_matching being no edges
  at all. The only reasonable option is True. The parameter will be removed completely in v3.0.

Deprecations
------------

- [`#5227 <https://github.com/networkx/networkx/pull/5227>`_]
  Deprecate the ``n_communities`` parameter name in ``greedy_modularity_communities``
  in favor of ``cutoff``.
- [`#5422 <https://github.com/networkx/networkx/pull/5422>`_]
  Deprecate ``extrema_bounding``. Use the related distance measures with
  ``usebounds=True`` instead.
- [`#5427 <https://github.com/networkx/networkx/pull/5427>`_]
  Deprecate ``dict_to_numpy_array1`` and ``dict_to_numpy_array2`` in favor of
  ``dict_to_numpy_array``, which handles both.
- [`#5428 <https://github.com/networkx/networkx/pull/5428>`_]
  Deprecate ``utils.misc.to_tuple``.


Merged PRs
----------

- Fix docs
- Fix release notes
- Bump release version
- Fix missing backticks (#5381)
- Add Generator support to create_py_random_state. (#5380)
- modularity_max: introduce enforce_n_communities parameter (#5227)
- First draft. (#5359)
- Updated MultiDiGraph documentation to include more examples of actually (#5387)
- Multigraph docs update (#5389)
- Updates to greedy_modularity_communities docs (#5390)
- Finish up NXEP 4 first draft (#5391)
- Correct typo in docstring (int -> float) (#5398)
- DOC: examples code blacks needs a blank line (#5401)
- Add support for multigraphs to nx.bridges. (#5397)
- Update extrema bounding method for compute="eccentricities" parameter (#5409)
- Add Tutte polynomial (#5265)
- Update sparse6 urls to use https (#5424)
- Deprecate extrema bounding (#5422)
- Add NXEP4 to developer toctree and fix broken links (#5420)
- Rm _inherit_doc - default behavior as of Python 3.5. (#5416)
- Minor improvements from general code readthrough (#5414)
- Ignore formatting changes with black, pep8 for git blame (#5405)
- Deprecate dict to numpy helpers (#5427)
- Deprecate `to_tuple` (#5430)
- Fix average_neighbor_degree calculations for directed graph (#5404)
- Parametrize tutte polynomial tests (#5431)
- Update black (#5438)
- Ignore black formatting (#5440)
- Update sphinx (#5439)
- Use https links for conference.scipy.org (#5441)
- Don't use graph6 with directed graphs (#5443) (#5444)
- Fix min_weight_matching to convert edge weights without reciprocal (#5394)
- Make sympy extra dep (#5454)
- Optimize prim for mst (#5455)
- Adding more examples for to_numpy_array method's usage (#5451)
- MAINT: Prim MST test didn't pass algorithm name to all unit tests (#5457)
- Fixed wrong dict factory usage on MultiDiGraph (#5456)
- added extra condition for fancy arrow colors (#5407)
- Update dependencies (#5468)
- Update release notes
- Designate 2.8rc1 release
- Bump release version
- DOCS: add some guidelines for references (#5476)
- Fix for issue 5212 (#5471)
- shortest_path() example (#5491)
- Rm incorrect reference from spiral_layout docstring. (#5503)
- Improve docstring for bethe_hessian_matrix (#5458)
- Add notes about NumPy/SciPy integration to NX 2->3 migration guide (#5505)
- Run black on docs (#5513)

Contributors
------------

- Ross Barnowski
- Riccardo Bucco
- Matthias Bussonnier
- FabianBall
- Martha Frysztacki
- Chris Keefe
- Lukong123
- Peter Mawhorter
- Lucas H. McCabe
- Jarrod Millman
- Sultan Orazbayev
- Dan Schult
- Seon82
- Mridul Seth
- Nikita Sharma
- Dilara Tekinoglu
- blokhinnv
- yusuf-csdev
