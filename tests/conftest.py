import os

import pytest

from xlsx2postgresql.core import XLSXFile


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(__file__), "testdata.xlsx")


@pytest.fixture
def xlsxfile(test_file_path):
    return XLSXFile(test_file_path)
