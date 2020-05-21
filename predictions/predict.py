import json
import pandas as pd
# import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
from celery import shared_task
from predictions.models import Prediction


@shared_task
def forecast_timeseries(prediction_id):
    prediction = Prediction.objects.get(pk=prediction_id)

    df = create_dataframe_from_csv(prediction.data, prediction.frequency)

    results = auto_arima(
        df['data'], seasonal=True, m=prediction.seasonal_period,
        trace=True,  # just for testing
        maxiter=1,  # just for testing
        error_action='ignore',   # we don't want to know if an order does not work
        suppress_warnings=True,  # we don't want convergence warnings
        stepwise=True)

    model = SARIMAX(df['data'], order=results.order, seasonal_order=results.seasonal_order)
    result = model.fit()
    fcast = result.predict(
        len(df), len(df) + prediction.forecast_periods, typ='levels')

    # print(result.summary())
    print(fcast.to_json(orient='split', date_format='iso'))
    prediction.result = json.loads(fcast.to_json(orient='split', date_format='iso'))
    prediction.save()

    # print(json.loads(prediction.result))
    # self.update_state(state='PROGRESS',
    #             meta={'current': i, 'total': len(filenames)})

    return prediction.id


def create_dataframe_from_csv(csv_file, frequency):
    "Create and format dataframe from a csv file"

    df = pd.read_csv(csv_file, index_col='index', parse_dates=True)
    df.dropna()
    df.index.freq = frequency
    df = df.resample(rule=frequency)
    df = df.interpolate(method='polynomial', order=2)
    return df
