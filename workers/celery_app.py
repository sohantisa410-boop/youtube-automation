from tasks.celery_app import celery_app as _celery_app

__all__ = ["celery_app"]

celery_app = _celery_app
