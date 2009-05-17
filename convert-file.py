#! /usr/bin/env python
"""\
Usage: %(program)s FILE.odt [FILE1.odt [FILE2 ....]]

For each file `FILE.odt' will create a converted `FILE-NEW.odt' in 
the same directory.
"""

import sys
from os import path

from convertor import *

def main(files):
    result = 0
    for fn in files:
        try:
            newfn = '-NEW'.join(path.splitext(fn))
            doc = ODFFile(fn)
            convert_doc(doc)
            doc.save_changes(file(newfn, 'w'))
        except Exception, e:
            print>>sys.stderr, "Can't convert: %s : %s" % (fn, e)
            result = 2
    return result

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.exit(main(sys.argv[1:]))
    else:
        print __doc__ % dict(program=sys.argv[0])
        sys.exit(1)
