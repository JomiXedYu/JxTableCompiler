from TableFieldInfo import *

class ModelGenAbstract:

    def get_file_ext(self):
        pass

    def get_model(self, field_infos: TableFieldInfo) -> str:
        pass

    def get_all_model(self, table_field_infos: dict[str, TableFieldInfo]) -> str:
        pass
