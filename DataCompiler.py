import os
from TableData import gen_table_data, gen_table_datas
import ExtensionLoader


compilers = ExtensionLoader.get_classes("Compiler")

def __create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def compile(compiler_name: str, excel_path: str, out_folder: str):
    __create_folder(out_folder)
    tabledata = gen_table_data(excel_path)
    compilers[compiler_name].compile(tabledata, out_folder)
    pass

def batch_compile(compiler_name: str, excel_paths: list[str], out_folder: str, is_combine: bool):
    __create_folder(out_folder)
    tabledatas = gen_table_datas(excel_paths)
    compilers[compiler_name].batch_compile(tabledatas, out_folder, is_combine)
    pass

