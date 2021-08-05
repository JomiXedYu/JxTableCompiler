from TableFieldInfo import *


type_map = get_type_map()
type_map[TypeInt16] = "int16_t"
type_map[TypeInt32] = "int32_t"
type_map[TypeInt64] = "int64_t"
type_map[TypeString] = "std::string"

def gettype(key: str) -> str:
    if key in type_map:
        return type_map[key]
    return key

class cpp:

    def get_file_ext(self):
        return ".hpp"

    def gen_class(self, field_infos: TableFieldInfo) -> str:
        strlist = []
        strlist.append("\nclass " + field_infos.class_type_name)
        strlist.append("{")
        strlist.append("public:")
        for _field in field_infos.field_infos:
            field: FieldInfo = _field
            if field.note != None:
                strlist.append("    /// " + field.note)
            strlist.append("    {} {};".format(
                gettype(field.type), field.name))
        strlist.append("}\n")

        return "\n".join(strlist)

    def get_model(self, field_infos: TableFieldInfo) -> str:
        strlist = []

        namespace = field_infos.namespace

        if namespace != None:
            strlist.append("namespace {}".format(namespace))
            strlist.append("{")

        body = self.gen_class(field_infos)
        if namespace != None:
            body = body.replace("\n", "\n    ")
        strlist.append(body)

        if namespace != None:
            strlist.append("}")

        return "\n".join(strlist)

    def get_all_model(self, table_field_infos: dict[str, TableFieldInfo]) -> str:
        strlist = []

        nsinfo = get_namespace_dict(table_field_infos)

        for ns, tbinfos in nsinfo.items():
            if ns != "":
                strlist.append("namespace {}".format(ns))
                strlist.append("{")

            for tbinfo in tbinfos:
                body = self.gen_class(tbinfo)
                if ns != "":
                    body = body.replace("\n", "\n    ")
                strlist.append(body)
            if ns != "":
                strlist.append("}")

        return "\n".join(strlist)
