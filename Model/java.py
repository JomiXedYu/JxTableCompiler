import FieldType

from TableInfo import *

typemap = FieldType.get_fieldtype_map()
typemap[FieldType.TypeInt16] = "short"
typemap[FieldType.TypeInt32] = "int"
typemap[FieldType.TypeInt64] = "long"
typemap[FieldType.TypeBool] = "boolean"
typemap[FieldType.TypeString] = "String"

def gen_class(table_info: TableInfo, is_public: bool) -> str:
    strlist = []
    strlist.append("\n")

    head = "class "

    if is_public:
        head = "public " + head
        
    strlist.append(head + table_info.struct_name + " {")
    for _field in table_info.field_infos:
        field: FieldInfo = _field
        if field.note != None:
            strlist.append("    /**")
            strlist.append("    * " + field.note)
            strlist.append("    */")

        strlist.append("    public {} {};".format(FieldType.mapping_fieldtype(typemap, field.type), field.name))
    strlist.append("}\n")

    return "\n".join(strlist)


def generate(table_info: TableInfo, out_folder: str):
    strlist = []

    namespace = table_info.namespace

    if namespace != None:
        strlist.append("package {};".format(namespace))

    body = gen_class(table_info, True)
    strlist.append(body)

    outpath = out_folder + "/" + table_info.name + ".java"

    with open(outpath, "w+", encoding="utf-8") as f:
        f.write("\n".join(strlist))
    

def batch_generate(table_infos: list[TableInfo], out_folder: str, is_combine: bool):

    if not is_combine:
        for table_info in table_infos:
            generate(table_info, out_folder)
        return

    strlist = []

    nsinfo = tableinfos_to_namespacedic(table_infos)

    for ns, tbinfos in nsinfo.items():

        for tbinfo in tbinfos:
            body = gen_class(tbinfo, False)
            strlist.append(body)

    outpath = out_folder + out_folder[out_folder.rfind('/'):] + ".java"
    content = "\n".join(strlist)

    with open(outpath, "w+", encoding="utf-8") as f:
        f.write(content)