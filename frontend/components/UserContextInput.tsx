import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

interface UserContextInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function UserContextInput({
  value,
  onChange,
  disabled,
}: UserContextInputProps) {
  return (
    <div className="flex flex-col gap-2">
      <Label htmlFor="user-context">
        Contesto personale{" "}
        <span className="text-muted-foreground text-xs">(opzionale)</span>
      </Label>
      <Textarea
        id="user-context"
        placeholder="Es: Sto costruendo un agente con LangGraph. Il problema principale che ho incontrato è gestire l'interrupt per il human-in-the-loop..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        rows={3}
        className="resize-none"
      />
    </div>
  );
}
