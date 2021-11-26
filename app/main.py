from starlette.routing import Host
from fastapi import FastAPI
from app.tasks.video_proc import replace_background
from app.payloads import VideoProcessTaskRequest, VideoProcessResponse, VideoProcessResult
from fastapi.openapi.utils import get_openapi
import logging

app = FastAPI()


@app.post("/tasks", status_code=200)
async def run_task(request: VideoProcessTaskRequest):
    task = replace_background.delay(request)
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
