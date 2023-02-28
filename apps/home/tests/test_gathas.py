import random

from apps.home.gathas import gathas


def test_gathas():
    gatha = random.choice(gathas)
    assert len(gathas) > 2
    assert len(gatha) > 10
    assert isinstance(gatha, str)
