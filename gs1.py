# -*- coding: utf-8 -*-
"""
This module deals with GS1 barcode.
"""


import sys
import argparse
from re import match, search

__author__ = "Laszlo Tamas"
__copyright__ = "Copyright (c) 2048 Laszlo Tamas"
__licence__ = "MIT"
__version__ = "1.0"


GTIN_ID = "01"
LOT_ID = "10"
EXPIRATION_DATE_ID = "17"
CATALOG_NUMBER_ID = "21"

GS1_CHART_DICT = {
    0: "Â",
    1: "!",
    2: "",
    3: "#",
    4: "$",
    5: "%",
    6: "&",
    7: "'",
    8: "(",
    9: ")",
    10: "*",
    11: "+",
    12: ",",
    13: "-",
    14: ".",
    15: "/",
    16: "0",
    17: "1",
    18: "2",
    19: "3",
    20: "4",
    21: "5",
    22: "6",
    23: "7",
    24: "8",
    25: "9",
    26: ":",
    27: ";",
    28: "<",
    29: "=",
    30: ">",
    31: "?",
    32: "@",
    33: "A",
    34: "B",
    35: "C",
    36: "D",
    37: "E",
    38: "F",
    39: "G",
    40: "H",
    41: "I",
    42: "J",
    43: "K",
    44: "L",
    45: "M",
    46: "N",
    47: "O",
    48: "P",
    49: "Q",
    50: "R",
    51: "S",
    52: "T",
    53: "U",
    54: "V",
    55: "W",
    56: "X",
    57: "Y",
    58: "Z",
    59: "[",
    60: "\\",
    61: "]",
    62: "^",
    63: "_",
    64: "`",
    65: "a",
    66: "b",
    67: "c",
    68: "d",
    69: "e",
    70: "f",
    71: "g",
    72: "h",
    73: "i",
    74: "j",
    75: "k",
    76: "l",
    77: "m",
    78: "n",
    79: "o",
    80: "p",
    81: "q",
    82: "r",
    83: "s",
    84: "t",
    85: "u",
    86: "v",
    87: "w",
    88: "x",
    89: "y",
    90: "z",
    91: "{",
    92: "|",
    93: "}",
    94: "~",
    95: "Ã",
    96: "Ä",
    97: "Å",
    98: "Æ",
    99: "Ç",
    100: "È",
    101: "É",
    102: "Ê",
    103: "Ë",
    104: "Ì",
    105: "Í",
    106: "Î"

}
GS1_CHART_DICT_C = {
    "00": "Â",
    "01": "!",
    "02": "",
    "03": "#",
    "04": "$",
    "05": "%",
    "06": "&",
    "07": "'",
    "08": "(",
    "09": ")",
    "10": "*",
    "11": "+",
    "12": ",",
    "13": "-",
    "14": ".",
    "15": "/",
    "16": "0",
    "17": "1",
    "18": "2",
    "19": "3",
    "20": "4",
    "21": "5",
    "22": "6",
    "23": "7",
    "24": "8",
    "25": "9",
    "26": ":",
    "27": ";",
    "28": "<",
    "29": "=",
    "30": ">",
    "31": "?",
    "32": "@",
    "33": "A",
    "34": "B",
    "35": "C",
    "36": "D",
    "37": "E",
    "38": "F",
    "39": "G",
    "40": "H",
    "41": "I",
    "42": "J",
    "43": "K",
    "44": "L",
    "45": "M",
    "46": "N",
    "47": "O",
    "48": "P",
    "49": "Q",
    "50": "R",
    "51": "S",
    "52": "T",
    "53": "U",
    "54": "V",
    "55": "W",
    "56": "X",
    "57": "Y",
    "58": "Z",
    "59": "[",
    "60": "\\",
    "61": "]",
    "62": "^",
    "63": "_",
    "64": "`",
    "65": "a",
    "66": "b",
    "67": "c",
    "68": "d",
    "69": "e",
    "70": "f",
    "71": "g",
    "72": "h",
    "73": "i",
    "74": "j",
    "75": "k",
    "76": "l",
    "77": "m",
    "78": "n",
    "79": "o",
    "80": "p",
    "81": "q",
    "82": "r",
    "83": "s",
    "84": "t",
    "85": "u",
    "86": "v",
    "87": "w",
    "88": "x",
    "89": "y",
    "90": "z",
    "91": "{",
    "92": "|",
    "93": "}",
    "94": "~",
    "95": "Ã",
    "96": "Ä",
    "97": "Å",
    "98": "Æ",
    "99": "Ç"

}
GS1_CHART_DIC_REV = {
    "Â": 0,
    "!": 1,
    '"': 2,
    "#": 3,
    "$": 4,
    "%": 5,
    "&": 6,
    "'": 7,
    "(": 8,
    ")": 9,
    "*": 10,
    "+": 11,
    ",": 12,
    "-": 13,
    ".": 14,
    "/": 15,
    "0": 16,
    "1": 17,
    "2": 18,
    "3": 19,
    "4": 20,
    "5": 21,
    "6": 22,
    "7": 23,
    "8": 24,
    "9": 25,
    ":": 26,
    ";": 27,
    "<": 28,
    "=": 29,
    ">": 30,
    "?": 31,
    "@": 32,
    "A": 33,
    "B": 34,
    "C": 35,
    "D": 36,
    "E": 37,
    "F": 38,
    "G": 39,
    "H": 40,
    "I": 41,
    "J": 42,
    "K": 43,
    "L": 44,
    "M": 45,
    "N": 46,
    "O": 47,
    "P": 48,
    "Q": 49,
    "R": 50,
    "S": 51,
    "T": 52,
    "U": 53,
    "V": 54,
    "W": 55,
    "X": 56,
    "Y": 57,
    "Z": 58,
    "[": 59,
    "\\": 60,
    "]": 61,
    "^": 62,
    "_": 63,
    "`": 64,
    "a": 65,
    "b": 66,
    "c": 67,
    "d": 68,
    "e": 69,
    "f": 70,
    "g": 71,
    "h": 72,
    "i": 73,
    "j": 74,
    "k": 75,
    "l": 76,
    "m": 77,
    "n": 78,
    "o": 79,
    "p": 80,
    "q": 81,
    "r": 82,
    "s": 83,
    "t": 84,
    "u": 85,
    "v": 86,
    "w": 87,
    "x": 88,
    "y": 89,
    "z": 90,
    "{": 91,
    "|": 92,
    "}": 93,
    "~": 94,
    "Ã": 95,
    "Ä": 96,
    "Å": 97,
    "Æ": 98,
    "Ç": 99,
    "È": 100,
    "É": 101,
    "Ê": 102,
    "Ë": 103,
    "Ì": 104,
    "Í": 105,
    "Î": 106,

}


class GS1Check(object):
    """Class to deal with GS1 code
    """

    def __init__(self):
        self.barcode = ""

    def set_barcode(self, barcode):
        """Set and preformat barcode.

        Arguments:
            barcode {str} -- barcode
        """

        self.barcode = barcode
        self.format_barcode()

    def check_gtin_id(self):
        """Check GTIN ID.

        Arguments:
            code {str} -- barcode

        Returns:
            bool -- Wether the GTIN ID is (01)
        """

        ret = False
        if self.barcode[:2] == GTIN_ID:
            ret = True
        return ret

    def verify(self):
        """Verify barcode.

        Arguments:
            code {str} -- barcode

        Returns:
            bool -- barcode is verified
        """

        ret = False
        if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', self.barcode):
            ret = True
        return ret

    def format_barcode(self):
        """Format barcode.
        """

        self.barcode = self.barcode.replace("(", "")
        self.barcode = self.barcode.replace(")", "")


class GS1GetElement(object):
    """Class to deal with GS1 code
    """

    def __init__(self):
        self.barcode = ""
        self.ean_number = ""
        self.lot_number = ""
        self.expiration_date = ""
        self.catalog_number = ""

    def set_barcode(self, barcode):
        """Set and preformat barcode.

        Arguments:
            barcode {str} -- barcode
        """

        self.barcode = barcode
        self.format_barcode()

    def format_barcode(self):
        """Format barcode.
        """

        self.barcode = self.barcode.replace("(", "")
        self.barcode = self.barcode.replace(")", "")

    def get_ean_number(self):
        """Get EAN number.

        Returns:
            {str} -- EAN number (01)
        """

        ret = None
        if match(r'^01(\d{14})10(\d*)17(\d{6})21(\d{9})$', self.barcode):
            ret = search(r'^01(\d{14})', self.barcode).group(1)
        self.ean_number = ret
        return ret

    def get_lot_number(self):
        """Get LOT number.

        Returns:
            str -- LOT number (10)
        """

        ret = ""
        if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', self.barcode):
            ret = search(r'^01(\d{14})10(\d*)17', self.barcode).group(2)
        self.lot_number = ret
        return ret

    def get_expiration_date(self):
        """Get expiration date.

        Returns:
            str -- expiration date YYDDMM (17)
        """

        ret = ""
        if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', self.barcode):
            ret = search(r'^01(\d{14})10(\d*)17(\d{6})21',
                         self.barcode).group(3)
        self.expiration_date = ret
        return ret

    def get_catalog_number(self):
        """Get catalog number

        Returns:
            str -- catalog number (21)
        """

        ret = ""
        if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', self.barcode):
            ret = search(
                r'^01(\d{14})10(\d*)17(\d{6})21(\d{9})$',
                self.barcode).group(4)
        self.catalog_number = ret
        return ret

    def parse_gs1(self):
        """Parse GS1 code.

        Returns:
            str[] -- barcode elements, (01) EAN, (10) LOT,
            (17) expiration date, (21) catalog number
        """

        if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', self.barcode):
            m_ean = search(r'^01(\d{14})', self.barcode).group(1)
            m_lot = search(r'^01(\d{14})10(\d*)17', self.barcode).group(2)
            m_expiration = search(
                r'^01(\d{14})10(\d*)17(\d{6})21', self.barcode).group(3)
            m_catalog = search(
                r'^01(\d{14})10(\d*)17(\d{6})21(\d{9})$',
                self.barcode).group(4)
            return m_ean, m_lot, m_expiration, m_catalog
        self.ean_number = m_ean
        self.lot_number = m_lot
        self.expiration_date = m_expiration
        self.catalog_number = m_catalog
        return None


class GS1Create(object):
    """Class to deal with GS1 code
    """

    def __init__(self):
        self.barcode = ""
        self.ean_number = ""
        self.lot_number = ""
        self.expiration_date = ""
        self.catalog_number = ""
        self.output_style = "Normal"
        self.code_without_end = ""

    def set_barcode(self, barcode):
        """Set and preformat barcode.

        Arguments:
            barcode {str} -- barcode
        """

        self.barcode = barcode
        self.format_barcode()

    def format_barcode(self):
        """Format barcode.
        """

        self.barcode = self.barcode.replace("(", "")
        self.barcode = self.barcode.replace(")", "")

    def create_gs1(self):
        """Create GS1 code.

        Returns:
            str -- GS1 barcode
        """

        ret = ""
        bracket_before = ""
        bracket_after = ""
        if self.output_style == "Normal" or self.output_style == "Brackets":
            if self.output_style == "Brackets":
                bracket_before = "("
                bracket_after = ")"
            ret = bracket_before + GTIN_ID+bracket_after + self.ean_number + \
                bracket_before + LOT_ID + bracket_after + self.lot_number + \
                bracket_before + EXPIRATION_DATE_ID + bracket_after + \
                self.expiration_date + \
                bracket_before + CATALOG_NUMBER_ID + bracket_after + \
                self.catalog_number
        if self.output_style == "ZPL":
            # >;>80105996527176340102014>6AA>5>8171907312128012280>64
            ret = "^BCN,,N,N^FD>;>8" + GTIN_ID + self.ean_number + LOT_ID
            if len(self.lot_number) > 4:
                ret = ret + self.lot_number[:4] + \
                    ">6" + self.lot_number[4:] + ">5"
            else:
                ret = ret + self.lot_number
            ret = ret+">8"+EXPIRATION_DATE_ID + self.expiration_date
            ret = ret+CATALOG_NUMBER_ID + \
                self.catalog_number[:8]+">6" + self.catalog_number[8:] + "^FS"
        if self.output_style == "Character":
            # ÍÊ!%Ça;1_H*4.Ê13'?5<!6pÈ4pÎ
            ret = "ÍÊ!" + GS1_CHART_DICT_C[self.ean_number[0:2]] + \
                GS1_CHART_DICT_C[self.ean_number[2:4]] + \
                GS1_CHART_DICT_C[self.ean_number[4:6]] + \
                GS1_CHART_DICT_C[self.ean_number[6:8]] + \
                GS1_CHART_DICT_C[self.ean_number[8:10]] + \
                GS1_CHART_DICT_C[self.ean_number[10:12]] + \
                GS1_CHART_DICT_C[self.ean_number[12:]]
            ret = ret + "*" + GS1_CHART_DICT_C[self.lot_number[0:2]] + \
                GS1_CHART_DICT_C[self.lot_number[2:4]]
            if len(self.lot_number) > 4:
                ret = ret + "È" + self.lot_number[4:] + "Ç"
            ret = ret + "Ê1" + GS1_CHART_DICT_C[self.expiration_date[0:2]] + \
                GS1_CHART_DICT_C[self.expiration_date[2:4]] + \
                GS1_CHART_DICT_C[self.expiration_date[4:6]]
            ret = ret + "5" + GS1_CHART_DICT_C[self.catalog_number[0:2]] + \
                GS1_CHART_DICT_C[self.catalog_number[2:4]] + \
                GS1_CHART_DICT_C[self.catalog_number[4:6]] + \
                GS1_CHART_DICT_C[self.catalog_number[6:8]]
            ret = ret + "È" + self.catalog_number[8:]
            self.code_without_end = ret
            ret = ret + self.get_check_digit() + "Î"
        return ret

    def get_check_digit(self):
        """Generate CheckDigit.

        Returns:
            str -- CheckDigit
        """

        ret = ""
        ret_val = GS1_CHART_DIC_REV[self.code_without_end[0]]
        for i in range(2, len(self.code_without_end)+1):
            ret_val = ret_val + \
                (i-1) * GS1_CHART_DIC_REV[self.code_without_end[i-1:i]]
        ret = GS1_CHART_DICT[ret_val % 103]
        return ret


def parse_arguments():
    """
    Parse program arguments.

    @return arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--barcode', help='full barcode')
    parser.add_argument('-cn', '--catalognumber', help='catalog number')
    parser.add_argument('-ea', '--eannumber', help='EAN number')
    parser.add_argument('-ln', '--lotnumber', help='LOT number')
    parser.add_argument('-li', '--lic', help='LIC identifier')
    parser.add_argument('-ex', '--expiration', help='expiration date YYMMDD')
    parser.add_argument('-f', '--function', help='function to execute',
                        type=str, choices=['check_gtin_id',
                                           'format_barcode',
                                           'verify',
                                           'get_ean_number',
                                           'get_lot_number',
                                           'get_expiration_date',
                                           'get_catalog_number',
                                           'parse_gs1',
                                           'create_gs1',
                                           'create_gs1_with_brackets',
                                           'create_gs1_zpl',
                                           'create_gs1_character'])
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    return parser.parse_args()


def execute_program():
    """Execute the program by arguments.
    """

    args = parse_arguments()
    if args.function == 'check_gtin_id' or args.function == 'verify':
        execute_check()
    else:
        if args.function[0:4] == "get_":
            execute_get_element()
        else:
            if args.function[0:7] == "create_":
                execute_creation()

    if args.function == 'parse_gs1':
        GS1_ELEMENT.barcode = args.barcode
        res = GS1_ELEMENT.parse_gs1()
        if args.verbose:
            print("EAN number: " + res[0])
            print("LOT number: " + res[1])
            print("Expiration date: " + res[2])
            print("Catalog number: " + res[3])
        else:
            print(res)

    if args.function == 'format_barcode':
        GS1_ELEMENT.barcode = args.barcode
        GS1_ELEMENT.format_barcode()
        res = str(GS1_ELEMENT.barcode)
        if args.verbose:
            print("GS1 formatted barcode: " + res)
        else:
            print(res)


def execute_check():
    """Check functions.
    """

    args = parse_arguments()
    GS1_CHECK.set_barcode(args.barcode)
    if args.function == 'check_gtin_id':
        res = str(GS1_CHECK.check_gtin_id())
        if args.verbose:
            print("GTIN ID: " + res)
        else:
            print(res)
    if args.function == 'verify':
        res = str(GS1_CHECK.verify())
        if args.verbose:
            print("GS1 verification: " + res)
        else:
            print(res)


def execute_get_element():
    """Get elements functions.
    """

    args = parse_arguments()
    GS1_ELEMENT.barcode = args.barcode
    if args.function == 'get_ean_number':
        res = str(GS1_ELEMENT.get_ean_number())
        if args.verbose:
            print("EAN number: " + res)
        else:
            print(res)
    if args.function == 'get_lot_number':
        res = str(GS1_ELEMENT.get_lot_number())
        if args.verbose:
            print("LOT number: " + res)
        else:
            print(res)
    if args.function == 'get_expiration_date':
        res = str(GS1_ELEMENT.get_expiration_date())
        if args.verbose:
            print("Expiration date: " + res)
        else:
            print(res)
    if args.function == 'get_catalog_number':
        res = str(GS1_ELEMENT.get_catalog_number())
        if args.verbose:
            print("Catalog number: " + res)
        else:
            print(res)


def execute_creation():
    """Barcode craetion functions.
    """

    args = parse_arguments()
    GS1_CREATE.ean_number = args.eannumber
    GS1_CREATE.lot_number = args.lotnumber
    GS1_CREATE.expiration_date = args.expiration
    GS1_CREATE.catalog_number = args.catalognumber
    if args.function == 'create_gs1':
        GS1_CREATE.output_style = "Normal"
        res = str(GS1_CREATE.create_gs1())
        if args.verbose:
            print("GS1 barcode: " + res)
        else:
            print(res)
    if args.function == 'create_gs1_with_brackets':
        GS1_CREATE.output_style = "Brackets"
        res = str(GS1_CREATE.create_gs1())
        if args.verbose:
            print("GS1 barcode: " + res)
        else:
            print(res)
    if args.function == 'create_gs1_zpl':
        GS1_CREATE.output_style = "ZPL"
        res = str(GS1_CREATE.create_gs1())
        if args.verbose:
            print("GS1 barcode: " + res)
        else:
            print(res)

    if args.function == 'create_gs1_character':
        GS1_CREATE.output_style = "Character"
        res = str(GS1_CREATE.create_gs1())
        if args.verbose:
            print("GS1 barcode: " + res)
        else:
            print(res)


if __name__ == '__main__':
    GS1_ELEMENT = GS1GetElement()
    GS1_CHECK = GS1Check()
    GS1_CREATE = GS1Create()
    execute_program()
    sys.exit()
