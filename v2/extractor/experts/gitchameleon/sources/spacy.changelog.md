# ===== RELEASE explosion/spaCy v3.5.0 =====

## ✨ New features and improvements

- **NEW:** New `apply`  [CLI command](https://spacy.io/api/cli#apply) to annotate new documents with a trained pipeline (#11376).
- **NEW:** New `benchmark`  [CLI command](https://spacy.io/api/cli#benchmark) to benchmark pipelines. The new `benchmark speed` subcommand measures the speed of a pipeline, the `benchmark accuracy` subcommand is a new alias for  `evaluate`  (#11902).
- **NEW:** New `find-threshold`  [CLI command](https://spacy.io/api/cli#find-threshold) to identify an optimal threshold for classification models (#11280).
- **NEW:** New `FUZZY`  `Matcher` operator for [fuzzy matches](https://spacy.io/usage/rule-based-matching#fuzzy) based on Levenshtein edit distance. In addition, the `FUZZY` and `REGEX` operators are now supported in combination with `IN`/`NOT_IN`. (#11359).
- Language updates for Ancient Greek, Dutch, Russian, Slovenian and Ukrainian (#11345, #11162, #11426, #11753, #11811, #11997, more details below).
- Allow up to `typer` v0.7.x (#11720), `mypy` 0.990 (#11801) and `typing_extensions` v4.4.x (#12036).
- New `spacy.ConsoleLogger.v3` with expanded progress [tracking](https://spacy.io/api/top-level#ConsoleLogger) (#11972).
- Improved scoring behavior for `textcat` with `spacy.textcat_scorer.v2` (#11696 and #11971) and `spacy.textcat_multilabel_scorer.v2` (#11820).
- Improved customizability of the knowledge base used for entity linking, with the default implementation being the new [`InMemoryLookupKB`](https://spacy.io/api/inmemorylookupkb) (#11268).
- Optional `before_update` callback that is invoked at the start of each [training step](https://spacy.io/api/data-formats#config-training) (#11739).
- Improve performance of `SpanGroup` (#11380).
- Improve UX around `displacy.serve` when the default port is in use (#11948).
- Patch a [security vulnerability](https://github.com/advisories/GHSA-gw9q-c7gh-j9vm) in extracting tar files (#11746).
- Add equality definition for vectors (#11806).
- Allow interpolation of variables in directory names in projects (#11235).
- Update default component configs to use the latest `tok2vec` version (#11618).

## 🔴 Bug fixes

- #11382: Fix lookup behavior for the French and Catalan lemmatizers.
- #11385: Ensure that downstream components can train properly on a frozen `tok2vec` or `transformer` layer.
- #11762: Support local file system [remotes](https://spacy.io/usage/projects#remote) for projects.
- #11763: Raise an error when unsupported values are used for `textcat`.
- #11834: Ensure `Vocab.to_disk` respects the exclude setting for `lookups` and `vectors`.
- #12009: Fix a few typing issues for `SpanGroup` and `Span` objects. 
- #12098: Correctly handle missing annotations in the edit tree lemmatizer.

## ⚠️ Backwards incompatibilities and model updates

The following changes may require you to update code that is using the relevant functionality:

- An error is now raised when unsupported values are given as input to train a `textcat` or `textcat_multilabel` model - ensure that values are 0.0 or 1.0 as explained in the [docs](https://spacy.io/api/textcategorizer#assigned-attributes).
- As `KnowledgeBase` is now an abstract class, you should call the constructor of the new [`InMemoryLookupKB`](https://spacy.io/api/inmemorylookupkb) instead when you want to use spaCy's default KB implementation. If you've written a custom KB that inherits from [`KnowledgeBase`](https://spacy.io/api/kb), you'll need to implement its abstract methods, or alternatively inherit from `InMemoryLookupKB` instead.

The following changes may influence the output of your language pipeline or trained models:

- Updates to language defaults:
    - Extended support for Slovenian (#11162).
    - Switch Russian and Ukrainian lemmatizers to `pymorphy3` (#11345, #11811).
    - Support for editorial punctuation in Ancient Greek (#11426).
    - Update to Russian tokenizer exceptions (#11753).
    - Small fix in the list of Dutch stop words (#11997).
- Updates to model defaults:
    - Use the latest `tok2vec` defaults in all components (#11618).
    - Improve the default attributes used for the `textcat` and `textcat_multilabel` components (#11698).
    - Update the default scorer for `textcat` and `textcat_multilabel` to fix a bug related to `threshold` for `textcat` and to make it possible to score multiple `textcat`/`textcat_multilabel` components in a single pipeline with custom scorers. If no custom scorers are used, the `cat_p/r/f` scores will now only reflect the final component's labels and performance (#11696, #11820).
    - Correct the `token_acc` score to report the intended measure (`# correct tokens / # predicted tokens`, the same as in spaCy v2). The `token_acc` scores for v3.5 will be lower for the same performance because they were incorrectly inflated in v3.0-v3.4. The `token_p/r/f` scores should remain unchanged (#12073).

The following functionality will be changed in the near future - so it's best to start updating your scripts now to make them more generic:

- From v4 onwards, we'll rename the `master` branch to `main`.

## 📦 Trained pipelines updates

- The CNN pipelines add `IS_SPACE` as a `tok2vec` feature for `tagger` and `morphologizer` components to improve tagging of non-whitespace vs. whitespace tokens.
- The transformer pipelines require `spacy-transformers` v1.2, which uses the exact alignment from `tokenizers` for fast tokenizers instead of the heuristic alignment from `spacy-alignments`. For all trained pipelines except `ja_core_news_trf`, the alignments between spaCy tokens and transformer tokens may be slightly different. More details about the `spacy-transformers` changes in the [v1.2.0 release notes](https://github.com/explosion/spacy-transformers/releases/tag/v1.2.0).

## 📖 Documentation and examples

- We've ported our website from Gatsby to Next 🥳
- Updated the documentation on [supported languages](https://spacy.io/usage/models#languages).
- Added a note about experimental M1 GPU support to the [installation quickstart](https://spacy.io/usage).
- Included documentation for the `biluo_to_iob` and `iob_to_biluo`  functions.
- Fixed model links in the [v3.4 usage documentation](https://spacy.io/usage/v3-4).
- Removed "new" tags of functionality from spaCy v2.x.
- Various small additions, spelling and typo fixes.
- spaCy [Universe](https://spacy.io/universe) additions:
    - [greCy](https://spacy.io/universe/project/grecy): Providing Ancient Greek models
    - [spacy-pythainlp](https://spacy.io/universe/project/spacy-pythainlp): Add Thai support for spaCy
- New [projects](https://spacy.io/usage/projects):
    - [Accelerate NER with Speedster](https://github.com/explosion/projects/tree/v3/experimental/ner_wikiner_speedster) (experimental)

## 👥 Contributors

@aaronzipp, @adrianeboyd, @albertvillanova, @ArchiDevil, @cfuerbachersparks, @damian-romero, @danieldk, @darigovresearch, @DSLituiev, @essenmitsosse, @gremur, @honnibal, @ines, @jmyerston, @JosPolfliet, @kadarakos, @koaning, @kwhumphreys, @ljvmiranda921, @MarcoGorelli, @orglce, @pmbaumgartner, @polm, @richardpaulhudson, @rmitsch, @ryndaniels, @shadeMe, @svlandeg, @thomashacker, @TrellixVulnTeam, @wannaphong, @zhiiw, @zrpxx
