from zipfile import ZipFile


def handles(file_name):
    return (
        file_name.endswith(".zip")
    )


def do_handle(file_name):
    results = []
    with ZipFile(file_name, 'r') as zfile:
        with zfile.open("src/main/webapp/WEB-INF/web.xml") as ex_file:
            results.append(["src/main/webapp/WEB-INF/web.xml", ex_file.read()])
    return results
