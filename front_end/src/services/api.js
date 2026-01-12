const API_BASE_URL = "http://127.0.0.1:8000";

export async function predictCrops(inputData) {
  const response = await fetch(`${API_BASE_URL}/predict/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputData)
  });
  const data = await response.json();
  if (!response.ok) {
    // throw the backend error message if provided
    const message = data.detail || data.error || "Prediction failed";
    throw new Error(message);
  }
  return data;
}

export async function optimizePlacement(farmData) {
  const response = await fetch(`${API_BASE_URL}/placement/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(farmData)
  });
  const data = await response.json();
  if (!response.ok) {
    const message = data.detail || data.error || "Placement failed";
    throw new Error(message);
  }
  return data;
}

