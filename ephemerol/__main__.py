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

import argparse
import Scanner
from Models import JSONEncoderModels
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='python -m ephemerol',
                                     description='Scan a source archive for cloud readiness')
    parser.add_argument('-c', help="Flags the rule file as a CSV based rule file. "
                                   " Rules files are considered YAML by default.",
                        action='store_true')
    parser.add_argument('rulefile', help='The file describing the rules the scanner should use')
    parser.add_argument('archive', help='The source archive to scan')
    args = parser.parse_args()
    if args.c:
        Scanner.load_rules(args.rulefile)
    else:
        Scanner.load_yaml_rules(args.rulefile)
    results = Scanner.scan_archive(args.archive)

    print json.dumps(results, cls=JSONEncoderModels, indent=1, sort_keys=True)
