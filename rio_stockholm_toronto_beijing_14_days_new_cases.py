import pandas as pd
import datetime as datetime

df = pd.read_feather('./data/main.feather')
df = df[(df['subregion2_name'] == 'Toronto')]

df = df[df.date > datetime.datetime.now() - pd.to_timedelta("15day")]

# df = df[
#     (df['subregion2_name'] == 'Rio de Janeiro') |
#     (df['subregion1_name'] == 'Stockholm') |
#     (df['subregion2_name'] == 'Toronto') |
#     (df['subregion1_name'] == 'Beijing')
# ]


dg = df[['date', 'new_confirmed']].fillna(0)

dg['date'] = dg['date'].dt.strftime('%m-%d')
dg = dg.set_index('date')
# dg = dg[['new_confirmed']]
dg.plot()

