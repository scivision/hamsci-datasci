#!/usr/bin/env python
"""plots users who submitted logs
./ActiveCallsignMap.py data/2016cqww_ssb.asc

"""
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
    chist = cdata['country'].value_counts()
# %% chloropleth
# https://github.com/python-visualization/folium/tree/master/examples/data
    geo = 'data/world-countries.json'

    m = folium.Map(location=[37, -102], zoom_start=5)

    m.choropleth(
     geo_data=geo,
     name='choropleth',
     data=chist,
#     columns=['country', 'Unemployment'],
     key_on='feature.name',
     fill_color='YlGn',
     fill_opacity=0.7,
     line_opacity=0.2,
     legend_name=fn.name,
    )
# %% generate map output
    folium.LayerControl().add_to(m)
    m.save(str(fn.with_suffix('.html')))