from __future__ import annotations

import json
import os
from collections.abc import Iterable
from pathlib import Path

import numpy as np
from flwr.app import ArrayRecord, Context, Message
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg

from darius_demo.schema import CLASS_LABELS, FEATURE_NAMES

from .common import ROOT


class EvidenceFedAvg(FedAvg):
    """FedAvg which records how many train replies succeeded in each round."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.last_round = 0
        self.accepted_clients = 0
        self.failures = 0

    def aggregate_train(
        self,
        server_round: int,
        replies: Iterable[Message],
    ):
        reply_list = list(replies)
        self.last_round = server_round
        self.accepted_clients = sum(message.has_content() for message in reply_list)
        self.failures = sum(message.has_error() for message in reply_list)
        return super().aggregate_train(server_round, reply_list)


app = ServerApp()


@app.main()
def main(grid: Grid, context: Context) -> None:
    rounds = int(context.run_config["num-server-rounds"])
    initial_arrays = ArrayRecord(
        [
            np.zeros(
                (len(FEATURE_NAMES), len(CLASS_LABELS)),
                dtype=np.float64,
            ),
            np.zeros(len(CLASS_LABELS), dtype=np.float64),
        ]
    )
    strategy = EvidenceFedAvg(
        fraction_train=1.0,
        fraction_evaluate=1.0,
        min_train_nodes=3,
        min_evaluate_nodes=3,
        min_available_nodes=3,
    )

    result = strategy.start(
        grid=grid,
        initial_arrays=initial_arrays,
        num_rounds=rounds,
    )
    arrays = result.arrays.to_numpy_ndarrays()
    evidence_root = Path(os.environ.get("DARIUS_DEMO_ROOT", ROOT))
    output = evidence_root / "evidence" / "flower_network_result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "round": strategy.last_round,
                "synthetic_only": True,
                "accepted_clients": strategy.accepted_clients,
                "failures": strategy.failures,
                "weights_shape": list(arrays[0].shape),
                "bias_shape": list(arrays[1].shape),
                "flower_runtime": "SuperLink/SuperNode",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
