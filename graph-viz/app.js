const container = document.getElementById("graph-container");
const drawButton = document.getElementById("draw-button");

drawButton.addEventListener("click", (e) => {
  const dot = document.getElementById("graph-dot-textarea").value;
  const data = vis.parseDOTNetwork(dot);
  const network = new vis.Network(container, data);
});
