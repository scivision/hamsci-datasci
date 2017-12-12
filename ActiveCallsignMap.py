#!/usr/bin/env python
"""plots users who submitted logs
./ActiveCallsignMap.py data/2016cqww_ssb.asc

"""
import pycountry
import webbrowser
import folium
from pathlib import Path
import pandas as pd
from hamsci_datasci.findhams import readlogs,locatehams

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='.asc file to analyze')
    p = p.parse_args()

    fn = Path(p.fn).expanduser()

    cs = readlogs(fn)

    loc = locatehams(cs)

    cdata = pd.DataFrame(index=cs,data=loc)
# %% patch country names
# https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
# FIXME: this essentially reduces resolution for now, till we get JSON shapefile that distinguishes these regions
    cdata['country'] = cdata['country'].str.replace('European Russia','Russian Federation')
    cdata['country'] = cdata['country'].str.replace('Asiatic Russia','Russian Federation')
    cdata['country'] = cdata['country'].str.replace('Kaliningrad','Russian Federation')
    cdata['country'] = cdata['country'].str.replace('Scotland','United Kingdom')
    cdata['country'] = cdata['country'].str.replace('England','United Kingdom')
    cdata['country'] = cdata['country'].str.replace('Northern Ireland','United Kingdom')
    cdata['country'] = cdata['country'].str.replace('Wales','United Kingdom')
    cdata['country'] = cdata['country'].str.replace('Asiatic Turkey','Turkey')
    cdata['country'] = cdata['country'].str.replace('European Turkey','Turkey')
    cdata['country'] = cdata['country'].str.replace('Sicily','Italy')
    cdata['country'] = cdata['country'].str.replace('Sardinia','Italy')
    cdata['country'] = cdata['country'].str.replace('Balearic Islands','Spain')
    cdata['country'] = cdata['country'].str.replace('Canary Islands','Spain')
    cdata['country'] = cdata['country'].str.replace('Ceuta & Melilla','Spain')
    cdata['country'] = cdata['country'].str.replace('West Malaysia','Malaysia')
    cdata['country'] = cdata['country'].str.replace('East Malaysia','Malaysia')
    cdata['country'] = cdata['country'].str.replace('Hawaii','United States')
    cdata['country'] = cdata['country'].str.replace('Alaska','United States')
    cdata['country'] = cdata['country'].str.replace('US Virgin Islands','United States')
    cdata['country'] = cdata['country'].str.replace('Crete','Greece')
    cdata['country'] = cdata['country'].str.replace('Svalbard','Svalbard and Jan Mayen')
    cdata['country'] = cdata['country'].str.replace('Ogasawara','Japan')

# these are simple renamings
    cdata['country'] = cdata['country'].str.replace("Laos","Lao People's Democratic Republic")
    cdata['country'] = cdata['country'].str.replace('Bolivia','Bolivia, Plurinational State of')
    cdata['country'] = cdata['country'].str.replace('Fed. Rep. of Germany','Germany')
    cdata['country'] = cdata['country'].str.replace('Republic of Moldova','Moldova, Republic of')
    cdata['country'] = cdata['country'].str.replace('Moldova','Moldova, Republic of')
    cdata['country'] = cdata['country'].str.replace('Bosnia-Herzegovina','Bosnia and Herzegovina')
    cdata['country'] = cdata['country'].str.replace('Macedonia','Macedonia, Republic of')
    cdata['country'] = cdata['country'].str.replace('Micronesia','Micronesia, Federated States of')
    cdata['country'] = cdata['country'].str.replace('Republic of Korea','Korea, Republic of')
    cdata['country'] = cdata['country'].str.replace('Taiwan','Taiwan, Province of China')
    cdata['country'] = cdata['country'].str.replace('Czech Republic','Czechia')
    cdata['country'] = cdata['country'].str.replace('Slovak Republic','Slovakia')
    cdata['country'] = cdata['country'].str.replace('Venezuela','Venezuela, Bolivarian Republic of')
    cdata['country'] = cdata['country'].str.replace('Vietnam','Viet Nam')
    cdata['country'] = cdata['country'].str.replace('Tanzania','Tanzania, United Republic of')
# %% count entries
    chist = cdata['country'].value_counts()

    codes = []
    for i in chist.index:
        try:
            codes.append(pycountry.countries.get(name=i).alpha_3)
        except KeyError:
            print(i,chist[i])
            codes.append(i) #leave broken value

    chist.index=codes
# %% chloropleth
# https://github.com/python-visualization/folium/tree/master/examples/data
# https://github.com/python-visualization/folium/blob/106d8292afbc8952fa224f2be65a8839688714c2/folium/folium.py
    geo = 'data/world-countries.json'

    m = folium.Map(location=[37, -102], zoom_start=5)

    m.choropleth(
     geo_data=geo,
     name='choropleth',
     data=chist,
     columns=['country',],
     key_on='feature.id',
     fill_color='YlOrRd',
     threshold_scale=[1, 50, 100, 200, 1000],
#     fill_opacity=0.7,
#     line_opacity=0.2,
     legend_name=fn.name,
    )
# %% generate map output
    folium.LayerControl().add_to(m)

    ofn = fn.with_suffix('.html')
    print('writing',ofn)
    m.save(str(ofn))

    webbrowser.open(str(ofn))

  #  chist.hist(bins=20)