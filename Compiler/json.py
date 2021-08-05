import json as js
from TableData import *



class json:

    def compile(self, outdir: str, table_datas: list[TableData]):

        for data in table_datas:
            recs = data.to_pyobject()
            jstr = js.dumps(recs, indent=4, ensure_ascii=False)
            path = outdir + "/" + data.table_name + ".json"
            with open(path, "w+",encoding="utf-8") as f:
                f.write(jstr)

        pass
