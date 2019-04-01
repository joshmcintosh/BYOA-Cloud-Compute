import os

import pytest

import invert


def test_createImage():
    invert.process(["3959X_2017-3.jpg"])
    assert os.path.isfile("fixed.jpeg")
    os.remove("fixed.jpeg")
