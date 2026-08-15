import pytest

from plugins.example import ExamplePlugin
from plugins.registry import get_plugin


def test_get_example_plugin():
    plugin = get_plugin("example")

    assert isinstance(plugin, ExamplePlugin)


def test_unknown_plugin():
    with pytest.raises(ValueError):
        get_plugin("does_not_exist")


def test_example_plugin_execution():
    plugin = get_plugin("example")

    result = plugin.execute({
        "epochs": 10,
        "learning_rate": 0.01,
    })

    assert result["result"]["message"] == "Example plugin executed successfully"
    assert result["result"]["config"]["epochs"] == 10
    assert result["metrics"]["accuracy"] == 0.94
    assert result["metrics"]["loss"] == 0.12
    assert "artifacts" in result