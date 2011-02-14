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
    '@' :  0x0416,    # CYRILLIC CAPITAL LETTER ZHE
    'A' :  0x0410,    # CYRILLIC CAPITAL LETTER A
    'B' :  0x0411,    # CYRILLIC CAPITAL LETTER BE
    'C' :  0x0426,    # CYRILLIC CAPITAL LETTER TSE
    'D' :  0x0414,    # CYRILLIC CAPITAL LETTER DE
    'E' :  0x0415,    # CYRILLIC CAPITAL LETTER IE
    'F' :  0x0424,    # CYRILLIC CAPITAL LETTER EF
    'G' :  0x0413,    # CYRILLIC CAPITAL LETTER GHE
    'H' :  0x0425,    # CYRILLIC CAPITAL LETTER HA
    'I' :  0x0418,    # CYRILLIC CAPITAL LETTER I
    'J' :  0x0408,    # CYRILLIC CAPITAL LETTER JE
    'K' :  0x041a,    # CYRILLIC CAPITAL LETTER KA
    'L' :  0x041b,    # CYRILLIC CAPITAL LETTER EL
    'M' :  0x041c,    # CYRILLIC CAPITAL LETTER EM
    'N' :  0x041d,    # CYRILLIC CAPITAL LETTER EN
    'O' :  0x041e,    # CYRILLIC CAPITAL LETTER O
    'P' :  0x041f,    # CYRILLIC CAPITAL LETTER PE
    'Q' :  0x0409,    # CYRILLIC CAPITAL LETTER LJE
    'R' :  0x0420,    # CYRILLIC CAPITAL LETTER ER
    'S' :  0x0421,    # CYRILLIC CAPITAL LETTER ES
    'T' :  0x0422,    # CYRILLIC CAPITAL LETTER TE
    'U' :  0x0423,    # CYRILLIC CAPITAL LETTER U
    'V' :  0x0412,    # CYRILLIC CAPITAL LETTER VE
    'W' :  0x040a,    # CYRILLIC CAPITAL LETTER NJE
    'X' :  0x040f,    # CYRILLIC CAPITAL LETTER DZHE
    'Y' :  0x0405,    # CYRILLIC CAPITAL LETTER DZE
    'Z' :  0x0417,    # CYRILLIC CAPITAL LETTER ZE
    '[' :  0x0428,    # CYRILLIC CAPITAL LETTER SHA
    '\\' : 0x0403,    # CYRILLIC CAPITAL LETTER GJE
    ']' :  0x040c,    # CYRILLIC CAPITAL LETTER KJE
    '^' :  0x0427,    # CYRILLIC CAPITAL LETTER CHE
    '`' :  0x0436,    # CYRILLIC SMALL LETTER ZHE
    'a' :  0x0430,    # CYRILLIC SMALL LETTER A
    'b' :  0x0431,    # CYRILLIC SMALL LETTER BE
    'c' :  0x0446,    # CYRILLIC SMALL LETTER TSE
    'd' :  0x0434,    # CYRILLIC SMALL LETTER DE
    'e' :  0x0435,    # CYRILLIC SMALL LETTER IE
    'f' :  0x0444,    # CYRILLIC SMALL LETTER EF
    'g' :  0x0433,    # CYRILLIC SMALL LETTER GHE
    'h' :  0x0445,    # CYRILLIC SMALL LETTER HA
    'i' :  0x0438,    # CYRILLIC SMALL LETTER I
    'j' :  0x0458,    # CYRILLIC SMALL LETTER JE
    'k' :  0x043a,    # CYRILLIC SMALL LETTER KA
    'l' :  0x043b,    # CYRILLIC SMALL LETTER EL
    'm' :  0x043c,    # CYRILLIC SMALL LETTER EM
    'n' :  0x043d,    # CYRILLIC SMALL LETTER EN
    'o' :  0x043e,    # CYRILLIC SMALL LETTER O
    'p' :  0x043f,    # CYRILLIC SMALL LETTER PE
    'q' :  0x0459,    # CYRILLIC SMALL LETTER LJE
    'r' :  0x0440,    # CYRILLIC SMALL LETTER ER
    's' :  0x0441,    # CYRILLIC SMALL LETTER ES
    't' :  0x0442,    # CYRILLIC SMALL LETTER TE
    'u' :  0x0443,    # CYRILLIC SMALL LETTER U
    'v' :  0x0432,    # CYRILLIC SMALL LETTER VE
    'w' :  0x045a,    # CYRILLIC SMALL LETTER NJE
    'x' :  0x045f,    # CYRILLIC SMALL LETTER DZHE
    'y' :  0x0455,    # CYRILLIC SMALL LETTER DZE
    'z' :  0x0437,    # CYRILLIC SMALL LETTER ZE
    '{' :  0x0448,    # CYRILLIC SMALL LETTER SHA
    '|' :  0x0453,    # CYRILLIC SMALL LETTER GJE
    '}' :  0x045c,    # CYRILLIC SMALL LETTER KJE
    '~' :  0x0447,    # CYRILLIC SMALL LETTER CHE
}

variant2 = dict(variant1)
variant2.update({
    # MK Sans_K...
    # some of the letters are reverse positioned (vis-a-via capital/small)
    '[' :  0x0448,    # CYRILLIC SMALL LETTER SHA
    '\\' : 0x0453,    # CYRILLIC SMALL LETTER GJE
    ']' :  0x045c,    # CYRILLIC SMALL LETTER KJE
    '{' :  0x0428,    # CYRILLIC CAPITAL LETTER SHA
    '|' :  0x0403,    # CYRILLIC CAPITAL LETTER GJE
    '}' :  0x040c,    # CYRILLIC CAPITAL LETTER KJE
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
    'm_garamond' : Arial2,
    'marial'     : Arial1
})
# MAYBE: make it a class ^ .. that parses JSON/YAML
