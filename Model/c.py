from TableFieldInfo import *


type_map = get_type_map()
type_map[TypeInt16] = "short"
type_map[TypeInt32] = "int"
type_map[TypeInt64] = "long"
type_map[TypeBool] = "int"
type_map[TypeString] = "char*"


class c:

    def get_file_ext(self):
        return ".h"

    def gen_class(self, field_infos: TableFieldInfo) -> str:
        strlist = []
        strlist.append("\nstruct " + field_infos.class_type_name)
        strlist.append("{")
        for _field in field_infos.field_infos:
            field: FieldInfo = _field
            if field.note != None:
                strlist.append("    //" + field.note)
            strlist.append("    {} {};".format(
                type_map[field.type], field.name))
        strlist.append("}\n")

        return "\n".join(strlist)

    def get_model(self, field_infos: TableFieldInfo) -> str:
        strlist = []

        body = self.gen_class(field_infos)
        strlist.append(body)

        return "\n".join(strlist)

    def get_all_model(self, table_field_infos: dict[str, TableFieldInfo]) -> str:
        strlist = []

        nsinfo = get_namespace_dict(table_field_infos)

        for ns, tbinfos in nsinfo.items():

            for tbinfo in tbinfos:
                body = self.gen_class(tbinfo)
                strlist.append(body)

        return "\n".join(strlist)
