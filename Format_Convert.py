#!/bin/env python
"""
Tax Processing

This program does the heavy lifting and processes the incoming tax roll to be
formatted for printing. It's a fairly easy process with some small gotcha's.

The first thing is to make sure the number of columns has not changed or the
formatting of them has not. If either has changed then you need to change the
formatting var and the fields array to match up with all the counts, I included
a key both in the documents and inline. Also watch out for the last three
numbers columns.

They require extra formatting so there is a for loop that iterates through them
to clean them out. Make sure to edit what parts of the array they iterate
through

Usage
tax_processing.py (input.txt) [> output.txt]

All output is printed to stdout and is designed to be piped to an output file.
This uses stdout in order to speed up testing and trobleshooting new files.


Processing notes (As of 2009 when 2 digit year was removed)

Here is the starting line
901001-09-215-006A & H INVESTMENTS L L C              000052500000094313000000000

Here is the breakdown
district[3] account[14] name[37] number1[9] number2[9] number3[9]

Here is a visualization of the cut with pipelines
901|001-09-215-006|A & H INVESTMENTS L L C              |000052500|000094313|000000000|

Here is how we format it
dist\saccount\tname\tnumber1\tnumber2\tnumber3\n

The last three numbers need special attention though.
1) Leading zeros are discarded
2) "Empty" or zero sum numbers are not shown at all
3) Thousands commas are needed.

Here is the result
901 001-09-215-006	A & H INVESTMENTS L L C              	52,500	94,313

#Current format Key
    district	3
    account		14
    name		37
    number1		9
    number2		9
    number3		9
"""
from operator import add
import os
import sys


class ArgumentException(Exception):
    pass


def commafy(d):
    """
    RegEXPless commafy
    Only use this for cash since it evokes a 2 point precision.
    """
    s = '%0.2f' % d
    a, b = s.split('.')
    l = []
    while len(a) > 3:
        l.insert(0, a[-3:])
        a = a[0:-3]
    if a:
        l.insert(0, a)
    return ','.join(l)


def parse_arguments(arguments):
    """
    KISS
    """
    if not len(arguments) == 2:
        print "Please run this with the tax file to parse only"
        raise ArgumentException("incorrect arguments provided")
    return arguments[1]


def parse_file(inFile, outFile):
    """
    For the LOVE OF GODS keep the fields section up to date with docs
    """
    fields = [3, 14, 37, 9, 9, 9]
    outFormat = "{0} {1}\t{2}\t{3}\t{4}\t{5}\n"
    inHandle = open(inFile, mode='r')
    outHandle = open(outFile, mode='w')

    lineCount = 0
    for line in inHandle:
        index = 0
        outList = []
        for count in fields:
            outList.append(line[index:add(index, count)])
            index += count
        outHandle.write(outFormat.format(outList))
        lineCount += 1
    return lineCount


if __name__ == '__main__':
    inFile = parse_arguments(sys.argv)
    outFile = os.path.splitext(inFile)[0] + "-out.cvt"
    lineCount = parse_file(inFile, outFile)
    print "Total Lines: {}\n".format(lineCount)
