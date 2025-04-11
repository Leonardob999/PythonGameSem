// frontend/script.js
const player = localStorage.getItem("player");
const slider = document.getElementById("slider");
const ball1 = document.getElementById("ball1");
const ball2 = document.getElementById("ball2");

// Verbindung zum Backend
const socket = new WebSocket(`ws://100.125.106.71:5000/ws/${player}`);

// Slider-Änderung senden
slider.addEventListener("input", () => {
  socket.send(JSON.stringify({ value: parseInt(slider.value) }));
});

// Ball-Positionen empfangen
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  ball1.style.left = `calc(${data.ball1}% - 15px)`;
  ball2.style.left = `calc(${data.ball2}% - 15px)`;
};
