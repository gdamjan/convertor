from zipfile import ZipFile
from cStringIO import StringIO

import lxml.etree


class ODFFile(ZipFile):
    def __init__(self, file, mode='r', compression=0, allowZip64=False):
        ZipFile.__init__(self, file, mode=mode, \
                compression=compression, allowZip64=allowZip64)
        self.__unchanged = self.namelist()
        self.__updated = {}

    def get_xml(self, name):
        fp  = self.open('%s.xml' % name)
        return lxml.etree.parse(fp)

    def set_xml(self, name, tree):
        name = '%s.xml' % name
        if name in self.__unchanged:
            self.__unchanged.remove(name)
        if tree is not None:
            self.__updated[name] = tree

    def save_changes(self, fp=None):
        # TODO: fails second time called, WHY?
        if fp is None:
            fp = StringIO()
        zo = ZipFile(fp, mode='w', compression=self.compression)
        updated = dict(self.__updated)
        for zinfo in self.infolist():
            name = zinfo.filename
            # just copy the unchanged
            if name in self.__unchanged:
                zo.writestr(zinfo, self.read(zinfo))
            # write the changed in the same order
            elif name in updated:
                s = lxml.etree.tostring(updated.pop(name))
                zo.writestr(name, s)
        # append the possible remaining (new?)
        for name, tree in updated.items():
            s = lxml.etree.tostring(tree)
            zo.writestr(name, s)
        zo.close()
        return fp
