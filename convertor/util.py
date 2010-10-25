from functools import partial
from collections import namedtuple
import string

from caselessdict import CaselessDict

def build_namespace_tuple(nsmap):
    keys = []
    values = []
    def create_f(x):
        fmt = '{%s}%%s' % x
        def f(y):
            return fmt % y
        return f
    for prefix, namespace in nsmap.items():
        keys.append(prefix) # maybe clean-up prefix first
        values.append(create_f(namespace))
    factory = namedtuple('namespaces', " ".join(keys))
    return factory(*values)

def convert_text(text, variant):
    return unicode(text).translate(variant)

variant1 = {
    # MAC C Swiss, Macedonian Times...
    0x0040: 0x0416,    # CYRILLIC CAPITAL LETTER ZHE
    0x0041: 0x0410,    # CYRILLIC CAPITAL LETTER A
    0x0042: 0x0411,    # CYRILLIC CAPITAL LETTER BE
    0x0043: 0x0426,    # CYRILLIC CAPITAL LETTER TSE
    0x0044: 0x0414,    # CYRILLIC CAPITAL LETTER DE
    0x0045: 0x0415,    # CYRILLIC CAPITAL LETTER IE
    0x0046: 0x0424,    # CYRILLIC CAPITAL LETTER EF
    0x0047: 0x0413,    # CYRILLIC CAPITAL LETTER GHE
    0x0048: 0x0425,    # CYRILLIC CAPITAL LETTER HA
    0x0049: 0x0418,    # CYRILLIC CAPITAL LETTER I
    0x004a: 0x0408,    # CYRILLIC CAPITAL LETTER JE
    0x004b: 0x041a,    # CYRILLIC CAPITAL LETTER KA
    0x004c: 0x041b,    # CYRILLIC CAPITAL LETTER EL
    0x004d: 0x041c,    # CYRILLIC CAPITAL LETTER EM
    0x004e: 0x041d,    # CYRILLIC CAPITAL LETTER EN
    0x004f: 0x041e,    # CYRILLIC CAPITAL LETTER O
    0x0050: 0x041f,    # CYRILLIC CAPITAL LETTER PE
    0x0051: 0x0409,    # CYRILLIC CAPITAL LETTER LJE
    0x0052: 0x0420,    # CYRILLIC CAPITAL LETTER ER
    0x0053: 0x0421,    # CYRILLIC CAPITAL LETTER ES
    0x0054: 0x0422,    # CYRILLIC CAPITAL LETTER TE
    0x0055: 0x0423,    # CYRILLIC CAPITAL LETTER U
    0x0056: 0x0412,    # CYRILLIC CAPITAL LETTER VE
    0x0057: 0x040a,    # CYRILLIC CAPITAL LETTER NJE
    0x0058: 0x040f,    # CYRILLIC CAPITAL LETTER DZHE
    0x0059: 0x0405,    # CYRILLIC CAPITAL LETTER DZE
    0x005a: 0x0417,    # CYRILLIC CAPITAL LETTER ZE
    0x005b: 0x0428,    # CYRILLIC CAPITAL LETTER SHA
    0x005c: 0x0403,    # CYRILLIC CAPITAL LETTER GJE
    0x005d: 0x040c,    # CYRILLIC CAPITAL LETTER KJE
    0x005e: 0x0427,    # CYRILLIC CAPITAL LETTER CHE
    0x0060: 0x0436,    # CYRILLIC SMALL LETTER ZHE
    0x0061: 0x0430,    # CYRILLIC SMALL LETTER A
    0x0062: 0x0431,    # CYRILLIC SMALL LETTER BE
    0x0063: 0x0446,    # CYRILLIC SMALL LETTER TSE
    0x0064: 0x0434,    # CYRILLIC SMALL LETTER DE
    0x0065: 0x0435,    # CYRILLIC SMALL LETTER IE
    0x0066: 0x0444,    # CYRILLIC SMALL LETTER EF
    0x0067: 0x0433,    # CYRILLIC SMALL LETTER GHE
    0x0068: 0x0445,    # CYRILLIC SMALL LETTER HA
    0x0069: 0x0438,    # CYRILLIC SMALL LETTER I
    0x006a: 0x0458,    # CYRILLIC SMALL LETTER JE
    0x006b: 0x043a,    # CYRILLIC SMALL LETTER KA
    0x006c: 0x043b,    # CYRILLIC SMALL LETTER EL
    0x006d: 0x043c,    # CYRILLIC SMALL LETTER EM
    0x006e: 0x043d,    # CYRILLIC SMALL LETTER EN
    0x006f: 0x043e,    # CYRILLIC SMALL LETTER O
    0x0070: 0x043f,    # CYRILLIC SMALL LETTER PE
    0x0071: 0x0459,    # CYRILLIC SMALL LETTER LJE
    0x0072: 0x0440,    # CYRILLIC SMALL LETTER ER
    0x0073: 0x0441,    # CYRILLIC SMALL LETTER ES
    0x0074: 0x0442,    # CYRILLIC SMALL LETTER TE
    0x0075: 0x0443,    # CYRILLIC SMALL LETTER U
    0x0076: 0x0432,    # CYRILLIC SMALL LETTER VE
    0x0077: 0x045a,    # CYRILLIC SMALL LETTER NJE
    0x0078: 0x045f,    # CYRILLIC SMALL LETTER DZHE
    0x0079: 0x0455,    # CYRILLIC SMALL LETTER DZE
    0x007a: 0x0437,    # CYRILLIC SMALL LETTER ZE
    0x007b: 0x0448,    # CYRILLIC SMALL LETTER SHA
    0x007c: 0x0453,    # CYRILLIC SMALL LETTER GJE
    0x007d: 0x045c,    # CYRILLIC SMALL LETTER KJE
    0x007e: 0x0447,    # CYRILLIC SMALL LETTER CHE
}

variant2 = dict(variant1)
variant2.update({
    # MK Sans_K...
    # some of the letters are reverse positioned (vis-a-via capital/small)
    0x005b: 0x0448,    # CYRILLIC SMALL LETTER SHA
    0x005c: 0x0453,    # CYRILLIC SMALL LETTER GJE
    0x005d: 0x045c,    # CYRILLIC SMALL LETTER KJE
    0x007b: 0x0428,    # CYRILLIC CAPITAL LETTER SHA
    0x007c: 0x0403,    # CYRILLIC CAPITAL LETTER GJE
    0x007d: 0x040c,    # CYRILLIC CAPITAL LETTER KJE
})

Replacement = namedtuple('Replacement', 'replacement_font convert_func')

Arial1 = Replacement('Arial', partial(convert_text, variant=variant1))
Times1 = Replacement('Times', partial(convert_text, variant=variant1))
Arial2 = Replacement('Arial', partial(convert_text, variant=variant2))
Times2 = Replacement('Times', partial(convert_text, variant=variant2))


# this list needs to be filled with all other fonts
# font name(lower case) : ( replacement font, convert func )
the_stupid_fonts = CaselessDict({
    'mac c swiss': Arial1,
    'mac c times': Times1,
    'makcirh'    : Arial1,
    'macedonian helv': Arial1,
    'macedonian helvetika': Arial1,
    'makedonska helvetika': Arial1,
    'macedonian ancient': Arial1,
    'macedonian penguin': Arial1,
    'macedonian tms': Times1,
    'makedonski tajms': Times1,
    'mak_hebar': Arial1,
    'mak_puls_helvetika': Arial1,
    'mak_puls_times': Times1,
    'mak_times': Times1,
    'sans_k'     : Arial2,
    'marial';     : Arial1
})
# MAYBE: make it a class ^ .. that parses JSON/YAML
