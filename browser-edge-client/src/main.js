import * as ort from "onnxruntime-web";
import ortMjsUrl from "../node_modules/onnxruntime-web/dist/ort-wasm-simd-threaded.jsep.mjs?url";
import ortWasmUrl from "../node_modules/onnxruntime-web/dist/ort-wasm-simd-threaded.jsep.wasm?url";
import { boundedWhatIf, inferJson } from "./inference.js";

const slider = document.querySelector("#delta");
const output = document.querySelector("#delta-value");
const runButton = document.querySelector("#run");
const jsonResult = document.querySelector("#json-result");
const onnxResult = document.querySelector("#onnx-result");
const parity = document.querySelector("#parity");
let model;
let session;

slider.addEventListener("input", () => { output.value = `${slider.value}%`; });

runButton.addEventListener("click", async () => {
  if (!model) return;
  runButton.disabled = true;
  const input = boundedWhatIf(model.example_input, slider.value);
  const json = inferJson(input, model);
  jsonResult.textContent = JSON.stringify({ label: json.label, probabilities: json.probabilities.map((v) => Number(v.toFixed(6))) }, null, 2);

  if (!session) {
    onnxResult.textContent = "ONNX runtime is unavailable. JSON inference still completed locally.";
    parity.textContent = "JSON inference: PASS · ONNX parity unavailable; see the startup error above.";
    runButton.disabled = false;
    return;
  }

  const tensor = new ort.Tensor("float32", Float32Array.from(json.scaled), [1, model.feature_names.length]);
  try {
    const onnxOutput = await session.run({ features: tensor });
    const probabilities = Array.from(onnxOutput.probabilities.data);
    const onnxClass = probabilities.indexOf(Math.max(...probabilities));
    onnxResult.textContent = JSON.stringify({ label: model.classes[onnxClass], probabilities: probabilities.map((v) => Number(v.toFixed(6))) }, null, 2);
    const maximumDifference = Math.max(...probabilities.map((value, index) => Math.abs(value - json.probabilities[index])));
    parity.textContent = `Local format parity: ${json.classIndex === onnxClass && maximumDifference < 1e-5 ? "PASS" : "FAIL"} · maximum probability difference ${maximumDifference.toExponential(2)}`;
  } catch (error) {
    onnxResult.textContent = `ONNX inference failed: ${error instanceof Error ? error.message : String(error)}`;
    parity.textContent = "JSON inference completed, but ONNX parity failed.";
  } finally {
    runButton.disabled = false;
  }
});

async function initialize() {
  try {
    model = await fetch("/models/synthetic_softmax.json").then((response) => {
      if (!response.ok) throw new Error(`Model request failed: ${response.status}`);
      return response.json();
    });
    if (!model.demonstration_only || !model.training_data_provenance.startsWith("synthetic-only")) {
      throw new Error("Refusing a model without explicit synthetic-only provenance.");
    }
    runButton.disabled = false;
    runButton.textContent = "Run local inference";
    parity.textContent = "JSON model ready. Loading ONNX runtime…";
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    jsonResult.textContent = `JSON model failed to load: ${message}`;
    parity.textContent = "Initialization failed. Check the model files and reload.";
    return;
  }

  try {
    ort.env.wasm.numThreads = 1;
    ort.env.wasm.wasmPaths = {
      mjs: new URL(ortMjsUrl, window.location.href).href,
      wasm: new URL(ortWasmUrl, window.location.href).href,
    };
    session = await ort.InferenceSession.create("/models/synthetic_softmax.onnx", { executionProviders: ["wasm"] });
    runButton.textContent = "Run both local formats";
    parity.textContent = "JSON and ONNX runtimes ready. Run inference to check parity.";
    runButton.click();
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    onnxResult.textContent = `ONNX runtime failed to load: ${message}`;
    parity.textContent = "JSON is ready; ONNX is unavailable. JSON inference can still run.";
    runButton.click();
  }
}

initialize();
