from TableInfo import *
import openpyxl

class TableData:
    name: str
    table_info: TableInfo
    records: list[list[any]]

    def __init__(self,  name: str, field_infos: TableInfo, records: list[list[any]]) -> None:
        self.name = name
        self.table_info = field_infos
        self.records = records

    def to_pyobject(self) -> list[dict[str, any]]:
        arr = []
        for record in self.records:
            rec_dic = {}
            for i in range(len(self.table_info.field_infos)):
                field_name = self.table_info.field_infos[i].name
                rec_dic[field_name] = record[i]
            arr.append(rec_dic)
        return arr


def __get_filename_without_ext(filename: str) -> str:
    filename = filename.replace('\\', '/')
    if filename[-1] == '/':
        return filename
    sfn = filename[filename.rfind('/')+1:]
    dotpos = sfn.rfind('.')
    if dotpos == -1:
        return sfn
    return sfn[:dotpos]

exceldata_cache : dict[str, TableData] = {}

def gen_table_data(excel_path: str) -> TableData:
    '''
    传入一个excel文件路径，返回数据
    '''

    if excel_path in exceldata_cache:
        return exceldata_cache[excel_path]

    table_data : TableData = None
    table_name = __get_filename_without_ext(excel_path)

    table_field_info = TableInfo(table_name, [])
    records = []
    table_data = TableData(table_name, table_field_info, records)

    excel = openpyxl.load_workbook(excel_path)
    sheet = excel.active
    rows = list(sheet.rows)

    line_note = 0
    line_type = 1
    line_field = 2

    field_count = len(rows[line_field])
    # model
    for i in range(0, field_count):
        type = rows[line_type][i].value
        if type == None:
            type = "string"
        field = rows[line_field][i].value
        note = rows[line_note][i].value
        isprop = type.endswith("$")
        type = type.replace('$', "")
        table_data.table_info.field_infos.append(
            FieldInfo(type, field, note, isprop))
    # data
    for line in range(line_field + 1, len(rows)):
        rec = []
        for r in rows[line]:
            rec.append(r.value)
        table_data.records.append(rec)

    #cache
    exceldata_cache[excel_path] = table_data

    return table_data

def gen_table_datas(excel_paths: list[str]) -> dict[str, TableData]:
    '''
    传入一个excel文件路径列表，返回数据
    '''
    table_datas: dict[str, TableData] = {}

    for path in excel_paths:
        data = gen_table_data(path)
        table_name = __get_filename_without_ext(path)
        table_datas[table_name] = data

    return table_datas