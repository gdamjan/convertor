from functools import partial
from collections import namedtuple

from .caselessdict import CaselessDict

# Python2/3 compatibility
try: str = unicode
except: pass

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
    return str(text).translate(variant)

variant1 = {
    # MAC C Swiss, Macedonian Times...
    ord('@') :  0x0416,    # CYRILLIC CAPITAL LETTER ZHE
    ord('A') :  0x0410,    # CYRILLIC CAPITAL LETTER A
    ord('B') :  0x0411,    # CYRILLIC CAPITAL LETTER BE
    ord('C') :  0x0426,    # CYRILLIC CAPITAL LETTER TSE
    ord('D') :  0x0414,    # CYRILLIC CAPITAL LETTER DE
    ord('E') :  0x0415,    # CYRILLIC CAPITAL LETTER IE
    ord('F') :  0x0424,    # CYRILLIC CAPITAL LETTER EF
    ord('G') :  0x0413,    # CYRILLIC CAPITAL LETTER GHE
    ord('H') :  0x0425,    # CYRILLIC CAPITAL LETTER HA
    ord('I') :  0x0418,    # CYRILLIC CAPITAL LETTER I
    ord('J') :  0x0408,    # CYRILLIC CAPITAL LETTER JE
    ord('K') :  0x041a,    # CYRILLIC CAPITAL LETTER KA
    ord('L') :  0x041b,    # CYRILLIC CAPITAL LETTER EL
    ord('M') :  0x041c,    # CYRILLIC CAPITAL LETTER EM
    ord('N') :  0x041d,    # CYRILLIC CAPITAL LETTER EN
    ord('O') :  0x041e,    # CYRILLIC CAPITAL LETTER O
    ord('P') :  0x041f,    # CYRILLIC CAPITAL LETTER PE
    ord('Q') :  0x0409,    # CYRILLIC CAPITAL LETTER LJE
    ord('R') :  0x0420,    # CYRILLIC CAPITAL LETTER ER
    ord('S') :  0x0421,    # CYRILLIC CAPITAL LETTER ES
    ord('T') :  0x0422,    # CYRILLIC CAPITAL LETTER TE
    ord('U') :  0x0423,    # CYRILLIC CAPITAL LETTER U
    ord('V') :  0x0412,    # CYRILLIC CAPITAL LETTER VE
    ord('W') :  0x040a,    # CYRILLIC CAPITAL LETTER NJE
    ord('X') :  0x040f,    # CYRILLIC CAPITAL LETTER DZHE
    ord('Y') :  0x0405,    # CYRILLIC CAPITAL LETTER DZE
    ord('Z') :  0x0417,    # CYRILLIC CAPITAL LETTER ZE
    ord('[') :  0x0428,    # CYRILLIC CAPITAL LETTER SHA
    ord('\\') : 0x0403,    # CYRILLIC CAPITAL LETTER GJE
    ord(']') :  0x040c,    # CYRILLIC CAPITAL LETTER KJE
    ord('^') :  0x0427,    # CYRILLIC CAPITAL LETTER CHE
    ord('`') :  0x0436,    # CYRILLIC SMALL LETTER ZHE
    ord('a') :  0x0430,    # CYRILLIC SMALL LETTER A
    ord('b') :  0x0431,    # CYRILLIC SMALL LETTER BE
    ord('c') :  0x0446,    # CYRILLIC SMALL LETTER TSE
    ord('d') :  0x0434,    # CYRILLIC SMALL LETTER DE
    ord('e') :  0x0435,    # CYRILLIC SMALL LETTER IE
    ord('f') :  0x0444,    # CYRILLIC SMALL LETTER EF
    ord('g') :  0x0433,    # CYRILLIC SMALL LETTER GHE
    ord('h') :  0x0445,    # CYRILLIC SMALL LETTER HA
    ord('i') :  0x0438,    # CYRILLIC SMALL LETTER I
    ord('j') :  0x0458,    # CYRILLIC SMALL LETTER JE
    ord('k') :  0x043a,    # CYRILLIC SMALL LETTER KA
    ord('l') :  0x043b,    # CYRILLIC SMALL LETTER EL
    ord('m') :  0x043c,    # CYRILLIC SMALL LETTER EM
    ord('n') :  0x043d,    # CYRILLIC SMALL LETTER EN
    ord('o') :  0x043e,    # CYRILLIC SMALL LETTER O
    ord('p') :  0x043f,    # CYRILLIC SMALL LETTER PE
    ord('q') :  0x0459,    # CYRILLIC SMALL LETTER LJE
    ord('r') :  0x0440,    # CYRILLIC SMALL LETTER ER
    ord('s') :  0x0441,    # CYRILLIC SMALL LETTER ES
    ord('t') :  0x0442,    # CYRILLIC SMALL LETTER TE
    ord('u') :  0x0443,    # CYRILLIC SMALL LETTER U
    ord('v') :  0x0432,    # CYRILLIC SMALL LETTER VE
    ord('w') :  0x045a,    # CYRILLIC SMALL LETTER NJE
    ord('x') :  0x045f,    # CYRILLIC SMALL LETTER DZHE
    ord('y') :  0x0455,    # CYRILLIC SMALL LETTER DZE
    ord('z') :  0x0437,    # CYRILLIC SMALL LETTER ZE
    ord('{') :  0x0448,    # CYRILLIC SMALL LETTER SHA
    ord('|') :  0x0453,    # CYRILLIC SMALL LETTER GJE
    ord('}') :  0x045c,    # CYRILLIC SMALL LETTER KJE
    ord('~') :  0x0447,    # CYRILLIC SMALL LETTER CHE
}

variant2 = dict(variant1)
variant2.update({
    # MK Sans_K...
    # some of the letters are reverse positioned (vis-a-via capital/small)
    ord('[') :  0x0448,    # CYRILLIC SMALL LETTER SHA
    ord('\\') : 0x0453,    # CYRILLIC SMALL LETTER GJE
    ord(']') :  0x045c,    # CYRILLIC SMALL LETTER KJE
    ord('{') :  0x0428,    # CYRILLIC CAPITAL LETTER SHA
    ord('|') :  0x0403,    # CYRILLIC CAPITAL LETTER GJE
    ord('}') :  0x040c,    # CYRILLIC CAPITAL LETTER KJE
})
variant3 = dict(variant2)
# REMOVE SMALL/CAPITAL CHE
variant3.pop(ord('~'))
variant3.pop(ord('^'))
# CHE (ч) е на ; и :
variant2.update({
    ord(';') :  0x0447,    # CYRILLIC SMALL LETTER CHE
    ord(':') :  0x0427,    # CYRILLIC CAPITAL LETTER CHE
})

Replacement = namedtuple('Replacement', 'replacement_font convert_func')

Arial1 = Replacement('Arial', partial(convert_text, variant=variant1))
Times1 = Replacement('Times', partial(convert_text, variant=variant1))
Arial2 = Replacement('Arial', partial(convert_text, variant=variant2))
Times2 = Replacement('Times', partial(convert_text, variant=variant2))
Arial3 = Replacement('Arial', partial(convert_text, variant=variant3))


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
    'marial'     : Arial1,
    'makarial_beta' : Arial3
})
# MAYBE: make it a class ^ .. that parses JSON/YAML
