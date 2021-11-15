import json as js

from TableInfo import *
from TableData import *


def compile(table_data: TableData, out_folder: str):
    recs = table_data.to_pyobject()
    jstr = js.dumps(recs, indent=4, ensure_ascii=False)
    path = out_folder + "/" + table_data.name + ".json"
    with open(path, "w+", encoding="utf-8") as f:
        f.write(jstr)


def batch_compile(table_datas: dict[str, TableData], out_folder: str, is_combine: bool):
    for table in table_datas.values():
        compile(table, out_folder)
    pass
