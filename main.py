import logging
import uuid
from os import path

from fastapi import FastAPI, File, UploadFile

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

VIDEOS_DIR = 'videos'


async def save_video(file: UploadFile) -> str:
    video_path = path.join(VIDEOS_DIR, uuid.uuid4())

    with open(video_path, 'wb') as out_file:
        while content := await file.read(1024):
            out_file.write(content)

    logger.info(f'Saved video to {video_path}')
    return video_path


@app.post('/upload/')
async def upload_video(video_file: UploadFile = File(...)):
    video_path = await save_video(video_file)

    return {'filename': video_file.filename}
