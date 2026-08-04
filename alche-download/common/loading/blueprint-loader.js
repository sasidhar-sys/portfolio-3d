console.log("########################");
console.log("MY BLUEPRINT LOADER IS RUNNING");
console.log("########################");
// Alert removed

class BlueprintLoader {
  constructor(container) {
    this.container = container;
    this.svg = null;
    this.timeline = null;
  }

  async load() {
    console.log("✅ BlueprintLoader load()");
    const response = await fetch("/common/loading/s_logo.svg");
    const text = await response.text();

    this.container.innerHTML = `
<div class="bp-root">

    <div class="bp-vignette"></div>

    <div class="bp-grid"></div>

    <div class="bp-noise"></div>

    <div class="bp-crosshair"></div>

    <div class="bp-guides"></div>

    <div class="bp-circles"></div>

    <div class="bp-measurements"></div>

    <div class="bp-labels"></div>

    <div class="bp-svg">
        ${text}
    </div>

    <div class="bp-glow"></div>

</div>
`;

    this.root = this.container.querySelector(".bp-root");

    this.vignette = this.root.querySelector(".bp-vignette");

    this.grid = this.root.querySelector(".bp-grid");

    this.noise = this.root.querySelector(".bp-noise");

    this.crosshair = this.root.querySelector(".bp-crosshair");

    this.guides = this.root.querySelector(".bp-guides");

    this.circles = this.root.querySelector(".bp-circles");

    this.measurements = this.root.querySelector(".bp-measurements");

    this.labels = this.root.querySelector(".bp-labels");

    this.glow = this.root.querySelector(".bp-glow");

    this.svgContainer = this.root.querySelector(".bp-svg");

    this.svg = this.svgContainer.querySelector("svg");

    if (!this.svg) {
      throw new Error("SVG not found.");
    }

    this.svg.style.width = "170px";
    this.svg.style.height = "170px";
    this.svg.style.opacity = "1";
    this.svg.style.overflow = "visible";

    this.preparePaths();
    this.createGrid();
    this.createConstructionCircles();
    this.createCrosshair();
    this.createHud();
    this.createScanLine();
  }

  preparePaths() {
    const paths = this.svg.querySelectorAll("path");

    paths.forEach((path) => {
      const len = path.getTotalLength();

      path.style.fill = "none";
      path.style.stroke = "#ffffff";
      path.style.strokeWidth = "0.7";
      path.style.vectorEffect = "non-scaling-stroke";
      path.style.strokeLinecap = "butt";
      path.style.strokeLinejoin = "miter";
      path.style.strokeMiterlimit = "4";
      
      path.style.strokeDasharray = len;
      path.style.strokeDashoffset = len;
    });
  }

  createGrid() {
    const grid = document.createElement("div");

    grid.className = "blueprint-grid";

    Object.assign(grid.style, {
      position: "absolute",
      inset: "-120px",
      pointerEvents: "none",
      opacity: "0",
      backgroundImage: `
        linear-gradient(rgba(255,255,255,.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px)
      `,
      backgroundSize: "32px 32px"
    });

    this.container.style.position = "relative";

    this.container.prepend(grid);

    this.grid = grid;
  }

  createConstructionCircles() {

    const svgNS = "http://www.w3.org/2000/svg";

    const svg = document.createElementNS(svgNS, "svg");

    svg.setAttribute("viewBox", "0 0 500 500");

    Object.assign(svg.style,{
        position:"absolute",
        inset:"-140px",
        width:"500px",
        height:"500px",
        overflow:"visible",
        pointerEvents:"none"
    });

    const radii=[70,115,165];

    radii.forEach(r=>{

        const c=document.createElementNS(svgNS,"circle");

        c.setAttribute("cx","250");
        c.setAttribute("cy","250");
        c.setAttribute("r",r);

        c.setAttribute("fill","none");
        c.setAttribute("stroke","rgba(255,255,255,.18)");
        c.setAttribute("stroke-width","1");

        svg.appendChild(c);

    });

    this.circles.innerHTML="";
    this.circles.appendChild(svg);

    this.circleElements=[...svg.querySelectorAll("circle")];

    this.circleElements.forEach(circle=>{

        const len=2*Math.PI*circle.r.baseVal.value;

        circle.style.strokeDasharray=len;
        circle.style.strokeDashoffset=len;

    });

  }

  createCrosshair(){

    this.crosshair.innerHTML="";

    const h=document.createElement("div");
    const v=document.createElement("div");

    Object.assign(h.style,{
        position:"absolute",
        left:"50%",
        top:"50%",
        width:"260px",
        height:"1px",
        background:"rgba(255,255,255,.18)",
        transform:"translate(-50%,-50%)"
    });

    Object.assign(v.style,{
        position:"absolute",
        left:"50%",
        top:"50%",
        width:"1px",
        height:"260px",
        background:"rgba(255,255,255,.18)",
        transform:"translate(-50%,-50%)"
    });

    this.crosshair.appendChild(h);
    this.crosshair.appendChild(v);

  }

  createHud(){

    this.labels.innerHTML="";

    const hud=document.createElement("div");

    hud.style.position="absolute";

    hud.style.left="-120px";

    hud.style.top="-95px";

    hud.style.color="rgba(255,255,255,.45)";

    hud.style.fontFamily="IBM Plex Mono, monospace";

    hud.style.fontSize="10px";

    hud.style.letterSpacing="2px";

    hud.style.lineHeight="18px";

    hud.style.opacity="0";

    hud.innerHTML=`
X 145.002<br>
Y 088.442<br>
R 128.00<br>
ANGLE 45°<br>
STATUS READY
`;

    this.labels.appendChild(hud);

    this.hud=hud;

  }

  createScanLine() {
    const line = document.createElement("div");

    Object.assign(line.style, {
      position: "absolute",
      left: "-80px",
      top: "-80px",
      width: "380px",
      height: "1px",
      background: "linear-gradient(90deg,transparent,#fff,transparent)",
      opacity: "0",
      pointerEvents: "none",
      boxShadow: "0 0 18px white"
    });

    this.container.appendChild(line);

    this.scanLine = line;
  }

  play(onCameraStart, onComplete) {
    console.log("BlueprintLoader play()");
    const paths = [...this.svg.querySelectorAll("path")];

    this.timeline = gsap.timeline({
      onComplete: () => {
        onComplete?.();
        this.onComplete?.();
      }
    });

    this.timeline

      .to(this.grid, {
        opacity: 0.35,
        duration: 0.4
      })

      .to(
        this.grid,
        {
          backgroundPosition: "32px 32px",
          duration: 8,
          ease: "none",
          repeat: -1
        },
        0
      )

      .to(
        this.noise,
        {
          backgroundPositionY: "120px",
          duration: 2.5,
          ease: "none",
          repeat: -1
        },
        0
      )

      .fromTo(
        this.crosshair,
        {
          rotation: 0,
          opacity: 0
        },
        {
          rotation: 15,
          opacity: 1,
          duration: 1.8,
          ease: "power2.out"
        },
        "<"
      )

      .to(this.hud,{
        opacity:1,
        duration:.45
      },"<")
      .to(this.title,{
        opacity:1,
        duration:.45
      },"<")

      .to(this.circleElements,{
        strokeDashoffset:0,
        duration:.9,
        stagger:.15,
        ease:"power2.out"
      },"<")

      .to(
        this.circleElements,
        {
          opacity: 0.45,
          stagger: .15,
          repeat: 1,
          yoyo: true,
          duration: .6
        },
        "<"
      )

      .fromTo(
        this.scanLine,
        {
          opacity: 1,
          y: -120
        },
        {
          y: 260,
          opacity: 1,
          duration: 1.4,
          ease: "power1.inOut"
        },
        "<"
      )

      .to(paths, {
        strokeDashoffset: 0,
        stagger: 0.08,
        duration: 2.1,
        ease: "power2.out"
      })

      .to(this.glow,{
          opacity:.65,
          duration:.18,
          yoyo:true,
          repeat:1,
          ease:"power2.out"
      },"<")

      .to(
        this.svg,
        {
          scale: 1.03,
          filter: `
            drop-shadow(0 0 4px rgba(255,255,255,.45))
            drop-shadow(0 0 10px rgba(255,255,255,.20))
          `,
          duration: .45,
          yoyo: true,
          repeat: 1
        }
      )

      .to(this.scanLine, {
        opacity: 0,
        duration: 0.25
      })

      .to(this.hud,{
        opacity:.25,
        duration:.4
      },"<")

      // STEP 1 — Fade layers independently
      .to(this.hud,{
          opacity:0,
          duration:0.25
      })
      .to(this.title,{
          opacity:0,
          duration:0.25
      },"<")

      .to(this.circles,{
          opacity:0,
          duration:0.35
      },"<")

      .to(this.crosshair,{
          opacity:0,
          duration:0.35
      },"<")

      .to(this.grid,{
          opacity:0,
          duration:0.5
      },"<")

      .to(this.noise,{
          opacity:0,
          duration:0.5
      },"<")

      // STEP 2 — Keep the logo alive
      .to(this.svg,{
          opacity:1,
          duration:.4
      })

      .to(this.svg,{
          scale:1.03,
          duration:.35,
          ease:"power2.out",
          onStart: () => {
              onCameraStart?.();
              this.onCameraStart?.();
          }
      })

      .to(this.svg,{
          opacity:0,
          scale:1.10,
          duration:.45,
          ease:"power2.in"
      },"<+0.12")

      .call(() => {
          this.destroy();
      });
  }

  destroy() {
    this.timeline?.kill();
    this.container.innerHTML = "";
  }
}

window.BlueprintLoader = BlueprintLoader;