# Aeroponic Tower Placement & Crop Recommendation System

Minimal instructions to run the project locally.
---

## Quick Overview
- Backend: FastAPI application located in `backend/` (entry: `backend/app/main.py`).
- Frontend: Vite + React located in `front_end/` (`front_end/package.json`).

## Prerequisites
- Git
- Python 3.11 (recommended)
- Node.js 18.x and npm

## Recommended versions (tested)
- Python 3.11
- Node.js 18.x

## Backend setup (local)

1. Create & activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Upgrade pip and install runtime dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

3. (Optional) Install dev/test dependencies

```bash
python -m pip install -r backend/requirements-dev.txt
```

4. Create `.env` from the example and provide secrets

```bash
cp .env.example .env

## Windows-only quick run (single optimal path)

Prereqs: Windows 10/11, Git, Python 3.11, Node.js 18.x.

1) Clone the repository:

```powershell
git clone https://github.com/<your-username>/<repo>.git
cd AI-Based-Aeroponic-Tower-Placement-Crop-Recommendation-System
```

2) Allow running the setup script in the current PowerShell session (one-time):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
```

3) Run the provided Windows setup script (recommended — automates everything):

```powershell
.\setup-windows.ps1
# To only perform installation (do not start servers):
.\setup-windows.ps1 -SkipStart
```

What the script does:
- Creates and activates `.venv`
- Installs `backend/requirements.txt`
- Copies `.env.example` → `.env` (if missing)
- Runs `npm ci` in `front_end/`
- Opens two PowerShell windows to start backend (`uvicorn` on port 8000) and frontend (Vite on port 3000)

Access after start:
- Backend API: http://localhost:8000
- OpenAPI docs: http://localhost:8000/docs
- Frontend: URL printed by Vite (typically http://localhost:3000)

If anything fails, re-run the script with `-SkipStart` and follow the printed error message.

License: MIT

	cd C:\Users\sriba\OneDrive\Desktop\AI-Based-Aeroponic-Tower-Placement-Crop-Recommendation-System\front_end
	npm install
	```
3) Start Vite dev server:
	```powershell
	npm run dev
	```
	The app will be at http://localhost:5173/

### Notes
- scikit-learn is pinned to 1.5.2 to match the saved models.
- Stop servers with `Ctrl+C` in their terminals.

## Structure
- backend/: Backend API and services
- front_end/: Frontend app
- notebooks/: Data and model notebooks

## License
MIT
 
 