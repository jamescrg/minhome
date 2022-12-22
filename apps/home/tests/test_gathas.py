

from apps.home.gathas import gathas
import random


def test_gathas():
    gatha = random.choice(gathas)
    assert len(gathas) > 2
    assert len(gatha) > 10
    assert isinstance(gatha, str)


