const BASE_URL = "https://aiproject-250112486278.europe-west1.run.app";

export async function sendChatRequest(payload) {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let message = "Request failed";
    try {
      const data = await response.json();
      message = data.error || message;
    } catch {
      // ignore JSON parse errors
    }
    throw new Error(message);
  }

  return response.json();
}