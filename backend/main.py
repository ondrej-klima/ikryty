import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tortoise import Tortoise

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

Tortoise.init_models(["src.database.models"], "models")
from src.routes import shelters, targets, routes
from fastapi.staticfiles import StaticFiles

# https://testdriven.io/blog/developing-a-single-page-app-with-fastapi-and-vuejs/

# --- Configuration ---
SWAGGER_CLIENT_ID = "my-fastapi-swagger" # The Client ID you created in Keycloak

app = FastAPI(
    title="Shelter Management API",
    swagger_ui_init_oauth={
        "clientId": SWAGGER_CLIENT_ID,
        "appName": "Shelter API - Swagger UI",
        "usePkceWithAuthorizationCodeGrant": True,  # Use PKCE for better security
        "scopes": "openid profile email roles"  # Request all the scopes we defined
    }
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost",
        "http://civildefense.fit.vutbr.cz",
        "https://civildefense.fit.vutbr.cz"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shelters.router)
app.include_router(targets.router)
app.include_router(routes.router)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True)


@app.get("/")
def home():
    return {"Message": "Hello, World!"}


if __name__ == '__main__':
    #uvicorn.run("main:app", port=8000, host="civildefense.fit.vutbr.cz", reload=True, ssl_keyfile="/etc/letsencrypt/live/civildefense.fit.vutbr.cz/privkey.pem", ssl_certfile="/etc/letsencrypt/live/civildefense.fit.vutbr.cz/fullchain.pem")
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)
