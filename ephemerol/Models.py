# Copyright (C) 2016-Present Pivotal Software, Inc. All rights reserved.
#
# This program and the accompanying materials are made available under
# the terms of the under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from operator import attrgetter

class ScanItem():
    def __init__(self, app_type, file_category, file_type, file_name, refactor_rating, description, text_pattern
                 , replatform_advice=None):
        self.app_type = app_type if app_type is not None else "n/a"
        self.file_category = file_category if file_category is not None else "n/a"
        self.file_type = file_type if file_type is not None else "n/a"
        self.refactor_rating = str(refactor_rating) if refactor_rating is not None else "0"
        self.file_name = file_name if file_name is not None else "n/a"
        self.description = description if description is not None else "n/a"
        self.text_pattern = text_pattern if text_pattern is not None else "n/a"
        self.replatform_advice = replatform_advice if replatform_advice is not None else "n/a"

    def __key(self):
        return (
            self.app_type, self.file_category, self.file_type, self.refactor_rating, self.file_name, self.description,
            self.text_pattern, self.replatform_advice)

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
        self.app_type = scan_item.app_type
        self.file_category = scan_item.file_category
        self.file_type = scan_item.file_type
        self.refactor_rating = scan_item.refactor_rating
        self.file_name = scan_item.file_name
        self.description = scan_item.description
        self.text_pattern = scan_item.text_pattern
        self.replatform_advice = scan_item.replatform_advice
        self.flagged_file_id = flagged_file_id

    def category_key(self):
        return (self.app_type, self.category, self.file_type, self.refactor_rating, self.description)

    def __key(self):
        return (
            self.app_type, self.file_category, self.file_type, self.refactor_rating, self.file_name, self.description,
            self.text_pattern, self.replatform_advice, self.flagged_file_id)

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
        self.category_result = {}
        self.category_info = []
        score = 1000
        categories_flagged = []
        files_flagged = []
        for entry in self.scan_result_list:
            scan_result_cnt = len(scan_result_list)
            result_count_adj = float(100.00 / scan_result_cnt)
            score = score - float(result_count_adj * float(entry.refactor_rating))
            if entry.file_category not in categories_flagged:
                categories_flagged.append(entry.file_category)
            if entry.flagged_file_id not in files_flagged and entry.refactor_rating != "0":
                files_flagged.append(entry.flagged_file_id)
            if entry.refactor_rating != "0":
                self.category_result[entry.category_key] = entry
            else:
                self.category_info.append(entry)

        self.cloud_readiness_index = round((score / 1000 * 100), 2)
        self.categories_flagged = categories_flagged
        self.files_flagged = files_flagged

    def __key(self):
        return (self.scan_result_list)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class JSONEncoderModels(json.JSONEncoder):
    def default(self, obj):
        result = {}
        if isinstance(obj, ScanStats):
            result['scan_stats'] = {'cloud_readiness_index': obj.cloud_readiness_index,
                                    'categories_flagged': len(obj.categories_flagged),
                                    'files_flagged': len(obj.files_flagged),
                                    'total_results': len(obj.scan_result_list)}
            scan_items_arr = []
            for scan_result in sorted(obj.category_result.values(), key=attrgetter('refactor_rating'), reverse=True):
                scan_items_arr.append(scan_result.__dict__)
                # scan_items_arr.append(json.dumps(scan_result.__dict__,ensure_ascii=False))

            result['scan_stats']['scan_items'] = scan_items_arr

            scan_items_info_arr = []
            for scan_info in obj.category_info:
                scan_items_info_arr.append(scan_info.__dict__)

            result['scan_stats']['scan_items_info'] = scan_items_info_arr

            return result
        return json.JSONEncoder.default(self, obj)
