import { ApplySuggestionsRequest, ApplySuggestionsResponse } from "../types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const applySuggestions = async (
  data: ApplySuggestionsRequest,
): Promise<ApplySuggestionsResponse> => {
  const response = await fetch(`${API_URL}/api/apply-suggestions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok)
    throw new Error("Errore nell'applicazione dei suggerimenti");
  return response.json();
};
