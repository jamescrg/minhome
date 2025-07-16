import requests
from django.conf import settings
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def collect(symbols):
    """Fetch the data for each asset from the coinmarketcap api.

    Args:
        symbols (str): a string of crypto symbols

    Returns:
        result (list): a list of assets and their associated data

    """

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {
        "symbol": symbols,
        "convert": "USD",
        "CMC_PRO_API_KEY": settings.CRYPTO_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        result = response.json()["data"]

    except (ConnectionError, Timeout, TooManyRedirects):
        result = None

    return result


def condense(data):
    """Extract the most relevant data into a smaller dict.

    Args:
        data(list): crypto data from the "collect" function

    Returns:
        condensed_data(dict): reorganized data with relevant data points extracted

    Notes:
        This includes the name of the symbol in the dict data

    """

    condensed_data = {}
    for key, val in data.items():
        condensed_data[key] = data[key]["quote"]["USD"]
        condensed_data[key]["symbol"] = key
        condensed_data[key]["name"] = data[key]["name"]
        condensed_data[key]["slug"] = data[key]["slug"]
        condensed_data[key]["market_cap"] = (
            condensed_data[key]["market_cap"] / 1000000000
        )

    return condensed_data


def sort(data, ord="market_cap"):
    """Convert the dict to a list and sort the list according to the chosen field.

    Args:
        data (list): the list of assets produced by the "collect" function
        ord (str): the user's preferred sort order

    Returns:
        sorted_data (list): a list of assets, sorted

    """

    # convert to a list of dicts
    sequential_data = []
    for key in data.keys():
        sequential_data.append(data[key])

    if ord == "name" or ord == "symbol":
        reverse_value = False
    else:
        reverse_value = True

    # sort list of dicts by common key
    sorted_data = sorted(sequential_data, key=lambda k: k[ord], reverse=reverse_value)

    return sorted_data
