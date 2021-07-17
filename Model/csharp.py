import RecordInfo


type_map = RecordInfo.get_type_map()
type_map[RecordInfo.TypeInt16] = "short"
type_map[RecordInfo.TypeInt32] = "int"
type_map[RecordInfo.TypeInt64] = "long"


class csharp:

    def get_file_ext(self):
        return ".cs"

    def gen_class(self, name: str, field_infos: list[RecordInfo.TableFieldInfo]) -> str:
        strlist = []
        strlist.append("\npublic class " + name)
        strlist.append("{")
        for _field in field_infos:
            field: RecordInfo.TableFieldInfo = _field
            if field.note != None:
                strlist.append("    /// <summary>")
                strlist.append("    /// " + field.note)
                strlist.append("    /// </summary>")
            strlist.append("    public {} {};".format(
                type_map[field.type], field.name))
        strlist.append("}\n")

        return "\n".join(strlist)

    def get_model(self, name: str, field_infos: list[RecordInfo.TableFieldInfo], namespace: str) -> str:
        strlist = []

        if namespace != None:
            strlist.append("namespace {}".format(namespace))
            strlist.append("{")

        body = self.gen_class(name, field_infos)
        if namespace != None:
            body = body.replace("\n", "\n    ")
        strlist.append(body)

        if namespace != None:
            strlist.append("}")

        return "\n".join(strlist)

    def get_all_model(self, table_field_infos: dict[str, list[RecordInfo.TableFieldInfo]], namespace: str) -> str:
        strlist = []

        if namespace != None:
            strlist.append("namespace {}".format(namespace))
            strlist.append("{")

        for table_name, field_infos in table_field_infos.items():
            body = self.gen_class(table_name, field_infos)
            if namespace != None:
                body = body.replace("\n", "\n    ")
            strlist.append(body)

        if namespace != None:
            strlist.append("}")

        return "\n".join(strlist)
