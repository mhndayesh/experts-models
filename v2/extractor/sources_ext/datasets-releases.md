# HF datasets releases (v3-v4)

## 4.8.5 (2026-04-27T15:46:14Z)

## Main bug fixes
* fix: decode Json() values before calling DataFrame.to_json() (#8116) by @Brianzhengca in https://github.com/huggingface/datasets/pull/8122
* Fix: decode JSON type before to_list or to_dict is called by @ItsTania in https://github.com/huggingface/datasets/pull/8137
* Fix batching for table-formatted datasets by @bluehyena in https://github.com/huggingface/datasets/pull/8126
* Fix iterable map resume state by @Brianzhengca in https://github.com/huggingface/datasets/pull/8147
* don't embed remote files in download_and_prepare to parquet by @lhoestq in https://github.com/huggingface/datasets/pull/8150

## Other improvements and bug fixes
* Parse agent traces by @lhoestq in https://github.com/huggingface/datasets/pull/8113
* ðŸ”’ Pin GitHub Actions to commit SHAs by @paulinebm in https://github.com/huggingface/datasets/pull/8114
* chore: bump doc-builder SHA for PR upload workflow by @rtrompier in https://github.com/huggingface/datasets/pull/8134
* Remove print statement in JSON processing by @lhoestq in https://github.com/huggingface/datasets/pull/8136
* Don't include files list DatasetInfo (and remove old stuff) by @lhoestq in https://github.com/huggingface/datasets/pull/8128
* update ci uer by @lhoestq in https://github.com/huggingface/datasets/pull/8139
* fix warning in ci by @lhoestq in https://github.com/huggingface/datasets/pull/8140
* fix mask in embed_storage for remote files by @lhoestq in https://github.com/huggingface/datasets/pull/8151
* fix original_files missing in ci json test by @lhoestq in https://github.com/huggingface/datasets/pull/8152
* Fix null in embed storage by @lhoestq in https://github.com/huggingface/datasets/pull/8154
* Fix base_path in integration tests by @lhoestq in https://github.com/huggingface/datasets/pull/8155

## New Contributors
* @paulinebm made their first contribution in https://github.com/huggingface/datasets/pull/8114
* @Brianzhengca made their first contribution in https://github.com/huggingface/datasets/pull/8122
* @bluehyena made their first contribution in https://github.com/huggingface/datasets/pull/8126
* @rtrompier made their first contribution in https://github.com/huggingface/datasets/pull/8134
* @ItsTania made their first contribution in https://github.com/huggingface/datasets/pull/8137

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.8.4...4.8.5

## 4.8.4 (2026-03-23T14:21:52Z)

## What's Changed
* Support latest torchvision by @lhoestq in https://github.com/huggingface/datasets/pull/8087
* fix regression when loading JSON with one file = one object by @lhoestq in https://github.com/huggingface/datasets/pull/8086


**Full Changelog**: https://github.com/huggingface/datasets/compare/4.8.3...4.8.4

## 4.8.3 (2026-03-19T17:44:39Z)

## What's Changed
* Fix split_dataset_by_node step by @lhoestq in https://github.com/huggingface/datasets/pull/8081
* Fix docstring of Json.cast_storage by @albertvillanova in https://github.com/huggingface/datasets/pull/8080


**Full Changelog**: https://github.com/huggingface/datasets/compare/4.8.2...4.8.3

## 4.8.2 (2026-03-17T01:10:32Z)

## What's Changed
* Json type for empty struct by @lhoestq in https://github.com/huggingface/datasets/pull/8074


**Full Changelog**: https://github.com/huggingface/datasets/compare/4.8.1...4.8.2

## 4.8.1 (2026-03-17T00:13:34Z)

## What's Changed
* Fix formatted iter arrow double yield by @HaukurPall in https://github.com/huggingface/datasets/pull/8063


**Full Changelog**: https://github.com/huggingface/datasets/compare/4.8.0...4.8.1

## 4.8.0 (2026-03-16T23:52:47Z)

## Dataset Features
* Read (and write) from [HF Storage Buckets](https://huggingface.co/storage): load raw data, process and save to Dataset Repos by @lhoestq in https://github.com/huggingface/datasets/pull/8064

  ```python
  from datasets import load_dataset
  # load raw data from a Storage Bucket on HF
  ds = load_dataset("buckets/username/data-bucket", data_files=["*.jsonl"])
  # or manually, using hf:// paths
  ds = load_dataset("json", data_files=["hf://buckets/username/data-bucket/*.jsonl"])
  # process, filter
  ds = ds.map(...).filter(...)
  # publish the AI-ready dataset
  ds.push_to_hub("username/my-dataset-ready-for-training")
  ```

  This also fixes multiprocessed push_to_hub on macos that was causing segfault (now it uses spawn instead of fork).
  And it bumps `dill` and `multiprocess` versions to support python 3.14
* Datasets streaming iterable packaged improvements and fixes by @Michael-RDev in https://github.com/huggingface/datasets/pull/8068
  * added `max_shard_size` to IterableDataset.push_to_hub (but requires iterating twice to know the full dataset twice - improvements are welcome)
  * more arrow-native iterable operations for IterableDataset
  * better support of glob patterns in archives, e.g. `zip://*.jsonl::hf://datasets/username/dataset-name/data.zip`
  * fixes for to_pandas, videofolder, load_dataset_builder kwargs

## What's Changed
* fix reshard_data_sources by @lhoestq in https://github.com/huggingface/datasets/pull/8061
* Improve error message for invalid data_files pattern format by @kushalkkb in https://github.com/huggingface/datasets/pull/8060
* fix null filling in missing jsonl columns by @lhoestq in https://github.com/huggingface/datasets/pull/8069

## New Contributors
* @kushalkkb made their first contribution in https://github.com/huggingface/datasets/pull/8060
* @Michael-RDev made their first contribution in https://github.com/huggingface/datasets/pull/8068

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.7.0...4.8.0

## 4.7.0 (2026-03-09T19:09:25Z)

## Datasets Features
* Add `Json()` type by @lhoestq in https://github.com/huggingface/datasets/pull/8027
  * JSON Lines files that contain arbitrary JSON objects like tool calling datasets are now supported. When there is a field or subfield containing mixed types (e.g. mix of str/int/float/dict/list or dictionaries with arbitrary keys), the `Json()`type is used to store such data that would normally not be supported in Arrow/Parquet
  * Use the `Json()` type in `Features()` for any dataset, it is supported in any functions that accepts `features=`like `load_dataset()`, `.map()`, `.cast()`, `.from_dict()`, `.from_list()`
  * Use `on_mixed_types="use_json"` to automatically set the `Json()` type on mixed types in `.from_dict()`, `.from_list()` and `.map()`

Examples:

You can use `on_mixed_types="use_json"` or specify `features=` with a [`Json`] type:

```python
>>> ds = Dataset.from_dict({"a": [0, "foo", {"subfield": "bar"}]})
Traceback (most recent call last):
  ...
  File "pyarrow/error.pxi", line 92, in pyarrow.lib.check_status
pyarrow.lib.ArrowInvalid: Could not convert 'foo' with type str: tried to convert to int64

>>> features = Features({"a": Json()})
>>> ds = Dataset.from_dict({"a": [0, "foo", {"subfield": "bar"}]}, features=features)
>>> ds.features
{'a': Json()}
>>> list(ds["a"])
[0, "foo", {"subfield": "bar"}]
```

This is also useful for lists of dictionaries with arbitrary keys and values, to avoid filling missing fields with None:

```python
>>> ds = Dataset.from_dict({"a": [[{"b": 0}, {"c": 0}]]})
>>> ds.features
{'a': List({'b': Value('int64'), 'c': Value('int64')})}
>>> list(ds["a"])
[[{'b': 0, 'c': None}, {'b': None, 'c': 0}]]  # missing fields are filled with None

>>> features = Features({"a": List(Json())})
>>> ds = Dataset.from_dict({"a": [[{"b": 0}, {"c": 0}]]}, features=features)
>>> ds.features
{'a': List(Json())}
>>> list(ds["a"])
[[{'b': 0}, {'c': 0}]]  # OK
```

Another example with tool calling data and the `on_mixed_types="use_json"` argument (useful to not have to specify `features=` manually):

```python
>>> messages = [
...     {"role": "user", "content": "Turn on the living room lights and play my electronic music playlist."},
...     {"role": "assistant", "tool_calls": [
...         {"type": "function", "function": {
...             "name": "control_light",
...             "arguments": {"room": "living room", "state": "on"}
...         }},
...         {"type": "function", "function": {
...             "name": "play_music",
...             "arguments": {"playlist": "electronic"}  # mixed-type here since keys ["playlist"] and ["room", "state"] are different
...         }}]
...     },
...     {"role": "tool", "name": "control_light", "content": "The lights in the living room are now on."},
...     {"role": "tool", "name": "play_music", "content": "The music is now playing."},
...     {"role": "assistant", "content": "Done!"}
... ]
>>> ds = Dataset.from_dict({"messages": [messages]}, on_mixed_types="use_json")
>>> ds.features
{'messages': List({'role': Value('string'), 'content': Value('string'), 'tool_calls': List(Json()), 'name': Value('string')})}
>>> ds[0][1]["tool_calls"][0]["function"]["arguments"]
{"room": "living room", "state": "on"}
```


## What's Changed
* Fix typos in iterable_dataset.py by @omkar-334 in https://github.com/huggingface/datasets/pull/8049
* Fix non-deterministic by sorting metadata extensions (#8034) by @Nexround in https://github.com/huggingface/datasets/pull/8039
* Use num_examples instead of len(self) for iterable_dataset's SplitInfo by @HaukurPall in https://github.com/huggingface/datasets/pull/8041
* Fix silent data loss in push_to_hub when num_proc > num_shards by @HaukurPall in https://github.com/huggingface/datasets/pull/8044
* Don't extract bad files by @lhoestq in https://github.com/huggingface/datasets/pull/8056
* fix(iterable_dataset): preserve features when chaining filter() on typed IterableDataset by @s-zx in https://github.com/huggingface/datasets/pull/8053
* fix: handle nested null types in feature alignment for multi-proc map by @ain-soph in https://github.com/huggingface/datasets/pull/8047
* Fix unstable tokenizer fingerprinting (enables map cache reuse) by @KOKOSde in https://github.com/huggingface/datasets/pull/7982
* Limit dataset listing to first 20 entries in readme by @lhoestq in https://github.com/huggingface/datasets/pull/8057

## New Contributors
* @omkar-334 made their first contribution in https://github.com/huggingface/datasets/pull/8049
* @Nexround made their first contribution in https://github.com/huggingface/datasets/pull/8039
* @HaukurPall made their first contribution in https://github.com/huggingface/datasets/pull/8041
* @s-zx made their first contribution in https://github.com/huggingface/datasets/pull/8053
* @ain-soph made their first contribution in https://github.com/huggingface/datasets/pull/8047
* @KOKOSde made their first contribution in https://github.com/huggingface/datasets/pull/7982

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.6.1...4.7.0

## 4.6.1 (2026-02-27T23:27:26Z)

## Bug fix
* Remove tmp file in push to hub by @lhoestq in https://github.com/huggingface/datasets/pull/8030


**Full Changelog**: https://github.com/huggingface/datasets/compare/4.6.0...4.6.1

## 4.6.0 (2026-02-25T12:15:45Z)

## Dataset Features
* Support Image, Video and Audio types in Lance datasets
  * Infer types from lance blobs by @lhoestq in https://github.com/huggingface/datasets/pull/7966
 
  ```python
  >>> from datasets import load_dataset
  >>> ds = load_dataset("lance-format/Openvid-1M", streaming=True, split="train")
  >>> ds.features
  {'video_blob': Video(),
   'video_path': Value('string'),
   'caption': Value('string'),
   'aesthetic_score': Value('float64'),
   'motion_score': Value('float64'),
   'temporal_consistency_score': Value('float64'),
   'camera_motion': Value('string'),
   'frame': Value('int64'),
   'fps': Value('float64'),
   'seconds': Value('float64'),
   'embedding': List(Value('float32'), length=1024)}
  ```
* Push to hub now supports Video types
  * push_to_hub() for videos by @lhoestq in https://github.com/huggingface/datasets/pull/7971
  
  ```python
   >>> from datasets import Dataset, Video
  >>> ds = Dataset.from_dict({"video": ["path/to/video.mp4"]})
  >>> ds = ds.cast_column("video", Video())
  >>> ds.push_to_hub("username/my-video-dataset")
  ```
* Write image/audio/video blobs as is in parquet (PLAIN) in `push_to_hub()` by @lhoestq in https://github.com/huggingface/datasets/pull/7976
  * this enables cross-format Xet deduplication for image/audio/video, e.g. deduplicate videos between Lance, WebDataset, Parquet files and plain video files and make downloads and uploads faster to Hugging Face
  * E.g. if you convert a Lance video dataset to a Parquet video dataset on Hugging Face, the upload will be much faster since videos don't need to be reuploaded. Under the hood, the Xet storage reuses the binary chunks from the videos in Lance format for the videos in Parquet format
  * See more info here: https://huggingface.co/docs/hub/en/xet/deduplication
  
<p align="center">
<a href="https://huggingface.co/docs/hub/en/xet/deduplication">
<img height="200" alt="image" src="https://github.com/user-attachments/assets/dd0de6a2-24a1-4945-8d25-44b763c1151e" />
</a>
</p>

* Add `IterableDataset.reshard()` by @lhoestq in https://github.com/huggingface/datasets/pull/7992

  Reshard the dataset if possible, i.e. split the current shards further into more shards.
  This increases the number of shards and the resulting dataset has num_shards >= previous_num_shards.
  Equality may happen if no shard can be split further.

  The resharding mechanism depends on the dataset file format:

    * Parquet: shard per row group instead of per file
    * Other: not implemented yet (contributions are welcome !)

  ```python
  >>> from datasets import load_dataset
  >>> ds = load_dataset("fancyzhx/amazon_polarity", split="train", streaming=True)
  >>> ds
  IterableDataset({
      features: ['label', 'title', 'content'],
      num_shards: 4
  })
  >>> ds.reshard()
  IterableDataset({
      features: ['label', 'title', 'content'],
      num_shards: 3600
  })
  ```

## What's Changed
* Fix load_from_disk progress bar with redirected stdout by @omarfarhoud in https://github.com/huggingface/datasets/pull/7919
* Revert "feat: avoid some copies in torch formatter (#7787)" by @lhoestq in https://github.com/huggingface/datasets/pull/7961
* docs: fix grammar and add type hints in splits.py by @Edge-Explorer in https://github.com/huggingface/datasets/pull/7960
* Fix interleave_datasets with all_exhausted_without_replacement strategy by @prathamk-tw in https://github.com/huggingface/datasets/pull/7955
* Add examples for Lance datasets by @prrao87 in https://github.com/huggingface/datasets/pull/7950
* Support null in json string cols by @lhoestq in https://github.com/huggingface/datasets/pull/7963
* handle blob lance by @lhoestq in https://github.com/huggingface/datasets/pull/7964
* Count examples in lance by @lhoestq in https://github.com/huggingface/datasets/pull/7969
* Use temp files in push_to_hub to save memory by @lhoestq in https://github.com/huggingface/datasets/pull/7979
* Drop python 3.9 by @lhoestq in https://github.com/huggingface/datasets/pull/7980
* Support pandas 3 by @lhoestq in https://github.com/huggingface/datasets/pull/7981
* Remove unused data files optims by @lhoestq in https://github.com/huggingface/datasets/pull/7985
* Remove pre-release workaround in CI for `transformers v5` and `huggingface_hub v1` by @hanouticelina in https://github.com/huggingface/datasets/pull/7989
* very basic support for more hf urls by @lhoestq in https://github.com/huggingface/datasets/pull/8003
* Bump fsspec upper bound to 2026.2.0 (fixes #7994) by @jayzuccarelli in https://github.com/huggingface/datasets/pull/7995
* Fix: make environment variable naming consistent (issue #7998) by @AnkitAhlawat7742 in https://github.com/huggingface/datasets/pull/8000
* More IterableDataset.from_x methods and docs and polars.Lazyframe support by @lhoestq in https://github.com/huggingface/datasets/pull/8009
* Support empty shard in from_generator by @lhoestq in https://github.com/huggingface/datasets/pull/8023
* Allow import polars in map() by @lhoestq in https://github.com/huggingface/datasets/pull/8024

## New Contributors
* @omarfarhoud made their first contribution in https://github.com/huggingface/datasets/pull/7919
* @Edge-Explorer made their first contribution in https://github.com/huggingface/datasets/pull/7960
* @prathamk-tw made their first contribution in https://github.com/huggingface/datasets/pull/7955
* @prrao87 made their first contribution in https://github.com/huggingface/datasets/pull/7950
* @hanouticelina made their first contribution in https://github.com/huggingface/datasets/pull/7989
* @jayzuccarelli made their first contribution in https://github.com/huggingface/datasets/pull/7995
* @AnkitAhlawat7742 made their first contribution in https://github.com/huggingface/datasets/pull/8000

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.5.0...4.6.0

## 4.5.0 (2026-01-14T18:33:15Z)

## Dataset Features
* Add lance format support by @eddyxu in https://github.com/huggingface/datasets/pull/7913
  * Support for both Lance dataset (including metadata / manifests) and standalone .lance files
  * e.g. with [lance-format/fineweb-edu](https://huggingface.co/datasets/lance-format/fineweb-edu)

  ```python
  from datasets import load_dataset

  ds = load_dataset("lance-format/fineweb-edu", streaming=True)
  for example in ds["train"]:
      ...
  ```

## What's Changed

* Raise early for invalid `revision` in `load_dataset` by @Scott-Simmons in https://github.com/huggingface/datasets/pull/7929
* fix low but large example indexerror by @CloseChoice in https://github.com/huggingface/datasets/pull/7912
* Fix method to retrieve attributes from file object by @lhoestq in https://github.com/huggingface/datasets/pull/7938
* add _OverridableIOWrapper by @lhoestq in https://github.com/huggingface/datasets/pull/7942
* Add _generate_shards by @lhoestq in https://github.com/huggingface/datasets/pull/7943

## New Contributors
* @eddyxu made their first contribution in https://github.com/huggingface/datasets/pull/7913
* @Scott-Simmons made their first contribution in https://github.com/huggingface/datasets/pull/7929

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.4.2...4.5.0

## 4.4.2 (2025-12-19T15:05:34Z)

## Bug fixes
* Fix embed storage nifti by @CloseChoice in https://github.com/huggingface/datasets/pull/7853
* ArXiv -> HF Papers by @qgallouedec in https://github.com/huggingface/datasets/pull/7855
* fix some broken links by @julien-c in https://github.com/huggingface/datasets/pull/7859
* Nifti visualization support by @CloseChoice in https://github.com/huggingface/datasets/pull/7874
* Replace papaya with niivue by @CloseChoice in https://github.com/huggingface/datasets/pull/7878
* Fix 7846: add_column and add_item erroneously(?) require new_fingerprint parameter  by @sajmaru in https://github.com/huggingface/datasets/pull/7884
* fix(fingerprint): treat TMPDIR as strict API and fail (Issue #7877) by @ada-ggf25 in https://github.com/huggingface/datasets/pull/7891
* encode nifti correctly when uploading lazily by @CloseChoice in https://github.com/huggingface/datasets/pull/7892
* fix(nifti): enable lazy loading for Nifti1ImageWrapper by @The-Obstacle-Is-The-Way in https://github.com/huggingface/datasets/pull/7887

## Minor additions
* Add type overloads to load_dataset for better static type inference by @Aditya2755 in https://github.com/huggingface/datasets/pull/7888
* Add inspect_ai eval logs support by @lhoestq in https://github.com/huggingface/datasets/pull/7899
* Save input shard lengths by @lhoestq in https://github.com/huggingface/datasets/pull/7897
* Don't save original_shard_lengths by default for backward compat by @lhoestq in https://github.com/huggingface/datasets/pull/7906

## New Contributors
* @sajmaru made their first contribution in https://github.com/huggingface/datasets/pull/7884
* @Aditya2755 made their first contribution in https://github.com/huggingface/datasets/pull/7888
* @ada-ggf25 made their first contribution in https://github.com/huggingface/datasets/pull/7891
* @The-Obstacle-Is-The-Way made their first contribution in https://github.com/huggingface/datasets/pull/7887

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.4.1...4.4.2

## 4.4.1 (2025-11-05T16:01:38Z)

## Bug fixes and improvements
* Better streaming retries (504 and 429) by @lhoestq in https://github.com/huggingface/datasets/pull/7847
* DOC: remove mode parameter in docstring of pdf and video feature by @CloseChoice in https://github.com/huggingface/datasets/pull/7848


**Full Changelog**: https://github.com/huggingface/datasets/compare/4.4.0...4.4.1

## 4.4.0 (2025-11-04T10:42:47Z)

## Dataset Features
* Add nifti support by @CloseChoice in https://github.com/huggingface/datasets/pull/7815
  * Load medical imaging datasets from Hugging Face:

  ```python
  ds = load_dataset("username/my_nifti_dataset")
  ds["train"][0]  # {"nifti": <nibabel.nifti1.Nifti1Image>}
  ```
  * Load medical imaging datasets from your disk:

  ```python
  files = ["/path/to/scan_001.nii.gz", "/path/to/scan_002.nii.gz"]
  ds = Dataset.from_dict({"nifti": files}).cast_column("nifti", Nifti())
  ds["train"][0]  # {"nifti": <nibabel.nifti1.Nifti1Image>}
  ```

  * Documentation: https://huggingface.co/docs/datasets/nifti_dataset
* Add num channels to audio by @CloseChoice in https://github.com/huggingface/datasets/pull/7840

```python
# samples have shape (num_channels, num_samples)
ds = ds.cast_column("audio", Audio())  # default, use all channels
ds = ds.cast_column("audio", Audio(num_channels=2))  # use stereo
ds = ds.cast_column("audio", Audio(num_channels=1))  # use mono
```

* Python 3.14 support by @lhoestq in https://github.com/huggingface/datasets/pull/7836

## What's Changed
* Fix random seed on shuffle and interleave_datasets by @CloseChoice in https://github.com/huggingface/datasets/pull/7823
* fix ci compressionfs by @lhoestq in https://github.com/huggingface/datasets/pull/7830
* fix: better args passthrough for `_batch_setitems()` by @sghng in https://github.com/huggingface/datasets/pull/7817
* Fix: Properly render [!TIP] block in stream.shuffle documentation by @art-test-stack in https://github.com/huggingface/datasets/pull/7833
* resolves the ValueError: Unable to avoid copy while creating an array by @ArjunJagdale in https://github.com/huggingface/datasets/pull/7831
* fix column with transform by @lhoestq in https://github.com/huggingface/datasets/pull/7843
* support fsspec 2025.10.0 by @lhoestq in https://github.com/huggingface/datasets/pull/7844

## New Contributors
* @sghng made their first contribution in https://github.com/huggingface/datasets/pull/7817
* @art-test-stack made their first contribution in https://github.com/huggingface/datasets/pull/7833

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.3.0...4.4.0

## 4.3.0 (2025-10-23T16:33:59Z)

## Dataset Features

Enable large scale distributed dataset streaming:

* Keep hffs cache in workers when streaming by @lhoestq in https://github.com/huggingface/datasets/pull/7820
* Retry open hf file by @lhoestq in https://github.com/huggingface/datasets/pull/7822

These improvements require `huggingface_hub>=1.1.0` to take full effect

## What's Changed
* fix conda deps by @lhoestq in https://github.com/huggingface/datasets/pull/7810
* Add pyarrow's binary view to features by @delta003 in https://github.com/huggingface/datasets/pull/7795
* Fix polars cast column image by @CloseChoice in https://github.com/huggingface/datasets/pull/7800
* Allow streaming hdf5 files by @lhoestq in https://github.com/huggingface/datasets/pull/7814
* Fix batch_size default description in to_polars docstrings by @albertvillanova in https://github.com/huggingface/datasets/pull/7824
* docs: document_dataset PDFs & OCR by @ethanknights in https://github.com/huggingface/datasets/pull/7812
* Add custom fingerprint support to `from_generator` by @simonreise in https://github.com/huggingface/datasets/pull/7533
* picklable batch_fn by @lhoestq in https://github.com/huggingface/datasets/pull/7826

## New Contributors
* @delta003 made their first contribution in https://github.com/huggingface/datasets/pull/7795
* @CloseChoice made their first contribution in https://github.com/huggingface/datasets/pull/7800
* @ethanknights made their first contribution in https://github.com/huggingface/datasets/pull/7812
* @simonreise made their first contribution in https://github.com/huggingface/datasets/pull/7533

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.2.0...4.3.0

## 4.2.0 (2025-10-09T16:18:22Z)

## Dataset Features
* Sample without replacement option when interleaving datasets by @radulescupetru in https://github.com/huggingface/datasets/pull/7786

  ```python
  ds = interleave_datasets(datasets, stopping_strategy="all_exhausted_without_replacement")
  ```

* Parquet: add `on_bad_files` argument to error/warn/skip bad files by @lhoestq in https://github.com/huggingface/datasets/pull/7806

  ```python
  ds = load_dataset(parquet_dataset_id, on_bad_files="warn")
  ```

* Add parquet scan options and docs by @lhoestq in https://github.com/huggingface/datasets/pull/7801

  * docs to select columns and filter data efficiently

  ```python
  ds = load_dataset(parquet_dataset_id, columns=["col_0", "col_1"])
  ds = load_dataset(parquet_dataset_id, filters=[("col_0", "==", 0)])
  ```
  * new argument to control buffering and caching when streaming

  ```python
  fragment_scan_options = pyarrow.dataset.ParquetFragmentScanOptions(cache_options=pyarrow.CacheOptions(prefetch_limit=1, range_size_limit=128 << 20))
  ds = load_dataset(parquet_dataset_id, streaming=True, fragment_scan_options=fragment_scan_options)
  ```

## What's Changed
* Document HDF5 support by @klamike in https://github.com/huggingface/datasets/pull/7740
* update tips in docs by @lhoestq in https://github.com/huggingface/datasets/pull/7790
* feat: avoid some copies in torch formatter by @drbh in https://github.com/huggingface/datasets/pull/7787
* Support huggingface_hub v0.x and v1.x by @Wauplin in https://github.com/huggingface/datasets/pull/7783
* Define CI future by @lhoestq in https://github.com/huggingface/datasets/pull/7799
* More Parquet streaming docs by @lhoestq in https://github.com/huggingface/datasets/pull/7803
* Less api calls when resolving data_files by @lhoestq in https://github.com/huggingface/datasets/pull/7805
* typo by @lhoestq in https://github.com/huggingface/datasets/pull/7807

## New Contributors
* @drbh made their first contribution in https://github.com/huggingface/datasets/pull/7787

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.1.1...4.2.0

## 4.1.1 (2025-09-18T13:15:08Z)

## What's Changed
* fix iterate nested field by @lhoestq in https://github.com/huggingface/datasets/pull/7775
* Add support for arrow iterable when concatenating or interleaving by @radulescupetru in https://github.com/huggingface/datasets/pull/7771
* fix empty dataset to_parquet by @lhoestq in https://github.com/huggingface/datasets/pull/7779

## New Contributors
* @radulescupetru made their first contribution in https://github.com/huggingface/datasets/pull/7771

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.1.0...4.1.1

## 4.1.0 (2025-09-15T16:41:46Z)

## Dataset Features
* feat: use content defined chunking  by @kszucs in https://github.com/huggingface/datasets/pull/7589
  * Parquet datasets are now [Optimized Parquet](https://huggingface.co/docs/hub/datasets-libraries#optimized-parquet-files) !
   <img width="462" height="103" alt="image" src="https://github.com/user-attachments/assets/43703a47-0964-421b-8f01-1a790305de79" />

  * internally uses `use_content_defined_chunking=True` when writing Parquet files
  * this enables fast deduped uploads to Hugging Face !
  
  ```python
  # Now faster thanks to content defined chunking
  ds.push_to_hub("username/dataset_name")
  ```
  * this optimizes Parquet for Xet, the dedupe-based storage backend of Hugging Face. It allows to not have to upload data that already exist somewhere on HF (on an other file / version for example). Parquet content defined chunking defines Parquet pages boundaries based on the content of the data, in order to detect duplicate data easily.
  * with this change, the new default row group size for Parquet is set to 100MB
  * `write_page_index=True` is also used to enable fast random access for the Dataset Viewer and tools that need it
* Concurrent push_to_hub by @lhoestq in https://github.com/huggingface/datasets/pull/7708
* Concurrent IterableDataset push_to_hub by @lhoestq in https://github.com/huggingface/datasets/pull/7710
* HDF5 support by @klamike in https://github.com/huggingface/datasets/pull/7690
  * load HDF5 datasets in one line of code
  ```python
  ds = load_dataset("username/dataset-with-hdf5-files")
  ```
  * each (possibly nested) field in the HDF5 file is parsed a a column, with the first dimension used for rows

## Other improvements and bug fixes
* Convert to string when needed + faster .zstd by @lhoestq in https://github.com/huggingface/datasets/pull/7683
* fix audio cast storage from array + sampling_rate by @lhoestq in https://github.com/huggingface/datasets/pull/7684
* Fix misleading add_column() usage example in docstring by @ArjunJagdale in https://github.com/huggingface/datasets/pull/7648
* Allow dataset row indexing with np.int types (#7423) by @DavidRConnell in https://github.com/huggingface/datasets/pull/7438
* Update fsspec max version to current release 2025.7.0 by @rootAvish in https://github.com/huggingface/datasets/pull/7701
* Update dataset_dict push_to_hub by @lhoestq in https://github.com/huggingface/datasets/pull/7711
* Retry intermediate commits too by @lhoestq in https://github.com/huggingface/datasets/pull/7712
* num_proc=0 behave like None, num_proc=1 uses one worker (not main process) and clarify num_proc documentation by @tanuj-rai in https://github.com/huggingface/datasets/pull/7702
* Update cli.mdx to refer to the new "hf" CLI by @evalstate in https://github.com/huggingface/datasets/pull/7713
* fix num_proc=1 ci test by @lhoestq in https://github.com/huggingface/datasets/pull/7714
* Docs: Use Image(mode="F") for PNG/JPEG depth maps  by @lhoestq in https://github.com/huggingface/datasets/pull/7715
* typo by @lhoestq in https://github.com/huggingface/datasets/pull/7716
* fix largelist repr by @lhoestq in https://github.com/huggingface/datasets/pull/7735
* Grammar fix: correct "showed" to "shown" in fingerprint.py by @brchristian in https://github.com/huggingface/datasets/pull/7730
* Fix type hint `train_test_split` by @qgallouedec in https://github.com/huggingface/datasets/pull/7736
* fix(webdataset): don't .lower() field_name by @YassineYousfi in https://github.com/huggingface/datasets/pull/7726
* Refactor HDF5 and preserve tree structure by @klamike in https://github.com/huggingface/datasets/pull/7743
* docs: Add column overwrite example to batch mapping guide by @Sanjaykumar030 in https://github.com/huggingface/datasets/pull/7737
* Audio: use TorchCodec instead of Soundfile for encoding by @lhoestq in https://github.com/huggingface/datasets/pull/7761
* Support pathlib.Path for feature input by @Joshua-Chin in https://github.com/huggingface/datasets/pull/7755
* add support for pyarrow string view in features by @onursatici in https://github.com/huggingface/datasets/pull/7718
* Fix typo in error message for cache directory deletion by @brchristian in https://github.com/huggingface/datasets/pull/7749
* update torchcodec in ci by @lhoestq in https://github.com/huggingface/datasets/pull/7764
* Bump dill to 0.4.0 by @Bomme in https://github.com/huggingface/datasets/pull/7763

## New Contributors
* @DavidRConnell made their first contribution in https://github.com/huggingface/datasets/pull/7438
* @rootAvish made their first contribution in https://github.com/huggingface/datasets/pull/7701
* @tanuj-rai made their first contribution in https://github.com/huggingface/datasets/pull/7702
* @evalstate made their first contribution in https://github.com/huggingface/datasets/pull/7713
* @brchristian made their first contribution in https://github.com/huggingface/datasets/pull/7730
* @klamike made their first contribution in https://github.com/huggingface/datasets/pull/7690
* @YassineYousfi made their first contribution in https://github.com/huggingface/datasets/pull/7726
* @Sanjaykumar030 made their first contribution in https://github.com/huggingface/datasets/pull/7737
* @kszucs made their first contribution in https://github.com/huggingface/datasets/pull/7589
* @Joshua-Chin made their first contribution in https://github.com/huggingface/datasets/pull/7755
* @onursatici made their first contribution in https://github.com/huggingface/datasets/pull/7718
* @Bomme made their first contribution in https://github.com/huggingface/datasets/pull/7763

**Full Changelog**: https://github.com/huggingface/datasets/compare/4.0.0...4.1.0

## 4.0.0 (2025-07-09T14:54:50Z)

## New Features
* Add `IterableDataset.push_to_hub()` by @lhoestq in https://github.com/huggingface/datasets/pull/7595

  ```python
  # Build streaming data pipelines in a few lines of code !
  from datasets import load_dataset

  ds = load_dataset(..., streaming=True)
  ds = ds.map(...).filter(...)
  ds.push_to_hub(...)
  ```

* Add `num_proc=` to `.push_to_hub()` (Dataset and IterableDataset) by @lhoestq in https://github.com/huggingface/datasets/pull/7606

  ```python
  # Faster push to Hub ! Available for both Dataset and IterableDataset
  ds.push_to_hub(..., num_proc=8)
  ```

* New `Column` object
  - Implementation of iteration over values of a column in an IterableDataset object by @TopCoder2K in https://github.com/huggingface/datasets/pull/7564
  - Lazy column by @lhoestq in https://github.com/huggingface/datasets/pull/7614

  ```python
  # Syntax:
  ds["column_name"]  # datasets.Column([...]) or datasets.IterableColumn(...)

  # Iterate on a column:
  for text in ds["text"]:
      ...

  # Load one cell without bringing the full column in memory
  first_text = ds["text"][0]  # equivalent to ds[0]["text"]
  ```
* Torchcodec decoding by @TyTodd in https://github.com/huggingface/datasets/pull/7616
  - Enables streaming only the ranges you need ! 

  ```python
  # Don't download full audios/videos when it's not necessary
  # Now with torchcodec it only streams the required ranges/frames:
  from datasets import load_dataset

  ds = load_dataset(..., streaming=True)
  for example in ds:
      video = example["video"]
      frames = video.get_frames_in_range(start=0, stop=6, step=1)  # only stream certain frames
  ```

  - Requires `torch>=2.7.0` and FFmpeg >= 4
  - Not available for Windows yet but it is [coming soon](https://github.com/pytorch/torchcodec/issues/640) - in the meantime please use `datasets<4.0`
  - Load audio data with `AudioDecoder`:

  ```python
  audio = dataset[0]["audio"]  # <datasets.features._torchcodec.AudioDecoder object at 0x11642b6a0>
  samples = audio.get_all_samples()  # or use get_samples_played_in_range(...)
  samples.data  # tensor([[ 0.0000e+00,  0.0000e+00,  0.0000e+00,  ...,  2.3447e-06, -1.9127e-04, -5.3330e-05]]
  samples.sample_rate  # 16000

  # old syntax is still supported
  array, sr = audio["array"], audio["sampling_rate"]
  ```

  - Load video data with `VideoDecoder`:

  ```python
  video = dataset[0]["video"] <torchcodec.decoders._video_decoder.VideoDecoder object at 0x14a61d5a0>
  first_frame = video.get_frame_at(0)
  first_frame.data.shape  # (3, 240, 320)
  first_frame.pts_seconds  # 0.0
  frames = video.get_frames_in_range(0, 6, 1)
  frames.data.shape  # torch.Size([5, 3, 240, 320])
  ```

## Breaking changes
* Remove scripts altogether by @lhoestq in https://github.com/huggingface/datasets/pull/7592
  - `trust_remote_code` is no longer supported 
* Torchcodec decoding by @TyTodd in https://github.com/huggingface/datasets/pull/7616
  - torchcodec replaces soundfile for audio decoding
  - torchcodec replaces decord for video decoding
* Replace Sequence by List by @lhoestq in https://github.com/huggingface/datasets/pull/7634
  - Introduction of the `List` type

  ```python
  from datasets import Features, List, Value

  features = Features({
      "texts": List(Value("string")),
      "four_paragraphs": List(Value("string"), length=4)
  })
  ```

  - `Sequence` was a legacy type from tensorflow datasets which converted list of dicts to dicts of lists. It is no longer a type but it becomes a utility that returns a `List` or a `dict` depending on the subfeature

  ```python
  from datasets import Sequence

  Sequence(Value("string"))  # List(Value("string"))
  Sequence({"texts": Value("string")})  # {"texts": List(Value("string"))}
  ```

## Other improvements and bug fixes
* Refactor `Dataset.map` to reuse cache files mapped with different `num_proc` by @ringohoffman in https://github.com/huggingface/datasets/pull/7434
* fix string_to_dict test by @lhoestq in https://github.com/huggingface/datasets/pull/7571
* Preserve formatting in concatenated IterableDataset by @francescorubbo in https://github.com/huggingface/datasets/pull/7522
* Fix typos in PDF and Video documentation by @AndreaFrancis in https://github.com/huggingface/datasets/pull/7579
* fix: Add embed_storage in Pdf feature by @AndreaFrancis in https://github.com/huggingface/datasets/pull/7582
* load_dataset splits typing by @lhoestq in https://github.com/huggingface/datasets/pull/7587
* Fixed typos by @TopCoder2K in https://github.com/huggingface/datasets/pull/7572
* Fix regex library warnings by @emmanuel-ferdman in https://github.com/huggingface/datasets/pull/7576
* [MINOR:TYPO] Update save_to_disk docstring by @cakiki in https://github.com/huggingface/datasets/pull/7575
* Add missing property on `RepeatExamplesIterable` by @SilvanCodes in https://github.com/huggingface/datasets/pull/7581
* Avoid multiple default config names by @albertvillanova in https://github.com/huggingface/datasets/pull/7585
* Fix broken link to albumentations by @ternaus in https://github.com/huggingface/datasets/pull/7593
* fix string_to_dict usage for windows by @lhoestq in https://github.com/huggingface/datasets/pull/7598
* No TF in win tests by @lhoestq in https://github.com/huggingface/datasets/pull/7603
* Docs and more methods for IterableDataset: push_to_hub, to_parquet... by @lhoestq in https://github.com/huggingface/datasets/pull/7604
* Tests typing and fixes for push_to_hub by @lhoestq in https://github.com/huggingface/datasets/pull/7608
* fix parallel push_to_hub in dataset_dict by @lhoestq in https://github.com/huggingface/datasets/pull/7613
* remove unused code by @lhoestq in https://github.com/huggingface/datasets/pull/7615
* Update `_dill.py` to use `co_linetable` for Python 3.10+ in place of `co_lnotab` by @qgallouedec in https://github.com/huggingface/datasets/pull/7609
* Fixes in docs by @lhoestq in https://github.com/huggingface/datasets/pull/7620
* Add albumentations to use dataset by @ternaus in https://github.com/huggingface/datasets/pull/7596
* minor docs data aug by @lhoestq in https://github.com/huggingface/datasets/pull/7621
* fix: raise error in FolderBasedBuilder when data_dir and data_files are missing by @ArjunJagdale in https://github.com/huggingface/datasets/pull/7623
* fix save_infos by @lhoestq in https://github.com/huggingface/datasets/pull/7639
* better features repr by @lhoestq in https://github.com/huggingface/datasets/pull/7640
* update docs and docstrings by @lhoestq in https://github.com/huggingface/datasets/pull/7641
* fix length for ci by @lhoestq in https://github.com/huggingface/datasets/pull/7642
* Backward compat sequence instance by @lhoestq in https://github.com/huggingface/datasets/pull/7643
* fix sequence ci by @lhoestq in https://github.com/huggingface/datasets/pull/7644
* Custom metadata filenames by @lhoestq in https://github.com/huggingface/datasets/pull/7663
* Update the beans dataset link in Preprocess by @HJassar in https://github.com/huggingface/datasets/pull/7659
* Backward compat list feature by @lhoestq in https://github.com/huggingface/datasets/pull/7666
* Fix infer list of images by @lhoestq in https://github.com/huggingface/datasets/pull/7667
* Fix audio bytes by @lhoestq in https://github.com/huggingface/datasets/pull/7670
* Fix double sequence by @lhoestq in https://github.com/huggingface/datasets/pull/7672

## New Contributors
* @TopCoder2K made their first contribution in https://github.com/huggingface/datasets/pull/7564
* @francescorubbo made their first contribution in https://github.com/huggingface/datasets/pull/7522
* @emmanuel-ferdman made their first contribution in https://github.com/huggingface/datasets/pull/7576
* @SilvanCodes made their first contribution in https://github.com/huggingface/datasets/pull/7581
* @ternaus made their first contribution in https://github.com/huggingface/datasets/pull/7593
* @ArjunJagdale made their first contribution in https://github.com/huggingface/datasets/pull/7623
* @TyTodd made their first contribution in https://github.com/huggingface/datasets/pull/7616
* @HJassar made their first contribution in https://github.com/huggingface/datasets/pull/7659

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.6.0...4.0.0

## 3.6.0 (2025-05-07T15:17:49Z)

## Dataset Features
* Enable xet in push to hub by @lhoestq in https://github.com/huggingface/datasets/pull/7552
  * Faster downloads/uploads with Xet storage
  * more info: https://github.com/huggingface/datasets/issues/7526

## Other improvements and bug fixes
* Add try_original_type to DatasetDict.map by @yoshitomo-matsubara in https://github.com/huggingface/datasets/pull/7544
* Avoid global umask for setting file mode. by @ryan-clancy in https://github.com/huggingface/datasets/pull/7547
* Rebatch arrow iterables before formatted iterable by @lhoestq in https://github.com/huggingface/datasets/pull/7553
* Document the HF_DATASETS_CACHE environment variable in the datasets cache documentation by @Harry-Yang0518 in https://github.com/huggingface/datasets/pull/7532
* fix regression by @lhoestq in https://github.com/huggingface/datasets/pull/7558
* fix: Image Feature in Datasets Library Fails to Handle bytearray Objects from Spark DataFrames (#7517) by @giraffacarp in https://github.com/huggingface/datasets/pull/7521
* Remove `aiohttp` from direct dependencies by @akx in https://github.com/huggingface/datasets/pull/7294

## New Contributors
* @ryan-clancy made their first contribution in https://github.com/huggingface/datasets/pull/7547
* @Harry-Yang0518 made their first contribution in https://github.com/huggingface/datasets/pull/7532
* @giraffacarp made their first contribution in https://github.com/huggingface/datasets/pull/7521
* @akx made their first contribution in https://github.com/huggingface/datasets/pull/7294

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.5.1...3.6.0

## 3.5.1 (2025-04-28T14:02:58Z)

## Bug fixes
* support pyarrow 20 by @lhoestq in https://github.com/huggingface/datasets/pull/7540
  * Fix pyarrow error `TypeError: ArrayExtensionArray.to_pylist() got an unexpected keyword argument 'maps_as_pydicts'`
* Write pdf in map by @lhoestq in https://github.com/huggingface/datasets/pull/7487

## Other improvements
* update fsspec 2025.3.0 by @peteski22 in https://github.com/huggingface/datasets/pull/7478
* Support underscore int read instruction by @lhoestq in https://github.com/huggingface/datasets/pull/7488
* Support skip_trying_type  by @yoshitomo-matsubara in https://github.com/huggingface/datasets/pull/7483
* pdf docs fixes by @lhoestq in https://github.com/huggingface/datasets/pull/7519
* Remove conditions for Python < 3.9 by @cyyever in https://github.com/huggingface/datasets/pull/7474
* mention av in video docs by @lhoestq in https://github.com/huggingface/datasets/pull/7523
* correct use with polars example by @SiQube in https://github.com/huggingface/datasets/pull/7524
* chore: fix typos by @afuetterer in https://github.com/huggingface/datasets/pull/7436

## New Contributors
* @peteski22 made their first contribution in https://github.com/huggingface/datasets/pull/7478
* @yoshitomo-matsubara made their first contribution in https://github.com/huggingface/datasets/pull/7483
* @SiQube made their first contribution in https://github.com/huggingface/datasets/pull/7524
* @afuetterer made their first contribution in https://github.com/huggingface/datasets/pull/7436

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.5.0...3.5.1

## 3.5.0 (2025-03-27T16:38:30Z)

## Datasets Features
* Introduce PDF support (#7318) by @yabramuvdi in https://github.com/huggingface/datasets/pull/7325

```python
>>> from datasets import load_dataset, Pdf
>>> repo = "path/to/pdf/folder"  # or username/dataset_name on Hugging Face
>>> dataset = load_dataset(repo, split="train")
>>> dataset[0]["pdf"]
<pdfplumber.pdf.PDF at 0x1075bc320>
>>> dataset[0]["pdf"].pages[0].extract_text()
...
```

## What's Changed
* Fix local pdf loading by @lhoestq in https://github.com/huggingface/datasets/pull/7466
* Minor fix for metadata files in extension counter by @lhoestq in https://github.com/huggingface/datasets/pull/7464
* Priotitize json by @lhoestq in https://github.com/huggingface/datasets/pull/7476

## New Contributors
* @yabramuvdi made their first contribution in https://github.com/huggingface/datasets/pull/7325

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.4.1...3.5.0

## 3.4.1 (2025-03-17T16:00:06Z)

## Bug Fixes
* Fix data_files filtering by @lhoestq in https://github.com/huggingface/datasets/pull/7459


**Full Changelog**: https://github.com/huggingface/datasets/compare/3.4.0...3.4.1

## 3.4.0 (2025-03-14T16:46:23Z)

## Dataset Features
* Faster folder based builder + parquet support + allow repeated media + use torchvideo by @lhoestq in https://github.com/huggingface/datasets/pull/7424
  * /!\ Breaking change: we replaced `decord` with `torchvision` to read videos, since `decord` is not maintained anymore and isn't available for recent python versions, see the [video dataset loading documentation here](https://huggingface.co/docs/datasets/main/en/video_load) for more details. The `Video` type is still marked as *experimental* is this version

  ```python
  from datasets import load_dataset, Video
  
  dataset = load_dataset("path/to/video/folder", split="train")
  dataset[0]["video"]  # <torchvision.io.video_reader.VideoReader at 0x1652284c0>
  ```

  * faster streaming for image/audio/video folder from Hugging Face
  * support for `metadata.parquet` in addition to `metadata.csv` or `metadata.jsonl` for the metadata of the image/audio/video files
* Add IterableDataset.decode with multithreading by @lhoestq in https://github.com/huggingface/datasets/pull/7450
  * even faster streaming for image/audio/video folder from Hugging Face if you enable multithreading to decode image/audio/video data:

  ```python
  dataset = dataset.decode(num_threads=num_threads)
  ```
* Add with_split to DatasetDict.map by @jp1924 in https://github.com/huggingface/datasets/pull/7368

## General improvements and bug fixes
* fix: None default with bool type on load creates typing error by @stephantul in https://github.com/huggingface/datasets/pull/7426
* Use pyupgrade --py39-plus by @cyyever in https://github.com/huggingface/datasets/pull/7428
* Refactor `string_to_dict` to return `None` if there is no match instead of raising `ValueError` by @ringohoffman in https://github.com/huggingface/datasets/pull/7435
* Fix small bugs with async map by @lhoestq in https://github.com/huggingface/datasets/pull/7445
* Fix resuming after `ds.set_epoch(new_epoch)` by @lhoestq in https://github.com/huggingface/datasets/pull/7451
* minor docs changes by @lhoestq in https://github.com/huggingface/datasets/pull/7452

## New Contributors
* @stephantul made their first contribution in https://github.com/huggingface/datasets/pull/7426
* @cyyever made their first contribution in https://github.com/huggingface/datasets/pull/7428
* @jp1924 made their first contribution in https://github.com/huggingface/datasets/pull/7368

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.3.2...3.4.0

## 3.3.2 (2025-02-20T17:44:25Z)

## Bug fixes
* Attempt to fix multiprocessing hang by closing and joining the pool before termination by @dakinggg in https://github.com/huggingface/datasets/pull/7411
* Gracefully cancel async tasks by @lhoestq in https://github.com/huggingface/datasets/pull/7414

## Other general improvements
* Update use_with_pandas.mdx: to_pandas() correction in last section by @ibarrien in https://github.com/huggingface/datasets/pull/7407
* Fix a typo in arrow_dataset.py by @jingedawang in https://github.com/huggingface/datasets/pull/7402

## New Contributors
* @dakinggg made their first contribution in https://github.com/huggingface/datasets/pull/7411
* @ibarrien made their first contribution in https://github.com/huggingface/datasets/pull/7407
* @jingedawang made their first contribution in https://github.com/huggingface/datasets/pull/7402

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.3.1...3.3.2

## 3.3.1 (2025-02-17T14:53:39Z)

## Bug fixes
* Fix filter speed regression by @lhoestq in https://github.com/huggingface/datasets/pull/7408


**Full Changelog**: https://github.com/huggingface/datasets/compare/3.3.0...3.3.1

## 3.3.0 (2025-02-14T10:15:39Z)

## Dataset Features
* Support async functions in map() by @lhoestq in https://github.com/huggingface/datasets/pull/7384
  * Especially useful to download content like images or call inference APIs

  ```python
  prompt = "Answer the following question: {question}. You should think step by step."
  async def ask_llm(example):
      return await query_model(prompt.format(question=example["question"]))
  ds = ds.map(ask_llm)
  ```
* Add repeat method to datasets by @alex-hh in https://github.com/huggingface/datasets/pull/7198
  ```python
  ds = ds.repeat(10)
  ```
* Support faster processing using pandas or polars functions in `IterableDataset.map()` by @lhoestq in https://github.com/huggingface/datasets/pull/7370
  * Add support for "pandas" and "polars" formats in IterableDatasets
  * This enables optimized data processing using pandas or polars functions with zero-copy, e.g.

  ```python
  ds = load_dataset("ServiceNow-AI/R1-Distill-SFT", "v0", split="train", streaming=True)
  ds = ds.with_format("polars")
  expr = pl.col("solution").str.extract("boxed\\{(.*)\\}").alias("value_solution")
  ds = ds.map(lambda df: df.with_columns(expr), batched=True)
  ```

* Apply formatting after iter_arrow to speed up format -> map, filter for iterable datasets by @alex-hh in https://github.com/huggingface/datasets/pull/7207
  * IterableDatasets with "numpy" format are now much faster

## What's Changed
* don't import soundfile in tests by @lhoestq in https://github.com/huggingface/datasets/pull/7340
* minor video docs on how to install by @lhoestq in https://github.com/huggingface/datasets/pull/7341
* Fix typo in arrow_dataset by @AndreaFrancis in https://github.com/huggingface/datasets/pull/7328
* remove filecheck to enable symlinks by @fschlatt in https://github.com/huggingface/datasets/pull/7133
* Webdataset special columns in last position by @lhoestq in https://github.com/huggingface/datasets/pull/7349
* Bump hfh to 0.24 to fix ci by @lhoestq in https://github.com/huggingface/datasets/pull/7350
* fsspec 2024.12.0 by @lhoestq in https://github.com/huggingface/datasets/pull/7352
* changes to MappedExamplesIterable to resolve #7345 by @vttrifonov in https://github.com/huggingface/datasets/pull/7353
* Catch OSError for arrow by @lhoestq in https://github.com/huggingface/datasets/pull/7348
* Remove .h5 from imagefolder extensions by @lhoestq in https://github.com/huggingface/datasets/pull/7374
* Add Pandas, PyArrow and Polars docs by @lhoestq in https://github.com/huggingface/datasets/pull/7382
* Optimized sequence encoding for scalars by @lukasgd in https://github.com/huggingface/datasets/pull/7393
* Update docs by @lhoestq in https://github.com/huggingface/datasets/pull/7395
* Update README.md by @lhoestq in https://github.com/huggingface/datasets/pull/7396
* Release: 3.3.0 by @lhoestq in https://github.com/huggingface/datasets/pull/7398

## New Contributors
* @AndreaFrancis made their first contribution in https://github.com/huggingface/datasets/pull/7328
* @vttrifonov made their first contribution in https://github.com/huggingface/datasets/pull/7353
* @lukasgd made their first contribution in https://github.com/huggingface/datasets/pull/7393

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.2.0...3.3.0

## 3.2.0 (2024-12-10T17:00:11Z)

## Dataset Features
* Faster parquet streaming + filters with predicate pushdown by @lhoestq in https://github.com/huggingface/datasets/pull/7309
  * Up to +100% streaming speed
  * Fast filtering via predicate pushdown (skip files/row groups based on predicate instead of downloading the full data), e.g.
    ```python
    from datasets import load_dataset
    filters = [('date', '>=', '2023')]
    ds = load_dataset("HuggingFaceFW/fineweb-2", "fra_Latn", streaming=True, filters=filters)
    ```

## Other improvements and bug fixes
* fix conda release worlflow by @lhoestq in https://github.com/huggingface/datasets/pull/7272
* Add link to video dataset by @NielsRogge in https://github.com/huggingface/datasets/pull/7277
* Raise error for incorrect JSON serialization by @varadhbhatnagar in https://github.com/huggingface/datasets/pull/7273
* support for custom feature encoding/decoding by @alex-hh in https://github.com/huggingface/datasets/pull/7284
* update load_dataset doctring by @lhoestq in https://github.com/huggingface/datasets/pull/7301
* Let server decide default repo visibility by @Wauplin in https://github.com/huggingface/datasets/pull/7302
* fix: update elasticsearch version by @ruidazeng in https://github.com/huggingface/datasets/pull/7300
* Fix typing in iterable_dataset.py by @lhoestq in https://github.com/huggingface/datasets/pull/7304
* Updated inconsistent output in documentation examples for `ClassLabel` by @sergiopaniego in https://github.com/huggingface/datasets/pull/7293
* More docs to from_dict to mention that the result lives in RAM by @lhoestq in https://github.com/huggingface/datasets/pull/7316
* Release: 3.2.0 by @lhoestq in https://github.com/huggingface/datasets/pull/7317

## New Contributors
* @ruidazeng made their first contribution in https://github.com/huggingface/datasets/pull/7300
* @sergiopaniego made their first contribution in https://github.com/huggingface/datasets/pull/7293

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.1.0...3.2.0

## 3.1.0 (2024-10-31T15:21:42Z)

## Dataset Features
* Video support by @lhoestq in https://github.com/huggingface/datasets/pull/7230
    ```python
    >>> from datasets import Dataset, Video, load_dataset
    >>> ds = Dataset.from_dict({"video":["path/to/Screen Recording.mov"]}).cast_column("video", Video())
    >>> # or from the hub
    >>> ds = load_dataset("username/dataset_name", split="train")
    >>> ds[0]["video"]
    <decord.video_reader.VideoReader at 0x105525c70>
    ```
* Add IterableDataset.shard() by @lhoestq in https://github.com/huggingface/datasets/pull/7252
    ```python
    >>> from datasets import load_dataset
    >>> full_ds = load_dataset("amphion/Emilia-Dataset", split="train", streaming=True)
    >>> full_ds.num_shards
    2360
    >>> ds = full_ds.shard(num_shards=ds.num_shards, index=0)
    >>> ds.num_shards
    1
    >>> ds = full_ds.shard(num_shards=8, index=0)
    >>> ds.num_shards
    295
    ```
* Basic XML support  by @lhoestq in https://github.com/huggingface/datasets/pull/7250

## What's Changed
* (Super tiny doc update) Mention to_polars by @fzyzcjy in https://github.com/huggingface/datasets/pull/7232
* [MINOR:TYPO] Update arrow_dataset.py by @cakiki in https://github.com/huggingface/datasets/pull/7236
* Missing video docs by @lhoestq in https://github.com/huggingface/datasets/pull/7251
* fix decord import by @lhoestq in https://github.com/huggingface/datasets/pull/7255
* fix ci for pyarrow 18 by @lhoestq in https://github.com/huggingface/datasets/pull/7257
* Retry all requests timeouts by @lhoestq in https://github.com/huggingface/datasets/pull/7256
* Always set non-null writer batch size by @lhoestq in https://github.com/huggingface/datasets/pull/7258
* Don't embed videos by @lhoestq in https://github.com/huggingface/datasets/pull/7259
* Allow video with disabeld decoding without decord by @lhoestq in https://github.com/huggingface/datasets/pull/7262
* Small addition to video docs by @lhoestq in https://github.com/huggingface/datasets/pull/7263
* fix docs relative links by @lhoestq in https://github.com/huggingface/datasets/pull/7264
* Disallow video push_to_hub by @lhoestq in https://github.com/huggingface/datasets/pull/7265

## New Contributors
* @fzyzcjy made their first contribution in https://github.com/huggingface/datasets/pull/7232

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.0.2...3.1.0

## 3.0.2 (2024-10-22T15:03:39Z)

## Main bug fixes
* fix unbatched arrow map for iterable datasets by @alex-hh in https://github.com/huggingface/datasets/pull/7204
* Support features in metadata configs by @albertvillanova in https://github.com/huggingface/datasets/pull/7182
* Preserve features in iterable dataset.filter by @alex-hh in https://github.com/huggingface/datasets/pull/7209
* Pin dill<0.3.9 to fix CI by @albertvillanova in https://github.com/huggingface/datasets/pull/7184
  * this should also fix cache issues

## What's Changed
* Fix release instructions by @albertvillanova in https://github.com/huggingface/datasets/pull/7177
* Pin multiprocess<0.70.1 to align with dill<0.3.9 by @albertvillanova in https://github.com/huggingface/datasets/pull/7188
* with_format docstring by @lhoestq in https://github.com/huggingface/datasets/pull/7203
* fix ci benchmark by @lhoestq in https://github.com/huggingface/datasets/pull/7205
* Fix the environment variable for huggingface cache by @torotoki in https://github.com/huggingface/datasets/pull/7200
* Support Python 3.11 by @albertvillanova in https://github.com/huggingface/datasets/pull/7179
* bump fsspec by @lhoestq in https://github.com/huggingface/datasets/pull/7219
* Fix typo in image dataset docs by @albertvillanova in https://github.com/huggingface/datasets/pull/7231
* No need for dataset_info by @lhoestq in https://github.com/huggingface/datasets/pull/7234
* use huggingface_hub offline mode by @lhoestq in https://github.com/huggingface/datasets/pull/7244

## New Contributors
* @alex-hh made their first contribution in https://github.com/huggingface/datasets/pull/7204
* @torotoki made their first contribution in https://github.com/huggingface/datasets/pull/7200

**Full Changelog**: https://github.com/huggingface/datasets/compare/3.0.1...3.0.2
