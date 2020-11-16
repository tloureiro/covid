import pandas as pd


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

# instead of doing total_confirmed I could sum last 30 or 60 days


