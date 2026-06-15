import { Button } from "@/components/ui/button";

interface PostActionsProps {
  onApprove: () => void;
  disabled?: boolean;
  isPending?: boolean;
}

export function PostActions({
  onApprove,
  disabled,
  isPending,
}: PostActionsProps) {
  return (
    <div className="flex gap-2">
      <Button
        onClick={onApprove}
        disabled={disabled || isPending}
        className="w-full"
      >
        {isPending ? "Generazione diagramma..." : "Approva e genera diagramma"}
      </Button>
    </div>
  );
}
