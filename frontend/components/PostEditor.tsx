"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { PostTextArea } from "./PostTextArea";
import { PostActions } from "./PostActions";
import { ReviewNotes } from "./ReviewNotes";
import { DiagramImage } from "./DiagramImage";

import { GenerateResponse, ResumeResponse } from "@/lib/types";
import { useApplySuggestions, useResumePost } from "@/lib";

interface PostEditorProps {
  generateData: GenerateResponse;
}

export function PostEditor({ generateData }: PostEditorProps) {
  const [postText, setPostText] = useState(generateData.post_text);
  const [resumeData, setResumeData] = useState<ResumeResponse | null>(null);

  const { mutate: resume, isPending: isResumePending } = useResumePost(
    (data) => {
      setResumeData(data);
    },
  );

  const { mutate: apply, isPending: isApplyPending } = useApplySuggestions(
    (data) => {
      setPostText(data.post_text);
    },
  );

  const handleApprove = () => {
    resume({
      thread_id: generateData.thread_id,
      post_text: postText,
    });
  };

  const handleApplySuggestions = () => {
    if (!resumeData) return;
    apply({
      post_text: postText,
      review_notes: resumeData.review_notes,
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Il tuo post</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <PostTextArea
          value={postText}
          onChange={setPostText}
          disabled={isResumePending}
        />
        <PostActions
          onApprove={handleApprove}
          onApplySuggestions={handleApplySuggestions}
          isPending={isResumePending}
          isApplyPending={isApplyPending}
          disabled={!!resumeData}
          showApplySuggestions={!!resumeData}
        />
        {resumeData && (
          <>
            <Separator />
            <DiagramImage image_url={resumeData.image_url} />
            <Separator />
            <ReviewNotes review_notes={resumeData.review_notes} />
          </>
        )}
      </CardContent>
    </Card>
  );
}
