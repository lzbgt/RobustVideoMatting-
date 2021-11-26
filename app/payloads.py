from pydantic import BaseModel, Field


class VideoProcessTaskRequest(BaseModel):
    video_url: str = Field(
        example='http://public-1255423687.cos.ap-shanghai.myqcloud.com/tmn1637895917645.mp4')
    bgr_url: str = Field(
        example='http://public-1255423687.cos.ap-shanghai.myqcloud.com/bJj1637895964061.jpg')


class BaseResponse(BaseModel):
    #code: int = Field(default=0, example="0")
    exc_type: str = Field(default='', example='OSErr')
    exc_message: str = Field(default='', example='err msg')


class VideoProcessResult(BaseResponse):
    url: str = Field(default='')


class VideoProcessResponse(BaseModel):
    id: str = Field(..., example='08953e59-0ed1-3666-a5ed-5a1aa0b1c124')
    status: str = Field(..., example='PENDING')
    result: VideoProcessResult
