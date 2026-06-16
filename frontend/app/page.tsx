"use client";

import { useState } from "react";
import { PostForm } from "@/components/PostForm";
import { PostEditor } from "@/components/PostEditor";
import { GenerateResponse } from "@/lib/types";

export default function Home() {
  const [generateData, setGenerateData] = useState<GenerateResponse | null>(
    null,
  );

  return (
    <main className="min-h-screen p-6 max-w-2xl mx-auto flex flex-col gap-6">
      <h1 className="text-2xl font-bold">LinkedIn Post Generator</h1>
      <PostForm onSuccess={setGenerateData} />
      {generateData && <PostEditor generateData={generateData} />}
    </main>
  );
}
