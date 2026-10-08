from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create the transport shell without public DAEN business routes."""
    return FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
