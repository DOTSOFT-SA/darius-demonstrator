from __future__ import annotations

import json
from pathlib import Path

from flwr.app import ArrayRecord, Context, Message, MetricRecord, RecordDict
from flwr.clientapp import ClientApp

from darius_demo.model import accuracy
from darius_demo.synthetic import CITY_RULES

from .common import ROOT, load_city, train_parameters


app = ClientApp()


def load_client_data(context: Context):
    city = str(context.node_config["city"])
    if city not in CITY_RULES:
        raise ValueError(f"Unknown synthetic city in node config: {city}")

    model_path = (
        ROOT
        / "browser-edge-client"
        / "public"
        / "models"
        / "synthetic_softmax.json"
    )
    model = json.loads(model_path.read_text(encoding="utf-8"))
    means = model["scaler_mean"]
    scales = model["scaler_scale"]
    train_x, train_y = load_city(city, "train", means, scales)
    val_x, val_y = load_city(city, "val", means, scales)
    return city, train_x, train_y, val_x, val_y


@app.train()
def train(message: Message, context: Context) -> Message:
    _, train_x, train_y, _, _ = load_client_data(context)
    parameters = message.content["arrays"].to_numpy_ndarrays()
    updated = train_parameters(parameters, train_x, train_y)
    content = RecordDict(
        {
            "arrays": ArrayRecord(updated),
            "metrics": MetricRecord(
                {
                    "num-examples": len(train_y),
                }
            ),
        }
    )
    return Message(content=content, reply_to=message)


@app.evaluate()
def evaluate(message: Message, context: Context) -> Message:
    _, _, _, val_x, val_y = load_client_data(context)
    parameters = message.content["arrays"].to_numpy_ndarrays()
    weights = parameters[0].astype(float).tolist()
    bias = parameters[1].astype(float).tolist()
    value = accuracy(val_x, val_y, weights, bias)
    content = RecordDict(
        {
            "metrics": MetricRecord(
                {
                    "loss": 1.0 - value,
                    "accuracy": value,
                    "num-examples": len(val_y),
                }
            )
        }
    )
    return Message(content=content, reply_to=message)
