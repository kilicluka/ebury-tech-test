# -*- coding: utf-8 -*-

import pytest
from identity.generation import generate


def test_id_is_the_correct_length():
    assert len(generate()) == 7


def test_id_is_alphanumeric():
    generated_id = generate()
    assert generated_id.isalnum()


def test_ids_are_unique():
    ids = set()
    for i in range(0,10):
        ids.add(generate())

    assert len(ids) == 10
