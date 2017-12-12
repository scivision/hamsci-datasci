#!/usr/bin/env python
"""plots users who submitted logs"""
from pathlib import Path
import numpy as np
from matplotlib.pyplot import figure,show
#
from pyhamtools import LookupLib,Callinfo

def readlogs(fn:Path):
    fn = Path(fn).expanduser()

    cs = np.loadtxt(fn,delimiter='\t',skiprows=3,
                    dtype=np.string_,usecols=range(8))
    cs = np.char.strip(cs.ravel(order='F'))
# %% line above could fail if input format changes, so double-check total number
    with fn.open('r') as f:
        count = int(f.readline().split()[-1])

    i=0
    for c in cs[::-1]:
        if not c:
            i+=1
        else:
            break
    if i:
        cs = cs[:-i]

    assert cs.size == count,'was callsign file read correctly?'

    return cs.astype(str)


def locatehams(cs):
    lu = LookupLib(lookuptype='countryfile',filename='cty.plist')
    ci = Callinfo(lu)
    for c in cs:
        i = ci.get_all(c)
        print(i)

def plotlogs(cs):
    ax = figure().gca()


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='.asc file to analyze')
    p = p.parse_args()

    cs = readlogs(p.fn)

    countries = locatehams(cs)

    plotlogs(countries)

    show()