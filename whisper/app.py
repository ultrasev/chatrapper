#!/usr/bin/env python3
import logging
import shutil
from pathlib import Path

import whisper
from fastapi import FastAPI, File, Query, UploadFile
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()
model = whisper.load_model("small")


# add an language parameter
@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    lang: str = Query("en", description="Language parameter (default: 'en')"),
) -> JSONResponse:
    try:
        save_path = Path("/tmp") / file.filename
        with open(save_path, "wb") as audio_file:
            shutil.copyfileobj(file.file, audio_file)

        logging.info(f"save_path: {save_path}")
        intial_prompt = "以下是普通话的示例：" if lang == "zh" else ""
        logging.info(f"intial_prompt: {intial_prompt}, {lang}")
        text = model.transcribe(str(save_path), initial_prompt=intial_prompt)

        return JSONResponse(content={
            "response": text,
        }, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
