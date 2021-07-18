from ModelGenAbstract import ModelGenAbstract
import openpyxl
import importlib
import os
from TableFieldInfo import *
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


def get_model_gens() -> dict[str, ModelGenAbstract]:
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


def get_namespace(class_name: str) -> str:
    if class_name.find('.') == -1:
        return None
    return class_name[:class_name.rfind('.')]


def get_class_type_name(class_name: str) -> str:
    if class_name.find('.') == -1:
        return class_name
    return class_name[class_name.rfind('.')+1:]

def get_table_datas(excel_paths: list):

    table_datas: dict[str, TableFieldInfo] = {}

    for excel_path in excel_paths:
        table_name = get_filename_without_ext(excel_path)
        namespace = get_namespace(table_name)
        class_type_name = get_class_type_name(table_name)
        table_datas[table_name] = TableFieldInfo(class_type_name, [], namespace)

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

            table_datas[table_name].field_infos.append(
                FieldInfo(type, field, note))
        # data
        rec_list = []
        for line in range(line_field + 1, len(rows)):
            rec = []
            for rec_item in rows[line]:
                rec.append(rec_item.value)
            rec_list.append(rec)

    return table_datas

def compile(excel_paths: list, modelcfg: ModelConfig, compiler: CompilerConfig):

    table_models: dict[str, TableFieldInfo] = get_table_datas(excel_paths)

    # end loop
    # generate model
    model_gens = get_model_gens()
    for gen_name in modelcfg.generator_names:
        gen = model_gens[gen_name]

        if modelcfg.is_combine:
            text = gen.get_all_model(table_models)
            path = modelcfg.outdir + "/" + modelcfg.out_filename + gen.get_file_ext()
            write_all_text(path, text)
        else:
            for table_name, field_infos in table_models.items():
                text = gen.get_model(field_infos)

                folder = modelcfg.outdir
                if field_infos.namespace != None:
                    folder = folder + "/" + field_infos.namespace.replace('.', '/')
                if not os.path.exists(folder):
                    os.makedirs(folder)
                path = folder + "/" + field_infos.class_type_name + gen.get_file_ext()
                write_all_text(path, text)
    # compile
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


compile(path, model, None)