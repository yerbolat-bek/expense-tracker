import sys, os
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

import pytest


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