import uvicorn
from api.v1 import base
from core.config import app_settings
from fastapi import FastAPI
from middlware.black_list import BlackListMiddleware

app = FastAPI(
    title=app_settings.app_title,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.include_router(base.router, prefix=app_settings.api_v1_prefix, )
app.add_middleware(BlackListMiddleware, black_list=app_settings.black_list)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.project_host,
        port=app_settings.project_port,
    )
