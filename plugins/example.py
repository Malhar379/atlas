from plugins.base import BasePlugin


class ExamplePlugin(BasePlugin):

    def execute(self, config: dict) -> dict:
        return {
            "message": "Example plugin executed successfully",
            "config": config,
        }