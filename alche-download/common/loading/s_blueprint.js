export function createBlueprintS(container){

    const svgNS="http://www.w3.org/2000/svg";

    const svg=document.createElementNS(svgNS,"svg");

    svg.setAttribute("viewBox","0 0 420 420");

    svg.style.width="220px";
    svg.style.height="220px";
    svg.style.overflow="visible";

    container.innerHTML="";

    container.appendChild(svg);

    function addPath(d){

        const p=document.createElementNS(svgNS,"path");

        p.setAttribute("d",d);

        p.setAttribute("fill","none");

        p.setAttribute("stroke","#fff");

        p.setAttribute("stroke-width","1");

        p.setAttribute("stroke-linecap","round");

        p.setAttribute("stroke-linejoin","round");

        svg.appendChild(p);

        return p;

    }

    addPath("M110 80 H250 L300 130 V170");
    addPath("M300 170 H180 V220 H280");
    addPath("M280 220 L330 270 V340");
    addPath("M330 340 L280 390 H120");
    addPath("M120 390 L90 360 V320");
    addPath("M90 320 H210");

    return [...svg.querySelectorAll("path")];

}
