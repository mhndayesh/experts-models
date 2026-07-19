"""Smoke tests for the factbank package — the first first-party tests in the repo.
Cover the schema mapping, bank loading/search, and the empty-bank guard.
"""
import glob
import os
import pytest
from factbank.bank import Bank, Fact

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
EXPERTS = os.path.join(PKG, "..", "extractor", "experts")
SHIPPED = os.path.join(PKG, "factbank", "facts_v2.jsonl")


def test_from_row_native():
    f = Fact.from_row({"id": "x", "text": "t", "source": "s", "version": "1"})
    assert f.kind == "doc" and f.source == "s" and f.text == "t"


def test_from_row_expert_landmine():
    f = Fact.from_row({"id": "y", "lib": "openssl", "version": "3",
                       "type": "REPLACED", "truth": "use EVP_PKEY_new()",
                       "keywords": {"from_fact": ["RSA_new"]}})
    assert f.kind == "landmine" and f.source == "openssl"
    assert "EVP_PKEY_new" in f.text and f.meta.get("type") == "REPLACED"


def test_from_row_strips_pipeline_meta():
    f = Fact.from_row({"id": "z", "lib": "x", "version": "1", "type": "CHANGED",
                       "truth": "t", "_repaired": True, "_flags": ["a"]})
    assert "_repaired" not in f.meta and "_flags" not in f.meta


def test_empty_bank_raises():
    with pytest.raises(ValueError):
        Bank([])


@pytest.mark.skipif(not os.path.exists(SHIPPED), reason="facts_v2.jsonl not built")
def test_shipped_bank_loads_and_searches():
    bk = Bank.from_jsonl(SHIPPED)
    assert len(bk.facts) > 1000
    hits = bk.search("openssl RSA_new deprecated in 3.0", k=3, min_score=0.1)
    assert any(f.source == "openssl" for f, _ in hits)


def test_every_expert_bank_loads():
    banks = glob.glob(os.path.join(EXPERTS, "*", "facts", "*.jsonl"))
    assert banks, "no expert banks found"
    for b in banks:
        bk = Bank.from_jsonl(b)          # must not raise (utf-8 + schema mapping)
        assert bk.facts
