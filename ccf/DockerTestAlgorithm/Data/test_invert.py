import os

import pytest

import invert


def test_createImage():
    pathname = [os.getcwd() + "/ccf/DockerTestAlgorithm/Data/testImage.jpg"]
    invert.process(pathname)
    assert os.path.isfile(os.getcwd() + "/ccf/DockerTestAlgorithm/Data/fixed.jpeg")


# os.remove("fixed.jpeg")
