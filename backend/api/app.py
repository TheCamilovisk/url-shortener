"""
Root module for the FastAPI application.

Defines the root endpoint that returns a greeting message.
"""

from http import HTTPStatus

from fastapi import FastAPI

from api.schemas import MessageSchema

app = FastAPI()


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def get_root() -> dict:
    """Handle GET requests to the root path.

    Returns:
        dict: A dictionary containing a greeting message.
    """
    return {'message': 'Hello, World!!!'}
