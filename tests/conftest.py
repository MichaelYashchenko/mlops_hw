import pytest


@pytest.fixture
def empty_call():
    def _call(*args, **kwargs):
        pass
    return _call
