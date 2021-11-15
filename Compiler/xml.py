import xml.dom.minidom

from TableInfo import *
from TableData import *


def compile(table_data: TableData, out_folder: str):

    doc = xml.dom.minidom.Document()
    
    root = doc.createElement("ArrayOf" + table_data.table_info.struct_name)
    doc.appendChild(root)
    field_infos = table_data.table_info.field_infos

    for record in table_data.records:
        record_node = doc.createElement(table_data.table_info.struct_name)
        root.appendChild(record_node)

        for i in range(0, len(field_infos)):
            if field_infos[i].isprop:
                record_node.setAttribute(field_infos[i].name, record[i])
            else:
                node = doc.createElement(field_infos[i].name)
                #防止写入None
                appstr = None
                if record[i] != None:
                    appstr = str(record[i])
                else:
                    appstr = ""
                node.appendChild(doc.createTextNode(appstr))
                record_node.appendChild(node)

    path = out_folder + "/" + table_data.name + ".xml"
    with open(path, "w+", encoding="utf-8") as f:
        doc.writexml(f, addindent="  ", newl="\n", encoding="utf-8")


def batch_compile(table_datas: dict[str, TableData], out_folder: str, is_combine: bool):
    for table in table_datas.values():
        compile(table, out_folder)
    pass
