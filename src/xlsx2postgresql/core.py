from datetime import datetime

import xlrd
import click


def get_header_row(sheet):
    return 7


def normalize_identifier(s):
    s = (
        s.replace("(", "_")
        .replace(")", "_")
        .replace(" ", "_")
        .replace(".", "_")
        .replace("-", "_")
    )
    while s.find("__") >= 0:
        s = s.replace("__", "_")
    if s.endswith("_"):
        s = s[:-1]
    return s.lower()


def ctype_to_pgsql_type(t):
    if t == 2:
        return "numeric"
    elif t == 1:
        return "text"
    elif t == 3:
        return "timestamp"

    raise NotImplementedError(f"ctype {t} not implemented")


class XLSXFile:
    def __init__(self, path):
        self.wb = xlrd.open_workbook(path)
        self.sheet_names = self.wb.sheet_names()
        self.col_types = []
        self.get_col_types()

    def get_col_types(self):
        for name in self.sheet_names:
            xl_sheet = self.wb.sheet_by_name(name)
            col_types = [
                ctype_to_pgsql_type(c.ctype)
                for c in xl_sheet.row(get_header_row(xl_sheet) + 1)
            ]
            self.col_types.append(col_types)

    def create_tables(self):
        for name, col_types in zip(self.sheet_names, self.col_types):
            xl_sheet = self.wb.sheet_by_name(name)
            labels_row = xl_sheet.row(get_header_row(xl_sheet))
            labels = [normalize_identifier(s.value) for s in labels_row]

            ret = f"CREATE TABLE IF NOT EXISTS {normalize_identifier(name)} (\n"

            mret = []
            for l, c in zip(labels, col_types):
                mret.append(f"\t{l} {c}")
            ret += ",\n".join(mret)
            ret += "\n);"

            yield ret

    def load_data(self):
        for name, col_types in zip(self.sheet_names, self.col_types):
            n_name = normalize_identifier(name)
            xl_sheet = self.wb.sheet_by_name(name)
            labels_row = get_header_row(xl_sheet)

            for row in range(labels_row + 1, xl_sheet.nrows):
                res = f"INSERT INTO f{n_name} VALUES(\n"
                data = xl_sheet.row(row)
                values = [d.value for d in data]
                mres = []
                for v, t in zip(values, col_types):
                    if t == "text":
                        mres.append("\t'%s'" % v)
                    elif t == "numeric":
                        mres.append("\t'%s'" % v)
                    elif t == "timestamp":
                        if v == "":
                            mres.append("\tNULL")
                            continue

                        v = datetime(*xlrd.xldate_as_tuple(v, self.wb.datemode))
                        mres.append("\t'%s'" % v)
                    else:
                        raise NotImplementedError(t)

                res += ",\n".join(mres)
                res += ");\n"
                yield res


@click.command()
@click.argument("input", type=XLSXFile)
def xlsx2postgresql(input):
    for elem in input.create_tables():
        print(elem)
    for elem in input.load_data():
        print(elem)


if __name__ == "__main__":
    xlsx2postgresql()
