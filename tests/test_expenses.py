import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import storage
from expenses import ExpenseTracker


def make_tracker():
    t = ExpenseTracker()
    t.add(100, "food")
    t.add(50, "transport")
    t.add(30, "food")
    return t


def test_total():
    assert make_tracker().total() == 180


def test_total_by_category():
    assert make_tracker().total_by_category("food") == 130


def test_remove():
    t = make_tracker()
    t.remove(0)
    assert t.total() == 80


def test_total_with_tax():
    t = ExpenseTracker()
    t.add(100, "food")
    assert round(t.total_with_tax(), 2) == 105.00


def test_save_and_load(tmp_path):
    path = tmp_path / "data.json"
    storage.save(make_tracker(), str(path))
    loaded = storage.load(str(path))
    assert loaded.total() == 180



@pytest.mark.parametrize(
    "category, expected",
    [
        ("food", 105.00),
        ("transport", 110.00),
        ("entertainment", 120.00),
        ("other", 100.00),
    ],
)
def test_tax_rates_per_category(category, expected):
    t = ExpenseTracker()
    t.add(100, category)
    assert round(t.total_with_tax(), 2) == expected


def test_format_expense_contains_taxed_amount():
    t = ExpenseTracker()
    e = t.add(100, "food", "2026-01-01", "lunch")
    line = t.format_expense(e)
    assert "105.00" in line
    assert "lunch" in line

@pytest.mark.parametrize(
    "bad", [-500, 0, float("nan"), float("inf"), float("-inf"), "abc", None, True]
)
def test_add_rejects_invalid_amount(bad):
    t = ExpenseTracker()
    with pytest.raises(ValueError):
        t.add(bad, "food")
    assert t.expenses == []


def test_add_accepts_positive_float():
    t = ExpenseTracker()
    t.add(19.99, "food")
    assert t.total() == 19.99


def test_failed_save_keeps_previous_file(tmp_path, monkeypatch):
    path = tmp_path / "data.json"
    storage.save(make_tracker(), str(path))
    before = path.read_text()

    def failing_dump(obj, fp, *args, **kwargs):
        fp.write("[{partial")
        raise OSError("disk full")

    monkeypatch.setattr(storage.json, "dump", failing_dump)
    with pytest.raises(OSError):
        storage.save(make_tracker(), str(path))

    assert path.read_text() == before
    assert list(tmp_path.iterdir()) == [path]