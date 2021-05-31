import numpy as np
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

today = datetime.date.today()

data = {
    'Days': [today - datetime.timedelta(days=5), today - datetime.timedelta(days=4), today - datetime.timedelta(days=3), today - datetime.timedelta(days=2), today - datetime.timedelta(days=1)],
    'Cases': [10, 20, 80, 85, 85]
}

df = pd.DataFrame(data=data)

df['Days'] = df['Days'].map(datetime.datetime.toordinal)

x = df['Days'].values.reshape(-1, 1)
y = df['Cases'].values.reshape(-1, 1)

linear_regressor = LinearRegression()
linear_regressor.fit(x, y)
#
y_pred = linear_regressor.predict(x)

plt.scatter(x, y)
plt.plot(x, y_pred, color='red')
plt.show()

#one day after
linear_regressor.predict([[737941]])
