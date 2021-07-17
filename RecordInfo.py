
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


class TableFieldInfo:
    def __init__(self, type: str, name: str, note: str) -> None:
        self.type = type
        self.name = name
        self.note = note

    def __str__(self) -> str:
        return str.format("{{type: {}, name: {}, note: {}}}", self.type, self.name, self.note)


