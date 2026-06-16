import { applySuggestions } from "@/lib/api/suggestions";
import { ApplySuggestionsResponse } from "@/lib/types";
import { useMutation } from "@tanstack/react-query";

export const useApplySuggestions = (
  onSuccess: (data: ApplySuggestionsResponse) => void,
) => {
  return useMutation({
    mutationFn: applySuggestions,
    onSuccess,
    onError: (error: Error) => {
      console.error("Errore applySuggestions:", error.message);
    },
  });
};
