import pathlib
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator, PostgresDsn
from envparse import env

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    env.read_envfile(f'{ROOT}/.env')

    API_V1_STR: str = "/api/v1"
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = env.str('JWT_SECRET_KEY')

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000", ]

    # Origins that match this regex OR are in the above list are allowed
    BACKEND_CORS_ORIGIN_REGEX: Optional[str] = "https.*\.(netlify.app|herokuapp.com)"  # noqa: W605

    # noinspection PyMethodParameters
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:  # noqa
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ASYNC_DATABASE_URL: Optional[PostgresDsn] = \
        f"postgresql+asyncpg://" \
        f"{env.str('PG_SUPERUSER')}:{env.str('PG_SUPERUSER_PASSWORD')}" \
        f"@localhost:{env.str('PG_PORT')}" \
        f"/{env.str('PG_NAME')}"

    FIRST_SUPERUSER_USERNAME: EmailStr = env.str('FIRST_SUPERUSER_USERNAME')
    FIRST_SUPERUSER_PASSWORD: str = env.str('FIRST_SUPERUSER_PASSWORD')

    class Config:
        case_sensitive = True


settings = Settings()
