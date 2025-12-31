const API_BASE_URL = "http://127.0.0.1:8000";

export async function predictCrops(inputData) {
  const response = await fetch(`${API_BASE_URL}/predict/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputData)
  });
  return response.json();
}

export async function optimizePlacement(farmData) {
  const response = await fetch(`${API_BASE_URL}/placement/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(farmData)
  });
  return response.json();
}
