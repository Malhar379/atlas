import os
import pickle

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from plugins.base import BasePlugin


class SklearnRegressionPlugin(BasePlugin):

    def execute(self, config: dict) -> dict:
        test_size = config.get("test_size", 0.2)
        random_state = config.get("random_state", 42)

        # Small built-in dataset
        X = [
            [1],
            [2],
            [3],
            [4],
            [5],
            [6],
            [7],
            [8],
            [9],
            [10],
        ]

        y = [
            3,
            5,
            7,
            9,
            11,
            13,
            15,
            17,
            19,
            21,
        ]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        # Temporary artifact location
        os.makedirs("artifacts", exist_ok=True)

        artifact_path = "artifacts/model.pkl"

        with open(artifact_path, "wb") as file:
            pickle.dump(model, file)

        return {
            "result": {
                "model": "LinearRegression",
            },
            "metrics": {
                "mse": float(mse),
                "r2": float(r2),
            },
            "artifacts": {
                "model": artifact_path,
            },
        }