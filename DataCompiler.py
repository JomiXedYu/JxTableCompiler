import os
from TableData import gen_table_data, gen_table_datas
import Utility

from Compiler import _loader

def get_compiler(name: str):
    return getattr(_loader, name)

# compilers = ExtensionLoader.get_classes("Compiler")

def __create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def compile(compiler_name: str, excel_path: str, out_folder: str):
    __create_folder(out_folder)
    tabledata = gen_table_data( Utility.std_paths(excel_path) )
    get_compiler(compiler_name).compile(tabledata, Utility.std_path(out_folder))
    pass

def batch_compile(compiler_name: str, excel_paths: list[str], out_folder: str, is_combine: bool):
    __create_folder(out_folder)
    tabledatas = gen_table_datas( Utility.std_paths(excel_paths) )
    get_compiler(compiler_name).batch_compile(tabledatas, Utility.std_path(out_folder), is_combine)
    pass

