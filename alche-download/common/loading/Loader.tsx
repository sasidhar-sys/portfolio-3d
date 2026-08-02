import { useEffect, useState } from "react";
import Blueprint from "./Blueprint";
import gsap from "gsap";

interface LoaderProps {
  onComplete?: () => void;
}

export default function Loader({ onComplete }: LoaderProps) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const tl = gsap.timeline({
      onComplete: () => {
        gsap.to(".loader-container", {
          opacity: 0,
          duration: 0.8,
          onComplete: () => {
            setVisible(false);
            onComplete?.();
          },
        });
      },
    });

    // Timeline
    tl.from(".loader-grid", {
      opacity: 0,
      duration: 0.5,
    });

    tl.from(".loader-circles", {
      opacity: 0,
      duration: 0.5,
    });

    tl.from(".loader-text", {
      opacity: 0,
      y: 10,
      duration: 0.4,
    });

    tl.to({}, { duration: 2.0 }); // keep logo visible
  }, []);

  if (!visible) return null;

  return (
    <div className="loader-container">
      <div className="loader-grid"></div>

      <div className="loader-circles">
        <Blueprint />
      </div>

      <div className="loader-text">
        Building Intelligent Experiences
      </div>
    </div>
  );
}
