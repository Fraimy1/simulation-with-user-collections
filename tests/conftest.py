import random

import pytest


@pytest.fixture(autouse=True)
def reset_random_seed():
    random.seed(33)
    yield
    random.seed()

