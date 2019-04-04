import os

import pytest

import invert


def test_createImage():
    invert.process(["ccf/DockerTestAlgorithm/Data/testImage.jpg"])
    assert os.path.isfile("ccf/DockerTestAlgorithm/Data/fixed.jpeg")
    os.remove("fixed.jpeg")
