# -*- coding: utf-8 -*-
import re

import pytest
from identity.generation import generate, generate_bulk


def test_id_is_the_correct_length():
    assert len(generate()) == 7


def test_id_is_alphanumeric():
    generated_id = generate()
    assert generated_id.isalnum()


def test_ids_are_unique_and_correct_format():
    ids = set()
    generated_count = 0
    has_letters_and_numbers = False
    alphanum_check = re.compile('([0-9].*[A-Za-z])|([A-Za-z].*[0-9])')
    while generated_count < 22000:
        generated_id = generate()
        generated_count += 1
        assert generated_id not in ids
        ids.add(generated_id)
        if not has_letters_and_numbers:
            has_letters_and_numbers = len(
                alphanum_check.findall(generated_id)) > 0
    # at least one of the generated ids must have a mix of
    # letters and numbers
    assert has_letters_and_numbers


def test_ids_are_unique_generated_in_bulk():
    generated_ids = set()
    generated_count = 0
    while generated_count < 100:
        generated_ids.update(generate_bulk(1000))
        generated_count += 1
        assert len(generated_ids) == generated_count * 1000
