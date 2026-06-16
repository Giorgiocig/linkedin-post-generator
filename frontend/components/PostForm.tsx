"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PostInput } from "./PostInput";
import { UserContextInput } from "./UserContextInput";
import { GenerateResponse } from "@/lib/types";
import { useGeneratePost } from "@/lib";

interface PostFormProps {
  onSuccess: (data: GenerateResponse) => void;
}

export function PostForm({ onSuccess }: PostFormProps) {
  const [input, setInput] = useState("");
  const [userContext, setUserContext] = useState("");

  const { mutate, isPending } = useGeneratePost(onSuccess);

  const handleSubmit = () => {
    if (!input.trim()) return;
    mutate({
      user_input: input,
      user_context: userContext || undefined,
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Crea il tuo post LinkedIn</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <PostInput value={input} onChange={setInput} disabled={isPending} />
        <UserContextInput
          value={userContext}
          onChange={setUserContext}
          disabled={isPending}
        />
        <Button
          onClick={handleSubmit}
          disabled={isPending || !input.trim()}
          className="w-full"
        >
          {isPending ? "Generazione in corso..." : "Genera Post"}
        </Button>
      </CardContent>
    </Card>
  );
}
