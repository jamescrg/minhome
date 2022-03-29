
import pytest
import json
from pathlib import Path

import apps.finance.crypto_data as crypto_data
import apps.finance.tests.sample_crypto_data as sample_data


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def data():
    data = sample_data.sample_data
    return json.loads(data)


# ---------------------------------------------------------------------------
# tests
# ---------------------------------------------------------------------------

def test_crypto_fetch():
    symbols = 'ALGO,ETH,ATOM,MATIC,BTC'
    data = crypto_data.fetch(symbols)
    assert data['BTC']
    assert data['BTC']['quote']['USD']['market_cap'] > 0
    assert data['MATIC']['quote']['USD']['price'] > 0


def test_crypto_condense(data):
    condensed_data = crypto_data.condense(data)
    assert 'BTC' in condensed_data
    assert 'symbol' in condensed_data['BTC']
    assert 'name' in condensed_data['BTC']


def test_crypto_sort(data):
    condensed_data = crypto_data.condense(data)
    sorted_data = crypto_data.sort(condensed_data)
    assert sorted_data[0]['symbol'] == 'BTC'
    sorted_data = crypto_data.sort(condensed_data, 'symbol')
    assert sorted_data[2]['symbol'] == 'ETH'

