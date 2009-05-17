from zipfile import ZipFile
from collections import namedtuple

from lxml import etree

from util import convert_text, the_stupid_fonts
from odffile import ODFFile


def build_namespace_tuple(nsmap):
    factory = namedtuple('namespaces', ' '.join(nsmap.keys()))
    return factory(*['{%s}' % x for x in nsmap.values()])

def convert_doc(doc):
    the_stupid_styles = {}

    styles = doc.get_xml("styles")
    styles = convert_styles(styles, the_stupid_styles)

    content = doc.get_xml("content")
    content = convert_styles(content, the_stupid_styles)
    content = convert_body(content, the_stupid_styles)

    doc.set_xml("styles", styles)
    doc.set_xml("content", content)
    return doc

def convert_styles(tree, the_stupid_styles):
    # TODO: style inheritance??? implicit inherit from "Standard"?
    root = tree.getroot()
    ns = build_namespace_tuple(root.nsmap)

    # find the styles with the stupid fonts
    #styles = "/office:document-content|office:document-styles/office:automatic-styles"
    prop_path = "//style:text-properties[@style:font-name|@style:font-name-complex]"
    for text_prop in root.xpath(prop_path, namespaces=root.nsmap):
        font = text_prop.get(ns.style + 'font-name') or text_prop.get(ns.style + 'font-name-complex')
        font = font.lower()
        if font in the_stupid_fonts:
            style_name = text_prop.getparent().get(ns.style + 'name')
            the_stupid_styles[style_name] = font
            text_prop.set(ns.style + "font-name", the_stupid_fonts[font][0])
    return tree

def convert_body(tree, the_stupid_styles):
    root = tree.getroot()

    # find the text with the selected styles, for each style loop the whole tree
    # maybe it's smarter to iterate the tree and then compare for style
    # test with really big documents ???

    text_path = "/office:document-content/office:body/office:text"
    text_find = etree.XPath(text_path + '//*[@text:style-name=$name]', namespaces=root.nsmap)
    #text = root.xpath(text_path, namespaces=root.nsmap)[0]
    for style, font in the_stupid_styles.items():
        for para in text_find(root, name=style):
            if para.text:
                para.text = convert_text(para.text, font)
            for child in para:
                if child.tail:
                    child.tail = convert_text(child.tail, font)
    return tree



# pretty_print = lambda el: lxml.etree.tostring(el, pretty_print=True)
# find = lxml.etree.XPath("//b")
# tree = lxml.etree.parse(StringIO.StringIO(xml))
# root = tree.getroot()
# nsmap = root.nsmap
# tree.xpath('.//style:font-face', namespaces=nsmap)
# tree.xpath('.//style:text-properties', namespaces=nsmap)

# XPath:
#   //style:style[style:text-properties[@style:font-name|@style:font-name-complex]]
#   /office:document-content/office:body/office:text
