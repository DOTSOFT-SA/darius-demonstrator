from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CITIES = (
    "synthetic_city_alpha",
    "synthetic_city_beta",
    "synthetic_city_gamma",
)


def port_is_open(host: str, port: int, timeout: float = 0.3) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def stream_output(process: subprocess.Popen[str], prefix: str) -> None:
    assert process.stdout is not None
    for line in process.stdout:
        print(f"[{prefix}] {line}", end="", flush=True)


def stop_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def start_process(
    arguments: list[str],
    prefix: str,
    environment: dict[str, str],
) -> tuple[subprocess.Popen[str], threading.Thread]:
    process = subprocess.Popen(
        arguments,
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    thread = threading.Thread(
        target=stream_output,
        args=(process, prefix),
        daemon=True,
    )
    thread.start()
    return process, thread


def wait_for_port(
    process: subprocess.Popen[str],
    host: str,
    port: int,
    label: str,
    timeout: float,
) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"{label} exited early with code {process.returncode}.")
        if port_is_open(host, port):
            return
        time.sleep(0.2)
    raise TimeoutError(f"{label} did not listen on {host}:{port} within {timeout:g} seconds.")


def wait_for_run(process: subprocess.Popen[str], timeout: float) -> None:
    try:
        exit_code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise TimeoutError(
            f"Flower run did not complete within {timeout:g} seconds."
        ) from error
    if exit_code != 0:
        raise RuntimeError(f"`flwr run` failed with exit code {exit_code}.")


def write_flower_config(runtime_home: Path, control_address: str) -> None:
    runtime_home.mkdir(parents=True, exist_ok=True)
    (runtime_home / "config.toml").write_text(
        "[superlink]\n"
        'default = "darius-local"\n\n'
        "[superlink.darius-local]\n"
        f'address = "{control_address}"\n'
        "insecure = true\n",
        encoding="utf-8",
    )


def validate_result(rounds: int) -> dict[str, object]:
    result_path = ROOT / "evidence" / "flower_network_result.json"
    if not result_path.is_file():
        raise RuntimeError(f"Flower result was not created: {result_path}")
    result = json.loads(result_path.read_text(encoding="utf-8"))
    expected = {
        "round": rounds,
        "accepted_clients": len(CITIES),
        "failures": 0,
        "weights_shape": [24, 3],
        "bias_shape": [3],
        "synthetic_only": True,
        "flower_runtime": "SuperLink/SuperNode",
    }
    mismatches = {
        key: {"expected": value, "actual": result.get(key)}
        for key, value in expected.items()
        if result.get(key) != value
    }
    if mismatches:
        raise RuntimeError(f"Flower result validation failed: {mismatches}")
    return result


def require_command(name: str) -> str:
    command = shutil.which(name)
    if command is None:
        raise SystemExit(
            f"Required command `{name}` was not found. Install dependencies with "
            "`python -m pip install -r flower-federated-learning/requirements.txt`."
        )
    return command


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    parser = argparse.ArgumentParser(
        description=(
            "Run the DARIUS Flower App on one SuperLink and three SuperNodes."
        )
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument(
        "--base-port",
        type=int,
        default=9091,
        help="First of six consecutive ports used by the local Flower runtime.",
    )
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--startup-timeout", type=float, default=30.0)
    parser.add_argument("--workflow-timeout", type=float, default=180.0)
    args = parser.parse_args()

    if args.rounds <= 0:
        raise SystemExit("--rounds must be positive.")
    if not 1 <= args.base_port <= 65530:
        raise SystemExit("--base-port must be between 1 and 65530.")

    ports = list(range(args.base_port, args.base_port + 6))
    busy_ports = [port for port in ports if port_is_open(args.host, port)]
    if busy_ports:
        raise SystemExit(
            f"Required local ports are already in use: {busy_ports}. Stop the old "
            "Flower processes with Ctrl+C or choose another --base-port."
        )

    superlink_command = require_command("flower-superlink")
    supernode_command = require_command("flower-supernode")
    flwr_command = require_command("flwr")

    serverapp_port, fleet_port, control_port = ports[:3]
    clientapp_ports = ports[3:]
    runtime_home = ROOT / ".flower-runtime"
    write_flower_config(runtime_home, f"{args.host}:{control_port}")
    runtime_temp = runtime_home / "tmp"
    runtime_temp.mkdir(parents=True, exist_ok=True)
    result_path = ROOT / "evidence" / "flower_network_result.json"
    if result_path.exists():
        result_path.unlink()

    environment = os.environ.copy()
    environment["PYTHONUNBUFFERED"] = "1"
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["FLWR_HOME"] = str(runtime_home)
    environment["DARIUS_DEMO_ROOT"] = str(ROOT)
    environment["TEMP"] = str(runtime_temp)
    environment["TMP"] = str(runtime_temp)

    print(
        f"Starting Flower deployment runtime for {args.rounds} rounds: "
        f"1 SuperLink and {len(CITIES)} SuperNodes.",
        flush=True,
    )

    infrastructure: list[subprocess.Popen[str]] = []
    threads: list[threading.Thread] = []
    run_process: subprocess.Popen[str] | None = None
    try:
        superlink, thread = start_process(
            [
                superlink_command,
                "--insecure",
                "--disable-runtime-dependency-installation",
                "--serverappio-api-address",
                f"{args.host}:{serverapp_port}",
                "--fleet-api-address",
                f"{args.host}:{fleet_port}",
                "--control-api-address",
                f"{args.host}:{control_port}",
            ],
            "superlink",
            environment,
        )
        infrastructure.append(superlink)
        threads.append(thread)
        wait_for_port(
            superlink,
            args.host,
            control_port,
            "Flower SuperLink",
            args.startup_timeout,
        )

        for city, clientapp_port in zip(CITIES, clientapp_ports, strict=True):
            supernode, thread = start_process(
                [
                    supernode_command,
                    "--insecure",
                    "--superlink",
                    f"{args.host}:{fleet_port}",
                    "--clientappio-api-address",
                    f"{args.host}:{clientapp_port}",
                    "--node-config",
                    f'city="{city}"',
                ],
                city,
                environment,
            )
            infrastructure.append(supernode)
            threads.append(thread)
            wait_for_port(
                supernode,
                args.host,
                clientapp_port,
                f"SuperNode {city}",
                args.startup_timeout,
            )

        run_process, thread = start_process(
            [
                flwr_command,
                "run",
                ".",
                "darius-local",
                "--stream",
                "--run-config",
                f"num-server-rounds={args.rounds}",
            ],
            "flwr-run",
            environment,
        )
        threads.append(thread)
        wait_for_run(run_process, args.workflow_timeout)
        thread.join(timeout=2)
        result = validate_result(args.rounds)
    except KeyboardInterrupt:
        print("\nInterrupted; stopping Flower processes.", flush=True)
        raise SystemExit(130)
    finally:
        if run_process is not None:
            stop_process(run_process)
        for process in reversed(infrastructure):
            stop_process(process)
        for thread in threads:
            thread.join(timeout=1)

    print("\nFLOWER DEMO COMPLETE", flush=True)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
