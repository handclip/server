import logging
import uuid
from os import path

from fastapi import FastAPI, File, HTTPException, UploadFile

import video

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

VIDEOS_DIR = 'videos'

app = FastAPI()


async def save_video(file: UploadFile) -> str:
    video_path = path.join(VIDEOS_DIR, str(uuid.uuid4()))

    with open(video_path, 'wb') as out_file:
        while content := await file.read(4096):
            out_file.write(content)

    logger.info('Saved video to %s', video_path)
    return video_path


@app.post('/')
async def upload_video(file: UploadFile = File(...)):
    video_path = await save_video(file)

    try:
        return {'marks': video.get_marks(video_path)}
    except video.InvalidVideoFile as ex:
        raise HTTPException(status_code=400, detail='Invalid video.') from ex
