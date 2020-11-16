import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import datetime
from yattag import Doc


def get_places():
    df = pd.read_feather('./data/main.feather')

    places = {
        'Ontario': df[(df['subregion1_name'] == 'Ontario') & (df['aggregation_level'] == 1)],
        'Toronto': df[(df['subregion2_name'] == 'Toronto')],
        'Rio de Janeiro (City)': df[(df['subregion2_name'] == 'Rio de Janeiro')],
        'Rio de Janeiro (State)': df[(df['subregion1_name'] == 'Rio de Janeiro') & (df['aggregation_level'] == 1)],
        'São Paulo (City)': df[(df['subregion2_name'] == 'São Paulo')],
        'São Paulo (State)': df[(df['subregion1_name'] == 'São Paulo') & (df['aggregation_level'] == 1)],
        'Manaus': df[(df['subregion2_name'] == 'Manaus')],
        'Stockholm': df[(df['subregion1_name'] == 'Stockholm') & (df['aggregation_level'] == 1)],
        'New York': df[(df['subregion1_name'] == 'New York') & (df['aggregation_level'] == 1)],
        'London': df[(df['subregion1_name'] == 'London Region') & (df['aggregation_level'] == 1)],
        'Cape Town (City)': df[(df['subregion2_name'] == 'City of Cape Town Metropolitan Municipality')],
        'Beijing': df[(df['subregion1_name'] == 'Beijing') & (df['aggregation_level'] == 1)],
        'Brazil': df[(df['country_name'] == 'Brazil') & (df['aggregation_level'] == 0)],
        'Canada': df[(df['country_name'] == 'Canada') & (df['aggregation_level'] == 0)],
        'Argentina': df[(df['country_name'] == 'Argentina') & (df['aggregation_level'] == 0)],
        'France': df[(df['country_name'] == 'Argentina') & (df['aggregation_level'] == 0)],
        'Italy': df[(df['country_name'] == 'Argentina') & (df['aggregation_level'] == 0)],
        'South Africa': df[(df['country_name'] == 'South Africa') & (df['aggregation_level'] == 0)],
        'Japan': df[(df['country_name'] == 'Japan') & (df['aggregation_level'] == 0)],
        'China': df[(df['country_name'] == 'China') & (df['aggregation_level'] == 0)],
        'United States of America': df[(df['country_name'] == 'United States of America') & (df['aggregation_level'] == 0)],
        'Wisconsin': df[(df['subregion1_name'] == 'Wisconsin') & (df['aggregation_level'] == 1)],
        'Florida': df[(df['subregion1_name'] == 'Florida') & (df['aggregation_level'] == 1)],
        'Miami-Dade County': df[(df['subregion2_name'] == 'Miami-Dade County') & (df['aggregation_level'] == 2)],
        'Brasília': df[(df['subregion2_name'] == 'Brasília') & (df['aggregation_level'] == 2)],
        'Barcelona': df[(df['subregion2_name'] == 'Barcelona') & (df['aggregation_level'] == 2)],
        'Belgium': df[(df['country_name'] == 'Belgium') & (df['aggregation_level'] == 0)],
        'Israel': df[(df['country_name'] == 'Israel') & (df['aggregation_level'] == 0)],
        'Qatar': df[(df['country_name'] == 'Qatar') & (df['aggregation_level'] == 0)],
    }

    places['Toronto']['population'] = 6197000.00

    world = df[df['aggregation_level'] == 0].groupby('date')
    world_dict = {
        'date': world['date'].unique().index,
        'new_confirmed': world['new_confirmed'].sum(),
        'total_confirmed': world['total_confirmed'].sum(),
        'population': world['population'].sum(),
        'total_deceased': world['total_deceased'].sum(),
    }
    places['World'] = pd.DataFrame(world_dict)

    # trying to free memory here
    df = None

    # temporary fix because of pandas bug to deal with ints and na's
    for place_key, value in places.items():
        places[place_key]['new_confirmed'] = places[place_key]['new_confirmed'].astype(float)
        places[place_key]['total_confirmed'] = places[place_key]['total_confirmed'].astype(float)
        places[place_key]['population'] = places[place_key]['population'].astype(float)
        places[place_key]['total_deceased'] = places[place_key]['total_deceased'].astype(float)

    return places


def generate_report_new_cases_per_day(places, days):
    fig = make_subplots(rows=len(places), cols=1, subplot_titles=list(places.keys()))

    row = 1
    for place_key, value in places.items():
        place = places[place_key]
        place_slice = place[place.date > datetime.datetime.now() - pd.to_timedelta(str(days) + 'day')]

        fig.append_trace(go.Scatter(
            x=place_slice['date'],
            y=place_slice['new_confirmed'],
            showlegend=False,
            marker_color='blue'
        ), row=row, col=1)

        row += 1

    fig.update_layout(title_text="New Cases Per Day, Last " + str(days) + " Days", height=(len(places) * 300))
    # fig.show()
    fig.write_html('./site/new_cases_per_day_' + str(days) + '.html')


def generate_report_new_cases_percentage_of_population_infected_per_day(places, days):
    fig = make_subplots(rows=len(places), cols=1, subplot_titles=list(places.keys()))

    row = 1
    for place_key, value in places.items():
        place = places[place_key]
        place_slice = place[place.date > datetime.datetime.now() - pd.to_timedelta(str(days) + 'day')]

        place_slice['percentage_infected'] = (place_slice['new_confirmed'] / place_slice['population']) * 100

        fig.append_trace(go.Scatter(
            x=place_slice['date'],
            y=place_slice['percentage_infected'],
            showlegend=False,
            marker_color='blue'
        ), row=row, col=1)

        row += 1

    fig.update_layout(title_text='Percentage of population infected per day in the last ' + str(days) + ' days', height=(len(places) * 300))
    # fig.show()
    fig.write_html('./site/new_cases_percentage_of_population_infected_per_day_' + str(days) + '.html')


def generate_report_percentage_of_population_infected(places):
    fig = make_subplots(rows=len(places), cols=1, subplot_titles=list(places.keys()))

    row = 1
    for place_key, value in places.items():
        place = places[place_key]
        place['percentage_infected_total'] = (place['total_confirmed'] / place['population']) * 100

        fig.append_trace(go.Scatter(
            x=place['date'],
            y=place['percentage_infected_total'],
            showlegend=False,
            marker_color='blue'
        ), row=row, col=1)

        row += 1

    fig.update_layout(title_text='Percentage of population infected', height=(len(places) * 300))
    # fig.show()
    fig.write_html('./site/percentage_of_population_infected.html')


def generate_report_last_report_cases_in_a_day(places):
    doc, tag, text = Doc().tagtext()
    row = 1

    with tag('html'):
        with tag('body'):
            with tag('h1'):
                text('Last reported cases in a day')

            for place_key, value in places.items():
                place = places[place_key]
                last_day = place.loc[place['new_confirmed'].notna()].iloc[-1]

                if place_key == 'World':
                    last_day = place.loc[place['new_confirmed'].notna()].iloc[-3]
                elif last_day['new_confirmed'] == 0:
                    index = -2
                    while place.loc[place['new_confirmed'].notna()].iloc[index]['new_confirmed'] == 0:
                        index -= 1

                    last_day = place.loc[place['new_confirmed'].notna()].iloc[index]

                with tag('h2'):
                    text(place_key + ' ' + last_day['date'].strftime('%m-%d'))
                with tag('h3'):
                    text('Cases: ' + str(int(last_day['new_confirmed'])))
                with tag('h3'):
                    text('Percentage of population: ' +
                         str(round(last_day['new_confirmed'] / last_day['population'] * 100, 3)) + '%')
                doc.stag('br')
                doc.stag('br')

    with open('./site/last_reported_cases_in_a_day.html', 'w') as writer:
        writer.write(doc.getvalue())


def generate_report_total_and_percentage_deceased(places):
    fig = make_subplots(rows=len(places), cols=1, subplot_titles=list(places.keys()))

    row = 1
    for place_key, value in places.items():
        place = places[place_key]

        place['percentage_deceased_total'] = (place['total_deceased'] / place['population']) * 100

        fig.add_trace(go.Scatter(
            x=place['date'],
            y=place['total_deceased'],
            customdata=np.dstack((place['percentage_deceased_total'])),
            hovertemplate='<b>Total Deceased: %{y}</b><br><b>Percentage Deceased: %{text:.3f}%</b>',
            text=place['percentage_deceased_total'],
            showlegend=False,
            marker_color='blue'
        ), row=row, col=1)

        row += 1

    fig.update_layout(title_text='Total and percentage of population deceased', height=(len(places) * 300))
    # fig.show()
    fig.write_html('./site/total_and_percentage_of_population_deceased.html')


places = get_places()

generate_report_new_cases_per_day(places, days=30)
generate_report_new_cases_per_day(places, days=90)
generate_report_new_cases_per_day(places, days=180)
generate_report_new_cases_per_day(places, days=999)

generate_report_new_cases_percentage_of_population_infected_per_day(places, days=30)
generate_report_new_cases_percentage_of_population_infected_per_day(places, days=90)
generate_report_new_cases_percentage_of_population_infected_per_day(places, days=180)
generate_report_new_cases_percentage_of_population_infected_per_day(places, days=999)

generate_report_total_and_percentage_deceased(places)

generate_report_percentage_of_population_infected(places)

generate_report_last_report_cases_in_a_day(places)


