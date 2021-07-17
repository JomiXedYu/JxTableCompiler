import RecordInfo


type_map = RecordInfo.get_type_map()
type_map[RecordInfo.TypeInt16] = "short"
type_map[RecordInfo.TypeInt32] = "int"
type_map[RecordInfo.TypeInt64] = "long"
type_map[RecordInfo.TypeBool] = "boolean"
type_map[RecordInfo.TypeString] = "String"

class java:

    def get_file_ext(self):
        return ".java"

    def gen_class(self, name: str, field_infos: list[RecordInfo.TableFieldInfo], prem:str) -> str:
        strlist = []
        if prem == None:
            strlist.append("\nclass " + name + " {")
        else:
            strlist.append("\n{} class {} {{".format(prem, name))

        for _field in field_infos:
            field: RecordInfo.TableFieldInfo = _field
            if field.note != None:
                strlist.append("    /** ")
                strlist.append("    * " + field.note)
                strlist.append("    */")
            strlist.append("    public {} {};".format(
                type_map[field.type], field.name))
        strlist.append("}\n")

        return "\n".join(strlist)

    def get_model(self, name: str, field_infos: list[RecordInfo.TableFieldInfo], namespace: str) -> str:
        strlist = []

        if namespace != None:
            strlist.append("package {};".format(namespace))

        body = self.gen_class(name, field_infos, "public")

        strlist.append(body)

        return "\n".join(strlist)

    def get_all_model(self, table_field_infos: dict[str, list[RecordInfo.TableFieldInfo]], namespace: str) -> str:
        strlist = []

        if namespace != None:
            strlist.append("package {};".format(namespace))

        for table_name, field_infos in table_field_infos.items():
            body = self.gen_class(table_name, field_infos, None)
            strlist.append(body)

        return "\n".join(strlist)
