import numpy as np
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from generate_html_reports import get_places


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


def generate_report_vaccination_coverage(places):

    plotable_places = {}
    figs = []

    for place_key, value in places.items():
        # last month only
        place = places[place_key].loc[places[place_key].date > datetime.datetime.now() - pd.to_timedelta(str(30) + 'day')]

        place.dropna(subset=['total_vaccine_doses_administered'], inplace=True)

        if 'population_age_10_19' not in place or place['population_age_10_19'].isnull().all():
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


generate_report_vaccination_coverage(get_places())