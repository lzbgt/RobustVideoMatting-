from fastapi.param_functions import Header
from starlette.routing import Host
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.tasks.video_proc import replace_background
from app.payloads import VideoProcessTaskRequest, VideoProcessResponse, VideoProcessResult
from fastapi.openapi.utils import get_openapi
from app.auth.jwt_bearer import JWTBearer
import logging

app = FastAPI()


@app.post("/tasks", dependencies=[Depends(JWTBearer())], status_code=200)
async def run_task(request: VideoProcessTaskRequest, authorization: str = Header(None)):
    logging.error(f'auth: {authorization}')
    task = replace_background.delay(request, authorization)
    return {"task_id": task.id}


@app.get("/tasks/{task_id}", status_code=200, response_model=VideoProcessResponse)
async def get_status(task_id: str) -> VideoProcessResponse:
    task_result = replace_background.AsyncResult(task_id)
    logging.info(task_id)
    logging.info(task_result.status)
    logging.info(task_result.result)

    result: VideoProcessResponse
    if not task_result or not task_result.result:
        result = VideoProcessResponse(
            id=task_id,
            status="None",
            result=VideoProcessResult(url='')
        )
    elif task_result.status == 'FAILURE':
        result = VideoProcessResponse(
            id=task_id,
            status="FAILURE",
            result=VideoProcessResult(url='',
                                      exc_type=str(type(task_result.result)),
                                      exc_message=str(task_result.result)
                                      )
        )

    else:
        logging.info(task_id)
        logging.info(task_result.status)
        logging.info(task_result.result)
        result = VideoProcessResponse(
            id=task_id,
            status=task_result.status,
            result=VideoProcessResult.parse_obj(task_result.result)
        )

    return result

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    # if app.openapi_schema:
    #     return app.openapi_schema
    openapi_schema = get_openapi(
        title="Video Background Replace API",
        version="2.5.0",
        description="replacing video background based on RobustVideoMatting",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "www.unidt.com"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi_schema = custom_openapi()
