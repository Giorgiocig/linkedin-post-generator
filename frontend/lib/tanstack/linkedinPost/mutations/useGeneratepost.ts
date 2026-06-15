import { generatePost } from "@/lib/api/post";
import { GenerateResponse } from "@/lib/types";
import { useMutation } from "@tanstack/react-query";

export const useGeneratePost = (
  onSuccess: (data: GenerateResponse) => void,
) => {
  return useMutation({
    mutationFn: generatePost,
    onSuccess,
    onError: (error: Error) => {
      console.error("Errore generatePost:", error.message);
    },
  });
};
