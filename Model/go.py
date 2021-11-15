import FieldType
import Utility
from TableInfo import *

typemap = FieldType.get_fieldtype_map()
typemap[FieldType.TypeFloat] = "float32"
typemap[FieldType.TypeDouble] = "float64"

def gen_class(table_info: TableInfo) -> str:
    strlist = []
    strlist.append("\ntype " + table_info.struct_name + " struct {")
    for _field in table_info.field_infos:
        field: FieldInfo = _field
        if field.note != None:
            strlist.append("    //" + field.note)
        strlist.append("    {} {};".format(field.name, FieldType.mapping_fieldtype(typemap, field.type)))
    strlist.append("}\n")

    return "\n".join(strlist)


def generate(table_info: TableInfo, out_folder: str):
    strlist = []
    strlist.append(Utility.get_model_geninfo("//", "go"))
    namespace = table_info.namespace

    if namespace != None:
        strlist.append("package {}".format(namespace))

    body = gen_class(table_info)
    strlist.append(body)

    outstr = "\n".join(strlist)
    outpath = out_folder + "/" + table_info.name + ".go"

    with open(outpath, "w+", encoding="utf-8") as f:
        f.write(outstr)
    

def batch_generate(table_infos: list[TableInfo], out_folder: str, is_combine: bool):

    for table_info in table_infos:
        generate(table_info, out_folder)
    return