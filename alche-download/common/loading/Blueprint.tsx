import { useEffect, useRef } from "react";
import gsap from "gsap";

export default function Blueprint() {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    const svg = svgRef.current;
    if (!svg) return;

    const paths = svg.querySelectorAll("path");

    paths.forEach((path) => {
      const length = path.getTotalLength();

      path.style.strokeDasharray = `${length}`;
      path.style.strokeDashoffset = `${length}`;
    });

    gsap.to(paths, {
      strokeDashoffset: 0,
      duration: 2,
      ease: "power2.out",
      stagger: 0.08,
    });

    gsap.fromTo(
      svg,
      { opacity: 0 },
      {
        opacity: 1,
        duration: 0.4,
      }
    );
  }, []);

  return (
    <svg
      ref={svgRef}
      className="blueprint-logo"
      viewBox="0 0 1000 1000"
    >
      {/* We'll import the S next */}
    </svg>
  );
}
