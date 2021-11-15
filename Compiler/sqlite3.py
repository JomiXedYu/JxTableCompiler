import os
import sqlite3

from TableInfo import *
from TableData import *
import FieldType

typemap = {
    FieldType.TypeInt16: "INTEGER",
    FieldType.TypeInt32: "INTEGER",
    FieldType.TypeInt64: "INTEGER",
    FieldType.TypeBool: "INTEGER",
    FieldType.TypeFloat: "REAL",
    FieldType.TypeDouble: "REAL",
    FieldType.TypeString: "TEXT",
}

def get_type(type: str) -> str:
    if type in typemap:
        return typemap[type]
    return "TEXT"

def get_value(value) -> str:

    if value == None:
        return "NULL"

    t = type(value)
    if t == str:
        return "\"" + value + "\""
    elif t == bool:
        if value:
            return "1"
        else:
            return "0"
    else:
        return str(value)


def create_table(conn, table_info: TableInfo):
    createtb_sb = []
    createtb_sb.append("CREATE TABLE ")
    createtb_sb.append(table_info.struct_name)
    createtb_sb.append("(")

    field_infos = table_info.field_infos
    for i in range(0, len(field_infos)):
        createtb_sb.append(field_infos[i].name)
        createtb_sb.append(" ")
        createtb_sb.append(get_type(field_infos[i].type))

        if i != len(field_infos)-1:
            createtb_sb.append(', ')

    createtb_sb.append(");")

    createtb_str = "".join(createtb_sb)
    conn.execute(createtb_str)

def insert_data(conn, table_data: TableData):
    insert_sb = []
    for record in table_data.records:
        insert_sb.append("INSERT INTO ")
        insert_sb.append(table_data.table_info.struct_name)
        insert_sb.append(" values (")
        for i in range(0, len(record)):
            insert_sb.append(get_value(record[i]))
            if i != len(record)-1:
                insert_sb.append(',')
        insert_sb.append(");")
        pass

    insert_str = "".join(insert_sb)
    conn.executescript(insert_str)

def compile(table_data: TableData, out_folder: str):

    dbpath = out_folder + "/" + table_data.name + ".db"

    if(os.path.exists(dbpath)):
        os.remove(dbpath)

    conn = sqlite3.connect(dbpath)

    create_table(conn, table_data.table_info)
    insert_data(conn, table_data)

    conn.close()
    print("DATA: " + dbpath)


def batch_compile(table_datas: dict[str, TableData], out_folder: str, is_combine: bool):
    if not is_combine:
        for table in table_datas.values():
            compile(table, out_folder)
        return

    dbpath = out_folder + out_folder[out_folder.rfind('/'):] + ".db"
    
    conn = sqlite3.connect(dbpath)

    for table_data in table_datas.values():
        create_table(conn, table_data.table_info)
        insert_data(conn, table_data)
    
    conn.close()
    print("DATA: " + dbpath)