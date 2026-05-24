import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

VALID_ENVIRONMENTS = {"local", "production"}
APP_ENV = os.getenv("APP_ENV", "local").strip().lower()

if APP_ENV not in VALID_ENVIRONMENTS:
    raise ValueError(f"Unsupported APP_ENV '{APP_ENV}'. Use one of: {', '.join(sorted(VALID_ENVIRONMENTS))}.")


def _env_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


IS_PRODUCTION = APP_ENV == "production"

DATABASE_URL = os.getenv(
    "DATABASE_URL_PRODUCTION" if IS_PRODUCTION else "DATABASE_URL_LOCAL",
    "mysql://civildefense:r8AbuAbu@147.229.177.177:3306/dbikryty"
    if IS_PRODUCTION
    else "mysql://ikryty:ikryty123@localhost:3306/dbikryty",
)

UVICORN_HOST = os.getenv(
    "UVICORN_HOST_PRODUCTION" if IS_PRODUCTION else "UVICORN_HOST_LOCAL",
    "0.0.0.0" if IS_PRODUCTION else "localhost",
)
UVICORN_PORT = int(os.getenv("UVICORN_PORT", "8000"))
UVICORN_RELOAD = _env_flag(
    "UVICORN_RELOAD_PRODUCTION" if IS_PRODUCTION else "UVICORN_RELOAD_LOCAL",
    default=not IS_PRODUCTION,
)


def get_uvicorn_run_kwargs() -> dict:
    return {
        "host": UVICORN_HOST,
        "port": UVICORN_PORT,
        "reload": UVICORN_RELOAD,
    }
