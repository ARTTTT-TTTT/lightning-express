from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.configs.app_config import app_config


def custom_generate_unique_id(route: APIRoute) -> str:
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    return route.name


app = FastAPI(
    title=app_config.PROJECT_NAME,
    openapi_url=f"{app_config.API_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

if app_config.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=app_config.API_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to LIGHTNING EXPRESS API"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="API for LIGHTNING EXPRESS",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    # 👇 NOTE: Use full path with prefix
                    "tokenUrl": f"{app_config.API_STR}/auth/login",
                    "scopes": {},
                }
            },
        }
    }

    # Add security globally to all paths
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"OAuth2PasswordBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
