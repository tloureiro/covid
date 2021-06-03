import numpy as np
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def predict_date_based_on_vaccines(linear_regressor, future_vaccine_quantities):
    dates = []
    dates_ordinal = []

    for future_vaccine_quantity in future_vaccine_quantities:
        predicted_date = (future_vaccine_quantity - linear_regressor.intercept_) / linear_regressor.coef_
        dates_ordinal.append(round(predicted_date[0][0]))
        dates.append(datetime.datetime.fromordinal(round(predicted_date[0][0])))
    return dates, dates_ordinal


today = datetime.date.today()

data = {
    'Dates': [today - datetime.timedelta(days=10), today - datetime.timedelta(days=5),
              today - datetime.timedelta(days=3), today - datetime.timedelta(days=2),
              today - datetime.timedelta(days=1)],
    'Vaccines': [10, 20, 80, 85, 85]
}
future_vaccine_quantities = [200, 500, 700]
future_vaccine_quantities_labels = ['10%', '20%', '30%']

df = pd.read_feather('./data/main.feather')


# df = pd.DataFrame(data=data)

days_ordinal = df['Dates'].map(datetime.datetime.toordinal)

x = days_ordinal.values.reshape(-1, 1)
y = df['Vaccines'].values.reshape(-1, 1)

linear_regressor = LinearRegression()
linear_regressor.fit(x, y)

y_pred = linear_regressor.predict(x)

predicted_dates, predicted_dates_ordinal = predict_date_based_on_vaccines(linear_regressor, future_vaccine_quantities)

fig = make_subplots(rows=1, cols=1, subplot_titles='Test')

# what we know (points)
fig.add_scatter(
    x=x.flatten().tolist(),
    y=y.flatten().tolist(),
    mode='markers',
    showlegend=False,
    marker_color='black'
)

# predictions (points)
fig.add_scatter(
    x=predicted_dates_ordinal,
    y=future_vaccine_quantities,
    mode='markers+text',
    showlegend=False,
    marker_color='red',
    textposition='top center',
    text=future_vaccine_quantities_labels
)

# prediction line # TODO ? MAX MIN X Y to reduce to 2 points? points = predictions + known appended
fig.add_trace(
    go.Scatter(x=x.flatten().tolist() + predicted_dates_ordinal,
               y=y_pred.flatten().tolist() + future_vaccine_quantities,
               mode="lines",
               showlegend=False)
)

# replacing x labels
fig.update_layout(
    xaxis={
        'tickmode': 'array',
        'tickvals': x.flatten().tolist() + predicted_dates_ordinal,
        'ticktext': [item.strftime('%d %b') for item in df['Dates'].to_list() + predicted_dates],
    },
)

fig.show()
