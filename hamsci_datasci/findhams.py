from pathlib import Path
import numpy as np
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

    loc = [ci.get_all(c) for c in cs]

    return loc