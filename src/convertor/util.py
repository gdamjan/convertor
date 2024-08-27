from types import MappingProxyType
from dataclasses import dataclass

# MAC C Swiss, Macedonian Times...
variant1 = MappingProxyType(
    {
        ord("@"): 0x0416,  # CYRILLIC CAPITAL LETTER ZHE
        ord("A"): 0x0410,  # CYRILLIC CAPITAL LETTER A
        ord("B"): 0x0411,  # CYRILLIC CAPITAL LETTER BE
        ord("C"): 0x0426,  # CYRILLIC CAPITAL LETTER TSE
        ord("D"): 0x0414,  # CYRILLIC CAPITAL LETTER DE
        ord("E"): 0x0415,  # CYRILLIC CAPITAL LETTER IE
        ord("F"): 0x0424,  # CYRILLIC CAPITAL LETTER EF
        ord("G"): 0x0413,  # CYRILLIC CAPITAL LETTER GHE
        ord("H"): 0x0425,  # CYRILLIC CAPITAL LETTER HA
        ord("I"): 0x0418,  # CYRILLIC CAPITAL LETTER I
        ord("J"): 0x0408,  # CYRILLIC CAPITAL LETTER JE
        ord("K"): 0x041A,  # CYRILLIC CAPITAL LETTER KA
        ord("L"): 0x041B,  # CYRILLIC CAPITAL LETTER EL
        ord("M"): 0x041C,  # CYRILLIC CAPITAL LETTER EM
        ord("N"): 0x041D,  # CYRILLIC CAPITAL LETTER EN
        ord("O"): 0x041E,  # CYRILLIC CAPITAL LETTER O
        ord("P"): 0x041F,  # CYRILLIC CAPITAL LETTER PE
        ord("Q"): 0x0409,  # CYRILLIC CAPITAL LETTER LJE
        ord("R"): 0x0420,  # CYRILLIC CAPITAL LETTER ER
        ord("S"): 0x0421,  # CYRILLIC CAPITAL LETTER ES
        ord("T"): 0x0422,  # CYRILLIC CAPITAL LETTER TE
        ord("U"): 0x0423,  # CYRILLIC CAPITAL LETTER U
        ord("V"): 0x0412,  # CYRILLIC CAPITAL LETTER VE
        ord("W"): 0x040A,  # CYRILLIC CAPITAL LETTER NJE
        ord("X"): 0x040F,  # CYRILLIC CAPITAL LETTER DZHE
        ord("Y"): 0x0405,  # CYRILLIC CAPITAL LETTER DZE
        ord("Z"): 0x0417,  # CYRILLIC CAPITAL LETTER ZE
        ord("["): 0x0428,  # CYRILLIC CAPITAL LETTER SHA
        ord("\\"): 0x0403,  # CYRILLIC CAPITAL LETTER GJE
        ord("]"): 0x040C,  # CYRILLIC CAPITAL LETTER KJE
        ord("^"): 0x0427,  # CYRILLIC CAPITAL LETTER CHE
        ord("`"): 0x0436,  # CYRILLIC SMALL LETTER ZHE
        ord("a"): 0x0430,  # CYRILLIC SMALL LETTER A
        ord("b"): 0x0431,  # CYRILLIC SMALL LETTER BE
        ord("c"): 0x0446,  # CYRILLIC SMALL LETTER TSE
        ord("d"): 0x0434,  # CYRILLIC SMALL LETTER DE
        ord("e"): 0x0435,  # CYRILLIC SMALL LETTER IE
        ord("f"): 0x0444,  # CYRILLIC SMALL LETTER EF
        ord("g"): 0x0433,  # CYRILLIC SMALL LETTER GHE
        ord("h"): 0x0445,  # CYRILLIC SMALL LETTER HA
        ord("i"): 0x0438,  # CYRILLIC SMALL LETTER I
        ord("j"): 0x0458,  # CYRILLIC SMALL LETTER JE
        ord("k"): 0x043A,  # CYRILLIC SMALL LETTER KA
        ord("l"): 0x043B,  # CYRILLIC SMALL LETTER EL
        ord("m"): 0x043C,  # CYRILLIC SMALL LETTER EM
        ord("n"): 0x043D,  # CYRILLIC SMALL LETTER EN
        ord("o"): 0x043E,  # CYRILLIC SMALL LETTER O
        ord("p"): 0x043F,  # CYRILLIC SMALL LETTER PE
        ord("q"): 0x0459,  # CYRILLIC SMALL LETTER LJE
        ord("r"): 0x0440,  # CYRILLIC SMALL LETTER ER
        ord("s"): 0x0441,  # CYRILLIC SMALL LETTER ES
        ord("t"): 0x0442,  # CYRILLIC SMALL LETTER TE
        ord("u"): 0x0443,  # CYRILLIC SMALL LETTER U
        ord("v"): 0x0432,  # CYRILLIC SMALL LETTER VE
        ord("w"): 0x045A,  # CYRILLIC SMALL LETTER NJE
        ord("x"): 0x045F,  # CYRILLIC SMALL LETTER DZHE
        ord("y"): 0x0455,  # CYRILLIC SMALL LETTER DZE
        ord("z"): 0x0437,  # CYRILLIC SMALL LETTER ZE
        ord("{"): 0x0448,  # CYRILLIC SMALL LETTER SHA
        ord("|"): 0x0453,  # CYRILLIC SMALL LETTER GJE
        ord("}"): 0x045C,  # CYRILLIC SMALL LETTER KJE
        ord("~"): 0x0447,  # CYRILLIC SMALL LETTER CHE
    }
)

# MK Sans_K, M Garamond...
# се разликува од variant1 дека големи/мали букви за ш, ѓ, ќ се обратно
variant2 = MappingProxyType(
    {
        **variant1,
        ord("{"): 0x0428,  # CYRILLIC CAPITAL LETTER SHA
        ord("["): 0x0448,  # CYRILLIC SMALL LETTER SHA
        ord("|"): 0x0403,  # CYRILLIC CAPITAL LETTER GJE
        ord("\\"): 0x0453,  # CYRILLIC SMALL LETTER GJE
        ord("}"): 0x040C,  # CYRILLIC CAPITAL LETTER KJE
        ord("]"): 0x045C,  # CYRILLIC SMALL LETTER KJE
    }
)

# makarial
# Исто како variant2 но CHE (ч) е на `;` и `:`, а не на `~` и `^`
variant3 = MappingProxyType(
    {k: v for k, v in variant2.items() if k not in (ord("~"), ord("^"))}
    | {
        ord(";"): 0x0447,  # CYRILLIC SMALL LETTER CHE
        ord(":"): 0x0427,  # CYRILLIC CAPITAL LETTER CHE
    }
)


@dataclass(frozen=True)
class Conversion:
    target_font: str
    variant: MappingProxyType

    def convert(self, text):
        return text.translate(self.variant)


Sans_1 = Conversion("Arial", variant1)
Serif_1 = Conversion("Times", variant1)
Sans_2 = Conversion("Arial", variant2)
Serif_2 = Conversion("Times", variant2)
Sans_3 = Conversion("Arial", variant3)
Serif_3 = Conversion("Times", variant3)


# this list/mapping needs to be filled with all other fonts
# font name(lower case) : ( replacement font, convert func )
the_stupid_fonts = MappingProxyType(
    {
        "mac c swiss": Sans_1,
        "mac c times": Serif_1,
        "makcirh": Sans_1,
        "macedonian helv": Sans_1,
        "macedonian helvetika": Sans_1,
        "makedonska helvetika": Sans_1,
        "macedonian ancient": Sans_1,
        "macedonian penguin": Sans_1,
        "macedonian tms": Serif_1,
        "makedonski tajms": Serif_1,
        "mak_hebar": Sans_1,
        "mak_puls_helvetika": Sans_1,
        "mak_puls_times": Serif_1,
        "mak_times": Serif_1,
        "sans_k": Sans_2,
        "m_garamond": Sans_2,
        "marial": Sans_1,
        "makarial_beta": Sans_3,
    }
)
# MAYBE: make it a class ^ .. that parses JSON/YAML
