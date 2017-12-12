#!/usr/bin/env python
"""plots users who submitted logs"""

from hamsci_datasci.findhams import readlogs,locatehams

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='.asc file to analyze')
    p = p.parse_args()

    cs = readlogs(p.fn)

    loc = locatehams(cs)
