import pandas as pd
# import plotly.express as px

from plotly.subplots import make_subplots
import plotly.graph_objects as go

df = pd.read_feather('../data/main.feather')

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

# fig = px.line(places['Rio de Janeiro'], x="date", y="new_confirmed", title='Life expectancy in Canada')
# fig.write_html('./data/test.html')




fig = make_subplots(rows=4, cols=1, subplot_titles=('Rio de Janeiro', 'Rio de Janeiro', 'Rio de Janeiro'))

fig.append_trace(go.Scatter(
    x=places['Rio de Janeiro']['date'],
    y=places['Rio de Janeiro']['new_confirmed'],
    showlegend=False,
    marker_color='blue'
), row=1, col=1)

fig.append_trace(go.Scatter(
    x=places['Rio de Janeiro']['date'],
    y=places['Rio de Janeiro']['new_confirmed'],
    showlegend=False,
), row=2, col=1)

fig.append_trace(go.Scatter(
    x=places['Rio de Janeiro']['date'],
    y=places['Rio de Janeiro']['new_confirmed'],
    showlegend=False,
), row=3, col=1)

fig.update_layout(title_text="New Cases per day")
fig.show()
# fig.write_html('./data/test.html', full_html=False)

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


