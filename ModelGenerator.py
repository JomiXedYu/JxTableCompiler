import os
from TableData import gen_table_data, gen_table_datas
from TableInfo import TableInfo
import Utility

from Model import _loader

def get_generator(name: str):
    return getattr(_loader, name)

# models = ExtensionLoader.get_classes("Model")

def __create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def generate(generator_name: str, excel_path: str, out_folder: str):
    __create_folder(out_folder)
    tabledata = gen_table_data(Utility.std_path(excel_path))
    get_generator(generator_name).generate(tabledata.table_info, Utility.std_path(out_folder))
    pass

def batch_generate(generator_name: str, excel_paths: list[str], out_folder:str, is_combine: bool):
    __create_folder(out_folder)
    tabledatas = gen_table_datas(Utility.std_paths(excel_paths))

    infos : list[TableInfo] = []
    for name, tabledata in tabledatas.items():
        infos.append(tabledata.table_info)

    get_generator(generator_name).batch_generate(infos, Utility.std_path(out_folder), is_combine)
    pass