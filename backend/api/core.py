"""
Module for application settings and database session management.

This module defines the Settings class which loads configuration from
environment variables, provides a cached settings instance, initializes
the SQLAlchemy async engine, and supplies an asynchronous session generator.
"""

from functools import lru_cache
from typing import AsyncGenerator

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


class Settings(BaseSettings):
    """Configuration settings loaded from environment variables.

    Attributes:
        DATABASE_URL (str): Database connection URL.
    """

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str


@lru_cache()
def get_settings() -> Settings:
    """Get the cached application settings.

    Returns:
        Settings: A cached instance of the Settings class.
    """
    return Settings()


# Initialize the asynchronous SQLAlchemy engine using the DATABASE_URL from
# settings.
engine = create_async_engine(get_settings().DATABASE_URL)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session generator for dependency injection.

    This function yields an asynchronous SQLAlchemy session with
    `expire_on_commit=False` to prevent attributes from expiring after commit.

    Yields:
        AsyncGenerator[AsyncSession, None]: An async session generator.
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
