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
                                           'create_gs1_with_brackets'
                                           ])
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    return parser.parse_args()


gtin_id = "01"
lot_id = "10"
expiration_date_id = "17"
catalog_number_id = "21"


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
                             args.expiration, args.catalognumber, False))
        if args.verbose:
            print("GS1 barcode: " + res)
        else:
            print(res)
    if args.function == 'create_gs1_with_brackets':
        res = str(create_gs1(args.eannumber, args.lotnumber,
                             args.expiration, args.catalognumber, True))
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
               with_brackets=False):
    """Create GS1 code.

    Arguments:
        ean_number {str} -- EAN number
        lot_number {str} -- LOT number
        expiration_date {str} -- expiration date YYMMDD
        catalog_number {str} -- catalog number

    Keyword Arguments:
        with_brackets {bool} -- wether output contains brackets
        for human reading (default: {False})

    Returns:
        str -- GS1 barcode
    """

    ret = ""
    bracket_before = ""
    bracket_after = ""
    if with_brackets:
        bracket_before = "("
        bracket_after = ")"
    ret = bracket_before + gtin_id+bracket_after + ean_number + \
        bracket_before + lot_id + bracket_after + lot_number + \
        bracket_before + expiration_date_id + bracket_after + \
        expiration_date + \
        bracket_before + catalog_number_id + bracket_after + \
        catalog_number
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
        [type] -- [description]
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
