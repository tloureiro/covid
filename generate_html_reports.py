import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime


def get_places():
    df = pd.read_feather('./data/main.feather')

    places = {
        'Ontario': df[(df['subregion1_name'] == 'Ontario') & (df['aggregation_level'] == 1)],
        'Rio de Janeiro': df[(df['subregion2_name'] == 'Rio de Janeiro')],
        'Manaus': df[(df['subregion2_name'] == 'Manaus')],
        'Stockholm': df[(df['subregion1_name'] == 'Stockholm') & (df['aggregation_level'] == 1)],
        'Beijing': df[(df['subregion1_name'] == 'Beijing') & (df['aggregation_level'] == 1)],
        'Brazil': df[(df['country_name'] == 'Brazil') & (df['aggregation_level'] == 0)],
        'Canada': df[(df['country_name'] == 'Canada') & (df['aggregation_level'] == 0)],
        'Argentina': df[(df['country_name'] == 'Argentina') & (df['aggregation_level'] == 0)],
        'China': df[(df['country_name'] == 'China') & (df['aggregation_level'] == 0)],
        'United States of America': df[(df['country_name'] == 'United States of America') & (df['aggregation_level'] == 0)],
    }

    world = df[df['aggregation_level'] == 0].groupby('date')
    world_dict = {
        'date': world['date'].unique().index,
        'new_confirmed': world['new_confirmed'].sum()
    }
    places['World'] = pd.DataFrame(world_dict)

    for place_key, value in places.items():
        places[place_key]['new_confirmed'] = places[place_key]['new_confirmed'].astype(float)

    return places


def generate_report_new_cases_per_day(places, days):
    fig = make_subplots(rows=len(places), cols=1, subplot_titles=list(places.keys()))

    row = 1
    for place_key, value in places.items():

        place_slice = places[place_key][places[place_key].date > datetime.datetime.now() - pd.to_timedelta(str(days) + 'day')]

        fig.append_trace(go.Scatter(
            x=place_slice['date'],
            y=place_slice['new_confirmed'],
            showlegend=False,
            marker_color='blue'
        ), row=row, col=1)

        row += 1

    fig.update_layout(title_text="New Cases Per Day, Last " + str(days) + " Days", height=(len(places) * 300))
    # fig.show()
    fig.write_html('./site/new_cases_per_day_' + str(days) + '.html', full_html=False)


places = get_places()

generate_report_new_cases_per_day(places, days=30)
generate_report_new_cases_per_day(places, days=90)
generate_report_new_cases_per_day(places, days=180)
generate_report_new_cases_per_day(places, days=999)


