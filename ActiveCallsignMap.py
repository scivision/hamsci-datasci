#!/usr/bin/env python
"""plots users who submitted logs
./ActiveCallsignMap.py data/2016cqww_ssb.asc

"""
import pycountry
import webbrowser
import folium
from pathlib import Path
import pandas as pd
from hamsci_datasci.findhams import readlogs,locatehams,country_rename

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='.asc file to analyze')
    p = p.parse_args()

    fn = Path(p.fn).expanduser()

    cs = readlogs(fn)

    loc = locatehams(cs)

    cdata = pd.DataFrame(index=cs,data=loc)

    cdata['country'] = country_rename(cdata['country'])
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