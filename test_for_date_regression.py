import numpy as np
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots
import plotly.graph_objects as go

today = datetime.date.today()

data = {
    'Dates': [today - datetime.timedelta(days=10), today - datetime.timedelta(days=5),
              today - datetime.timedelta(days=3), today - datetime.timedelta(days=2),
              today - datetime.timedelta(days=1)],
    'Vaccines': [10, 20, 80, 85, 85]
}

df = pd.DataFrame(data=data)

days_ordinal = df['Dates'].map(datetime.datetime.toordinal)

x = days_ordinal.values.reshape(-1, 1)
y = df['Vaccines'].values.reshape(-1, 1)

linear_regressor = LinearRegression()
linear_regressor.fit(x, y)

y_pred = linear_regressor.predict(x)

#TODO predict points


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


# prediction line # TODO ? MAX MIN X Y to reduce to 2 points? points = predictions + known appended
fig.add_trace(
    go.Scatter(x=x.flatten().tolist(),
               y=y_pred.flatten().tolist(),
               mode="lines",
               showlegend=False)
)

# replacing x labels
fig.update_layout(
    xaxis={
        'tickmode': 'array',
        'tickvals': x.flatten().tolist(),
        'ticktext': [item.strftime('%d %b') for item in df['Dates'].to_list()], #x to date string?
    },
)

fig.add_scatter(
    x=[737943],
    y=[80],
    mode='markers+text',
    textposition='top center',
    showlegend=False,
    marker_color='red',
    text='My label'
)

# 20, 30, 40, 50, 60, 70, 80, 90, 100 fully
# predict them, add them to x

fig.show()

# plt.scatter(x, y)
# plt.xticks(x, [item.strftime('%d %b') for item in df['Dates'].to_list()])
# plt.plot(x, y_pred, color='red')
# plt.show()


# one day after
linear_regressor.predict([[737941]])
