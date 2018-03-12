# -*- coding: utf-8 -*-
"""
This module deals with GS1 barcode.
"""
# TODO Copyright info, functions, substring, length, unittest

import logging
import sys
import argparse
from re import match, search, sub

logger = logging.getLogger('program')
# set level for file handling (NOTSET>DEBUG>INFO>WARNING>ERROR>CRITICAL)
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
logger_fh = logging.FileHandler('gs1.log')

# create console handler with a higher log level
logger_ch = logging.StreamHandler()
logger_ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = \
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                      )
logger_fh.setFormatter(formatter)
logger_ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(logger_fh)
logger.addHandler(logger_ch)


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
                                           'format_barcode'
                                           'verify',
                                           'get_ean_number',
                                           'get_lot_number',
                                           'get_expiration_date',
                                           'get_catalog_number',
                                           'parse_gs1',
                                           'create_gs1',
                                           'create_gs1_with_brackets',
                                           'create_gs1_zpl',
                                           'create_gs1_character',
                                           ])
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    return parser.parse_args()


gtin_id = "01"
lot_id = "10"
expiration_date_id = "17"
catalog_number_id = "21"

gs1_chart_dict = {
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
gs1_chart_dict_c = {
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
gs1_chart_dict_rev = {
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


def execute_program():
    """Execute the program by arguments.
    """

    args = parse_arguments()
    if args.function == 'check_gtin_id':
        res = str(check_gtin_id(args.barcode))
        if args.verbose:
            print("GTIN ID: " + res)
        else:
            print(res)
    if args.function == 'verify':
        res = str(verify(args.barcode))
        if args.verbose:
            print("GS1 verification: " + res)
        else:
            print(res)
    if args.function == 'get_ean_number':
        res = str(get_ean_number(args.barcode))
        if args.verbose:
            print("EAN number: " + res)
        else:
            print(res)
    if args.function == 'get_lot_number':
        res = str(get_lot_number(args.barcode))
        if args.verbose:
            print("LOT number: " + res)
        else:
            print(res)
    if args.function == 'get_expiration_date':
        res = str(get_expiration_date(args.barcode))
        if args.verbose:
            print("Expiration date: " + res)
        else:
            print(res)
    if args.function == 'get_catalog_number':
        res = str(get_catalog_number(args.barcode))
        if args.verbose:
            print("Catalog number: " + res)
        else:
            print(res)
    if args.function == 'parse_gs1':
        res = parse_gs1(args.barcode)
        if args.verbose:
            print("EAN number: " + res[0])
            print("LOT number: " + res[1])
            print("Expiration date: " + res[2])
            print("Catalog number: " + res[3])
        else:
            print(res)
    if args.function == 'create_gs1':
        res = str(create_gs1(args.eannumber, args.lotnumber,
                             args.expiration, args.catalognumber, "Normal"))
        if args.verbose:
            print("GS1 barcode: " + res)
        else:
            print(res)
    if args.function == 'create_gs1_with_brackets':
        res = str(create_gs1(args.eannumber, args.lotnumber,
                             args.expiration, args.catalognumber, "Brackets"))
        if args.verbose:
            print("GS1 barcode: " + res)
        else:
            print(res)
    if args.function == 'create_gs1_zpl':
        res = str(create_gs1(args.eannumber, args.lotnumber,
                             args.expiration, args.catalognumber, "ZPL"))
        if args.verbose:
            print("GS1 barcode: " + res)
        else:
            print(res)

    if args.function == 'create_gs1_character':
        res = str(create_gs1(args.eannumber, args.lotnumber,
                             args.expiration, args.catalognumber, "Character"))
        if args.verbose:
            print("GS1 barcode: " + res)
        else:
            print(res)
    if args.function == 'format_barcode':
        res = str(format_barcode(args.barcode))
        if args.verbose:
            print("GS1 formatted barcode: " + res)
        else:
            print(res)


def create_gs1(ean_number, lot_number, expiration_date, catalog_number,
               output_style="Normal"):
    """Create GS1 code.

    Arguments:
        ean_number {str} -- EAN number
        lot_number {str} -- LOT number
        expiration_date {str} -- expiration date YYMMDD
        catalog_number {str} -- catalog number

    Keyword Arguments:
        output_style {str} -- output style Normal, Brackets,
        ZPL, Charcter (default: {Normal})

    Returns:
        str -- GS1 barcode
    """

    ret = ""
    bracket_before = ""
    bracket_after = ""
    if output_style == "Normal" or output_style == "Brackets":
        if output_style == "Brackets":
            bracket_before = "("
            bracket_after = ")"
        ret = bracket_before + gtin_id+bracket_after + ean_number + \
            bracket_before + lot_id + bracket_after + lot_number + \
            bracket_before + expiration_date_id + bracket_after + \
            expiration_date + \
            bracket_before + catalog_number_id + bracket_after + \
            catalog_number
    if output_style == "ZPL":
        # >;>80105996527176340102014>6AA>5>8171907312128012280>64
        ret = "^BCN,,N,N^FD>;>8" + gtin_id + ean_number + lot_id
        if len(lot_number) > 4:
            ret = ret+lot_number[:4] + ">6"+lot_number[4:] + ">5"
        else:
            ret = ret+lot_number
        ret = ret+">8"+expiration_date_id+expiration_date
        ret = ret+catalog_number_id + \
            catalog_number[:8]+">6"+catalog_number[8:] + "^FS"
    if output_style == "Character":
        # ÍÊ!%Ça;1_H*4.Ê13'?5<!6pÈ4`Î
        ret = "ÍÊ!" + gs1_chart_dict_c[ean_number[0:2]] + \
            gs1_chart_dict_c[ean_number[2:4]] + \
            gs1_chart_dict_c[ean_number[4:6]] + \
            gs1_chart_dict_c[ean_number[6:8]] + \
            gs1_chart_dict_c[ean_number[8:10]] + \
            gs1_chart_dict_c[ean_number[10:12]] + \
            gs1_chart_dict_c[ean_number[12:]]
        ret = ret + "*" + gs1_chart_dict_c[lot_number[0:2]] + \
            gs1_chart_dict_c[lot_number[2:4]]
        if len(lot_number) > 4:
            ret = ret + "È" + lot_number[4:] + "Ç"
        ret = ret + "Ê1" + gs1_chart_dict_c[expiration_date[0:2]] + \
            gs1_chart_dict_c[expiration_date[2:4]] + \
            gs1_chart_dict_c[expiration_date[4:6]]
        ret = ret + "5" + gs1_chart_dict_c[catalog_number[0:2]] + \
            gs1_chart_dict_c[catalog_number[2:4]] + \
            gs1_chart_dict_c[catalog_number[4:6]] + \
            gs1_chart_dict_c[catalog_number[6:8]]
        ret = ret + "È" + catalog_number[8:]
        ret = ret + get_check_digit(ret) + "Î"
    return ret


def get_check_digit(code):
    """Generate CheckDigit.

    Arguments:
        code {str} -- code without CheckDigit and Stop charcter

    Returns:
        str -- CheckDigit
    """

    ret = ""
    ret_val = 0
    for i in range(1, len(code)+1):
        ret_val = ret_val + i * gs1_chart_dict_rev[code[i-1:i]]
        # Debug
    #     print(code[i-1:i] + ": " + str(i) + "> " +
    #           str(gs1_chart_dict_rev[code[i-1:i]]) + "> " +
    #           str(i * gs1_chart_dict_rev[code[i-1:i]]))
    # print(ret_val)
    # print(ret_val % 103)
    ret = gs1_chart_dict[ret_val % 103]
    return ret


def check_gtin_id(code):
    """Check GTIN ID.

    Arguments:
        code {str} -- barcode

    Returns:
        bool -- Wether the GTIN ID is (01)
    """

    ret = False
    if code[:2] == gtin_id:
        ret = True
    return ret


def verify(code):
    """Verify barcode.

    Arguments:
        code {str} -- barcode

    Returns:
        bool -- barcode is verified
    """

    ret = False
    if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', code):
        ret = True
    return ret


def get_ean_number(code):
    """Get EAN number.

    Arguments:
        code {str} -- barcode

    Returns:
        {str} -- EAN number (01)
    """

    ret = None
    if match(r'^01(\d{14})10(\d*)17(\d{6})21(\d{9})$', code):
        ret = search(r'^01(\d{14})', code).group(1)
    return ret


def get_lot_number(code):
    """Get LOT number.

    Arguments:
        code {str} -- barcode

    Returns:
        str -- LOT number (10)
    """

    ret = ""
    if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', code):
        ret = search(r'^01(\d{14})10(\d*)17', code).group(2)
    return ret


def get_expiration_date(code):
    """Get expiration date.

    Arguments:
        code {str} -- barcode

    Returns:
        str -- expiration date YYDDMM (17)
    """

    ret = ""
    if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', code):
        ret = search(r'^01(\d{14})10(\d*)17(\d{6})21', code).group(3)
    return ret


def get_catalog_number(code):
    """Get catalog number

    Arguments:
        code {str} -- barcode

    Returns:
        str -- catalog number (21)
    """

    ret = ""
    if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', code):
        ret = search(r'^01(\d{14})10(\d*)17(\d{6})21(\d{9})$', code).group(4)
    return ret


def parse_gs1(code):
    """Parse GS1 code.

    Arguments:
        code {str} -- barcode

    Returns:
        str[] -- barcode elements, (01) EAN, (10) LOT,
        (17) expiration date, (21) catalog number
    """

    if match(r'^(01)(\d{14})10(\d*)17(\d{6})21(\d{9})$', code):
        m_ean = search(r'^01(\d{14})', code).group(1)
        m_lot = search(r'^01(\d{14})10(\d*)17', code).group(2)
        m_expiration = search(r'^01(\d{14})10(\d*)17(\d{6})21', code).group(3)
        m_catalog = search(
            r'^01(\d{14})10(\d*)17(\d{6})21(\d{9})$', code).group(4)
        return m_ean, m_lot, m_expiration, m_catalog


def format_barcode(code):
    """Format barcode.

    Arguments:
        code {str} -- barcode

    Returns:
        str -- formatted barcode
    """

    ret = code.replace("(", "")
    ret = ret.replace(")", "")
    return ret


if __name__ == '__main__':
    logger.debug('Start program')
    execute_program()
    logger.debug('Exit program')
    sys.exit()
