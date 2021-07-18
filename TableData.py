from TableFieldInfo import TableFieldInfo


class TableData:

    table_name: str
    field_infos: list[TableFieldInfo]
    records: list[tuple]

    def __init__(self, name: str, field_infos: list[TableFieldInfo], records: list[tuple]) -> None:
        self.table_name = name
        self.field_infos = field_infos
        self.records = records
