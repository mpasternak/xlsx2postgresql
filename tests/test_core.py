import pytest

from xlsx2postgresql.core import get_header_row, normalize_identifier


def test_get_header_row():
    assert get_header_row(None) == 7


@pytest.mark.parametrize(
    "i,e",
    [
        ("Dane pacjenta - kod MIP", "dane_pacjenta_kod_mip"),
        ("L.p.", "l_p"),
        ("Czas trwania - (w minutach)", "czas_trwania_w_minutach"),
    ],
)
def test_normalize_identifier(i, e):
    assert normalize_identifier(i) == e


def test_XLSXFile_create_tables(xlsxfile):
    res = xlsxfile.create_tables()
    assert len(list(res)) == 1


def test_XLSXFile_load_data(xlsxfile):
    res = xlsxfile.load_data()
    assert len(list(res)) == 12
