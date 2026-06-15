import { resumePost } from "@/lib/api/post";
import { ResumeResponse } from "@/lib/types";
import { useMutation } from "@tanstack/react-query";

export const useResumePost = (onSuccess: (data: ResumeResponse) => void) => {
  return useMutation({
    mutationFn: resumePost,
    onSuccess,
    onError: (error: Error) => {
      console.error("Errore resumePost:", error.message);
    },
  });
};
