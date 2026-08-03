export function softmax(values) {
  const peak = Math.max(...values);
  const exp = values.map((value) => Math.exp(value - peak));
  const total = exp.reduce((sum, value) => sum + value, 0);
  return exp.map((value) => value / total);
}

export function standardize(input, model) {
  return input.map((value, index) => (value - model.scaler_mean[index]) / model.scaler_scale[index]);
}

export function inferJson(input, model) {
  if (input.length !== model.feature_names.length) throw new Error("Input feature count does not match model contract.");
  const scaled = standardize(input, model);
  const logits = model.bias.map((bias, classIndex) => bias + scaled.reduce((sum, value, featureIndex) => sum + value * model.weights[featureIndex][classIndex], 0));
  const probabilities = softmax(logits);
  const classIndex = probabilities.indexOf(Math.max(...probabilities));
  return { classIndex, label: model.classes[classIndex], probabilities, scaled };
}

export function boundedWhatIf(input, deltaPoints) {
  const bounded = Math.max(-15, Math.min(15, Number(deltaPoints))) / 100;
  const result = [...input];
  result[0] = Math.max(0, Math.min(1, result[0] + bounded));
  result[13] = Math.max(0, Math.min(1, result[13] + bounded * 0.75));
  result[15] = Math.max(0, Math.min(1, result[15] + bounded * 0.5));
  result[17] = Math.max(0, Math.min(1, result[17] + bounded * 0.25));
  return result;
}
