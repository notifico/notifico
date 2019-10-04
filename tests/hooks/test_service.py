from flask import current_app


def test_hook_metadata(app):
    """
    Ensure the minimum metadata is present for all hooks.
    """
    with app.app_context():
        for service in current_app.enabled_hooks.values():
            assert service.SERVICE_NAME is not None
            assert service.SERVICE_ID is not None
