import JavaModule


class SingleFileProcessor:

    def __init__(self, modules):
        self.modules = modules

    @classmethod
    def with_defaults(cls):
        return cls([
            JavaModule
        ])

    def process(self, file):
        results = [ ]
        for a_module in self.modules:
            if(a_module.handles(file)):
                results += a_module.do_handle(file)
        return results
