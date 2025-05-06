"""
Root module for the FastAPI application.

Defines the root endpoint that returns a greeting message.
"""

from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core import Settings, get_session, get_settings
from api.models import URL
from api.schemas import (
    MessageSchema,
    ShortenRequestSchema,
    ShortenResponseSchema,
)
from api.utils import generate_short_code

app = FastAPI()


DBSession = Annotated[AsyncSession, Depends(get_session)]
APISettings = Annotated[Settings, Depends(get_settings)]


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
async def get_root() -> dict:
    """Handle GET requests to the root path.

    Returns:
        dict: A dictionary containing a greeting message.
    """
    return {'message': 'Hello, World!!!'}


@app.post(
    '/shorten',
    status_code=HTTPStatus.CREATED,
    response_model=ShortenResponseSchema,
)
async def shorten_url(
    request: ShortenRequestSchema,
    session: DBSession,
    settings: APISettings,
) -> dict:
    """Create a shortened URL for the given original URL.

    Args:
        request (ShortenRequestSchema): The payload containing the URL.
        session (AsyncSession): The database session dependency.
        settings (Settings): Application settings dependency.

    Returns:
        dict: A dictionary containing the short and original URLs.
    """
    short_code = None
    code_exists = True
    # Check for collisions (retry if needed)
    while code_exists:
        short_code = generate_short_code()
        code_exists = bool(
            await session.scalar(
                select(URL).filter(URL.short_code == short_code)
            )
        )

    db_url = URL(short_code, request.url)
    session.add(db_url)
    await session.commit()
    await session.refresh(db_url)

    short_url = f'{settings.MY_DOMAIN}/{short_code}'

    return {'short_url': short_url, 'original_url': request.url}


@app.get('/{short_code}', status_code=HTTPStatus.PERMANENT_REDIRECT)
async def redirect_url(
    short_code: str, session: DBSession
) -> RedirectResponse:
    """Redirect to the original URL based on the short code.

    Args:
        short_code (str): The path parameter representing the short code.
        session (AsyncSession): The database session dependency.

    Returns:
        RedirectResponse: A redirect response to the original URL.

    Raises:
        HTTPException: If the short code is not found or inactive.
    """
    db_url = await session.scalar(
        select(URL).filter(URL.short_code == short_code, URL.active.is_(True))
    )
    if not db_url:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Short code '{short_code}' not found or inactive.",
        )
    return RedirectResponse(
        url=db_url.original_url, status_code=HTTPStatus.PERMANENT_REDIRECT
    )
