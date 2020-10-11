import pytest

from xlsx2postgresql.core import get_header_row, normalize_identifier, XLSXFile


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


def test_XLSXFile_create_tables_double_column(test_file_2_path):
    """Test for "duplicate column name"""

    xlsxfile = XLSXFile(test_file_2_path)

    import sqlite3

    conn = sqlite3.connect("example.db")
    cur = conn.cursor()

    for query in xlsxfile.create_tables():
        for elem in query.split(";"):
            cur.execute(elem)
