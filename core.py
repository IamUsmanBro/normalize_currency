import re
import json
import os
from forex_python.converter import CurrencyRates

# Load currency mapping data
data_path = os.path.join(os.path.dirname(__file__), "currency_data.json")
with open(data_path, "r") as f:
    currency_data = json.load(f)

symbol_to_code = currency_data.get("symbol_to_code", {})
currency_codes = currency_data.get("all_currency_codes", {})

def extract_currency_and_amount(value):
    value = str(value).lower().strip()
    value = re.sub(r'[\s]', '', value)

    for symbol, code in symbol_to_code.items():
        if symbol in value:
            amount = re.sub(r'[^\d\.]+', '', value)
            return code, float(amount) if amount else None

    for code in currency_codes.keys():
        if code.lower() in value:
            amount = re.sub(r'[^\d\.]+', '', value)
            return code, float(amount) if amount else None

    return None, None

def normalize_currency_series(series, to='USD'):
    cr = CurrencyRates()
    result = []

    for val in series:
        code, amount = extract_currency_and_amount(val)
        if code and amount:
            try:
                converted = cr.convert(code, to, amount)
                result.append(round(converted, 2))
            except:
                result.append(None)
        else:
            result.append(None)

    return series.__class__(result, index=series.index)