"""factbank — keep reasoning in the model, keep facts in a bank you own.

The evaluated Served-Loop system, packaged: a sealed draft->retrieve->refine
loop served as one OpenAI-compatible endpoint over any local backend, with an
editable JSONL fact bank as the source of truth. See `README.md` in this package,
`../../ARCHITECTURES.md` for how this relates to the baked-GGUF path, and the
research write-ups under `../../serving/` and `../../papers/`.
"""

__version__ = "0.1.0"
