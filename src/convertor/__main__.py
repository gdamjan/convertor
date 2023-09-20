# -*- encoding: utf-8 -*-
from __future__ import print_function

from .core import convert_doc

from os import path
import argparse
import sys

DESCRIPTION = """Convert ODF files from YUSCII to UTF-8.
For each file `FILE.odt' will create a converted `FILE-NEW.odt' in
the same directory.
"""

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--convert", dest='filenames', nargs='+', help="file(s) to convert", metavar="FILE")
    group.add_argument("--webapp", action='store_true', help="run a demo web app")
    args = parser.parse_args()
    if args.webapp:
        sys.exit(webapp())
    if args.filenames:
        result = convert_files(args.filenames)
        sys.exit(result)
    parser.print_help()

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

def webapp(hostname='localhost', port=5000, use_debugger=False, use_reloader=False):
    from werkzeug import run_simple
    from .web_app import application
    return run_simple(hostname, port, application, use_debugger, use_reloader)

if __name__ == '__main__':
    main()
