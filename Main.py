import openpyxl
import os

from TableData import TableData
from CompilerAbstract import CompilerAbstract
from ModelGenAbstract import ModelGenAbstract
from TableFieldInfo import *
from Config import *

import ExtensionLoader

def get_filename_ext(filename: str) -> str:
    return filename[filename.rfind('.'):]


def get_filename_without_ext(filename: str) -> str:
    filename = filename.replace('\\', '/')
    if filename[-1] == '/':
        return filename
    sfn = filename[filename.rfind('/')+1:]
    dotpos = sfn.rfind('.')
    if dotpos == -1:
        return sfn
    return sfn[:dotpos]

def get_model_gens() -> dict[str, ModelGenAbstract]:
    return ExtensionLoader.get_classes("Model")

def get_compiler() -> dict[str, CompilerAbstract]:
    return ExtensionLoader.get_classes("Compiler")


def write_all_text(filename: str, text: str):
    with open(filename, "w+") as f:
        f.write(text)


def get_namespace(class_name: str) -> str:
    if class_name.find('.') == -1:
        return None
    return class_name[:class_name.rfind('.')]


def get_class_type_name(class_name: str) -> str:
    if class_name.find('.') == -1:
        return class_name
    return class_name[class_name.rfind('.')+1:]


def get_tables_datas(excel_paths: list) -> dict[str, TableData]:

    table_datas: dict[str, TableData] = {}
    
    for excel_path in excel_paths:
        table_name = get_filename_without_ext(excel_path)
        namespace = get_namespace(table_name)
        class_type_name = get_class_type_name(table_name)

        table_field_info = TableFieldInfo(class_type_name, [], namespace)
        records = []
        table_datas[table_name] = TableData(
            table_name, class_type_name, table_field_info, records)

        excel = openpyxl.load_workbook(excel_path)
        sheet = excel.active
        rows = list(sheet.rows)

        line_note = 0
        line_type = 1
        line_field = 2

        field_count = len(rows[line_field])
        # model
        for i in range(0, field_count):
            type = rows[line_type][i].value
            if type == None:
                type = "string"
            field = rows[line_field][i].value
            note = rows[line_note][i].value

            table_datas[table_name].field_infos.field_infos.append(
                FieldInfo(type, field, note))
        # data
        for line in range(line_field + 1, len(rows)):
            rec = []
            for r in rows[line]:
                rec.append(r.value)
            table_datas[table_name].records.append(rec)

    return table_datas


def get_table_field_infos(tables_datas: dict[str, TableData]) -> dict[str, TableFieldInfo]:
    dic = {}
    for name, data in tables_datas.items():
        dic[name] = data.field_infos
    return dic


def compile(excel_paths: list, modelcfg: ModelConfig, compiler: CompilerConfig):

    tables_datas: dict[str, TableData] = get_tables_datas(excel_paths)
    field_infos = get_table_field_infos(tables_datas)
    # generate model
    model_gens = get_model_gens()
    for gen_name in modelcfg.generator_names:
        gen = model_gens[gen_name]

        if modelcfg.is_combine:
            text = gen.get_all_model(field_infos)
            path = modelcfg.outdir + "/" + modelcfg.out_filename + gen.get_file_ext()
            write_all_text(path, text)
        else:
            for field_info in field_infos.values():
                text = gen.get_model(field_info)

                folder = modelcfg.outdir
                if field_info.namespace != None:
                    folder = folder + "/" + \
                        field_info.namespace.replace('.', '/')
                if not os.path.exists(folder):
                    os.makedirs(folder)
                path = folder + "/" + field_info.class_type_name + gen.get_file_ext()
                write_all_text(path, text)
    # compile
    cmpls = get_compiler()
    for cmpl_name in compiler.names:
        cmpl = cmpls[cmpl_name]
        cmpl.compile(compiler.outdir, tables_datas.values())
    pass


desktop = r"C:\Users\JomiXedYu\Desktop\baba"
path = [desktop + "\\en.xlsx", desktop + "\\kk.ch.xlsx"]


model = ModelConfig(desktop, out_filename="ac")
model.add("csharp")
# model.add("java")
# model.add("cpp")
# model.add("lua")
# model.add("c")
# model.add("python")

comp = CompilerConfig(desktop)
comp.add("json")

compile(path, model, comp)
