import FieldType
import Utility
from TableInfo import *

typemap = FieldType.get_fieldtype_map()
typemap[FieldType.TypeInt16] = "number"
typemap[FieldType.TypeInt32] = "number"
typemap[FieldType.TypeInt64] = "number"
typemap[FieldType.TypeFloat] = "number"
typemap[FieldType.TypeDouble] = "number"
typemap[FieldType.TypeBool] = "boolean"
typemap[FieldType.TypeString] = "string"


def gen_class(field_infos: TableInfo) -> str:
    strlist = []
    strlist.append("\nlocal " + field_infos.struct_name + " = ")
    strlist.append("{")
    for _field in field_infos.field_infos:
        field: FieldInfo = _field
        if field.note != None:
            strlist.append("    -- " + field.note)
        strlist.append("    ---@type " + FieldType.mapping_fieldtype(typemap, field.type))
        strlist.append("    local {} = nil".format(field.name))
    strlist.append("}\n")

    return "\n".join(strlist)


def generate(table_info: TableInfo, out_folder: str) -> str:
    strlist = []
    strlist.append(Utility.get_data_geninfo("---", "lua"))

    body = gen_class(table_info)
    strlist.append(body)

    strlist.append("return " + table_info.struct_name)

    content = "\n".join(strlist)
    path = out_folder + "/" + table_info.name + ".lua"
    with open(path, "w+", encoding="utf-8") as fs:
        fs.write(content)

def batch_generate(table_infos: list[TableInfo], out_folder: str, is_combine: bool):
    if not is_combine:
        for table_info in table_infos:
            generate(table_info, out_folder)
        return

    content = []
    content.append(Utility.get_model_geninfo("---", "lua"))
    for table_info in table_infos:
        content.append(gen_class(table_info))

    content.append("return {")
    for table_info in table_infos:
        content.append("  " + table_info.struct_name + " = " + table_info.struct_name + ",")
    content.append("}")
    
    path = out_folder + out_folder[out_folder.rfind('/'):] + ".lua"
    with open(path, "w+", encoding="utf-8") as fs:
        fs.write('\n'.join(content))
    