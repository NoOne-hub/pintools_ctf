#!/usr/bin/env/python
# coding: utf8


import sys
import string as s
import argparse
from config import *
from Pin import Pin


def start():
    parser = argparse.ArgumentParser(prog='pintool.py')
    parser.add_argument('-e', dest='study', action='store_true', default=False,
                        help='Study the password length, for example -e -l 40, with 40 characters')
    parser.add_argument('-l', dest='len', type=str, nargs=1, default='10', help='Length of password (Default: 10 )')
    parser.add_argument('-c', dest='number', type=str, default=1,
                        help="Charset definition for brute force\n (1-Lowercase,\n2-Uppecase,\n3-Numbers,\n4-Hexadecimal,\n5-Punctuation,\n6-All)")
    parser.add_argument('-b', dest='character', type=str, nargs=1, default='',
                        help='Add characters for the charset, example -b _-')
    parser.add_argument('-a', dest='addr', type=str, nargs=1, default='0',
                        help='Program architecture 32 or 64 bits, -b 32 or -b 64 ')
    parser.add_argument('-i', dest='initpass', type=str, nargs=1, default='',
                        help='Inicial password characters, example -i CTF{')
    parser.add_argument('-s', dest='simbol', type=str, nargs=1, default='_',
                        help='Simbol for complete all password (Default: _ )')
    parser.add_argument('-d', dest='expression', type=str, nargs=1, default='QQ',
                        help="Difference between instructions that are successful or not (Default: != 0, example -d '== -12', -d '=> 900', -d '<= 17' or -d '!= 32')")
    parser.add_argument('-r', dest='reverse', action='store_true', default=False,
                        help='Reverse order. Bruteforce from the last character')
    parser.add_argument('-f', dest='find', action='store_true', default=False, help='Study the first word')
    parser.add_argument('Filename', help='Program for playing with Pin Tool')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    return args


def getCharset(num, addchar):
    char = ""
    charset = {'1': s.ascii_lowercase,
               '2': s.ascii_uppercase,
               '3': s.digits,
               '4': s.hexdigits,
               '5': s.punctuation,
               '6': s.printable}

    if num == 1:
        return charset['1']
    else:
        num = num.split(',')

    for i in num:
        if 1 <= int(i) <= 6:
            i = '%s' % i
            char += charset[i]
        else:
            print("Number %s out of range." % (i))

    return char + ''.join(addchar)


def addchar(initpass, char):
    if args.reverse:
        initpass = char + initpass
    else:
        initpass += char
    return initpass


def pretty_print(result):
    import prettytable as pt
    tb = pt.PrettyTable()
    table_length = len(result[0])
    tb.field_names = ["char", "payload", "instructions", "differences"][:table_length]
    for i in result:
        tb.add_row(i)
    print(tb)


def lengthdetect(passlen):
    argv = []
    for i in range(1, passlen + 1):
        password = "_" * i
        argv.append((i, password))
    pin.run_pin(argv)
    result = pin.get_all_result()
    pretty_print(result)



def finddetect(initpass, passlen, charset, symbfill):
    initlen = len(initpass)
    argv = []
    for char in charset:
        password = initpass + char + (passlen - initlen - 1) * symbfill
        argv.append((char, password))
    pin.run_pin(argv)
    result = pin.get_all_result()
    pretty_print(result)


def solve_equal(initpass, passlen, symbfill, charset):
    initlen = len(initpass)
    for i in range(initlen, passlen):
        if args.reverse:
            tempassword = symbfill * (passlen - i) + initpass
        else:
            tempassword = initpass + symbfill * (passlen - i)

        if args.reverse:
            i = passlen - i
        argv = []
        for char in charset:
            if args.reverse:
                password = tempassword[:i - 1] + char + tempassword[i:]
            else:
                password = tempassword[:i] + char + tempassword[i + 1:]
            argv.append((char, password))
            pin.run_pin(argv)
            pretty_print(pin.get_all_result())
            char = pin.get_equal(int(number))
            initpass = addchar(initpass, char)

    return initpass


def solve_unequal(initpass, passlen, symbfill, charset):
    initlen = len(initpass)
    for i in range(initlen, passlen):

        if args.reverse:
            tempassword = symbfill * (passlen - i) + initpass
        else:
            tempassword = initpass + symbfill * (passlen - i)

        if args.reverse:
            i = passlen - i
        argv = []
        for char in charset:

            if args.reverse:
                password = tempassword[:i - 1] + char + tempassword[i:]
            else:
                password = tempassword[:i] + char + tempassword[i + 1:]
            argv.append((char, password))
        pin.run_pin(argv)
        pretty_print(pin.get_all_result())
        char = pin.get_unequal(int(number))
        initpass = addchar(initpass, char)

    return initpass


def solve_below(initpass, passlen, symbfill, charset):
    initlen = len(initpass)
    for i in range(initlen, passlen):

        if args.reverse:
            tempassword = symbfill * (passlen - i) + initpass
        else:
            tempassword = initpass + symbfill * (passlen - i)

        argv = []

        if args.reverse:
            i = passlen - i
        for char in charset:

            if args.reverse:
                password = tempassword[:i - 1] + char + tempassword[i:]
            else:
                password = tempassword[:i] + char + tempassword[i + 1:]
            argv.append((char, password))
        pin.run_pin(argv)
        pretty_print(pin.get_all_result())
        char = pin.get_below(int(number))
        initpass = addchar(initpass, char)
    return initpass


def solve_after(initpass, passlen, symbfill, charset):
    initlen = len(initpass)
    for i in range(initlen, passlen):

        if args.reverse:
            tempassword = symbfill * (passlen - i) + initpass
        else:
            tempassword = initpass + symbfill * (passlen - i)

        argv = []
        if args.reverse:
            i = passlen - i
        for char in charset:

            if args.reverse:
                password = tempassword[:i - 1] + char + tempassword[i:]
            else:
                password = tempassword[:i] + char + tempassword[i + 1:]
            argv.append((char, password))
        pin.run_pin(argv)
        pretty_print(pin.get_all_result())
        char = pin.get_after(int(number))
        initpass = addchar(initpass, char)
    return initpass


def solve_min(initpass, passlen, symbfill, charset):
    initlen = len(initpass)
    for i in range(initlen, passlen):

        if args.reverse:
            tempassword = symbfill * (passlen - i) + initpass
        else:
            tempassword = initpass + symbfill * (passlen - i)
        if args.reverse:
            i = passlen - i
        argv = []
        for char in charset:
            if args.reverse:
                password = tempassword[:i - 1] + char + tempassword[i:]
            else:
                password = tempassword[:i] + char + tempassword[i + 1:]
            argv.append((char, password))
        pin.run_pin(argv)
        pretty_print(pin.get_all_result())
        char = pin.get_min()
        initpass = addchar(initpass, char)
    return initpass


def solve_max(initpass, passlen, symbfill, charset):
    initlen = len(initpass)
    for i in range(initlen, passlen):

        if args.reverse:
            tempassword = symbfill * (passlen - i) + initpass
        else:
            tempassword = initpass + symbfill * (passlen - i)
        if args.reverse:
            i = passlen - i
        argv = []
        for char in charset:
            if args.reverse:
                password = tempassword[:i - 1] + char + tempassword[i:]
            else:
                password = tempassword[:i] + char + tempassword[i + 1:]
            argv.append((char, password))
        pin.run_pin(argv)
        pretty_print(pin.get_all_result())
        char = pin.get_max()
        initpass = addchar(initpass, char)
    return initpass


def solve_diff(initpass, passlen, symbfill, charset):
    initlen = len(initpass)
    for i in range(initlen, passlen):

        if args.reverse:
            tempassword = symbfill * (passlen - i) + initpass
        else:
            tempassword = initpass + symbfill * (passlen - i)
        if args.reverse:
            i = passlen - i
        argv = []
        for char in charset:
            if args.reverse:
                password = tempassword[:i - 1] + char + tempassword[i:]
            else:
                password = tempassword[:i] + char + tempassword[i + 1:]
            argv.append((char, password))
        pin.run_pin(argv)
        pretty_print(pin.get_all_result())
        char = pin.get_diff()
        initpass = addchar(initpass, char)
    return initpass


if __name__ == '__main__':

    args = start()

    initpass = ''.join(args.initpass)
    passlen = int(''.join(args.len))
    symbfill = ''.join(args.simbol)
    # charset = symbfill + getCharset(args.number, args.character)
    charset = getCharset(args.number, args.character)
    addr = ''.join(args.addr)
    expression = ''.join(args.expression).rstrip()
    try:
        number = expression.split()[1]
    except Exception as e:
        pass
    study = args.study
    learn = args.find

    if len(initpass) >= passlen:
        print("The length of init password must be less than password length.")
        sys.exit()

    if passlen > 64:
        print("The password must be less than 64 characters.")
        sys.exit()

    if len(symbfill) > 1:
        print("Only one symbol is allowed.")
        sys.exit()

    import subprocess

    cmd = "file {} | cut -d' ' -f 3".format(args.Filename)
    res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sout, serr = res.communicate()
    file_arch = int(sout.decode().split("-")[0])
    if file_arch == 64:
        INSCOUNT = INSCOUNT64
    else:
        INSCOUNT = INSCOUNT32

    pin = Pin(INSCOUNT, args.Filename, addr)
    if study is True:
        lengthdetect(passlen)
        sys.exit()
    if learn is True:
        finddetect(initpass, passlen, charset, symbfill)
        sys.exit()

    if "!=" in expression:
        solve = solve_unequal
    elif "==" in expression:
        solve = solve_equal
    elif "<=" in expression:
        solve = solve_below
    elif "=>" in expression or ">=" in expression:
        solve = solve_after
    elif "min" in expression:
        solve = solve_min
    elif "max" in expression:
        solve = solve_max
    else:
        solve = solve_diff
    password = solve(initpass, passlen, symbfill, charset)
    print("Password: ", password)
