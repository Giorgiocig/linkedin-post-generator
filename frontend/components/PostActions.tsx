import { Button } from "@/components/ui/button";

interface PostActionsProps {
  onApprove: () => void;
  onApplySuggestions?: () => void;
  disabled?: boolean;
  isPending?: boolean;
  isApplyPending?: boolean;
  showApplySuggestions?: boolean;
}

export function PostActions({
  onApprove,
  onApplySuggestions,
  disabled,
  isPending,
  isApplyPending,
  showApplySuggestions,
}: PostActionsProps) {
  return (
    <div className="flex flex-col gap-2">
      <Button
        onClick={onApprove}
        disabled={disabled || isPending}
        className="w-full"
      >
        {isPending ? "Generazione diagramma..." : "Approva e genera diagramma"}
      </Button>
      {showApplySuggestions && (
        <Button
          variant="outline"
          onClick={onApplySuggestions}
          disabled={isApplyPending}
          className="w-full"
        >
          {isApplyPending ? "Applicazione..." : "Applica suggerimenti"}
        </Button>
      )}
    </div>
  );
}
