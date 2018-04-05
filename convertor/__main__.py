# -*- encoding: utf-8 -*-
from __future__ import print_function

from convertor import convert_doc

from os import path
import argparse
import sys

DESCRIPTION = """Convert ODF files from YUSCII to UTF-8.
For each file `FILE.odt' will create a converted `FILE-NEW.odt' in
the same directory.
"""

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("filenames", nargs='+', help="file(s) to convert ", metavar="FILE")
    args = parser.parse_args()
    result = convert_files(args.filenames)
    sys.exit(result)

def convert_files(filenames):
    result = 0
    for fname in filenames:
        try:
            newfn = '-NEW'.join(path.splitext(fname))
            buf = convert_doc(fname)
            fout = open(newfn, 'wb')
            fout.write(buf.getvalue())
            fout.close()
        except Exception as e:
            print("Can't convert: %s : %s" % (fname, e), file=sys.stderr)
            result = 2
    return result

if __name__ == '__main__':
    main()
