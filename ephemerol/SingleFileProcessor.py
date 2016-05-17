import JavaModule
import pandas as pd

class SingleFileProcessor:

    def __init__(self, modules):
        self.modules = modules

    @classmethod
    def with_defaults(cls):
        return cls([
            JavaModule
        ])

    def process(self, file):
        columns = ['SCAN_GROUP', 'FILE_NAME', 'REFACTOR_RATING']
        df_results = pd.DataFrame(columns=columns)
        for a_module in self.modules:
            if(a_module.handles(file)):
                df_results.append(a_module.do_handle(file))
        return df_results
