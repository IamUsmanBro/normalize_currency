import pandas as pd
from .core import normalize_currency_series

@pd.api.extensions.register_series_accessor("currency")
class CurrencyAccessor:
    def __init__(self, pandas_series):
        self._series = pandas_series

    def normalize(self, to='USD'):
        return normalize_currency_series(self._series, to)