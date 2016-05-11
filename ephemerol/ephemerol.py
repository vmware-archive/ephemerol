#!/usr/bin/python

import argparse
import sys
from SingleFileProcessor import SingleFileProcessor
from terminaltables import AsciiTable

arg_parser = argparse.ArgumentParser(description='Scan application for cloud readiness')
arg_parser.add_argument('file', metavar='files...', type=lambda x: is_valid_file(arg_parser, x),
                        help='application archives to scan for cloud readiness')


def is_valid_file(parser, arg):
    try:
        fn = open(arg, "U")
        fn.close()
        return arg
    except IOError:
        parser.error("The file %s does not appear to exist." % arg)


def main(argv):
    args = arg_parser.parse_args(argv)
    input_file = args.file
    print "Examining %s" % input_file
    # pass file to process strategy
    processor = SingleFileProcessor.with_defaults()
    results = processor.process(input_file)
    results.insert(0, ["Source", "Result"])
    table = AsciiTable(results)
    print table.table


if __name__ == '__main__':
    # only executed when the module is run directly.
    main(sys.argv[1:])
