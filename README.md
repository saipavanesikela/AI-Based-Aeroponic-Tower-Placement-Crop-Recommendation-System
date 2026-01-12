# Aeroponic Tower Placement & Crop Recommendation System

This project provides an AI-based solution for optimizing aeroponic tower placement and crop recommendations.

## Quick Start (Windows)

### Backend API
1) Open PowerShell and go to the project root:
	```powershell
	cd C:\Users\sriba\OneDrive\Desktop\AI-Based-Aeroponic-Tower-Placement-Crop-Recommendation-System
	```
2) Install deps inside the venv (created already in `.venv`):
	```powershell
	.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
	```
3) Start the API:
	```powershell
	cd backend
	..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
	```
	The API will be at http://127.0.0.1:8000/
	If you want to just type `uvicorn app.main:app --reload`, add the venv Scripts folder to PATH once, then reopen PowerShell:
	```powershell
	setx PATH "$($env:PATH);C:\Users\sriba\OneDrive\Desktop\AI-Based-Aeroponic-Tower-Placement-Crop-Recommendation-System\.venv\Scripts"
	```
	Then run from `backend/`:
	```powershell
	cd C:\Users\sriba\OneDrive\Desktop\AI-Based-Aeroponic-Tower-Placement-Crop-Recommendation-System\backend
	uvicorn app.main:app --reload
	```
	If you ever see scikit-learn version warnings, it means you are using the system Python instead of the venv. Fix by prepending the venv Scripts to PATH for the session, then start uvicorn:
	```powershell
	$env:Path = 'C:\Users\sriba\OneDrive\Desktop\AI-Based-Aeroponic-Tower-Placement-Crop-Recommendation-System\.venv\Scripts;' + $env:Path
	cd C:\Users\sriba\OneDrive\Desktop\AI-Based-Aeroponic-Tower-Placement-Crop-Recommendation-System\backend
	uvicorn app.main:app --reload
	```

### Frontend (Vite dev server)
1) In a new PowerShell window, add Node to this session PATH (if not already):
	```powershell
	$env:Path = 'C:\\Program Files\\nodejs;' + $env:Path
	```
	If you want it permanent: `setx PATH "$($env:PATH);C:\\Program Files\\nodejs\\"` then reopen terminals.
2) Go to the frontend folder and install deps:
	```powershell
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
 
 