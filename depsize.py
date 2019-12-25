#!/usr/bin/env python3
#
# This script analyses Cppcheck dump files to locate possible problems with
# struct fields which size are platform-dependent.
#
# The intended use case:
# * structs with network protocols messages
# * structs used in IPC between 32-bit and 64-bit applications [1]
#
# [1]: https://groups.google.com/forum/#!topic/comp.programming.threads/oJqtUwDpEWo
#

import argparse
import sys

import cppcheckdata

FIXED_WIDTH_INTEGERS_TYPES = [
    'int8_t',
    'int16_t',
    'int32_t',
    'int64_t',
    'int_fast8_t',
    'int_fast16_t',
    'int_fast32_t',
    'int_fast64_t',
    'int_least8_t',
    'int_least16_t',
    'int_least32_t',
    'int_least64_t',
    'intmax_t',
    'intptr_t',
    'uint8_t',
    'uint16_t',
    'uint32_t',
    'uint64_t',
    'uint_fast8_t',
    'uint_fast16_t',
    'uint_fast32_t',
    'uint_fast64_t',
    'uint_least8_t',
    'uint_least16_t',
    'uint_least32_t',
    'uint_least64_t',
    'uintmax_t',
    'uintptr_t',
]


ALLOWED_TYPES = FIXED_WIDTH_INTEGERS_TYPES + [
    'char',
    'bool'
]


def reportError(token, severity, msg, id):
    cppcheckdata.reportError(token, severity, msg,
                             'platform-dependent-size', id)


def has_field_width_violations_recursive(var, visited=set()):
    if var.isPointer:
        return True
    tt = var.typeStartToken
    if not tt:
        return False
    if tt.str in ALLOWED_TYPES:
        return False
    if tt.typeScopeId and tt.typeScopeId:  # nested struct
        if var in visited:
            return True
        else:
            return has_field_width_violations_recursive(var, visited | {var})
    return True


def check_fields_width(data):
    for v in data.variables:
        if not v.scope:
            return False
        if not v.scope.type:
            return False
        if v.scope.type != 'Struct':
            return False
        if has_field_width_violations_recursive(v):
            tt = v.typeStartToken
            sname = v.scope.className
            reportError(tt, 'info', 'Size of field \'%s %s\' in struct %s can be platform dependent' % (
                tt.str, v.nameToken.str, sname),
                'fields-width')


def get_args():
    parser = cppcheckdata.ArgumentParser()
    parser.add_argument("-verify", help=argparse.SUPPRESS, action="store_true")
    return parser.parse_args()


def main():
    args = get_args()

    for f in args.dumpfile:
        if f.startswith('-'):
            continue

        if not args.quiet:
            print('Checking %s...' % f)

        data = cppcheckdata.CppcheckData(f)
        for cfg in data.iterconfigurations():
            if not args.quiet:
                print('Checking %s, config %s...' % (f, cfg.name))
            check_fields_width(cfg)


if __name__ == "__main__":
    main()
