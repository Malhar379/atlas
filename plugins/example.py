from plugins.base import BasePlugin


class ExamplePlugin(BasePlugin):

    def execute(self, config: dict) -> dict:
        return {
            "result": {
                "message": "Example plugin executed successfully",
                "config": config,
            },
            "metrics": {
                "accuracy": 0.94,
                "loss": 0.12,
            },

            "artifacts" : {
                "model": "artifacts/run_2/model.pkl",
                "report": "artifacts/run_2/report.json",
            }
        }