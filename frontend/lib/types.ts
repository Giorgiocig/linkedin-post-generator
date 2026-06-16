export interface GenerateRequest {
  user_input: string;
  user_context?: string;
}

export interface GenerateResponse {
  thread_id: string;
  post_text: string;
  review_notes: string;
}

export interface ResumeRequest {
  thread_id: string;
  post_text: string;
}

export interface ResumeResponse {
  thread_id: string;
  post_text: string;
  image_url: string;
  review_notes: string;
}

export interface ApplySuggestionsRequest {
  post_text: string;
  review_notes: string;
}

export interface ApplySuggestionsResponse {
  post_text: string;
}
