"""Gunicorn configuration."""
import sys

from envparse import env

sys.path.append(env.str('BASE_DIR'))
workers = env.int('WORKERS_NUMBER')
address = env.str('BIND_ADDRESS')
port = env.str('BIND_PORT')
bind = f'{address}:{port}'
max_requests_jitter = 1000
