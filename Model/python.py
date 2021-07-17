import RecordInfo


type_map = RecordInfo.get_type_map()
type_map[RecordInfo.TypeInt16] = "int"
type_map[RecordInfo.TypeInt32] = "int"
type_map[RecordInfo.TypeInt64] = "int"
type_map[RecordInfo.TypeDouble] = "float"
type_map[RecordInfo.TypeString] = "str"

class python:

    def get_file_ext(self):
        return ".py"

    def gen_class(self, name: str, field_infos: list[RecordInfo.TableFieldInfo]) -> str:
        strlist = []
        strlist.append("\nclass " + name + ":")

        for _field in field_infos:
            field: RecordInfo.TableFieldInfo = _field
            if field.note != None:
                strlist.append("    # " + field.note)
            strlist.append("    " + field.name + " : " + type_map[field.type])

        strlist.append("\n    def __init__(self):")
        for _field in field_infos:
            field: RecordInfo.TableFieldInfo = _field
            strlist.append("        self." + field.name + " = None")

        return "\n".join(strlist)

    def get_model(self, name: str, field_infos: list[RecordInfo.TableFieldInfo], namespace: str) -> str:
        strlist = []

        body = self.gen_class(name, field_infos)
        strlist.append(body)

        return "\n".join(strlist)

    def get_all_model(self, table_field_infos: dict[str, list[RecordInfo.TableFieldInfo]], namespace: str) -> str:
        strlist = []

        for table_name, field_infos in table_field_infos.items():
            body = self.gen_class(table_name, field_infos)
            strlist.append(body)

        return "\n".join(strlist)
