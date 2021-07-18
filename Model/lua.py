from TableFieldInfo import *


type_map = get_type_map()
type_map[TypeInt16] = "number"
type_map[TypeInt32] = "number"
type_map[TypeInt64] = "number"
type_map[TypeFloat] = "number"
type_map[TypeDouble] = "number"
type_map[TypeBool] = "boolean"
type_map[TypeString] = "string"


class lua:

    def get_file_ext(self):
        return ".lua"

    def gen_class(self, field_infos: TableFieldInfo) -> str:
        strlist = []
        strlist.append("\nlocal " + field_infos.class_type_name + " = ")
        strlist.append("{")
        for _field in field_infos.field_infos:
            field: FieldInfo = _field
            if field.note != None:
                strlist.append("    -- " + field.note)
            strlist.append("    ---@type " + field.type)
            strlist.append("    local {} = nil".format(field.name))
        strlist.append("}\n")

        return "\n".join(strlist)

    def get_model(self, field_infos: TableFieldInfo) -> str:
        strlist = []

        body = self.gen_class(field_infos)
        strlist.append(body)

        strlist.append("return " + field_infos.class_type_name)

        return "\n".join(strlist)

    def get_all_model(self, table_field_infos: dict[str, TableFieldInfo]) -> str:
        strlist = []

        nsinfo = get_namespace_dict(table_field_infos)

        for ns, tbinfos in nsinfo.items():

            for tbinfo in tbinfos:
                body = self.gen_class(tbinfo)
                strlist.append(body)

        strlist.append("return {")
        for tb in nsinfo.values():
            for info in tb:
                strlist.append("    " + info.class_type_name +
                               " = " + info.class_type_name + ",")
        strlist.append("}")

        return "\n".join(strlist)
