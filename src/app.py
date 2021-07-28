# from fastapi import (
#     FastAPI,
#     File,
#     Form,
#     UploadFile,
#     HTTPException,
#     Query,
#     Request,
#     Depends,
# )
# import uvicorn
# from fastapi_jwt_auth import AuthJWT
# from ai_model.mcqquestgen import ai_function
# from config_loader import model_config
# import torch
# import requests

from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
    HTTPException,
    Query,
    Request,
    BackgroundTasks,
    Depends,
)
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from config_loader import backend_config
from avatar.create_avatar import create_avatar
import uvicorn
import os
import torch
from src.config_loader import model_config

PARAMETER_NAME_STATUS_CODE = "status_code"
STATUS_1100_SUCCESS = 1100
HTTP_400_BAD_REQUEST = 400

app = FastAPI()
use_jwt = True

def dummy_func():
    pass

@app.get("/ping")
def ping_pong():
    return {"pong" : "-"}

@app.post("/")
async def get_avatar_request(request: Request, background_tasks: BackgroundTasks):
    form = await request.form()
    result_path = create_avatar(form)  
    background_tasks.add_task(remove_files, paths=[result_path])
    return FileResponse(result_path, media_type='application/mp4')

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