import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

interface PostTextAreaProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function PostTextArea({ value, onChange, disabled }: PostTextAreaProps) {
  return (
    <div className="flex flex-col gap-2">
      <Label htmlFor="post-textarea">Modifica il tuo post</Label>
      <Textarea
        id="post-textarea"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        rows={10}
        className="resize-none"
      />
    </div>
  );
}
