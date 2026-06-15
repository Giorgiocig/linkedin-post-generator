import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

interface PostInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function PostInput({ value, onChange, disabled }: PostInputProps) {
  return (
    <div className="flex flex-col gap-2">
      <Label htmlFor="post-input">Di cosa vuoi scrivere?</Label>
      <Textarea
        id="post-input"
        placeholder="Es: Come funziona LangGraph e perché lo uso nei miei progetti..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        rows={4}
        className="resize-none"
      />
    </div>
  );
}
