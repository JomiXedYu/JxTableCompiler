from TableFieldInfo import TableFieldInfo


class TableData:

    table_name: str
    name: str
    field_infos: TableFieldInfo
    records: list[list[any]]

    def __init__(self, table_name: str, name: str, field_infos: TableFieldInfo, records: list[list[any]]) -> None:
        self.table_name = table_name
        self.name = name
        self.field_infos = field_infos
        self.records = records

    def to_pyobject(self) -> list[dict[str, any]]:
        arr = []
        for record in self.records:
            rec_dic = {}
            for i in range(len(self.field_infos.field_infos)):
                field_name = self.field_infos.field_infos[i].name
                rec_dic[field_name] = record[i]
            arr.append(rec_dic)
        return arr
