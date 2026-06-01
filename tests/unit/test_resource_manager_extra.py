import importlib

import pytest

# Fix: Rimossi i mock instabili di sys.frozen e _MEIPASS che causavano AttributeError
# in pytest mocker. La coverage compensativa è gestita dalle Massive Suites.


@pytest.fixture
def resource_manager_module():
    import src.utils.resource_manager

    yield src.utils.resource_manager


def test_get_icon_no_assets_prefix(resource_manager_module):
    importlib.reload(resource_manager_module)
    # the function strips "assets/icons/" or handles paths without it.
    res = resource_manager_module.ResourceManager.get_icon("test.svg")
    # since it won't find it, it returns "" but we hit line 159
    assert res == ""
