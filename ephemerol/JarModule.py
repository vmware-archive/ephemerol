from zipfile import ZipFile

class JarModule:

    def __init__(self):
        return

    @classmethod
    def handles(cls, file_name):
        return file_name.endswith(".jar")

    @classmethod
    def do_handle(cls, file_name):
        results = []
        with ZipFile(file_name, 'r') as zfile:
            with zfile.open("META-INF/MANIFEST.MF") as ex_file:
                results.append(["META-INF/MANIFEST.MF", ex_file.read()])
        return results
