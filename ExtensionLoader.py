import importlib
import os


def get_filename_ext(filename: str) -> str:
    return filename[filename.rfind('.'):]


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


def get_classes(folder: str) -> dict[str, any]:
    folder = folder.replace('\\', '/')
    names = get_module_names("./" + folder)
    dict = {}
    for name in names:
        module = importlib.import_module(folder.replace('/', '.') + '.' + name)
        class_type = getattr(module, name)
        dict[name] = class_type()
    return dict
