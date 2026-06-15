import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

interface ReviewNotesProps {
  review_notes: string;
}

export function ReviewNotes({ review_notes }: ReviewNotesProps) {
  const isApproved = review_notes.includes("APPROVATO");

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium">Revisione AI</span>
        <Badge variant={isApproved ? "default" : "destructive"}>
          {isApproved ? "Approvato" : "Da rivedere"}
        </Badge>
      </div>
      <Separator />
      <p className="text-sm text-muted-foreground whitespace-pre-line">
        {review_notes}
      </p>
    </div>
  );
}
