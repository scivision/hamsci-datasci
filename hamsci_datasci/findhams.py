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

def country_rename(clist):
    """Renames countries, for now losing resolution where countries have names regions"""

# %% patch country names
# https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
# FIXME: this essentially reduces resolution for now, till we get JSON shapefile that distinguishes these regions
    hive = {
    'European Russia':'Russian Federation',
    'European Russia':'Russian Federation',
    'Asiatic Russia':'Russian Federation',
    'Kaliningrad':'Russian Federation',
    'Scotland':'United Kingdom',
    'England':'United Kingdom',
    'Northern Ireland':'United Kingdom',
    'Wales':'United Kingdom',
    'Asiatic Turkey':'Turkey',
    'European Turkey':'Turkey',
    'Sicily':'Italy',
    'Sardinia':'Italy',
    'Balearic Islands':'Spain',
    'Canary Islands':'Spain',
    'Ceuta & Melilla':'Spain',
    'West Malaysia':'Malaysia',
    'East Malaysia':'Malaysia',
    'Hawaii':'United States',
    'Alaska':'United States',
    'US Virgin Islands':'United States',
    'Crete':'Greece',
    'Svalbard':'Svalbard and Jan Mayen',
    'Ogasawara':'Japan',
    'South Cook Islands':'Cook Islands',
    'Easter Island':'Chile',
    # renames
    'Trinidad & Tobago':'Trinidad and Tobago',
    "Laos":"Lao People's Democratic Republic",
    'Bolivia':'Bolivia, Plurinational State of',
    'Fed. Rep. of Germany':'Germany',
    'Republic of Moldova':'Moldova, Republic of',
    'Moldova':'Moldova, Republic of',
    'Bosnia-Herzegovina':'Bosnia and Herzegovina',
    'Macedonia':'Macedonia, Republic of',
    'Micronesia':'Micronesia, Federated States of',
    'Republic of Korea':'Korea, Republic of',
    'Taiwan':'Taiwan, Province of China',
    'Czech Republic':'Czechia',
    'Slovak Republic':'Slovakia',
    'Venezuela':'Venezuela, Bolivarian Republic of',
    'Vietnam':'Viet Nam',
    'Tanzania':'Tanzania, United Republic of',
    'Sint Maarten':'Sint Maarten (Dutch part)',
    'Turks & Caicos Islands':'Turks and Caicos Islands',
    'Antigua & Barbuda':'Antigua and Barbuda',
    'Curacao':'Curaçao',
    }


    for k,v in hive.items():
        clist = clist.str.replace(k,v)

    return clist
