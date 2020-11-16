import pandas as pd
from yattag import Doc
import numpy as np


df = pd.read_feather('./data/time_slice.feather')


countries = df.loc[df['aggregation_level'] == 0].groupby(['country_name'])
sub1 = df.loc[df['aggregation_level'] == 1].groupby(['subregion1_name'])
sub2 = df.loc[df['aggregation_level'] == 2].groupby(['subregion2_name'])

places = {
    'countries': countries,
    'sub1': sub1,
    'sub2': sub2
}

df = None

grouped_places = {}

for key, place in places.items():
    d = {
        'total_confirmed': place['total_confirmed'].max(),
        'population': place['population'].max(),
        'rate_infected': place['total_confirmed'].max() / place['population'].max()
    }

    grouped_places[key] = pd.DataFrame(d)
    grouped_places[key].dropna(0, inplace=True)
    grouped_places[key].sort_values('population', inplace=True, ascending=False)
    grouped_places[key] = grouped_places[key].head(150)
    grouped_places[key].sort_values('rate_infected', inplace=True, ascending=False)
    grouped_places[key]['position'] = np.arange(len(grouped_places[key]))


doc, tag, text = Doc().tagtext()
with tag('html'):
    with tag('body'):
        with tag('h1'):
            text('Highest Infection Rates In Highly Populated Places (countries, subregion1, subregion2)')
        with tag('h2'):
            text('Countries:')
        doc.asis(grouped_places['countries'].to_html())
        with tag('h2'):
            text('Subregion1:')
        doc.asis(grouped_places['sub1'].to_html())
        with tag('h2'):
            text('Subregion2:')
        doc.asis(grouped_places['sub2'].to_html())

print(doc.getvalue())