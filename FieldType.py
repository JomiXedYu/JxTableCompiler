

TypeInt16 = "int16"
TypeInt32 = "int32"
TypeInt64 = "int64"
TypeFloat = "float"
TypeDouble = "double"
TypeBool = "bool"
TypeString = "string"

def get_fieldtype_map():
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

def mapping_fieldtype(mapping: dict, type: str):
    if type in mapping:
        return mapping[type]
    return type