"""
Vi du Test Automation voi pytest (Chuong1_Phan1, slide 87/100) mo rong sang
2 bai tap: Equivalence Partitioning & Boundary Value Analysis cho mat khau
(slide 88-92/100).

Chay: pytest ch1_models/tests/test_testing.py -v
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ch1_models.testing import is_valid_age, is_valid_password_length, boundary_value_test_cases


def test_age_lower_boundary():
    assert is_valid_age(0) is True
    assert is_valid_age(-1) is False


def test_age_upper_boundary():
    assert is_valid_age(120) is True
    assert is_valid_age(121) is False


def test_password_boundary_values():
    # Dap an slide: 7 (invalid), 8 (valid), 20 (valid), 21 (invalid)
    for length, expected in boundary_value_test_cases(8, 20):
        pwd = "a" * max(length, 0)
        assert is_valid_password_length(pwd) == expected, f"do dai={length}"


def test_password_equivalence_classes():
    assert is_valid_password_length("a" * 3) is False    # lop khong hop le 1: < 8
    assert is_valid_password_length("a" * 12) is True     # lop hop le: 8..20
    assert is_valid_password_length("a" * 30) is False    # lop khong hop le 2: > 20
