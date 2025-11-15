# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.api import routes_workflow

app = FastAPI(title="Pyagram Backend", version="0.1.0")

# --- CORS setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or explicit origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Router registration ---
app.include_router(routes_workflow.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "message": "Pyagram backend running"}
