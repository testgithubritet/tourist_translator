from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.services.lemur_service import LemurService
from app.services.transcriber_service import TranscriberService
from app.utils.audio_utils import cleanup_temp_file, save_temp_audio

app = FastAPI(
    title="Tourist & Local AI Communicator",
    description="Two-way Speech-to-Text translation app powered by AssemblyAI",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static assets
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

transcriber_service = TranscriberService()
lemur_service = LemurService()


@app.get("/")
def serve_frontend():
    """Serves the main application page."""
    return FileResponse("frontend/index.html")


@app.post("/api/translate")
async def translate_audio_endpoint(
    audio: UploadFile = File(...),
    target_language: str = Form(...)
):
    temp_path = None
    try:
        # 1. Save uploaded audio temporarily
        temp_path = save_temp_audio(audio)

        # 2. Transcribe speech using AssemblyAI
        transcript = transcriber_service.transcribe_audio(temp_path)
        original_text = transcript.text or ""
        detected_language = transcript.json_response.get("language_code", "Unknown")

        if not original_text.strip():
            return JSONResponse(status_code=200, content={
                "original_text": "(No clear speech detected)",
                "translated_text": "",
                "detected_language": detected_language
            })

        # 3. Translate using LeMUR
        translated_text = lemur_service.translate_transcript(transcript, target_language)

        return JSONResponse(status_code=200, content={
            "original_text": original_text,
            "translated_text": translated_text,
            "detected_language": detected_language,
            "target_language": target_language
        })

    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": str(exc)})
    finally:
        if temp_path:
            cleanup_temp_file(temp_path)


if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)