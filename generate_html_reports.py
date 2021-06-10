import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from yattag import Doc
from sklearn.linear_model import LinearRegression


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
        'France': df[(df['country_name'] == 'France') & (df['aggregation_level'] == 0)],
        'Italy': df[(df['country_name'] == 'Italy') & (df['aggregation_level'] == 0)],
        'South Africa': df[(df['country_name'] == 'South Africa') & (df['aggregation_level'] == 0)],
        'Japan': df[(df['country_name'] == 'Japan') & (df['aggregation_level'] == 0)],
        'China': df[(df['country_name'] == 'China') & (df['aggregation_level'] == 0)],
        'United States of America': df[(df['country_name'] == 'United States of America') & (df['aggregation_level'] == 0)],
        'Wisconsin': df[(df['subregion1_name'] == 'Wisconsin') & (df['aggregation_level'] == 1)],
        'Florida': df[(df['subregion1_name'] == 'Florida') & (df['aggregation_level'] == 1)],
        'Miami-Dade County': df[(df['subregion2_name'] == 'Miami-Dade County') & (df['aggregation_level'] == 2)],
        'Brasília': df[(df['subregion2_name'] == 'Brasília') & (df['aggregation_level'] == 2)],
        'Barcelona': df[(df['subregion2_name'] == 'Barcelona') & (df['aggregation_level'] == 2)],
        'Boa Vista': df[(df['subregion2_name'] == 'Boa Vista') & (df['aggregation_level'] == 2)],
        'Lima': df[(df['subregion2_name'] == 'Lima') & (df['aggregation_level'] == 2)],
        'Belgium': df[(df['country_name'] == 'Belgium') & (df['aggregation_level'] == 0)],
        'Israel': df[(df['country_name'] == 'Israel') & (df['aggregation_level'] == 0)],
        'Qatar': df[(df['country_name'] == 'Qatar') & (df['aggregation_level'] == 0)],
        'Jerusalem District': df[(df['subregion1_name'] == 'Jerusalem District') & (df['aggregation_level'] == 1)],
        'Tel Aviv District': df[(df['subregion1_name'] == 'Tel Aviv District') & (df['aggregation_level'] == 1)],
        'Haifa District': df[(df['subregion1_name'] == 'Haifa District') & (df['aggregation_level'] == 1)],
        'Cook County': df[(df['subregion2_name'] == 'Cook County') & (df['subregion1_name'] == 'Illinois') & (df['aggregation_level'] == 2)],
        'United Kingdom': df[(df['country_name'] == 'United Kingdom') & (df['aggregation_level'] == 0)],
    }

    places['Toronto']['population'] = 6197000.00

    world = df[df['aggregation_level'] == 0].groupby('date')
    world_dict = {
        'date': world['date'].unique().index,
        'new_confirmed': world['new_confirmed'].sum(),
        'new_deceased': world['new_deceased'].sum(),
        'total_confirmed': world['total_confirmed'].sum(),
        'population': world['population'].sum(),
        'total_deceased': world['total_deceased'].sum(),
        'total_vaccine_doses_administered': world['total_vaccine_doses_administered'].sum(),
        'population_age_10_19': world['population_age_10_19'].sum(),
        'population_age_20_29': world['population_age_20_29'].sum(),
    }
    places['World'] = pd.DataFrame(world_dict)

    # trying to free memory here
    df = None

    # temporary fix because of pandas bug to deal with ints and na's
    for place_key, value in places.items():
        places[place_key]['new_confirmed'] = places[place_key]['new_confirmed'].astype(float)
        places[place_key]['new_deceased'] = places[place_key]['new_deceased'].astype(float)
        places[place_key]['total_confirmed'] = places[place_key]['total_confirmed'].astype(float)
        places[place_key]['population'] = places[place_key]['population'].astype(float)
        places[place_key]['total_deceased'] = places[place_key]['total_deceased'].astype(float)

    return places


def predict_date_based_on_vaccines(linear_regressor, future_vaccine_quantities):
    dates = []
    dates_ordinal = []

    for future_vaccine_quantity in future_vaccine_quantities:
        predicted_date = (future_vaccine_quantity - linear_regressor.intercept_) / linear_regressor.coef_
        dates_ordinal.append(round(predicted_date[0][0]))
        dates.append(datetime.datetime.fromordinal(round(predicted_date[0][0])))
    return dates, dates_ordinal


def get_spaced_out_x_texts(values, number_to_return):
    idx = np.round(np.linspace(0, len(values) - 1, number_to_return)).astype(int)

    for i in range(0, len(values) - 1):
        if i not in idx:
            values[i] = None

    return values


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


def generate_report_percentage_of_population_deceased_per_day(places, days):
    fig = make_subplots(rows=len(places), cols=1, subplot_titles=list(places.keys()))

    row = 1
    for place_key, value in places.items():
        place = places[place_key]
        place_slice = place[place.date > datetime.datetime.now() - pd.to_timedelta(str(days) + 'day')]

        place_slice['percentage_deceased'] = (place_slice['new_deceased'] / place_slice['population']) * 100

        fig.append_trace(go.Scatter(
            x=place_slice['date'],
            y=place_slice['percentage_deceased'],
            showlegend=False,
            marker_color='blue'
        ), row=row, col=1)

        row += 1

    fig.update_layout(title_text='Percentage of population deceased per day in the last ' + str(days) + ' days', height=(len(places) * 300))
    # fig.show()
    fig.write_html('./site/percentage_of_population_deceased_per_day_' + str(days) + '.html')


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

    doc.asis('<?xml version="1.0" encoding="UTF-8"?>')

    with tag('html'):
        with tag('body'):
            with tag('h1'):
                text('Last reported cases in a day')

            for place_key, value in places.items():
                place = places[place_key]

                if place.loc[place['new_confirmed'].notna()].shape[0] == 0:
                    continue
                else:
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

    with open('./site/last_reported_cases_in_a_day.html', 'w', encoding='utf-8') as writer:
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


def generate_ranking_reports():
    df = pd.read_feather('./data/main.feather')

    df.loc[(df['subregion2_name'] == 'Toronto') & (df['aggregation_level'] == 2), 'population'] = 6197000.00

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

    # first infections
    for key, place in places.items():
        d = {
            'total_confirmed': place['total_confirmed'].max(),
            'total_deceased': place['total_deceased'].max(),
            'population': place['population'].max(),
            'rate_infected_%': (place['total_confirmed'].max() / place['population'].max()) * 100,
            'rate_mortality_%': (place['total_deceased'].max() / place['population'].max()) * 100,
            'rate_mortality_by_infected_%': (place['total_deceased'].max() / place['total_confirmed'].max()) * 100,
        }

        grouped_places[key] = pd.DataFrame(d)
        grouped_places[key].dropna(0, inplace=True)
        grouped_places[key].sort_values('population', inplace=True, ascending=False)

        if key == 'countries':
            grouped_places[key] = grouped_places[key].head(100)
        else:
            grouped_places[key] = grouped_places[key].head(1000)

        grouped_places[key].sort_values('rate_infected_%', inplace=True, ascending=False)
        grouped_places[key]['position'] = np.arange(len(grouped_places[key])) + 1

    doc, tag, text = Doc().tagtext()

    doc.asis('<?xml version="1.0" encoding="UTF-8"?>')

    with tag('html'):
        with tag('body'):
            with tag('h1'):
                text('Highest Infection Rates In Highly Populated Places (countries, subregion1, subregion2)')
            with tag('h2'):
                text('Countries:')
            text('(analysis of the top 100 most populated countries)')
            doc.asis(grouped_places['countries'].drop(['rate_mortality_%', 'total_deceased', 'rate_mortality_by_infected_%'], axis=1).to_html())
            with tag('h2'):
                text('Subregion1 (states, provinces, etc):')
            text('(analysis of the top 1000 most populated regions)')
            doc.asis(grouped_places['sub1'].drop(['rate_mortality_%', 'total_deceased', 'rate_mortality_by_infected_%'], axis=1).to_html())
            with tag('h2'):
                text('Subregion2 (usually cities):')
            text('(analysis of the top 1000 most populated regions)')
            doc.asis(grouped_places['sub2'].drop(['rate_mortality_%', 'total_deceased', 'rate_mortality_by_infected_%'], axis=1).to_html())

    with open('./site/highest_infection_rates_in_highly_populate_places.html', 'w', encoding='utf-8') as writer:
        writer.write(doc.getvalue())

    # now mortality
    for key, place in places.items():
        grouped_places[key].sort_values('rate_mortality_%', inplace=True, ascending=False)
        grouped_places[key]['position'] = np.arange(len(grouped_places[key])) + 1

    doc, tag, text = Doc().tagtext()

    doc.asis('<?xml version="1.0" encoding="UTF-8"?>')

    with tag('html'):
        with tag('body'):
            with tag('h1'):
                text('Highest Mortality Rates In Highly Populated Places (countries, subregion1, subregion2)')
            with tag('h2'):
                text('Countries:')
            text('(analysis of the top 100 most populated countries)')
            doc.asis(grouped_places['countries'].drop(['rate_infected_%', 'total_confirmed', 'rate_mortality_by_infected_%'], axis=1).to_html())
            with tag('h2'):
                text('Subregion1 (states, provinces, etc):')
            text('(analysis of the top 1000 most populated regions)')
            doc.asis(grouped_places['sub1'].drop(['rate_infected_%', 'total_confirmed', 'rate_mortality_by_infected_%'], axis=1).to_html())
            with tag('h2'):
                text('Subregion2 (usually cities):')
            text('(analysis of the top 1000 most populated regions)')
            doc.asis(grouped_places['sub2'].drop(['rate_infected_%', 'total_confirmed', 'rate_mortality_by_infected_%'], axis=1).to_html())

    with open('./site/highest_mortality_rates_in_highly_populate_places.html', 'w', encoding='utf-8') as writer:
        writer.write(doc.getvalue())

    # now mortality by infections
    for key, place in places.items():
        grouped_places[key].sort_values('rate_mortality_by_infected_%', inplace=True, ascending=False)
        grouped_places[key]['position'] = np.arange(len(grouped_places[key])) + 1

    doc, tag, text = Doc().tagtext()

    doc.asis('<?xml version="1.0" encoding="UTF-8"?>')

    with tag('html'):
        with tag('body'):
            with tag('h1'):
                text('Highest Mortality By Infection Rate In Highly Populated Places (countries, subregion1, subregion2)')
            with tag('h2'):
                text('Countries:')
            text('(analysis of the top 100 most populated countries)')
            doc.asis(grouped_places['countries'].drop(['rate_infected_%', 'rate_mortality_%'], axis=1).to_html())
            with tag('h2'):
                text('Subregion1 (states, provinces, etc):')
            text('(analysis of the top 1000 most populated regions)')
            doc.asis(grouped_places['sub1'].drop(['rate_infected_%', 'rate_mortality_%'], axis=1).to_html())
            with tag('h2'):
                text('Subregion2 (usually cities):')
            text('(analysis of the top 1000 most populated regions)')
            doc.asis(grouped_places['sub2'].drop(['rate_infected_%', 'rate_mortality_%'], axis=1).to_html())

    with open('./site/highest_mortality_by_infected_rate_in_highly_populate_places.html', 'w', encoding='utf-8') as writer:
        writer.write(doc.getvalue())

    return grouped_places


def generate_report_distribution_highest_infection_rates_in_highly_populate_places(grouped_places):

    fig = make_subplots(rows=3, cols=1, subplot_titles=['Distribution of infection rates for countries with highest cases',
                                                        'Distribution of infection rates for subregion1\'s with highest cases',
                                                        'Distribution of infection rates for subregion2\'s with highest cases'])

    countries_rate_infected = grouped_places['countries']['rate_infected_%']
    sub1_rate_infected = grouped_places['sub1']['rate_infected_%']
    sub2_rate_infected = grouped_places['sub2']['rate_infected_%']

    fig.add_trace(go.Histogram(x=countries_rate_infected, xbins=dict(
        start=countries_rate_infected.min(),
        end=countries_rate_infected.max(),
        size=0.25
    ),), row=1, col=1)

    fig.add_trace(go.Histogram(x=sub1_rate_infected, xbins=dict(
        start=sub1_rate_infected.min(),
        end=sub1_rate_infected.max(),
        size=0.25
    ),), row=2, col=1)

    fig.add_trace(go.Histogram(x=sub2_rate_infected, xbins=dict(
        start=sub2_rate_infected.min(),
        end=sub2_rate_infected.max(),
        size=0.25
    ),), row=3, col=1)

    fig.write_html('./site/distribution_of_highest_infection_rates_in_highly_populate_places.html')


def generate_report_vaccination_coverage(places):

    plotable_places = {}
    figs = []

    for place_key, value in places.items():
        # last month only
        place = places[place_key].loc[places[place_key].date > datetime.datetime.now() - pd.to_timedelta(str(30) + 'day')]

        place.dropna(subset=['total_vaccine_doses_administered'], inplace=True)

        if 'population_age_10_19' not in place or place['population_age_10_19'].isnull().all() or 'population_age_30_39' not in place or place['population_age_30_39'].isnull().all():
            continue
        else:
            plotable_places[place_key] = value

    for place_key, value in plotable_places.items():

        fig = make_subplots(rows=1, cols=1, subplot_titles=[place_key])

        # last month only
        place = places[place_key].loc[places[place_key].date > datetime.datetime.now() - pd.to_timedelta(str(30) + 'day')]

        place.dropna(subset=['total_vaccine_doses_administered'], inplace=True)

        if 'total_vaccine_doses_administered_janssen' not in place:
            total_vaccine_doses_administered_janssen = 0
        else:
            total_vaccine_doses_administered_janssen = place['total_vaccine_doses_administered_janssen'].fillna(0)

        days_ordinal = place['date'].map(datetime.datetime.toordinal).values.reshape(-1, 1)
        total_vaccines = (place['total_vaccine_doses_administered'] + total_vaccine_doses_administered_janssen).values.reshape(-1, 1)

        population_above_10 = (int(place['population_age_10_19'].iloc[-1]) +  int(place['population_age_20_29'].iloc[-1]) +
                               int(place['population_age_30_39'].iloc[-1]) + int(place['population_age_40_49'].iloc[-1]) + int(place['population_age_50_59'].iloc[-1]) +
                               int(place['population_age_60_69'].iloc[-1]) + int(place['population_age_70_79'].iloc[-1]) + int(place['population_age_80_and_older'].iloc[-1]))

        population = population_above_10

        population_coverage_milestones = [0, (population * 0.1), (population * 0.2), (population * 0.3), (population * 0.4), (population * 0.5), (population * 0.6), (population * 0.7), (population * 0.8), (population * 0.9), population]
        population_coverage_milestones_labels = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']

        total_persons_vaccinated = place['total_persons_vaccinated'].values.reshape(-1, 1)
        total_persons_fully_vaccinated = place['total_persons_fully_vaccinated'].values.reshape(-1, 1)

        # predicting vaccination for 2 doses
        linear_regressor = LinearRegression()
        linear_regressor.fit(days_ordinal, (total_vaccines/2))

        total_vaccines_prediction = linear_regressor.predict(days_ordinal)

        predicted_dates, predicted_dates_ordinal = predict_date_based_on_vaccines(linear_regressor, population_coverage_milestones)

        # what we know (points)
        fig.add_scatter(
            x=days_ordinal.flatten().tolist(),
            y=total_vaccines.flatten().tolist(),
            mode='markers',
            name='Total Vaccines Administered',
            marker_color='black',
            showlegend=True,
        )

        # predictions (points)
        fig.add_scatter(
            x=predicted_dates_ordinal,
            y=population_coverage_milestones,
            mode='text',
            showlegend=False,
            marker_color='red',
            textposition='top center',
            text=population_coverage_milestones_labels,
        )

        # prediction line
        fig.add_trace(
            go.Scatter(x=days_ordinal.flatten().tolist() + predicted_dates_ordinal,
                       y=total_vaccines_prediction.flatten().tolist() + population_coverage_milestones,
                       mode='lines',
                       name='Full vaccination prediction for population above 10',
                       marker_color='blue',
                       showlegend=True),
        )

        fig.add_trace(
            go.Scatter(x=days_ordinal.flatten().tolist(),
                       y=total_persons_fully_vaccinated.flatten().tolist(),
                       name='Total Persons Fully Vaccinated',
                       mode="lines",
                       showlegend=True),
        )

        fig.add_trace(
            go.Scatter(x=days_ordinal.flatten().tolist(),
                       y=total_persons_vaccinated.flatten().tolist(),
                       name='Total Persons Vaccinated',
                       mode="lines",showlegend=True),
        )


        # replacing x labels
        fig.update_layout(
            xaxis={
                'tickmode': 'array',
                'tickvals': days_ordinal.flatten().tolist() + predicted_dates_ordinal,
                'ticktext': [item.strftime('%d %b') if item else '' for item in ['' for i in place['date'].tolist()] + predicted_dates],
            },
        )

        figs.append(fig)

    css = """
    <style>
        .legendtoggle {
            display: none;
        }
    </style>
    """

    index = 0
    with open('./site/vaccination_coverage_forecast.html', 'w') as f:
        for fig in figs:
            if index == 0:
                fig.update_layout(title_text='Vaccination Coverage/Forecast For Population Age 10 And Older')
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
            index += 1
        f.write(css)
        f.write('</body></html>')


if __name__ == "__main__" :
    places = get_places()

    generate_report_new_cases_per_day(places, days=30)
    generate_report_new_cases_per_day(places, days=90)
    generate_report_new_cases_per_day(places, days=180)
    generate_report_new_cases_per_day(places, days=999)

    generate_report_new_cases_percentage_of_population_infected_per_day(places, days=30)
    generate_report_new_cases_percentage_of_population_infected_per_day(places, days=90)
    generate_report_new_cases_percentage_of_population_infected_per_day(places, days=180)
    generate_report_new_cases_percentage_of_population_infected_per_day(places, days=999)

    generate_report_percentage_of_population_deceased_per_day(places, days=30)
    generate_report_percentage_of_population_deceased_per_day(places, days=90)
    generate_report_percentage_of_population_deceased_per_day(places, days=180)
    generate_report_percentage_of_population_deceased_per_day(places, days=999)

    generate_report_total_and_percentage_deceased(places)

    generate_report_percentage_of_population_infected(places)

    grouped_places = generate_ranking_reports()
    generate_report_distribution_highest_infection_rates_in_highly_populate_places(grouped_places)

    generate_report_last_report_cases_in_a_day(places)

    generate_report_vaccination_coverage(places)

