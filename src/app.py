from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    Request,
    BackgroundTasks,
)
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from avatar.create_avatar import create_avatar
import uvicorn
import os
import torch
from config_loader import model_config
from typing import List

PARAMETER_NAME_STATUS_CODE = "status_code"
STATUS_1100_SUCCESS = 1100
HTTP_400_BAD_REQUEST = 400

app = FastAPI()
use_jwt = True
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping_pong():
    return {"pong" : "-"}


@app.post("/")
async def get_avatar_request(
    background_tasks: BackgroundTasks, 
    request: Request,
    ):
    form = await request.form()
     
    result_path_list = create_avatar(form) 
    
    if type(result_path_list) is dict:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result_path_list["Error"])

    background_tasks.add_task(remove_files, paths=result_path_list)
    return FileResponse(result_path_list[0], media_type='application/mp4')

def remove_files(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

def run_function_in_jwt_wrapper(
    function, required_inputs, Authorize, jwt_required
) -> dict:
    function_return_value = {}
    
    function_return_value = function(required_inputs)
    function_return_value[PARAMETER_NAME_STATUS_CODE] = STATUS_1100_SUCCESS
    return function_return_value


if __name__ == '__main__':
    torch.cuda.empty_cache()
    uvicorn.run(
        "app:app",
        host = model_config["host"],
        port = model_config["port"], 
        log_level = "debug", 
        reload = True
    ) 