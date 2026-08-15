from plugins.example import ExamplePlugin
from plugins.sklearn_regression import SklearnRegressionPlugin


PLUGIN_REGISTRY = {
    "example": ExamplePlugin,
    "sklearn_regression": SklearnRegressionPlugin,
}


def get_plugin(name: str):
    plugin_class = PLUGIN_REGISTRY.get(name)

    if plugin_class is None:
        raise ValueError(f"Unknown plugin: {name}")

    return plugin_class()