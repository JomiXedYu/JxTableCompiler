import argparse
import os
import DataCompiler
import ModelGenerator

parser = argparse.ArgumentParser()
parser.add_argument("file", help="excel.xlsx or paths.txt")

parser.add_argument("--model", help="model generator")
parser.add_argument("--model_out", help="model output folder")
parser.add_argument("--combine_model", help="bool")

parser.add_argument("--data", help="data compiler")
parser.add_argument("--data_out", help="data output folder")
parser.add_argument("--combine_data", help="bool")

args = parser.parse_args()

is_batch = args.file.endswith(".txt")
excel_paths = []
if not is_batch:
    excel_paths.append(args.file)
else:
    with open(args.file, "r") as fs:
        while True:
            line = fs.readline()
            if line:
                pline = line.strip()
                if pline != "":
                    excel_paths.append(pline)
            else:
                break

if args.data:
    if not is_batch:
        DataCompiler.compile(args.data, excel_paths[0], args.data_out)
    else:
        DataCompiler.batch_compile(args.data, excel_paths, args.data_out, args.combine_data == "True")

if args.model:
    if not is_batch:
        ModelGenerator.generate(args.model, excel_paths[0], args.model_out)
    else:
        ModelGenerator.batch_generate(args.model, excel_paths, args.model_out, args.combine_model == "True")
    pass
