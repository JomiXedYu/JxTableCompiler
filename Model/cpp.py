import FieldType
import Utility
from TableInfo import *

typemap = FieldType.get_fieldtype_map()
typemap[FieldType.TypeInt16] = "int16_t"
typemap[FieldType.TypeInt32] = "int32_t"
typemap[FieldType.TypeInt64] = "int64_t"
typemap[FieldType.TypeString] = "std::string"

def gen_class(table_info: TableInfo) -> str:
    strlist = []
    strlist.append("\nstruct " + table_info.struct_name)
    strlist.append("{")
    for _field in table_info.field_infos:
        field: FieldInfo = _field
        if field.note != None:
            strlist.append("    //" + field.note)
        strlist.append("    {} {};".format(
            FieldType.mapping_fieldtype(typemap, field.type), field.name))
    strlist.append("};\n")

    return "\n".join(strlist)


def generate(table_info: TableInfo, out_folder: str):
    strlist = []
    strlist.append(Utility.get_model_geninfo("//", "cpp"))

    namespace = table_info.namespace

    if namespace != None:
        strlist.append("namespace {}".format(namespace))
        strlist.append("{")

    body = gen_class(table_info)

    if namespace != None:
        body = body.replace("\n", "\n    ")
    strlist.append(body)

    if namespace != None:
        strlist.append("}")

    outstr = "\n".join(strlist)
    outpath = out_folder + "/" + table_info.name + ".h"

    with open(outpath, "w+", encoding="utf-8") as f:
        f.write(outstr)

    print("MODEL: " + outpath)
    

def batch_generate(table_infos: list[TableInfo], out_folder: str, is_combine: bool):

    if not is_combine:
        for table_info in table_infos:
            generate(table_info, out_folder)
        return

    strlist = []
    strlist.append(Utility.get_model_geninfo("//", "cpp"))
    
    nsinfo = tableinfos_to_namespacedic(table_infos)

    for ns, tbinfos in nsinfo.items():
        if ns != "":
            strlist.append("namespace {}".format(ns))
            strlist.append("{")

        for tbinfo in tbinfos:
            body = gen_class(tbinfo)
            if ns != "":
                body = body.replace("\n", "\n    ")
            strlist.append(body)
        if ns != "":
            strlist.append("}")


    content = "\n".join(strlist)
    outpath = out_folder + out_folder[out_folder.rfind('/'):] + ".h"

    with open(outpath, "w+", encoding="utf-8") as f:
        f.write(content)

    print("MODEL: " + outpath)