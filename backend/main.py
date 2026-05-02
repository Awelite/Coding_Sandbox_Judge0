from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.coding import router as coding_router

app = FastAPI(title="AI Interview Copilot")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ include router
app.include_router(coding_router)

@app.get("/")
def root():
    return {"message": "Server running"}