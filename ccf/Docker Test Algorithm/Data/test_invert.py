import os

import pytest

import invert


def test_createImage():
    invert.process(["testImage.jpg"])
    assert os.path.isfile("fixed.jpeg")
    os.remove("fixed.jpeg")
