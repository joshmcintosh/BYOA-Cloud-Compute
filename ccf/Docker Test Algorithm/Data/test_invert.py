import os

import pytest

import invert


def test_createImage():
    invert.process(["ccf/Docker Test Algorithm/Data/testImage.jpg"])
    assert os.path.isfile("ccf/Docker Test Algorithm/Data/fixed.jpeg")
    os.remove("ccf/Docker Test Algorithm/Data/fixed.jpeg")
