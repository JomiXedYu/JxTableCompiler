from ModelGenAbstract import ModelGenAbstract
import openpyxl
import importlib
import os
from RecordInfo import *
from Config import *


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


def is_pyfile(filename: str) -> bool:
    return get_filename_ext(filename) == ".py"


def get_module_names(dir: str) -> list:
    ret = []
    for f in os.listdir(dir):
        if not is_pyfile(f):
            continue
        pos = f.rfind('.')
        ret.append(f[0:pos])
    return ret


def get_models() -> dict[str, ModelGenAbstract]:
    names = get_module_names("./Model")
    dict = {}
    for name in names:
        module = importlib.import_module("Model." + name)
        class_type = getattr(module, name)
        dict[name] = class_type()
    return dict


def get_compiler() -> dict[str, ModelGenAbstract]:
    names = get_module_names("./Compiler")
    dict = {}
    for name in names:
        module = importlib.import_module(name)
        class_type = getattr(module, name)
        dict[name] = class_type()
    return dict


def write_all_text(filename: str, text: str):
    with open(filename, "w+") as f:
        f.write(text)


def compile(excel_paths: list, model: ModelConfig, compiler: CompilerConfig):

    table_models: dict[str, list[TableFieldInfo]] = {}

    for excel_path in excel_paths:
        table_name = get_filename_without_ext(excel_path)
        table_models[table_name] = []

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

            table_models[table_name].append(TableFieldInfo(type, field, note))
        # data
        rec_list = []
        for line in range(line_field + 1, len(rows)):
            rec = []
            for rec_item in rows[line]:
                rec.append(rec_item.value)
            rec_list.append(rec)

    # end loop
    # generate model
    model_gens = get_models()
    for gen_name in model.generator_names:
        gen = model_gens[gen_name]

        if model.is_combine:
            text = gen.get_all_model(table_models, model.namespace)
            path = model.outdir + "/" + model.out_filename + gen.get_file_ext()
            write_all_text(path, text)
        else:
            for table_name, field_infos in table_models.items():
                text = gen.get_model(table_name, field_infos, model.namespace)
                path = model.outdir + "/" + table_name + gen.get_file_ext()
                write_all_text(path, text)
    # compile
    pass


desktop = r"C:\Users\JomiXedYu\Desktop"
path = [desktop + r"\en.xlsx"]

model = ModelConfig(desktop, namespace="ax", out_filename="kk")
model.add("csharp")
model.add("java")
model.add("cpp")
model.add("lua")
model.add("c")
model.add("python")


compile(path, model, None)
