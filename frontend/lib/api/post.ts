import {
  GenerateRequest,
  GenerateResponse,
  ResumeRequest,
  ResumeResponse,
} from "../types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const generatePost = async (
  data: GenerateRequest,
): Promise<GenerateResponse> => {
  const response = await fetch(`${API_URL}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error("Errore nella generazione del post");
  return response.json();
};

export const resumePost = async (
  data: ResumeRequest,
): Promise<ResumeResponse> => {
  const response = await fetch(`${API_URL}/api/resume`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error("Errore nella ripresa del post");
  return response.json();
};
