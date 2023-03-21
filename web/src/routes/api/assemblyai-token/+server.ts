import { ASSEMBLYAI_API_KEY } from "$env/static/private";
import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async () => {
  const expiresInSeconds = 3600;

  const response = await fetch("https://api.assemblyai.com/v2/realtime/token", {
    method: "POST",
    headers: {
      authorization: ASSEMBLYAI_API_KEY,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      expires_in: expiresInSeconds,
    }),
  });

  if (response.ok) {
    return json(await response.json());
  }

  return json(
    { error: "Failed to get token" },
    {
      status: response.status,
    }
  );
};
