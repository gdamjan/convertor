from .util import the_stupid_fonts, build_namespace_tuple

from lxml import etree
from zipfile import ZipFile
from io import StringIO

# Global sentinels
INHERIT_CONVERT = object()
DONT_CONVERT = object()
NO_PARENT_STYLE = object()

def convert_doc(document_file):
    '''Given a filename or a file object of a ODT file (a zip file really)
    returns a converted file object'''

    file_in = ZipFile(document_file)
    styles = etree.parse(file_in.open('styles.xml'))
    content = etree.parse(file_in.open('content.xml'))

    style_mapping = {}
    convert_styles(styles, style_mapping)
    convert_styles(content, style_mapping)
    convert_content(content, style_mapping)

    # build a new odt file in memory
    fp = StringIO()
    file_out = ZipFile(fp, mode='w', compression=file_in.compression)
    for zinfo in file_in.infolist():
        name = zinfo.filename
        if name not in ('styles.xml', 'content.xml'):
            file_out.writestr(zinfo, file_in.read(zinfo))
    file_out.writestr('styles.xml', etree.tostring(styles, encoding='utf8'))
    file_out.writestr('content.xml', etree.tostring(content, encoding='utf8'))
    file_out.close()
    return fp


def convert_styles(tree, style_mapping):
    '''Iterates through all styles defined in the tree and extracts the
    convertor function to use for that style.

    Also the tree will be changed inplace.
    '''
    root = tree.getroot()
    ns = build_namespace_tuple(root.nsmap)

    for style in root.xpath('//style:default-style|//style:style', namespaces=root.nsmap):
        if style.tag == ns.style('default-style'):
            style_name = style.get(ns.style('family'))
        else:
            style_name = style.get(ns.style('name'))
        parent_style_name = style.get(ns.style('parent-style-name'), NO_PARENT_STYLE)

        font = None
        font_xpath = './/style:text-properties[@style:font-name|@style:font-name-complex]'
        for text_properties in style.xpath(font_xpath, namespaces=root.nsmap):
            font = text_properties.get(ns.style('font-name')) \
                    or text_properties.get(ns.style('font-name-complex'))

        if font is None:
            if parent_style_name in style_mapping:
                # if the style has no font by itself but has a parent-style that
                # had the stupid font then just remember the style and use the
                # conversion from the parent style
                style_mapping[style_name] = style_mapping[parent_style_name]
                #msg = 'PARENT(%s)' % parent_style_name
            else:
                # no font-name, no parent-style in this style
                # the element will inherit the conversion from
                # it's parent in the content *tree*
                style_mapping[style_name] = INHERIT_CONVERT
                #msg = 'INHERITED from content parent'

        elif font in the_stupid_fonts:
            # if a stupid font is used in this style:
            #  - change the font in the style
            #  - and remember the style so that we can convert the text later
            text_properties.set(ns.style('font-name'), the_stupid_fonts[font].replacement_font)
            style_mapping[style_name] = the_stupid_fonts[font].convert_func
            #msg = 'REPLACE'
        else:
            # there's a font but not a stupid one, use null conversion
            style_mapping[style_name] = DONT_CONVERT
            #msg = "DON'T CONVERT"
        #print msg, '=>', style_name
    return

def convert_element(el, func):
    if el.text:
        el.text = func(el.text)
    for child in el:
        if child.tail:
            child.tail = func(child.tail)
    return

def convert_tree(tree, inherited_convert, style_mapping, ns):
   # iterate all direct children
    for el in tree:
        style = el.get(ns.text('style-name'))
        if style in style_mapping:
            convert_func = style_mapping[style]
        else:
            convert_func = DONT_CONVERT

        if convert_func is INHERIT_CONVERT:
            convert_func = inherited_convert
        if convert_func is not DONT_CONVERT:
            convert_element(el, convert_func)

        # recursively call itself until there are no children left
        # depth-first
        convert_tree(el, convert_func, style_mapping, ns)

def convert_content(tree, style_mapping):
    root = tree.getroot()
    ns = build_namespace_tuple(root.nsmap)

    text_path = '/office:document-content/office:body/office:text'
    body = root.xpath(text_path, namespaces=root.nsmap)

    convert_tree(body, DONT_CONVERT, style_mapping, ns)
    return


# pretty_print = lambda el: etree.tostring(el, pretty_print=True)
# find = lxml.etree.XPath("//b")
# tree = lxml.etree.parse(StringIO.StringIO(xml))
# root = tree.getroot()
# nsmap = root.nsmap
# tree.xpath('.//style:font-face', namespaces=nsmap)
# tree.xpath('.//style:text-properties', namespaces=nsmap)

# XPath:
#   //style:style[style:text-properties[@style:font-name|@style:font-name-complex]]
#   /office:document-content/office:body/office:text
