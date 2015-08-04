""" Gunicorn configuration module """

import os

from multiprocessing import cpu_count


env_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '../../.env'))

if os.path.exists(env_file):
    for line in open(env_file):
        var = line.strip().split('=')
        if 2 == len(var):
            os.environ[var[0]] = var[1]


procname = 'flapi_httpd'

workers = cpu_count() * 2 + 1

daemon = False

bind = '127.0.0.1:35274'


chdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

raw_env = ['FLASK_CONFIG=prod']


log_level = 'info'

accesslog = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../log/access.log'))

errorlog = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../log/error.log'))
