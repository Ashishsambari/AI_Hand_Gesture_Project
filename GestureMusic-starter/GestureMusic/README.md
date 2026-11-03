# GestureMusic

A web UI concept for a hands-free music controller driven by a hand-gesture recognition model.

## Current status

- [x] Responsive dashboard UI
- [x] Browser camera preview (requires permission and localhost/HTTPS)
- [x] Demo player controls and track progress (no audio is played)
- [x] Six gesture mappings displayed from the existing project
- [ ] Connect the existing Python gesture model
- [ ] Send predictions to the frontend
- [ ] Integrate Apple Music using MusicKit JS and the required Apple developer setup

## Project structure

```text
GestureMusic/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── gesture/
└── README.md
```

## Run the UI locally

Open a terminal in the `GestureMusic` folder and run:

```bash
python -m http.server 5500 --directory frontend
```

Then open `http://localhost:5500` in your browser. Click **Start camera** and allow camera access.

The frontend can be previewed independently. The player is currently a UI simulation: it does not play music, recognize gestures, or control Apple Music yet.

## Start the placeholder API (optional)

From the `GestureMusic` folder:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn app:app --app-dir backend --reload
```

Then open `http://127.0.0.1:8000/api/health`.

## Gesture mapping

| Gesture | Intended action |
|---|---|
| `open_palm` | Play / Pause |
| `thumbs_up` | Volume up |
| `thumbs_down` | Volume down |
| `pointing` | Next track |
| `victory` | Previous track |
| `fist` | Mute |

These are intended mappings only until the model and a supported playback API are connected.
