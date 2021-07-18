from TableFieldInfo import *


type_map = get_type_map()
type_map[TypeInt16] = "short"
type_map[TypeInt32] = "int"
type_map[TypeInt64] = "long"
type_map[TypeBool] = "boolean"
type_map[TypeString] = "String"


class java:

    def get_file_ext(self):
        return ".java"

    def gen_class(self, field_infos: TableFieldInfo, is_public: bool) -> str:
        strlist = []
        strlist.append("\npublic class " + field_infos.class_type_name + " {")
        for _field in field_infos.field_infos:
            field: FieldInfo = _field
            if field.note != None:
                strlist.append("    /**")
                strlist.append("    * " + field.note)
                strlist.append("    */")

            public_str = ""
            if is_public:
                public_str = "public "

            strlist.append("    {}{} {};".format(
                public_str, type_map[field.type], field.name))
        strlist.append("}\n")

        return "\n".join(strlist)

    def get_model(self, field_infos: TableFieldInfo) -> str:
        strlist = []

        namespace = field_infos.namespace

        if namespace != None:
            strlist.append("package {};".format(namespace))

        body = self.gen_class(field_infos, True)
        strlist.append(body)

        return "\n".join(strlist)

    def get_all_model(self, table_field_infos: dict[str, TableFieldInfo]) -> str:
        strlist = []

        nsinfo = get_namespace_dict(table_field_infos)

        for ns, tbinfos in nsinfo.items():

            for tbinfo in tbinfos:
                body = self.gen_class(tbinfo, False)
                strlist.append(body)

        return "\n".join(strlist)
