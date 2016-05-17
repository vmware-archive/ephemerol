class ScanRecord(dict):

   _keys = ['file_category', 'file_name', 'refactor_rating', 'file_type']

   def __init__(self, file_category, file_type, file_name, refactor_rating):
      self['file_category'] = file_category
      self['file_type'] = file_type
      self['refactor_rating'] = refactor_rating
      self['file_name'] = file_name