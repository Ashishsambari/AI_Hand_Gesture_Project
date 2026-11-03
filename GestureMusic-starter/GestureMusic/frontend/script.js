const $ = (selector) => document.querySelector(selector);

const cameraVideo = $("#camera-video");
const cameraStage = $("#camera-stage");
const cameraStatus = $("#camera-status");
const cameraStart = $("#camera-start");
const cameraStop = $("#camera-stop");
const toast = $("#toast");

let cameraStream = null;

let gestureSocket = null;
let gestureTimer = null;
let sendingFrame = false;

function connectGestureBackend() {
  if (gestureSocket?.readyState === WebSocket.OPEN) return;

  gestureSocket = new WebSocket("ws://127.0.0.1:8000/ws/gestures");

  gestureSocket.onopen = () => {
    showToast("Connected to gesture backend.");
    addActivity("Backend connected", "Ready to receive gesture predictions.", "✓");
  };

  gestureSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.error) {
      showToast(data.error);
      return;
    }

    const gesture = data.gesture || "waiting";
    const confidence = Number(data.confidence || 0);

    const symbols = {
      open_palm: "✋",
      thumbs_up: "👍",
      thumbs_down: "👎",
      pointing: "☝️",
      victory: "✌️",
      fist: "✊",
      no_hand: "⌁",
      uncertain: "❔",
      waiting: "⌁"
    };

    $("#gesture-symbol").textContent = symbols[gesture] || "✋";
    $("#gesture-name").textContent = gesture.replaceAll("_", " ").toUpperCase();
    $("#gesture-hint").textContent =
      gesture === "no_hand" ? "No hand detected" :
      gesture === "uncertain" ? "Confidence below 80%" :
      "Live prediction from your Python model";

    $("#confidence-value").textContent = `${(confidence * 100).toFixed(1)}%`;
    $("#confidence-bar").style.width = `${Math.min(100, confidence * 100)}%`;
  };

  gestureSocket.onclose = () => {
    $("#connection-label").textContent = "Backend disconnected";
    showToast("Gesture backend disconnected.");
  };

  gestureSocket.onerror = () => {
    showToast("Cannot connect to the backend. Check port 8000.");
  };
}

function sendCameraFrame() {
  if (
    !cameraStream ||
    !gestureSocket ||
    gestureSocket.readyState !== WebSocket.OPEN ||
    sendingFrame
  ) return;

  const video = $("#camera-video");

  if (!video.videoWidth || !video.videoHeight) return;

  sendingFrame = true;

  try {
    const canvas = document.createElement("canvas");
    canvas.width = 320;
    canvas.height = Math.round(320 * video.videoHeight / video.videoWidth);

    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL("image/jpeg", 0.65);
    const image = dataUrl.split(",")[1];

    gestureSocket.send(JSON.stringify({ image }));
  } finally {
    sendingFrame = false;
  }
}

let toastTimer = null;
let isPlaying = false;
let isMuted = false;
let volume = 65;
let progress = 0;
let progressTimer = null;
let currentTrack = 0;

const tracks = [
  { title: "Midnight Motion", artist: "GestureMusic Demo", duration: 204 },
  { title: "Neon Horizon", artist: "GestureMusic Demo", duration: 187 },
  { title: "Soft Signals", artist: "GestureMusic Demo", duration: 221 }
];

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2600);
}

function addActivity(title, description, icon = "✦") {
  const row = document.createElement("div");
  row.className = "activity-item";
  const symbol = document.createElement("span");
  symbol.className = "activity-icon";
  symbol.textContent = icon;
  const copy = document.createElement("div");
  const heading = document.createElement("strong");
  heading.textContent = title;
  const detail = document.createElement("small");
  detail.textContent = description;
  const time = document.createElement("time");
  time.textContent = "NOW";
  copy.append(heading, detail);
  row.append(symbol, copy, time);
  $("#activity-list").prepend(row);
  while ($("#activity-list").children.length > 5) {
    $("#activity-list").lastElementChild.remove();
  }
}

function setPlaying(playing) {
  isPlaying = playing;
  $("#play-button").textContent = isPlaying ? "Ⅱ" : "▶";
  $("#play-button").setAttribute("aria-label", isPlaying ? "Pause demo" : "Play demo");
  if (progressTimer) clearInterval(progressTimer);
  progressTimer = null;
  if (isPlaying) {
    progressTimer = setInterval(() => {
      progress += 1;
      const duration = tracks[currentTrack].duration;
      if (progress >= duration) progress = 0;
      updateProgress();
    }, 1000);
  }
}

function formatTime(seconds) {
  const min = Math.floor(seconds / 60);
  const sec = seconds % 60;
  return `${min}:${String(sec).padStart(2, "0")}`;
}

function updateProgress() {
  const duration = tracks[currentTrack].duration;
  $("#progress-fill").style.width = `${Math.min(100, (progress / duration) * 100)}%`;
  $("#current-time").textContent = formatTime(progress);
  $("#duration").textContent = formatTime(duration);
}

function changeTrack(direction) {
  currentTrack = (currentTrack + direction + tracks.length) % tracks.length;
  progress = 0;
  $("#track-title").textContent = tracks[currentTrack].title;
  $("#track-artist").textContent = tracks[currentTrack].artist;
  updateProgress();
  addActivity(direction > 0 ? "Next demo track" : "Previous demo track", tracks[currentTrack].title, "♫");
  showToast(`Demo track: ${tracks[currentTrack].title}`);
}

async function startCamera() {
  if (!navigator.mediaDevices?.getUserMedia) {
    showToast("Camera access needs localhost or a secure HTTPS page in a supported browser.");
    return;
  }
  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user" },
      audio: false
    });
    cameraVideo.srcObject = cameraStream;
    cameraStage.classList.add("camera-active");
    cameraStatus.textContent = "Camera on";
    cameraStart.disabled = true;
    cameraStop.disabled = false;
    
    connectGestureBackend();

    if (gestureTimer) clearInterval(gestureTimer);
    gestureTimer = setInterval(sendCameraFrame, 200);

    $("#connection-label").textContent = "Camera connected · Model pending";
    $("#connection-dot").style.background = "var(--green)";
    addActivity("Camera connected", "Live preview started. Gesture model is not connected yet.", "◉");
    showToast("Camera started. This preview does not detect gestures yet.");
  } catch (error) {
    let message = "Could not access the camera. Check browser permissions.";
    if (error.name === "NotAllowedError") message = "Camera permission was denied. Allow it in your browser settings.";
    if (error.name === "NotFoundError") message = "No camera was found on this device.";
    showToast(message);
    addActivity("Camera unavailable", message, "!");
  }
}

function stopCamera() {
  
  if (gestureTimer) clearInterval(gestureTimer);
  gestureTimer = null;

  if (gestureSocket) {
    gestureSocket.close();
    gestureSocket = null;
  }

  if (cameraStream) cameraStream.getTracks().forEach((track) => track.stop());
  cameraStream = null;
  cameraVideo.srcObject = null;
  cameraStage.classList.remove("camera-active");
  cameraStatus.textContent = "Camera off";
  cameraStart.disabled = false;
  cameraStop.disabled = true;
  $("#connection-label").textContent = "UI demo mode";
  addActivity("Camera stopped", "Live preview ended.", "◉");
  showToast("Camera stopped.");
}

cameraStart.addEventListener("click", startCamera);
cameraStop.addEventListener("click", stopCamera);

$("#play-button").addEventListener("click", () => {
  setPlaying(!isPlaying);
  addActivity(isPlaying ? "Demo playback started" : "Demo playback paused", "UI preview only — no real audio is playing.", isPlaying ? "▶" : "Ⅱ");
  showToast(isPlaying ? "Demo player started (no audio)." : "Demo player paused.");
});
$("#next-button").addEventListener("click", () => changeTrack(1));
$("#previous-button").addEventListener("click", () => changeTrack(-1));
$("#volume-slider").addEventListener("input", (event) => {
  volume = Number(event.target.value);
  $("#volume-value").textContent = `${volume}%`;
});
$("#shuffle-button").addEventListener("click", () => showToast("Shuffle will be wired to the real music player later."));
$("#repeat-button").addEventListener("click", () => showToast("Repeat will be wired to the real music player later."));
$("#theme-button").addEventListener("click", () => {
  document.body.classList.toggle("light");
  showToast(document.body.classList.contains("light") ? "Light appearance enabled." : "Dark appearance enabled.");
});

const gestureTiles = [...document.querySelectorAll(".gesture-tile")];
gestureTiles.forEach((tile) => {
  tile.addEventListener("click", () => {
    gestureTiles.forEach((item) => item.classList.remove("active"));
    tile.classList.add("active");
    $("#gesture-symbol").textContent = tile.dataset.symbol;
    $("#gesture-name").textContent = tile.dataset.label;
    $("#gesture-hint").textContent = `Demo mapping: ${tile.dataset.action} · not detected by the model`;
    $("#confidence-value").textContent = "Demo";
    $("#confidence-bar").style.width = "0%";
    addActivity(`Selected ${tile.dataset.label}`, `Demo mapping: ${tile.dataset.action}. No music command was sent.`, tile.dataset.symbol);
    showToast(`${tile.dataset.label} selected for UI preview only.`);
  });
});

window.addEventListener("beforeunload", () => {
  if (cameraStream) cameraStream.getTracks().forEach((track) => track.stop());
  if (progressTimer) clearInterval(progressTimer);
});

updateProgress();
