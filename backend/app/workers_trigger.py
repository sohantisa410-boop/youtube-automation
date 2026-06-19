"""Worker trigger helper.

This module is intentionally kept as a no-op stub to avoid a direct runtime dependency
from the backend package to the worker package. Worker task execution should be
coordinated via Celery broker messages instead of direct imports.
"""

__all__ = []
