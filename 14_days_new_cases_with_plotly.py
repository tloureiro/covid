import pandas as pd
import plotly.express as px
import datetime as datetime

df = pd.read_feather('./data/main.feather')

places = {
    'Rio de Janeiro': df[(df['subregion2_name'] == 'Rio de Janeiro')],
    'Manaus': df[(df['subregion2_name'] == 'Manaus')],
    'Stockholm': df[(df['subregion1_name'] == 'Stockholm')],
    'Ontario': df[(df['subregion1_name'] == 'Ontario')],
    'Beijing': df[(df['subregion1_name'] == 'Beijing')],
    'Brazil': df[((df['country_name'] == 'Brazil') & (df['subregion1_code'].isnull()))],
    'Canada': df[((df['country_name'] == 'Canada') & (df['subregion1_code'].isnull()))],
    'Argentina': df[((df['country_name'] == 'Argentina') & (df['subregion1_code'].isnull()))],
    'China': df[((df['country_name'] == 'China') & (df['subregion1_code'].isnull()))],
    'United States of America': df[((df['country_name'] == 'United States of America') & (df['subregion1_code'].isnull()))]
}

#I KNOW ILOC IS BETTER LEAVE ME ALONE
places['Rio de Janeiro']['new_confirmed'] = places['Rio de Janeiro']['new_confirmed'].astype(float)

fig = px.line(places['Rio de Janeiro'], x="date", y="new_confirmed", title='Life expectancy in Canada')
fig.show()

# confirmed cases total ratio
# fig.suptitle('Total Confirmed Cases / Population')
# for place_key, value in places.items():
#
#     place = places[place_key][places[place_key].date > datetime.datetime.now() - pd.to_timedelta('180day')]
#     place = place[['date', 'total_confirmed', 'population']].fillna(0)
#     place['date'] = place['date'].dt.strftime('%m-%d')
#     place = place.set_index('date')
#     place = place['total_confirmed'] / place['population']
#
#     subplot = axes_list.pop()
#     subplot.set_title(place_key)
#
#     place.plot(xlabel="", ax=subplot)


#TODO: try to use plotly
#TODO: check for na and remove the series


