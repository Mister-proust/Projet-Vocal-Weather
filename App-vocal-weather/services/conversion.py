from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from pydub import AudioSegment
from io import BytesIO
import os



UPLOAD_DIR = "./uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_audio(file: UploadFile = File()):
    print(type(file))
    file_content = await file.read()
    if not file_content:
        return JSONResponse(content={"message": "Fichier vide reçu"}, status_code=400)
    audio = AudioSegment.from_file(BytesIO(file_content), format="webm")
        
    with BytesIO() as wav_buffer:    
        audio.export(wav_buffer, format="wav")
        wav_path = UPLOAD_DIR + file.filename
        wav_buffer.seek(0)
        with open(wav_path, "wb") as wav_file:
            wav_file.write(wav_buffer.read())
        wav_buffer.close()
        
    return wav_path
