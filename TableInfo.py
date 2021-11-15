
class FieldInfo:
    def __init__(self, type: str, name: str, note: str, isprop: bool) -> None:
        self.type = type
        self.name = name
        self.note = note
        self.isprop = isprop

    def __str__(self) -> str:
        return str.format("{{type: {}, name: {}, note: {}}}", self.type, self.name, self.note)
        
class TableInfo:
    name: str
    struct_name: str
    field_infos: list[FieldInfo]
    namespace: str

    def __init__(self, name: str, field_infos: list[FieldInfo]) -> None:
        self.name = name
        self.field_infos = field_infos

        self.struct_name = None
        self.namespace = None
        if self.name.find('.') >= 0:
            self.struct_name = self.name[self.name.rfind('.')+1:]
            self.namespace = self.name[:self.name.find('.')]
        else:
            self.struct_name = name

    def __len__(self):
        return len(self.field_infos)

    def __str__(self) -> str:
        return str(self.field_infos)


def tableinfos_to_namespacedic(table_infos: list[TableInfo]) -> dict[str, list[TableInfo]]:
    dic = {}
    for tfinfo in table_infos:
        if tfinfo.namespace == None: # non namespace
            if "" not in dic:
                dic[""] = []
            dic[""].append(tfinfo)
        else: # namespace
            if tfinfo.namespace not in dic:
                dic[tfinfo.namespace] = []
            dic[tfinfo.namespace].append(tfinfo)
    return dic