import aiofiles
from fastapi import UploadFile


async def aiosave(outpath: str, in_file: UploadFile):
    async with aiofiles.open(outpath, 'wb') as out_file:
        while content := await in_file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk
