from __future__ import absolute_import, unicode_literals

from .celery import app as server

__all__ = ('server',)