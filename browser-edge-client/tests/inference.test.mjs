import test from "node:test";
import assert from "node:assert/strict";
import { boundedWhatIf, inferJson } from "../src/inference.js";
import model from "../public/models/synthetic_softmax.json" with { type: "json" };

test("JSON inference returns normalized probabilities", () => {
  const result = inferJson(model.example_input, model);
  assert.ok(Math.abs(result.probabilities.reduce((a, b) => a + b, 0) - 1) < 1e-12);
  assert.ok(model.classes.includes(result.label));
});

test("what-if is bounded and does not mutate input", () => {
  const original = [...model.example_input];
  const result = boundedWhatIf(original, 500);
  assert.equal(result[0], Math.min(1, original[0] + 0.15));
  assert.deepEqual(original, model.example_input);
});
