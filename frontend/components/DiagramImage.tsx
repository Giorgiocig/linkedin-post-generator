import Image from "next/image";

interface DiagramImageProps {
  image_url: string;
}

export function DiagramImage({ image_url }: DiagramImageProps) {
  if (!image_url) return null;

  return (
    <div className="flex flex-col gap-2">
      <span className="text-sm font-medium">Diagramma generato</span>
      <div className="relative w-full aspect-video rounded-lg overflow-hidden border">
        {/**
         * TODO to be updated with the correct nextjs tag <Image />
         */}
        <img
          src={image_url}
          alt="Diagramma tecnico"
          className="object-contain"
        />
      </div>
    </div>
  );
}
