from daen_geocore.transport.http.app import create_app


def test_app_has_no_public_v1_routes_or_unreviewed_docs() -> None:
    app = create_app()
    assert not any(route.path.startswith("/v1") for route in app.routes)
    assert app.docs_url is None
    assert app.redoc_url is None
    assert app.openapi_url is None
