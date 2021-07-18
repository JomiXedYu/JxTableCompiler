
TypeInt16 = "int16"
TypeInt32 = "int32"
TypeInt64 = "int64"
TypeFloat = "float"
TypeDouble = "double"
TypeBool = "bool"
TypeString = "string"


def get_type_map():
    type_map = {
        TypeInt16: TypeInt16,
        TypeInt32: TypeInt32,
        TypeInt64: TypeInt64,
        TypeFloat: TypeFloat,
        TypeDouble: TypeDouble,
        TypeBool: TypeBool,
        TypeString: TypeString
    }
    return type_map


class FieldInfo:
    def __init__(self, type: str, name: str, note: str) -> None:
        self.type = type
        self.name = name
        self.note = note

    def __str__(self) -> str:
        return str.format("{{type: {}, name: {}, note: {}}}", self.type, self.name, self.note)


class TableFieldInfo:

    class_type_name: str
    field_infos: list[FieldInfo]
    namespace: str

    def __init__(self, class_type_name: str, field_infos: list[FieldInfo], namespace: str = None) -> None:
        self.class_type_name = class_type_name
        self.field_infos = field_infos
        self.namespace = namespace

    def __len__(self):
        return len(self.field_infos)

    def __str__(self) -> str:
        return str(self.field_infos)

def get_namespace_dict(table_infos : dict[str, TableFieldInfo]) -> dict[str, list[TableFieldInfo]]:
    """
    return dict[ns:str, list[tb:TableFieldInfo]]
    """
    dic = {}
    for name, tfinfo in table_infos.items():
        if tfinfo.namespace == None: # non namespace
            if "" not in dic:
                dic[""] = []
            dic[""].append(tfinfo)
        else: # namespace
            if tfinfo.namespace not in dic:
                dic[tfinfo.namespace] = []
            dic[tfinfo.namespace].append(tfinfo)
    return dic