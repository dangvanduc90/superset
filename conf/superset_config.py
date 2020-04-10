import os

from werkzeug.contrib.cache import RedisCache
from celery.schedules import crontab
from dateutil import tz
from flask_appbuilder.security.manager import AUTH_DB

MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', '')
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://:redis:6379/1'}
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://postgres:superset@postgres:5432/superset'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'thisISaSECRET_1234'
SQLLAB_TIMEOUT=600
SUPERSET_WEBSERVER_TIMEOUT=1200

class CeleryConfig(object):
    BROKER_URL = 'redis://redis:6379/0'
    CELERY_IMPORTS = (
        'superset.sql_lab',
        'superset.tasks',
    )
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    CELERYD_LOG_LEVEL = 'DEBUG'
    CELERYD_PREFETCH_MULTIPLIER = 10
    CELERY_ACKS_LATE = True
    CELERY_ANNOTATIONS = {
        'sql_lab.get_sql_results': {
            'rate_limit': '100/s',
        },
        'email_reports.send': {
            'rate_limit': '1/s',
            'time_limit': 120,
            'soft_time_limit': 150,
            'ignore_result': True,
        },
    }
    CELERYBEAT_SCHEDULE = {
        'email_reports.schedule_hourly': {
            'task': 'email_reports.schedule_hourly',
            'schedule': crontab(minute=1, hour='*'),
        },
        'cache-warmup-hourly': {
            'task': 'cache-warmup',
            'schedule': crontab(minute=0, hour='*'),  # hourly
            'kwargs': {
                'strategy_name': 'top_n_dashboards',
                'top_n': 10,
                'since': '7 days ago',
            },
        },
    }

CELERY_CONFIG = CeleryConfig

RESULTS_BACKEND = RedisCache(
    host='redis', port=6379, key_prefix='superset_results')

