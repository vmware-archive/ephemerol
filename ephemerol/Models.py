class ScanItem():
    def __init__(self, app_type, file_category, file_type, file_name, refactor_rating, description, text_pattern):
        self.app_type = app_type
        self.file_category = file_category
        self.file_type = file_type
        self.refactor_rating = refactor_rating
        self.file_name = file_name
        self.description = description
        self.text_pattern = text_pattern

    def __key(self):
        return (
        self.app_type, self.file_category, self.file_type, self.refactor_rating, self.file_name, self.description,
        self.text_pattern)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

class ScanResult():
    def __init__(self, scan_item, flagged_file_id):
        self.scan_item = scan_item
        self.flagged_file_id = flagged_file_id

    def __key(self):
        return (
        self.scan_item, self.flagged_file_id)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

class ScanStats():
    def __init__(self, scan_result_list):
        self.scan_result_list = scan_result_list
        score = 100
        for entry in self.scan_result_list:
            score = score - int(entry.scan_item.refactor_rating)
        self.cloud_readiness_index = score