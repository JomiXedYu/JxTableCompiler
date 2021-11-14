from TableFieldInfo import *
import FieldType

type_map = FieldType.get_type_map()
type_map[FieldType.TypeInt16] = "short"
type_map[FieldType.TypeInt32] = "int"
type_map[FieldType.TypeInt64] = "long"
class csharp:

    def get_file_ext(self):
        return ".cs"

    def gen_class(self, field_infos: TableFieldInfo) -> str:
        strlist = []
        strlist.append("\n[System.Serializable]")
        strlist.append("public class " + field_infos.class_type_name)
        strlist.append("{")
        for _field in field_infos.field_infos:
            field: FieldInfo = _field
            if field.note != None:
                strlist.append("    /// <summary>")
                strlist.append("    /// " + field.note)
                strlist.append("    /// </summary>")
            strlist.append("    public {} {};".format(
                FieldType.mapping_fieldtype(type_map, field.type), field.name))
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
