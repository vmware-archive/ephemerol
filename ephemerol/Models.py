class ScanItem():

    def __init__(self, file_category, file_type, file_name, refactor_rating):
        self.file_category = file_category
        self.file_type = file_type
        self.refactor_rating = refactor_rating
        self.file_name = file_name

    def __key(self):
        return (self.file_category, self.file_type, self.refactor_rating, self.file_name)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)