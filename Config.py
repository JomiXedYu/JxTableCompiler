
class ModelConfig:

    generator_names: list[str]

    def __init__(self, outdir: str, out_filename: str = None) -> None:
        self.outdir = outdir
        self.out_filename = out_filename
        self.is_combine = out_filename != None
        self.generator_names = []

    def add(self, generator_name: str):
        self.generator_names.append(generator_name)


class CompilerConfig:

    def __init__(self, outdir: str) -> None:
        self.outdir = outdir
        self.names = []

    def add(self, name: str):
        self.names.append(name)
